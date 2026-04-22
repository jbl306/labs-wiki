---
title: "Recurring checkpoint patterns: Feature Engineering for NBA ML Engine Sprint 10, Warmstarting Hyperparameter Tuning with Optuna, Target Encoding with Shifted Expanding Mean for Time-Series Features"
type: synthesis
created: 2026-04-22
last_verified: 2026-04-22
source_hash: "synthesis-generated"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-implementing-sprint-29-ml-improvements-986267e7.md
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-10-complete-and-deployed-cb380016.md
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-10-implementation-and-deployment-693c9264.md
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-10-retrain-in-progress-742b0d94.md
concepts:
  - feature-engineering-for-nba-ml-engine-sprint-10
  - walk-forward-cross-validation-for-model-selection
  - warmstarting-hyperparameter-tuning-with-optuna
  - target-encoding-with-shifted-expanding-mean-for-time-series-features
related:
  - "[[Warmstarting Hyperparameter Tuning with Optuna]]"
  - "[[Copilot Session Checkpoint: Sprint 10 Retrain In Progress]]"
  - "[[Feature Engineering for NBA ML Engine Sprint 10]]"
  - "[[Target Encoding with Shifted Expanding Mean for Time-Series Features]]"
  - "[[Copilot Session Checkpoint: Implementing Sprint 29 ML Improvements]]"
  - "[[Copilot Session Checkpoint: Sprint 10 Implementation and Deployment]]"
  - "[[Copilot Session Checkpoint: Sprint 10 Complete and Deployed]]"
  - "[[Walk-Forward Cross-Validation for Model Selection]]"
tier: hot
checkpoint_cluster_community: 7
checkpoint_cluster_checkpoint_count: 4
checkpoint_cluster_signature: 7df12a16e3129cf6
tags: [checkpoint, checkpoint-synthesis, copilot-session, dashboard, durable-knowledge, fileback, homelab, machine learning, nba-ml-engine]
quality_score: 75
---

# Recurring checkpoint patterns: Feature Engineering for NBA ML Engine Sprint 10, Warmstarting Hyperparameter Tuning with Optuna, Target Encoding with Shifted Expanding Mean for Time-Series Features

## Question

What recurring decisions, fixes, and durable patterns appear across the 4 session checkpoints in this cluster, especially around Feature Engineering for NBA ML Engine Sprint 10, Warmstarting Hyperparameter Tuning with Optuna, Target Encoding with Shifted Expanding Mean for Time-Series Features?

## Summary

Across 4 NBA-ML feature-engineering and tuning checkpoints the recurring loop is: ship a new feature group, immediately wrap it in leak-prevention and stability guards (shifted-expanding-mean target encoding, walk-forward CV, NaN→default coercion), then warmstart Optuna from the prior best params so retraining converges fast. The thread is that *every* added expressivity (features, encodings, hyperparameter range) has a paired discipline that prevents that expressivity from contaminating the eval signal.

## Comparison

| Dimension | [[Feature Engineering for NBA ML Engine Sprint 10]] | [[Warmstarting Hyperparameter Tuning with Optuna]] | [[Target Encoding with Shifted Expanding Mean for Time-Series Features]] | [[Walk-Forward Cross-Validation for Model Selection]] |
|-----------|---------------------||---------------------||---------------------||---------------------|
| What it adds | Six feature groups (~20 features): B2B fatigue, minutes trend, injury return, season phase, matchup, target-encoded team/opp pts/reb/ast. Final matrix: 95,271 × 417. | Reuses prior best params via study.enqueue_trial(); seeds the next study with proven configurations. | Per-team/opp historical mean of target up to t-1 (min 10 prior obs). | Expanding-window splits; nested dict of metrics; selects model by cv_avg_val_mse → val_mse → test_mse → train_mse. |
| Contamination it prevents | NaN propagation in pd.cut (rest categories) → fixed by float-fill-int round trip. | Spending compute re-discovering already-known-good configurations. | Future-leakage from naive group-mean target encoding. | Lookahead bias from random or k-fold splits in time-series data. |
| Persistence mechanism | Modular `src/features/builder.py`—each group plugs in independently. | MLflow ModelRegistry config_snapshot.tuned_params persists across retrains. | USE_TARGET_ENCODING config flag gates inclusion; pandas shift+expanding kept in builder. | _run_walk_forward_cv returns a nested dict so trainer.py can choose by metric chain. |
| Cost paid for the discipline | Wider matrix → longer training; overfitting risk if not regularized. | Bias toward the prior best when data shifts—needs occasional cold restarts. | Sparse categories with <10 obs are missing for the warmup window. | N× training cost per fold; defers model registration until all folds finish. |

