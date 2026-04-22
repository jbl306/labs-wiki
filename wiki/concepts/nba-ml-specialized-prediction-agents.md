---
title: "NBA-ML Specialized Prediction Agents"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "5d62c5ec9d154108bd891ed92b71cf061018b412b20cfcfc2b686c64b646c9e9"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-nba-ml-agents-and-homelab-fixes-646cf99a.md
quality_score: 67
concepts:
  - nba-ml-specialized-prediction-agents
related:
  - "[[Agent Feedback Loop Mechanism]]"
  - "[[Agent Skill Integration for Time-Series Forecasting]]"
  - "[[Copilot Session Checkpoint: NBA-ML Agents and Homelab Fixes]]"
tier: hot
tags: [nba-ml, ai-agents, model-calibration, feature-engineering, data-quality, backtesting]
---

# NBA-ML Specialized Prediction Agents

## Overview

A set of four specialized AI agents developed to enhance the NBA-ML engine's prediction accuracy and operational robustness. These agents focus on model calibration, feature engineering, data quality validation, and backtesting performance to systematically improve the predictive pipeline.

## How It Works

The NBA-ML specialized agents are designed as context-loaded personas integrated into the Copilot CLI environment to assist in different aspects of the machine learning pipeline:

1. **Model-Calibration Agent:** Focuses on reducing Expected Calibration Error (ECE) by applying techniques such as Platt scaling and isotonic regression per statistic category. It monitors calibration spikes and inverse edge-accuracy problems, adjusting thresholds to improve probability estimates.

2. **Feature-Lab Agent:** Conducts feature engineering experiments and ablation studies to identify impactful features and gaps in the current feature set. It follows an 8-step experimental workflow to systematically test new features and analyze their contribution to model performance.

3. **Data-Quality Agent:** Validates data integrity, including timezone corrections and prop line consistency. It maintains a known bugs table and runs validation queries to detect silent failures and ensure data reliability.

4. **Backtest-Lab Agent:** Performs regression testing and A/B experiments to detect performance regressions before deployment. It executes a 10-point pre-deployment protocol and monitors drawdown metrics to safeguard model stability.

These agents operate under defined activation triggers, priority hierarchies, and diagnostic playbooks. They are integrated into the sprint workflow to automate quality gates and feedback loops, improving the overall prediction hit rate and system robustness.

## Key Properties

- **Integration:** Agents are integrated into the sprint workflow with mapped roles and activation points, enabling automated and semi-automated operation.
- **Calibration Focus:** Model-calibration agent targets reducing ECE from 0.36 towards a target below 0.20.
- **Feature Coverage:** Feature-lab agent identifies 6 missing feature categories and conducts ablation studies.
- **Data Validation:** Data-quality agent addresses timezone fixes and prop line integrity to prevent silent data failures.
- **Pre-Deployment Testing:** Backtest-lab agent enforces a 10-step pre-deployment checklist including A/B testing and drawdown monitoring.

## Limitations

These agents depend on accurate context loading and prompt integration within Copilot CLI; they are not standalone executables. Their effectiveness relies on the quality of input data and the correctness of the sprint workflow integration. Edge cases include unexpected data anomalies or model drift that may require manual intervention beyond automated agent capabilities.

## Example

Example pseudocode for running the model-calibration agent playbook:

```bash
# Run ECE spike diagnostic
copilot run agent model-calibration --playbook ece-spike

# Apply isotonic scaling per stat category
copilot run agent model-calibration --command apply-isotonic-scaling

# Validate calibration improvement
copilot run agent model-calibration --playbook validate-calibration
```

## Relationship to Other Concepts

- **[[Agent Feedback Loop Mechanism]]** — The agents implement feedback loops to iteratively improve model performance.
- **[[Agent Skill Integration for Time-Series Forecasting]]** — These agents specialize skills relevant to time-series and sports prediction.

## Practical Applications

Used in production NBA fantasy sports prediction pipelines to improve hit rates, reduce calibration error, and ensure data and model quality before deployment. The agents automate critical quality gates and testing phases in the sprint cycle, enabling more reliable and profitable betting predictions.

## Sources

- [[Copilot Session Checkpoint: NBA-ML Agents and Homelab Fixes]] — primary source for this concept
