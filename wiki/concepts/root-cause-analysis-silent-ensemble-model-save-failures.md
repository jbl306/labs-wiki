---
title: "Root-Cause Analysis of Silent Ensemble Model Save Failures"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "665c60129067f8fba29792521cb202b0e0ab91fc22982f1f58081019b034c549"
sources:
  - raw/2026-04-18-copilot-session-sprint-57-ensemble-save-diagnosis-e2943da5.md
quality_score: 100
concepts:
  - root-cause-analysis-silent-ensemble-model-save-failures
related:
  - "[[Artifact Registry Validation In ML Pipelines]]"
  - "[[Copilot Session Checkpoint: Sprint 57 Ensemble Save Diagnosis]]"
tier: hot
tags: [root-cause-analysis, ml-pipeline, artifact-saving, diagnosis, logging]
---

# Root-Cause Analysis of Silent Ensemble Model Save Failures

## Overview

Root-cause analysis is the systematic investigation of why the NBA ML Engine's ensemble model saving process failed silently for certain stats during Sprint 57. It involves log inspection, code tracing, and hypothesis testing to identify the underlying failure modes and inform remediation strategies.

## How It Works

The root-cause analysis process begins with the observation that, during a specific training run (2026-04-16), the `EnsembleModel.save()` method failed to persist `ensemblemodel.pkl` artifacts for several stats (pts, reb, ast, blk, tov), while others (stl, fg3m) were saved successfully. This asymmetry is suspicious and suggests a deeper issue in the artifact saving pipeline.

The investigation proceeds by examining relevant code sections:
- In `src/models/ensemble.py:189-215`, the `save()` method writes base model artifacts to a subdirectory, then pickles the meta model and metadata to the main path. A silent failure could occur if `pickle.dump` raises an exception after base models are written, but the error is not caught or logged.
- In `src/training/trainer.py:714-738`, the training loop calls `model.save(model_path)` followed by artifact logging. The absence of a try/except block means that exceptions in saving could terminate the process or be missed if the save call is skipped due to process interruption (e.g., OOM kill).

Audit logs from Sprint 56 reveal a key asymmetry: stl and fg3m had `ensemblemodel.pkl` but were missing `catboostmodel.pkl`, while pts/reb/ast/blk/tov had all base learner pkls but no ensemblemodel.pkl. This pattern suggests that the training loop may iterate over models in a specific order, and if the process is interrupted (e.g., OOM-killed) after base learners, the ensemble save step never executes.

Further investigation includes inspecting scheduler logs (`docker logs nba-ml-scheduler`) and mlflow logs around the relevant time window to identify signs of OOM, silent exceptions, or configuration-driven skips. The analysis also considers whether the model configuration changed (e.g., CatBoost removed for stl, Ensemble added), which could explain the inverse artifact patterns.

The root-cause analysis informs remediation strategies, such as hardening the save method, adding validation gates, and improving logging. It also highlights the importance of atomic writes and immediate validation to catch failures early.

## Key Properties

- **Systematic Log Inspection:** Analyzes scheduler and mlflow logs to identify signs of OOM, silent exceptions, or process interruptions.
- **Code Path Tracing:** Examines relevant code sections to understand how and where silent failures could occur.
- **Pattern Recognition:** Identifies asymmetries in artifact presence across stats to hypothesize about loop ordering and process interruptions.
- **Hypothesis Testing:** Tests possible causes (OOM, config changes, serialization errors) to narrow down the actual failure mode.

## Limitations

Root-cause analysis is only as effective as the available logs and code clarity. If logs are missing or incomplete, certain failure modes may remain undetected. It can be time-consuming and may require multiple iterations to confirm hypotheses. Some issues, such as hardware failures or rare race conditions, may be difficult to reproduce.

## Example

Inspecting logs:
```bash
docker logs nba-ml-scheduler 2>&1 | grep -A5 -E "(EnsembleModel|ensemblemodel\.pkl|save|OOM|killed)"
```
Code tracing:
- src/models/ensemble.py:189-215 (save method)
- src/training/trainer.py:714-738 (training loop)
Pattern recognition:
- stl and fg3m: ensemblemodel.pkl present, catboostmodel.pkl missing
- pts/reb/ast/blk/tov: base learner pkls present, ensemblemodel.pkl missing

## Visual

Null (no diagrams or charts in source).

## Relationship to Other Concepts

- **[[Artifact Registry Validation In ML Pipelines]]** — Root-cause analysis informs registry validation strategies by identifying failure modes in artifact saving.

## Practical Applications

Used in ML engineering to diagnose and fix silent failures in artifact saving, ensuring model reliability and integrity. Applicable in any production pipeline where artifact persistence is critical, such as financial models, healthcare systems, or sports analytics engines.

## Sources

- [[Copilot Session Checkpoint: Sprint 57 Ensemble Save Diagnosis]] — primary source for this concept
