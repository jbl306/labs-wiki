---
title: "Registry Health Validation via Scheduled Cron"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "924e132f95d9fa94650d78f540b91683d2ddb7c4f20d9fb9d776cf74f1885c5a"
sources:
  - raw/2026-04-18-copilot-session-sprint-58-shap-bug-planning-dfccfb5c.md
quality_score: 76
concepts:
  - registry-health-validation-via-scheduled-cron
related:
  - "[[Ensemble Model Save-Round-Trip Validation Gate]]"
  - "[[Copilot Session Checkpoint: Sprint 58 SHAP Bug Planning]]"
tier: hot
tags: [ml-engineering, registry-health, cron, artifact-validation, reliability]
---

# Registry Health Validation via Scheduled Cron

## Overview

Registry health validation is a proactive maintenance routine that checks the consistency and integrity of production model artifacts. In Sprint 58, this is implemented as a daily cron job using Ofelia to ensure the NBA ML Engine's registry remains healthy.

## How It Works

The registry health validation process involves running a script that inspects the production model registry and verifies that all expected artifacts are present, correctly formatted, and loadable. This is crucial for preventing silent failures in prediction and explainability routines.

The implementation uses Ofelia, a containerized job scheduler, to execute the validation script daily. The script calls `validate_production_artifacts(session)` from the inference module, which checks each production model's artifact path, attempts to load the model, and confirms its integrity. Any missing or corrupted artifacts are flagged for remediation.

The cron job is configured via Docker Compose labels, specifying the schedule, container, and command to run. The command initializes a database session, runs the validation function, and closes the session. This ensures that the registry is checked independently of retraining or deployment events.

By automating registry health checks, the pipeline can detect issues early, trigger alerts or remediation tasks, and maintain high reliability for downstream jobs. This is especially important as the model registry evolves and new artifacts are added or replaced.

## Key Properties

- **Automated Scheduling:** Runs daily via Ofelia cron, independent of manual retrain or deployment events.
- **Artifact Integrity Checking:** Validates presence, format, and loadability of all production model artifacts.
- **Early Failure Detection:** Flags missing or corrupted artifacts before they impact predictions or explainability.

## Limitations

Relies on correct configuration of cron and Docker Compose. If validation logic is incomplete, some errors may go undetected. Does not automatically remediate issues; manual intervention may be required.

## Example

```yaml
ofelia.job-exec.registry-health.schedule: "0 0 12 * * *"  # 07:00 ET daily
ofelia.job-exec.registry-health.container: nba-ml-api
ofelia.job-exec.registry-health.command: "python -c 'from src.db.connection import get_session; from src.inference.registry_health import validate_production_artifacts; s=get_session(); validate_production_artifacts(s); s.close()'"
```

## Relationship to Other Concepts

- **[[Ensemble Model Save-Round-Trip Validation Gate]]** — Both focus on validating model artifact integrity, but this concept applies to the entire registry.

## Practical Applications

Maintains production reliability by ensuring model artifacts are always available and valid. Reduces downtime and prevents explainability or prediction failures due to missing or corrupted files.

## Sources

- [[Copilot Session Checkpoint: Sprint 58 SHAP Bug Planning]] — primary source for this concept
