---
title: "Per-Model Subprocess Isolation for Memory-Safe Weekly Retrains"
type: concept
created: 2026-04-27
last_verified: 2026-04-27
source_hash: "165e5628d8ddd993272d93401f75c9d8f491e65e7efcf3a0deaddced6ef2cf38"
sources:
  - raw/2026-04-27-copilot-session-weekly-retrain-oom-debugging-c722e705.md
related:
  - "[[Out-of-Memory (OOM) Failure Diagnosis and Remediation in ML Containers]]"
  - "[[Daily/Weekly Validation Split for NBA ML Pipelines]]"
  - "[[Training Pipeline Status Tracking in ML Systems]]"
  - "[[Walk-Forward Cross-Validation for Model Selection]]"
tier: hot
tags: [ml-ops, nba-ml-engine, oom, subprocess-orchestration, weekly-retrain, walk-forward-cv]
quality_score: 65
---

# Per-Model Subprocess Isolation for Memory-Safe Weekly Retrains

## Overview

Per-model subprocess isolation is a weekly-retrain design pattern for resource-constrained ML systems where the parent command breaks the retrain into the smallest expensive units that still preserve correctness. In the NBA ML Engine checkpoint behind this concept, the key realization was that per-stat isolation was still too coarse: one stat child could still execute the full multi-model training loop plus walk-forward CV and get the host OOM-killed.

This pattern matters when the operator already proved that lighter scheduler guardrails are not enough. The job is still worth running weekly, but its internal execution graph has to be reshaped so peak memory is bounded by one model-sized stage at a time rather than one stat-sized super-stage.

## How It Works

The failure mode that motivates this pattern is subtle. A team may think it has already made a weekly retrain "memory-safe" by spawning one subprocess per target stat, for example `train --stat pts`, `train --stat reb`, and so on. That sounds isolated, but it often is not. In the checkpoint source, the per-stat child still called `train_all(stats=[stat], model_classes=...)`, which meant that each child continued to train every model family for that stat and then run the expensive post-loop routines tied to that code path. Most importantly, if [[Walk-Forward Cross-Validation for Model Selection]] remained enabled, the child still carried the validation tail that had caused earlier memory pressure.

That means the relevant peak-memory expression was still too large. Conceptually, the first design looked like:

$$
M_{\text{peak,stat-child}} \approx \sum_{m \in \mathcal{M}} M_{\text{train}}(m, s) + M_{\text{cv}}(s)
$$

where $s$ is one target stat such as `reb` and $\mathcal{M}$ is the set of model classes (XGBoost, LightGBM, RandomForest, Ridge, Ensemble, LSTM, and any auxiliaries). Even though only one stat ran at a time, the child was still a large composite workload. The artifact timeline in the checkpoint proved exactly that kind of late failure: `reb` artifacts finished, but the run died before `ast`, strongly implying the child got through core model training and then blew up in the heavier validation tail.

Per-model subprocess isolation attacks the problem by choosing a smaller execution unit. Instead of "one child per stat," the parent orchestrator plans "one child per stat-model pair," or another equivalently bounded stage boundary. The parent might run `train-minutes` first, then for each stat iterate through model classes one at a time, invoking hidden child flags such as `--skip-cv`, `--skip-register`, and `--metrics-json`. This changes the memory equation to something closer to:

$$
M_{\text{peak,weekly}} \approx \max \left(
M_{\text{minutes}},
\max_{s \in \mathcal{S}, m \in \mathcal{M}} M_{\text{train}}(m, s),
M_{\text{calibrator}}
\right)
$$

The point is not mathematical elegance; it is operational survivability. The host only needs enough headroom for one bounded model-training stage plus the API and other background services, rather than for an entire stat's model suite and CV follow-up.

Once the child unit is reduced, the parent becomes more important. It is no longer enough to fire subprocesses and hope each one performs the full business workflow independently. Child stages must be intentionally incomplete so they stay cheap: they should train one thing, emit metrics, save any needed split metadata, and exit. Registration, promotion, and cross-model comparison then happen in the parent after all children for a stat are done. In the checkpoint, this is why `train_all()` was being extended with `register_best: bool = True` and `split_metadata_sink: dict | None = None`: the training code needed a way to surface evaluation outputs without prematurely mutating the production registry inside every child.

