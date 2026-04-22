---
title: "Pipeline Resilience in Machine Learning Systems"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "e46b28ceb3142b4379144f0651127cee40410b71fb087908b377ab58ca92a883"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-pipeline-resilience-fixes-dashboard-metrics-inve-3ea0d6d8.md
quality_score: 79
concepts:
  - pipeline-resilience-in-machine-learning-systems
related:
  - "[[Ensemble Model Save-Round-Trip Validation Gate]]"
  - "[[Out-of-Memory (OOM) Failure Diagnosis and Remediation in ML Containers]]"
  - "[[Copilot Session Checkpoint: Pipeline Resilience Fixes, Dashboard Metrics Investigation]]"
tier: hot
tags: [machine-learning, pipeline-resilience, mlflow, model-fallback]
---

# Pipeline Resilience in Machine Learning Systems

## Overview

Pipeline resilience refers to the design and implementation of mechanisms that allow machine learning systems to continue operating correctly despite failures in components such as model artifacts, external services, or infrastructure. It is critical to maintain service availability, data freshness, and accuracy in production ML pipelines.

## How It Works

Pipeline resilience involves identifying potential points of failure and implementing fallback strategies to mitigate their impact. In the described NBA ML pipeline, resilience was enhanced by:

1. **Model Fallback Loading:** When the primary ensemble model artifact is missing (due to out-of-memory kills or interrupted training), the system attempts to load alternative base models in a prioritized order: CatBoost, XGBoost, LightGBM, and Ridge regression models. This ensures predictions can still be generated even if the ensemble model is unavailable.

2. **MLflow Connectivity Resilience:** The training orchestrator checks MLflow server availability before setting the tracking URI. If MLflow is unreachable (e.g., DNS resolution failure during container restart), it falls back to a local file-based tracking URI, allowing training to proceed without experiment logging interruptions.

3. **Error Diagnosis and Cascading Failure Identification:** The pipeline failure was traced through a chain of issues including missing ensemble models, MLflow DNS failures, and external API authorization errors. Understanding these dependencies is key to designing effective resilience.

4. **Testing and Verification:** Automated tests were created to validate fallback model loading, MLflow resilience, and hit rate consistency, ensuring that resilience mechanisms function as intended.

5. **Monitoring and Metrics Auditing:** Ongoing audits of dashboard metrics and data sources help detect discrepancies early and verify that fallback mechanisms maintain data integrity.

Resilience trade-offs include increased system complexity and potential use of less accurate fallback models, but these are balanced against the need for continuous service availability and data freshness.

## Key Properties

- **Fallback Model Loading Order:** CatBoost > XGBoost > LightGBM > Ridge regression models are tried sequentially when ensemble model artifact is missing.
- **MLflow Connectivity Check:** Connectivity is verified by attempting to search experiments; setting tracking URI alone does not guarantee connectivity.
- **Cascading Failure Impact:** Failures in model artifact availability, training orchestration, and external API authorization can cascade to cause stale or incomplete dashboard data.

## Limitations

Fallback models may have lower predictive accuracy compared to ensemble models, potentially degrading prediction quality temporarily. Local file-based MLflow tracking lacks centralized experiment logging, reducing observability. Resilience mechanisms require careful testing to avoid masking underlying systemic issues.

## Example

In the predictor.py module, the `_try_fallback_model()` method attempts to load alternative models if the ensemble model file is missing:

```python
_FALLBACK_ORDER = ['catboostmodel.pkl', 'xgboostmodel.pkl', 'lightgbmmodel.pkl', 'ridgemodel.pkl']

def _try_fallback_model(self, stat_dir):
    for model_file in _FALLBACK_ORDER:
        path = os.path.join(stat_dir, model_file)
        if os.path.exists(path):
            model = load_model(path)
            return model
    raise FileNotFoundError('No fallback model found')
```

Similarly, in trainer.py, `_ensure_mlflow()` verifies MLflow connectivity and falls back to local tracking:

```python
def _ensure_mlflow():
    try:
        mlflow.set_tracking_uri(config.MLFLOW_TRACKING_URI)
        mlflow.search_experiments(max_results=1)
        _mlflow_available = True
    except Exception:
        mlflow.set_tracking_uri('file:///tmp/mlflow-fallback')
        _mlflow_available = False
```


## Relationship to Other Concepts

- **[[Ensemble Model Save-Round-Trip Validation Gate]]** — Related to ensuring model artifact integrity and availability
- **[[Out-of-Memory (OOM) Failure Diagnosis and Remediation in ML Containers]]** — Related to causes of missing model artifacts due to OOM kills

## Practical Applications

Pipeline resilience techniques are essential in production ML systems where model training and inference depend on multiple components and external services. Implementing fallback loading ensures predictions continue despite partial failures. MLflow resilience allows uninterrupted training even during monitoring service outages. These practices reduce downtime and stale data exposure in dashboards, improving user trust and operational stability.

## Sources

- [[Copilot Session Checkpoint: Pipeline Resilience Fixes, Dashboard Metrics Investigation]] — primary source for this concept
