---
title: "Classifier Stats Extension and Calibration Audit"
type: concept
created: 2026-04-19
last_verified: 2026-04-19
source_hash: "d9cea72e0198e7d3d24aa2f2351ac17ebe1246338b49cf42f47130ad7dc14949"
sources:
  - raw/2026-04-19-copilot-session-sprint-60-pts-feature-planning-abd21993.md
quality_score: 100
concepts:
  - classifier-stats-extension-calibration-audit
related:
  - "[[Confidence Calibration Analysis in Machine Learning Models]]"
  - "[[Copilot Session Checkpoint: Sprint 60 PTS Feature Planning]]"
tier: hot
tags: [classifier-extension, calibration-audit, ece, platt-scaling, nba-ml]
---

# Classifier Stats Extension and Calibration Audit

## Overview

Sprint 60 includes extending classifier stats to new categories (fg_pct, ft_pct) and performing a calibration audit across all stat models. This ensures model outputs are well-calibrated and that classifier coverage aligns with available target columns.

## How It Works

The process begins with an audit of the configuration files ('config.py'), where 'CLASSIFIER_STATS' is defined. The extension involves adding new stats (fg_pct, ft_pct) to the classifier list, but only if these stats exist as target columns in the feature builder output. If not, the scope is limited to calibration and feature improvements.

Calibration audit is performed by running per-stat Expected Calibration Error (ECE) on models retrained as of 2026-04-17. The audit uses scripts in 'src/evaluation/calibration.py', evaluating each stat's predicted probabilities against actual outcomes. If any stat exhibits ECE greater than 0.05, Platt scaling is applied and calibrators are saved to 'models/calibrators/per_stat/'.

The audit is critical for ensuring that classifier outputs are interpretable and reliable, especially as new stats are added. It also informs whether retraining or additional calibration steps are needed before deployment. The process is documented in a JSON report for transparency and reproducibility.

Edge cases include missing target columns for new stats, which blocks classifier extension. The audit must handle stats with low sample sizes or imbalanced classes, adjusting calibration methods as needed. For stats with persistent calibration errors, further feature engineering or model selection may be required.

Trade-offs include additional computational overhead for calibration, and potential complexity in managing calibrators across multiple stats. The process is tightly integrated with the ML deployment protocol, ensuring only well-calibrated models are promoted.

## Key Properties

- **Config-Driven Classifier Extension:** Extends classifier stats in config files, contingent on target column availability.
- **Per-Stat Calibration Audit:** Runs ECE checks and applies Platt scaling for stats with calibration errors.
- **JSON Reporting:** Documents calibration results in a structured report for transparency.
- **Deployment Protocol Integration:** Calibration audit is required before model deployment, ensuring reliability.

## Limitations

Blocked if target columns for new stats do not exist. Calibration audit may be less effective for stats with low sample sizes or extreme class imbalance. Managing calibrators across many stats can be complex.

## Example

```python
for stat in CLASSIFIER_STATS:
    model = load_model(stat)
    ece = compute_ece(model, test_data)
    if ece > 0.05:
        calibrator = fit_platt_scaling(model, test_data)
        save_calibrator(stat, calibrator)
    report[stat] = {'ece': ece, 'calibrator_applied': ece > 0.05}
write_json_report(report, 'calibration_audit.json')
```

## Relationship to Other Concepts

- **[[Confidence Calibration Analysis in Machine Learning Models]]** — This concept operationalizes calibration analysis for NBA ML Engine classifier stats.

## Practical Applications

Ensures NBA ML Engine classifier outputs are well-calibrated for stats like points, assists, fg_pct, ft_pct. Critical for production deployment, betting, and analytics where probability estimates must be reliable.

## Sources

- [[Copilot Session Checkpoint: Sprint 60 PTS Feature Planning]] — primary source for this concept
