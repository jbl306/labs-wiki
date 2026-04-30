---
title: "Training-Mode-Aware Rolling Window Metadata"
type: concept
created: 2026-04-30
last_verified: 2026-04-30
source_hash: "02ef1738c2df2fa90f694299ca6aad3b0a2119bff4c33aee54a4c6b0da5a52b5"
sources:
  - raw/2026-04-25-copilot-session-audit-recommendations-implementation-4d25144f.md
quality_score: 85
concepts:
  - training-mode-aware-rolling-window-metadata
related:
  - "[[Phased Progress Tracking With Validation Gates]]"
  - "[[Calibration Leakage Mitigation in ML Model Training]]"
  - "[[Artifact Registry Validation In ML Pipelines]]"
  - "[[Prior-Season Feature Mapping for Temporal Leakage Prevention]]"
tier: hot
tags: [training, time-series, rolling-window, metadata, mlops, evaluation, nba-ml-engine]
---

# Training-Mode-Aware Rolling Window Metadata

## Overview

Training-mode-aware rolling window metadata is a training and model-registry pattern that makes temporal split policy explicit instead of burying it inside trainer logic. The checkpoint that introduced it separated production and research training modes, used a rolling chronological split for production, preserved the older fixed split for research, and surfaced the resulting date windows through registry snapshots and `/models` so operators could see exactly what data a model had learned from and been validated on.

## How It Works

The underlying issue is that “train/validation/test split” is not one thing. In a research setting, a fixed holdout split is often useful because it gives a stable comparison target. In a production setting, the same static split can become misleading because the model is no longer being validated against the most recent data it will face in deployment. The checkpoint addresses this by elevating split policy into an explicit configuration variable: `TRAINING_MODE=production|research`.

In production mode, the split becomes chronological and rolling. Instead of selecting a timeless random or fixed-season holdout, the trainer reserves the most recent configured days for validation and optionally an additional test window. If dates are indexed as increasing timestamps $t_0 < t_1 < \dots < t_n$, the intended policy is roughly:

$$
\text{train} = [t_0, t_{v-1}], \quad
\text{validate} = [t_v, t_{w-1}], \quad
\text{test} = [t_w, t_n]
$$

with the exact cut points determined by configured day windows. This better matches the real question production models face: “How well do we predict the near future using the past?”

Research mode deliberately preserves the previous split behavior. That matters because research often needs comparability across experiments, ablations, and reports. By naming both modes explicitly rather than letting one silently replace the other, the system avoids a common failure mode where a production hardening quietly invalidates prior experimental baselines. The same trainer can now serve two valid goals, but it must declare which goal it is serving.

The checkpoint also adds hard guardrails around the rolling split. A rolling scheme can fail in subtle ways on small or misconfigured datasets: if the configured validation or test window is too large, the training partition may become empty. Rather than proceeding with zero-row training data and producing nonsense artifacts, the implementation raises a `ValueError` and adds trainer-level guards that fail fast. This turns a silent data-shape bug into an explicit operational error, which is far easier to monitor and recover from.

Just as important, the split is exposed as metadata, not kept private. Registry snapshots record fields such as `training_mode`, `training_window_start`, `training_window_end`, `validation_window_start`, `validation_window_end`, optional test-window fields, and row counts. The `/models` endpoint then exposes these as top-level fields so the dashboard can render them directly. This closes the loop between modeling policy and operator visibility: when someone sees a weak model, they can immediately inspect whether it was trained on an outdated window, a tiny slice, or the wrong mode.

That metadata makes deployment audits much more honest. A model registry entry is no longer just “best model for rebounds”; it is “best model for rebounds trained in production mode on dates X through Y and validated on dates A through B.” The checkpoint turns temporal context into part of the public contract, which is crucial in time-series systems where most hidden failures are actually failures of time alignment.

## Key Properties

- **Explicit split policy:** `TRAINING_MODE` makes the distinction between production and research semantics machine-readable.
- **Chronological production validation:** Production mode validates on the latest configured windows rather than on a stale static holdout.
- **Research reproducibility:** Research mode preserves prior experimental behavior for stable comparison.
- **Fail-fast guardrails:** Empty-train rolling splits raise errors instead of registering invalid artifacts.
- **Registry visibility:** Training and validation windows become inspectable metadata in snapshots and dashboard views.

## Limitations

Rolling windows improve temporal honesty, but they can increase variance when the latest validation slice is small or unusually noisy. Mode flags also introduce operational complexity: teams must understand which mode a job should run in and avoid comparing research-mode and production-mode metrics as if they were identical. Finally, window metadata is only as useful as the date column quality feeding the splitter.

## Examples

```python
if training_mode == "production":
    train_df, val_df, test_df = rolling_split(df, validation_days=14, test_days=7)
else:
    train_df, val_df, test_df = research_split(df)

if train_df.empty:
    raise ValueError("rolling split left no training rows")

snapshot = {
    "training_mode": training_mode,
    "training_window_start": str(train_df["game_date"].min()),
    "training_window_end": str(train_df["game_date"].max()),
    "validation_window_start": str(val_df["game_date"].min()),
    "validation_window_end": str(val_df["game_date"].max()),
}
```

This is the essential pattern: make the split policy explicit, refuse invalid windows, and publish the resulting temporal boundaries.

## Practical Applications

This concept is broadly useful for forecasting, recommender systems, fraud models, and any ML pipeline where evaluation depends on time order. It is especially important for teams that maintain both research workflows and production retrains in the same codebase and need their model registry to explain not just model quality, but evaluation context.

## Related Concepts

- **[[Calibration Leakage Mitigation in ML Model Training]]** — Both concepts enforce temporal honesty by preventing future information from contaminating evaluation.
- **[[Artifact Registry Validation In ML Pipelines]]** — Registry validation becomes more meaningful when artifacts also expose the windows used to produce them.
- **[[Phased Progress Tracking With Validation Gates]]** — The fail-fast split guard is a concrete validation gate inside model training itself.
- **[[Prior-Season Feature Mapping for Temporal Leakage Prevention]]** — Split-level temporal integrity and feature-level temporal integrity solve adjacent halves of the same problem.

## Sources

- [[Copilot Session Checkpoint: Audit Recommendations Implementation]] — primary source for production vs research training modes, rolling chronological windows, guardrails, and surfaced registry metadata.
