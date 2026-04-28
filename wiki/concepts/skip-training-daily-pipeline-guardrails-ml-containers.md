---
title: "Skip-Training Daily Pipeline Guardrails in Shared ML Containers"
type: concept
created: 2026-04-26
last_verified: 2026-04-26
source_hash: "b3f0273fc681461d85cdd21c2845050babf29178ea5b90d9763ec60cc54409e3"
sources:
  - raw/2026-04-26-copilot-session-oom-mitigation-and-follow-up-93744ca8.md
related:
  - "[[Out-of-Memory (OOM) Failure Diagnosis and Remediation in ML Containers]]"
  - "[[Daily/Weekly Validation Split for NBA ML Pipelines]]"
  - "[[Training Pipeline Status Tracking in ML Systems]]"
tier: hot
tags: [ml-ops, nba-ml-engine, oom, homelab, scheduler, guardrails, pipeline-design]
quality_score: 62
---

# Skip-Training Daily Pipeline Guardrails in Shared ML Containers

## Overview

Skip-training daily pipeline guardrails are an operational pattern for machine-learning systems that share one container or host between API serving and scheduled maintenance work. Instead of letting the daily pipeline retrain models, recalibrate classifiers, and generate predictions in one monolithic run, the daily path is explicitly constrained to reuse existing production artifacts and perform only the freshness-critical steps.

The pattern matters when reliability depends more on bounded memory than on maximum daily model freshness. In the NBA ML checkpoint behind this concept, the daily job did not need to discover brand-new model weights every morning; it needed to keep predictions current without repeatedly pushing a shared homelab host into global OOM conditions.

## How It Works

The core idea is to separate **artifact freshness** from **prediction freshness**. A naive daily pipeline often bundles both: fetch new data, engineer features, retrain all models, recalibrate, prune, score, store predictions, refresh views, and notify downstream systems. That coupling feels convenient because there is only one command to run, but it makes the daily path inherit the peak-memory characteristics of the heaviest stage. In the checkpoint source, the daily Ofelia command was still invoking `python main.py pipeline`, so the "daily refresh" path was secretly a full training workflow.

In a shared-container setup, that is dangerous because the relevant memory budget is not just the container's local limit. The real envelope is the host-wide sum:

$$
M_{\text{total}} = M_{\text{api}} + M_{\text{other containers}} + M_{\text{host daemons}} + M_{\text{interactive tooling}}
$$

Once `M_total` exceeds available RAM plus remaining swap, the kernel does not care that one component is "just a scheduled task." It kills some process in the highest-pressure context it can reclaim. The session's first OOM made this explicit: kernel logs showed `constraint=CONSTRAINT_NONE`, which is a host-level signal rather than a narrow container cgroup breach. The fix therefore could not be "just raise the limit again" without risking a bigger host-wide blast radius.

The guardrail changes the daily objective. Instead of optimizing for "do everything every day," the system optimizes for "keep today's outputs fresh while staying inside a safe memory envelope":

$$
\min \; \text{prediction staleness} \quad \text{s.t.} \quad M_{\text{peak,daily}} < M_{\text{safe,host}}
$$

Operationally, that means the command path is taught to skip the highest-cost phases. In the checkpoint, `main.py` gained a `pipeline --skip-training` flag. When enabled, the pipeline does **not** retrain models, prune candidate models, or refit calibrators. It still performs the parts that matter for same-day product freshness: data ingest, feature generation, prediction generation using the already-registered production models, QA, materialized-view refreshes, and notifications. In effect, the daily path becomes an inference-and-validation job rather than a training job.

The pattern only works if the scheduler boundary is explicit. It is not enough to add a flag in code and assume operators will remember it. The homelab compose definition was changed so the actual Ofelia label became `python main.py pipeline --skip-training`. That turns the design into executable infrastructure: the scheduler itself declares that the daily path is not allowed to retrain. A separate weekly command remains the sanctioned heavy path for full model training, preserving a place for deeper statistical work without forcing that workload onto every daily refresh.

Testing is part of the mechanism, not an afterthought. The checkpoint used TDD to add failing tests before production edits: one set required the CLI help to expose `--skip-training`, another asserted that the daily pipeline can still run predictions and downstream refresh work without invoking training or recalibration, and a homelab-side test asserted that the Ofelia command string includes the flag. This is important because infrastructure drift is a common failure mode. Without tests, a future refactor can silently remove the guardrail even if the concept remains documented.