## Analysis

Sprint 10 is the smallest cluster in the wiki and the one with the clearest 'feature + guard' pairing. Every concept in the cluster *adds* something to the model's expressive surface and pairs it with a discipline that bounds the new failure mode that addition introduced.

Target encoding is the cleanest example. Adding per-team/opponent target means is a known winning move on time-series sports data; the catch is that the naive encoding leaks future information the moment you compute it on the full series. The shifted-expanding-mean implementation (`x.shift(1).expanding(min_periods=10).mean()`) is one line of pandas, but it's the difference between a feature that lifts holdout MSE and one that silently lifts in-sample MSE only.

Walk-forward CV is the eval-side counterpart. Once features have temporal meaning, k-fold CV becomes lookahead. The refactor that made `_run_walk_forward_cv` return a nested metric dict was small but load-bearing: the model-selection chain (cv_avg_val_mse → val_mse → test_mse → train_mse) now has somewhere to read from, and registration is *deferred* until the whole CV finishes—so a model that only looked good on its last fold can't be promoted.

Warmstarting is what makes the whole loop affordable. New feature groups arrive in every sprint; without warmstart, Optuna would explore the parameter space from scratch each time. Persisting `tuned_params` in the MLflow ModelRegistry config snapshot and replaying via `study.enqueue_trial()` lets the new study spend its trial budget exploring near the prior optimum rather than rediscovering it.

The NaN-handling fix in Sprint 10's rest-category feature is small in code (`astype(float).fillna(3).astype(int)`) but emblematic: even the tiniest expressivity increase—a bin from `pd.cut`—needs a contamination guard. The lesson the cluster embeds is that *every* added knob deserves a guard rail in the same PR.

## Key Insights

1. **The Sprint 10 cluster is the wiki's clearest demonstration of a 'feature + paired discipline' pattern: every feature addition (target encoding, B2B, season phase) shipped with a leak/stability guard (shifted expanding mean, walk-forward CV, NaN coercion).** — supported by [[Feature Engineering for NBA ML Engine Sprint 10]], [[Target Encoding with Shifted Expanding Mean for Time-Series Features]], [[Walk-Forward Cross-Validation for Model Selection]]
2. **Warmstarting via study.enqueue_trial isn't an optimization—it's what makes per-sprint retraining tractable; without it, every sprint pays full Optuna cost from scratch and the iteration loop breaks.** — supported by [[Warmstarting Hyperparameter Tuning with Optuna]]
3. **The model-selection fallback chain (cv_avg_val_mse → val_mse → test_mse → train_mse) encodes a temporal-honesty hierarchy that survives missing metrics in early folds—it's a defensive design, not just a default.** — supported by [[Walk-Forward Cross-Validation for Model Selection]]

## Open Questions

- What is the warmstart bias-vs-explore trade-off in seasons with regime shift (rule changes, paced changes)? Should warmstart be disabled or weighted down when a drift detector trips?
- Should target-encoding's `min_periods=10` floor be tuned per category cardinality—e.g. lower for small leagues/seasons, higher for stat types with high game-to-game variance?
- Is there a meaningful difference in selected model when cv_avg_val_mse and val_mse disagree, and if so, which has historically held up out-of-sample?

## Sources

- [[Copilot Session Checkpoint: Implementing Sprint 29 ML Improvements]]
- [[Copilot Session Checkpoint: Sprint 10 Complete and Deployed]]
- [[Copilot Session Checkpoint: Sprint 10 Implementation and Deployment]]
- [[Copilot Session Checkpoint: Sprint 10 Retrain In Progress]]
