---
title: "Task-Specific Feature Profiles for Memory-Bounded ML Training"
type: concept
created: 2026-05-18
last_verified: 2026-05-18
source_hash: "f1615c76dd0a7e0be29992b380c486942c47624fcf57a9e648a03b30912314f7"
sources:
  - raw/2026-05-18-copilot-session-homelab-nba-repairs-e405020e.md
quality_score: 86
related:
  - "[[Out-of-Memory (OOM) Failure Diagnosis and Remediation in ML Containers]]"
  - "[[Per-Model Subprocess Isolation for Memory-Safe Weekly Retrains]]"
  - "[[Training Pipeline Status Tracking in ML Systems]]"
tier: hot
tags: [ml-ops, feature-engineering, memory-optimization, nba-ml-engine, model-training]
---

# Task-Specific Feature Profiles for Memory-Bounded ML Training

## Overview

Task-specific feature profiles are a training design pattern in which a model requests only the feature families required for its prediction task instead of inheriting the full feature-building pipeline by default. The idea matters most in shared or memory-bounded ML systems, where a "one builder for every model" abstraction can silently push small models into large-model memory costs they do not actually need.

## How It Works

A typical feature pipeline starts from a good instinct: centralize feature construction so every model sees a consistent interface. Over time, though, the shared builder accumulates more and more sources—rolling advanced stats, interaction features, matchup enrichments, tracking aggregates, bookmaker signals, and auxiliary model outputs. If every caller always asks for the full matrix, the interface remains simple but the execution cost stops matching the needs of lighter tasks. The checkpoint shows exactly this failure mode in the [[NBA ML Engine]]: the minutes model uses a relatively small subset of features, yet the old training path still loaded high-memory sources designed for broader stat models.

The first step in the repair was diagnostic, not architectural. The failing weekly retrain showed `train-minutes` exiting with `-9`, Docker reporting `OOMKilled=true`, and cgroup `memory.events` recording repeated `oom_kill` increments. That proved the process was not merely slow or blocked; it was exhausting its memory budget. A stale live image complicated diagnosis because the scheduler still ran the older weekly command, but the durable root cause was narrower: the minutes stage was paying for the full feature-building graph even though its downstream model only needed a trimmed subset.

The implementation fix was to make scope explicit at the builder boundary. Instead of only toggling behavior indirectly through ad hoc flags, the pipeline introduced `feature_profile: Literal["full", "minutes"] = "full"` in `src/features/builder.py`. The minutes trainer then called `build_features(..., predicted_minutes_mode="disabled", feature_profile="minutes")`. That combination matters. `predicted_minutes_mode="disabled"` makes it clear the target workflow is the real minutes model rather than a downstream stat model consuming predicted minutes, while `feature_profile="minutes"` tells the builder to exclude feature sources that are expensive and irrelevant for this specific task.

In practice, the minutes profile skipped a concrete list of high-memory sources: game advanced rolling stats, teammate out usage share, tracking rolling, hustle features, BBRef features, opponent rolling, usage interactions, game lines, game time features, and matchup features. The pattern is important because it does not weaken the overall system by deleting those sources globally. Full-stat models can still request the `full` profile. The optimization is not "make the builder smaller" but "make the workload selection honest." A shared pipeline remains possible as long as the caller can declare which slice of the feature graph it truly needs.

The checkpoint also shows why test-driven development is useful here. The new behavior was locked in with failing tests first: one asserted that minutes training must call `build_features(..., predicted_minutes_mode="disabled", feature_profile="minutes")`, and another asserted that the minutes profile must skip expensive source loaders. Those tests protected the conceptual boundary, not just the current implementation. Without them, a future refactor could accidentally preserve the new parameter while still reintroducing full-profile loaders under the hood.

The result demonstrates the operational value of feature profiles. After redeploy, a live `train-minutes` run finished in about 48 seconds, built a `158353 x 262` matrix, used only `34 / 231` minutes features, and achieved `val_r2=0.55946` without another OOM. The important lesson is not that every model should have a tiny profile. It is that feature-building interfaces should make computational scope an explicit part of correctness. In memory-bounded systems, asking for the wrong profile is not merely inefficient; it can be the direct cause of training failure.

## Key Properties

- **Explicit workload selection:** The caller declares whether it needs the `full` or `minutes` feature graph.
- **Preserved shared pipeline:** One builder can still serve many models as long as it exposes honest task boundaries.
- **Regression-testable contract:** Tests can assert both the requested profile and which loaders must not run for that profile.
- **Performance with semantic intent:** Memory savings come from dropping irrelevant feature families, not from arbitrary sampling or degraded labels.

## Limitations

Feature profiles add another axis of configuration, which means profile drift can become a new failure mode if the mapping between task and profile is undocumented or inconsistently enforced. A profile that is too aggressive may omit information that eventually becomes useful for model quality, while a profile that is too lax simply recreates the original memory problem under a different name. This pattern also does not replace broader controls such as subprocess isolation, status tracking, or observability for long weekly retrains.

## Examples

```python
features = build_features(
    games_df,
    predicted_minutes_mode="disabled",
    feature_profile="minutes",
)
```

In the checkpoint's repaired path, the minutes profile intentionally bypassed expensive loaders that were valuable for full stat-model training but unnecessary for the dedicated minutes target.

## Practical Applications

This concept applies to sports forecasting, recommender systems, tabular AutoML, and multimodel pipelines where several tasks share infrastructure but not the same feature appetite. It is especially valuable when a smaller "supporting" model runs inside a larger orchestration path; giving that model its own honest feature profile can be cheaper and safer than repeated memory-limit increases.

## Related Concepts

- **[[Out-of-Memory (OOM) Failure Diagnosis and Remediation in ML Containers]]**: OOM diagnosis proves the failure mode; feature profiles provide one durable remediation path.
- **[[Per-Model Subprocess Isolation for Memory-Safe Weekly Retrains]]**: Subprocess isolation reduces the size of the execution unit, while feature profiles reduce the size of the work inside that unit.
- **[[Training Pipeline Status Tracking in ML Systems]]**: Status tracking helps operators see where a run failed, but feature profiles change whether the failing stage can fit in memory at all.

## Sources

- [[Copilot Session Checkpoint: Homelab NBA repairs]] — primary source for the minutes-profile redesign, tests, and live runtime outcome.

