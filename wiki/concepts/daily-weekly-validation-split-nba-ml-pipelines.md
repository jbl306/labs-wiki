---
title: "Daily/Weekly Validation Split for NBA ML Pipelines"
type: concept
created: 2026-04-23
last_verified: 2026-04-23
source_hash: "16035a6f5cdc2578c200345a8209b1b969443251f4126a9af138fbf055e69779"
sources:
  - raw/2026-04-23-copilot-session-nba-ml-pipeline-oom-fixes-2781c1dc.md
quality_score: 84
concepts:
  - daily-weekly-validation-split-nba-ml-pipelines
related:
  - "[[Walk-Forward Cross-Validation for Model Selection]]"
  - "[[Per-Stat Model Selection and Ensemble Learning in NBA ML Engine]]"
  - "[[Out-of-Memory (OOM) Failure Diagnosis and Remediation in ML Containers]]"
  - "[[Copilot Session Checkpoint: NBA ML Pipeline OOM Fixes]]"
tier: hot
tags: [machine-learning, ml-ops, nba-ml-engine, time-series, walk-forward-cv, model-registration, homelab]
---

# Daily/Weekly Validation Split for NBA ML Pipelines

## Overview

Daily/weekly validation splitting is an operational design pattern for time-series ML systems where the fast, failure-critical retrain path uses a lighter validation rule every day, while the more expensive and statistically stronger evaluation path runs on a slower cadence. In the NBA ML Engine context, the pattern exists to keep nightly retraining and model registration durable under homelab resource limits without abandoning the benefits of [[Walk-Forward Cross-Validation for Model Selection]].

## How It Works

The starting point is a common coupling mistake in production ML pipelines: the same job is asked to do two different things at once. One responsibility is **operational freshness**—train tonight's models, register them, and have tomorrow's predictions use the new artifacts. The other is **evaluation rigor**—run a more expensive validation regime, such as walk-forward CV, to estimate whether a model generalizes across multiple time windows. Those goals are aligned in principle, but they behave very differently under runtime and memory pressure.

In the checkpoint behind this concept, the daily NBA pipeline trained all seven target stats successfully but died partway through walk-forward CV. That exposed the hidden coupling: registration was deferred until after the CV routine completed. The training outputs existed on disk, but the production [[NBA-ML Model Registry]] still pointed at older artifacts because promotion was waiting on the slower evaluation stage. Operationally, this is a starvation bug: the job completed the work needed for tomorrow's predictions, but the control flow prevented those results from becoming live.

The split fixes that by separating the daily and weekly objectives. On the **daily path**, the pipeline temporarily overrides `USE_WALK_FORWARD_CV=False` and `USE_CV_MODEL_SELECTION=False`. That makes the nightly run choose the best model per stat using the immediate validation metric already produced by the ordinary train/validation split:

$$
m_{\text{daily}} = \arg \min_m \mathrm{val\_mse}(m)
$$

This path optimizes for bounded runtime, immediate registration, and lower failure blast radius. In the checkpoint, that matters because the daily run takes roughly 3-4 hours without walk-forward CV, while the full CV path adds about 5 more hours and materially raises memory pressure.

On the **weekly path**, the canonical retrain job keeps the full time-series evaluation loop:

$$
m_{\text{weekly}} = \arg \min_m \frac{1}{K}\sum_{k=1}^{K}\mathrm{val\_mse}_k(m)
$$

Here the system is allowed to pay the cost of multiple sequential folds because the job is explicitly about stronger selection and deeper review, not just freshness. The weekly cadence preserves the statistical honesty of walk-forward evaluation and still provides a place to compare models using `cv_avg_val_mse` rather than a single split.

The implementation detail that makes the split safe is **temporary override plus restoration**, not permanent config drift. The daily `pipeline()` command saves the relevant config flags, sets them to `False` only for the pipeline run, and restores them afterward. That means the fast operational mode is scoped to the daily command rather than redefining the entire training system. Weekly `train` keeps its defaults, so the project does not silently lose its more rigorous evaluation path.

Why does this work? Because the system recognizes that not every accuracy safeguard belongs on the latency-sensitive path. Walk-forward CV is still valuable, but it becomes a *governance* mechanism rather than a *gating dependency* for nightly freshness. In reliability terms, the split moves the highest-cost, highest-fragility stage off the failure-critical path. In product terms, it ensures that a partial failure in the evaluation stage cannot block tomorrow morning's predictions from using the models that were already trained successfully.

There is also a resource-management angle. Once the daily path stops carrying the full CV workload, operators can size the training container more aggressively. In the same checkpoint, `nba-ml-api` was reduced from 18 GB to 12 GB so the service becomes the preferred OOM victim before the whole host destabilizes. That change only becomes operationally sane because the daily job no longer tries to absorb both ordinary training and the heaviest validation work in one window.

## Key Properties

- **Separated objectives:** Daily runs optimize for freshness and successful registration; weekly runs optimize for stronger model comparison across time windows.
- **Immediate promotion path:** Freshly trained artifacts can be registered the same night instead of waiting for walk-forward CV completion.
- **Scoped configuration override:** The pattern relies on saving, overriding, and restoring config flags inside the daily command rather than globally changing training defaults.
- **Lower operational blast radius:** If the daily job fails, it is less likely to fail in the most memory-intensive section of the workflow.
- **Cadence-aware rigor:** Statistical rigor is preserved, but attached to a cadence that can tolerate longer runtimes and occasional operator attention.

## Limitations

A daily single-split selection rule is less robust than walk-forward CV when the data distribution is drifting or when one validation slice is unusually noisy. The pattern also creates a deliberate difference between what is "good enough to ship tonight" and what is "best under full evaluation," so teams need to accept that daily and weekly winners may not always match. Finally, the design only helps if the scoped overrides are restored correctly; if the fast path leaks into the weekly job, evaluation quality silently degrades.

## Examples

The checkpoint's implementation can be summarized like this:

```python
old_use_wf = config.USE_WALK_FORWARD_CV
old_use_cv_select = config.USE_CV_MODEL_SELECTION

config.USE_WALK_FORWARD_CV = False
config.USE_CV_MODEL_SELECTION = False
try:
    train_all_targets()
    register_best_models()
finally:
    config.USE_WALK_FORWARD_CV = old_use_wf
    config.USE_CV_MODEL_SELECTION = old_use_cv_select
```

Operationally, this means the nightly `pipeline` command trains and promotes with single-split validation, while the Sunday `train` job still executes the full fold-based selection flow.

## Practical Applications

This pattern is useful anywhere a time-series or sequential ML system has both a freshness requirement and a heavy validation regime: sports analytics retrains, demand forecasting, fraud models with nightly refreshes, or recommendation systems that need new models every day but only need full backtesting weekly. It is especially effective in constrained environments—single-node homelabs, small GPU boxes, or mixed-use servers—where evaluation rigor must coexist with hard memory ceilings and non-ML workloads.

## Related Concepts

- **[[Walk-Forward Cross-Validation for Model Selection]]**: The rigorous evaluation method that remains on the weekly path instead of gating every daily retrain.
- **[[Per-Stat Model Selection and Ensemble Learning in NBA ML Engine]]**: The downstream model-selection logic that the daily path still exercises, just with a lighter validation signal.
- **[[Out-of-Memory (OOM) Failure Diagnosis and Remediation in ML Containers]]**: The operational pressure that motivated moving the heaviest validation stage off the daily critical path.

## Sources

- [[Copilot Session Checkpoint: NBA ML Pipeline OOM Fixes]] — documents the outage, the deferred-registration failure mode, and the daily/weekly split introduced to fix it.
