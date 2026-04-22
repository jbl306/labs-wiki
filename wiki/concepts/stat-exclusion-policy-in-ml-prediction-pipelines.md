---
title: "Stat Exclusion Policy In ML Prediction Pipelines"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "e3e47d55fb1d0008f60d9a2e427faad4b28e2a2e353601179a533125dc59d19e"
sources:
  - raw/2026-04-18-copilot-session-sprint-56-no-retrain-fixes-planning-895454cb.md
quality_score: 76
concepts:
  - stat-exclusion-policy-in-ml-prediction-pipelines
related:
  - "[[Selective Tool Loading and Context Hygiene]]"
  - "[[Copilot Session Checkpoint: Sprint 56 No-Retrain Fixes Planning]]"
tier: hot
tags: [ml-pipeline, stat-exclusion, configuration, dashboard, production]
---

# Stat Exclusion Policy In ML Prediction Pipelines

## Overview

Stat exclusion policy is a configuration-driven mechanism that disables specific prediction targets (stats) across ML pipelines, dashboards, and downstream applications. By updating exclusion lists and cascading changes through code and UI, problematic or deprecated stats (such as PRA, fg_pct, ft_pct) are systematically removed from production, reducing error surfaces and improving hit rate reliability.

## How It Works

Stat exclusion operates via centralized configuration, typically in files like `config.py`, where lists such as `EXCLUDED_PROP_STATS` enumerate stats to be disabled. When a stat (e.g., 'pra') is added to this list, the exclusion cascades through all code paths: inference routines, evaluation modules, edge policies, and dashboard components.

In inference code (e.g., `src/inference/predictor.py:472-497`), stat-specific blocks (such as PRA composite prediction) are gated by checks against the exclusion list. If the stat is excluded, the block is skipped, preventing predictions and storage for that stat. SQL cleanup routines remove existing predictions from the database, ensuring dashboards do not surface stale bets.

Dashboard policies (e.g., `dashboard-ui/server/src/index.ts`) update fallback and threshold maps, removing excluded stats from UI dropdowns and panels. This ensures users cannot select or view predictions for retired stats. The exclusion policy is also reflected in model registry updates, demoting production entries for excluded stats via SQL.

Edge cases include stale exclusion lists, inconsistent UI updates, and accidental exclusion of critical stats (e.g., pts, ast). The policy requires careful audit and testing to ensure only intended stats are disabled and that all affected surfaces are updated. Trade-offs involve balancing operational simplicity with flexibility; exclusion is fast but may require retraining or policy revision for restoration.

## Key Properties

- **Centralized Configuration:** Stat exclusion is managed via config files, enabling rapid updates and consistent propagation.
- **Code Path Cascading:** Exclusion cascades through inference, evaluation, dashboard, and registry modules, ensuring comprehensive removal.
- **SQL and UI Cleanup:** Database and dashboard components are updated to remove predictions and options for excluded stats.
- **Testing and Validation:** Automated tests verify exclusion behavior, preventing accidental prediction or surfacing of retired stats.

## Limitations

Exclusion is configuration-driven; errors in lists or code audits can leave stats partially active. Restoration requires careful policy revision and, in some cases, retraining. UI and database cleanup must be thorough to prevent surfacing stale predictions. Over-exclusion can reduce pipeline flexibility.

## Example

```python
# Add 'pra' to exclusion list
EXCLUDED_PROP_STATS = ['pra', ...]

# Gate PRA prediction
if 'pra' not in EXCLUDED_PROP_STATS:
    # Write PRA composite prediction
```

SQL cleanup:
```sql
DELETE FROM predictions WHERE stat_name='pra' AND game_date >= CURRENT_DATE;
```

## Relationship to Other Concepts

- **[[Selective Tool Loading and Context Hygiene]]** — Both use exclusion lists to manage operational scope and reduce error surfaces.

## Practical Applications

Applied in ML pipelines for sports, finance, and other domains where certain stats become unreliable, deprecated, or problematic. Enables rapid response to API changes, quota exhaustion, or model drift by disabling affected stats without retraining.

## Sources

- [[Copilot Session Checkpoint: Sprint 56 No-Retrain Fixes Planning]] — primary source for this concept