That parent-side aggregation step is essential for correctness. A weekly retrain still needs to decide which model wins for `pts`, `reb`, `ast`, and the other stats, and it still needs all the existing guardrails around degradation thresholds, negative $R^2$, hit-rate floors, and artifact existence. The parent therefore collects each child's `metrics_json`, reconstructs the candidate set for the stat, and calls the registration routine once per stat. This preserves the semantics of "choose the best model per stat" while letting training happen in much smaller memory envelopes.

Another important part of the pattern is explicit feature gating for child runs. The checkpoint source made `--skip-cv` non-negotiable because the likely killer was the CV tail inside a stat child. The idea is not that CV is bad in general; it is that the per-model child should only do the work that belongs on that stage. In many systems, that means the weekly control flow becomes two-layered: one layer does cheap isolated child training; another layer optionally performs heavier governance tasks later, with separate cadence or separate execution infrastructure. That makes this concept a stricter form of [[Daily/Weekly Validation Split for NBA ML Pipelines]]: instead of merely moving heavy evaluation off the daily path, it makes the weekly path itself more granular and bounded.

Finally, per-model subprocess isolation is valuable because it lines up cleanly with failure recovery. If a `reb`-LightGBM child fails, operators know exactly which stage died, what model artifacts were produced before the failure, and which units remain. That makes resumability, artifact cleanup, and targeted reruns much more straightforward than with a monolithic stat child whose internal state is opaque. The design therefore improves both memory safety and debuggability at once.

## Key Properties

- **Smaller unit of work:** The retrain is decomposed into model-sized stages rather than stat-sized composite stages.
- **Parent-controlled correctness:** Child processes train and report; the parent aggregates metrics and performs best-model registration once per stat.
- **CV shedding on the hot path:** Hidden flags such as `--skip-cv` prevent memory-heavy evaluation logic from riding along inside every child.
- **Failure locality:** A failed stage is attributable to a concrete `stat × model` unit instead of a broad opaque retrain chunk.
- **Compatibility with existing guardrails:** Timeout limits, skip-stat filters, artifact validation, and degradation checks still apply, but at clearer boundaries.

## Limitations

This pattern increases orchestration complexity. The parent now needs reliable metrics files, manifest bookkeeping, stage ordering, and cleanup logic, and mistakes there can create new correctness bugs even if memory use improves. It also does not magically make every model cheap; one child can still be too large if a single model family is itself memory-prohibitive.

The design can also shift, rather than remove, evaluation costs. If full weekly CV is still required for governance, that work must move somewhere else in the workflow or onto different infrastructure. Finally, more subprocesses mean more partial artifacts and more states to reconcile after interruption, so the pattern depends heavily on good logging and status tracking.

## Examples

```python
def run_memory_safe_weekly(stats, model_classes):
    train_minutes_model()
    for stat in stats:
        metric_rows = []
        for model_name in model_classes:
            result = run_child(
                "train",
                stat=stat,
                model=model_name,
                skip_cv=True,
                skip_register=True,
                metrics_json=True,
            )
            metric_rows.append(result.metrics)
        register_best_for_stat(stat, metric_rows)
    train_calibrator()
```

In the checkpoint's concrete redesign, this pattern was paired with persistent run logs, manifest files, and status-tracker calls so the bounded child stages were also observable from outside the container.

## Practical Applications

Per-model subprocess isolation is useful in any ML system that must retrain on a shared node without monopolizing memory: sports prediction stacks, nightly demand models, fraud detectors on mixed-use hosts, or forecasting systems that share a box with a user-facing API. It is especially attractive when training correctness already depends on per-target winner selection, because parent-side registration can preserve that logic while drastically reducing peak memory.

## Related Concepts

- **[[Out-of-Memory (OOM) Failure Diagnosis and Remediation in ML Containers]]**: Explains why host-level OOM evidence should drive workload reshaping rather than blind memory bumps.
- **[[Daily/Weekly Validation Split for NBA ML Pipelines]]**: A related but coarser workload-shaping pattern that still allows daily training while moving the heaviest validation elsewhere.
- **[[Training Pipeline Status Tracking in ML Systems]]**: The status layer that should reflect each isolated retrain stage as the parent advances through them.
- **[[Walk-Forward Cross-Validation for Model Selection]]**: The evaluation routine intentionally removed from the model child path because it remained too expensive at that granularity.

## Sources

- [[Copilot Session Checkpoint: Weekly Retrain OOM Debugging]] — documents the failed per-stat design, the late-stage `reb` OOM evidence, and the second-generation shift to per-model orchestration.