The follow-up OOM in the same source shows another key aspect of the pattern: **runtime verification must distinguish stored intent from observed execution**. After deployment, the scheduler label correctly showed `--skip-training`, but later logs still contained model-training output around the time of a new OOM. That does not invalidate the guardrail; it shows that guardrails are only as good as the process path they actually constrain. There may be another cron job, a manual `docker exec`, a weekly path firing at an unexpected time, or simply misleading log interpretation. In other words, skip-training is a strong workload-shaping tool, but it does not eliminate the need for timestamped process correlation.

This concept is stronger than the earlier [[Daily/Weekly Validation Split for NBA ML Pipelines]]. That earlier pattern still allowed the daily job to train models while moving the heaviest evaluation routine off the critical path. Skip-training goes one step further by declaring that some daily runs should not train at all. It is the right move when the operational goal is "fresh predictions from known-good models" rather than "new models every day regardless of host pressure."

## Key Properties

- **Inference-first daily path:** The guardrail preserves prediction freshness by reusing existing production artifacts instead of creating new ones every day.
- **Scheduler-enforced intent:** The protection is encoded in the actual cron/orchestration command (`python main.py pipeline --skip-training`), not just in operator folklore.
- **Host-safety over local optimization:** The pattern assumes host-wide memory pressure is the real failure domain and treats container-level tuning as insufficient when the kernel is already killing processes globally.
- **Testable drift prevention:** CLI-level, orchestration-level, and behavior-level tests can all assert that the daily path still skips retraining.
- **Cadence separation:** The daily job handles freshness-critical inference work; the weekly job remains the deliberate location for expensive retraining.

## Limitations

This pattern trades some model freshness for operational stability. If the registered production models are already stale or degraded, skipping training protects uptime but may prolong accuracy loss. It also assumes the artifact-loading path is healthy; if the model registry or on-disk production bundle is broken, an inference-only daily job can fail without the self-healing effect of a new training run.

The pattern does not solve hidden alternate execution paths. A second scheduler job, a manual operator command, or a background process can still run full training and trigger the same OOM profile. Finally, the design requires discipline around naming and observability: once there are multiple paths (`train`, `pipeline`, `pipeline --skip-training`, `resume_pipeline`), logs and alerts must clearly distinguish which one actually ran.

## Examples

One concrete implementation shape is:

```python
@click.command()
@click.option("--skip-training", is_flag=True, help="Reuse production models.")
def pipeline(skip_training: bool) -> None:
    ingest_latest_data()
    feature_df = build_features()
    if not skip_training:
        train_models(feature_df)
        prune_models()
        refit_calibrators()
    generate_predictions(feature_df, use_production_models=skip_training)
    run_quality_checks()
    refresh_materialized_views()
    send_notifications()
```

And the scheduler boundary becomes explicit:

```yaml
command: python main.py pipeline --skip-training
```

That is exactly the kind of change that converts a memory-heavy daily training job into a bounded daily prediction-refresh job.

## Practical Applications

This pattern is useful anywhere one service mixes user-facing duties with scheduled ML work on the same machine: homelab analytics stacks, low-cost internal forecasting services, recommendation engines on shared nodes, or side-project inference APIs that cannot afford daily full retrains. It is especially attractive when a weekly or manually triggered retrain path already exists and the product value of daily runs comes mostly from updated inputs rather than newly optimized parameters.

## Related Concepts

- **[[Out-of-Memory (OOM) Failure Diagnosis and Remediation in ML Containers]]**: The broader debugging frame that explains why host-level evidence matters before choosing a fix.
- **[[Daily/Weekly Validation Split for NBA ML Pipelines]]**: A lighter workload-shaping strategy that still trains daily but moves the heaviest evaluation work off the critical path.
- **[[Training Pipeline Status Tracking in ML Systems]]**: The observability layer needed to prove which pipeline variant actually ran after the scheduler fires.

## Sources

- [[Copilot Session Checkpoint: OOM Mitigation and Follow-Up]] — primary source for the `--skip-training` design, the scheduler guardrail, and the follow-up caveat that labels alone do not prove runtime behavior.
