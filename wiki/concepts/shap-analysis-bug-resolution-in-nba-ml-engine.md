---
title: "SHAP Analysis Bug Resolution In NBA ML Engine"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "924e132f95d9fa94650d78f540b91683d2ddb7c4f20d9fb9d776cf74f1885c5a"
sources:
  - raw/2026-04-18-copilot-session-sprint-58-shap-bug-planning-dfccfb5c.md
quality_score: 79
concepts:
  - shap-analysis-bug-resolution-in-nba-ml-engine
related:
  - "[[LightGBM Feature Importance and SHAP Values]]"
  - "[[Ensemble Model Save-Round-Trip Validation Gate]]"
  - "[[Copilot Session Checkpoint: Sprint 58 SHAP Bug Planning]]"
tier: hot
tags: [ML explainability, SHAP, schema drift, model registry, atomic save, bug resolution]
---

# SHAP Analysis Bug Resolution In NBA ML Engine

## Overview

This concept describes the systematic resolution of a SHAP analysis bug in the NBA ML Engine, caused by schema drift and incorrect handling of model serialization. The bug prevented post-training SHAP analysis, impacting model explainability and workflow reliability. The fix involves correcting registry queries, model loading logic, and gracefully handling unsupported model types.

## How It Works

The SHAP analysis bug originated from three distinct issues in the NBA ML Engine's post-training workflow:

1. **Schema Drift in ModelRegistry**: The SHAP analysis script incorrectly assumed the existence of `stat_name` and `model_path` columns in the ModelRegistry database schema. In reality, the stat is encoded in the `model_name` suffix (e.g., `EnsembleModel_pts`), and the artifact path is stored in `artifact_path`. The fix requires filtering registry rows using `model_name.like(f"%_{stat_name}")` and reading the correct column for the model artifact.

2. **Custom Model Serialization Format**: Each model class (CatBoost, XGBoost, LightGBM, RandomForest, Ridge, Ensemble) saves artifacts as a pickled dictionary containing keys such as `model`, `feature_names`, `params`, and `residuals`. The previous SHAP script attempted to load these artifacts with `joblib.load(pkl)`, expecting a raw regressor, which resulted in errors. The correct approach is to instantiate the appropriate model class, call its `.load(path)` method, and extract the inner estimator via `instance.model` for SHAP analysis.

3. **TreeExplainer Compatibility**: SHAP's `TreeExplainer` only supports tree-based models (CatBoost, XGBoost, LightGBM, RandomForest). It does not support Ridge (linear regression) or custom EnsembleModel (meta-learner). The revised workflow adds an early-return mechanism: if the resolved class is RidgeModel or EnsembleModel, the script logs a warning and returns a stub result indicating the analysis was skipped, along with a reason.

**Algorithmic Steps:**
- Query ModelRegistry for production models matching the stat suffix.
- Resolve the model class from `model_name` using a lookup built from `MODEL_CLASSES` and additional custom classes.
- Instantiate the model class and call `.load(artifact_path)`.
- For supported tree-based models, pass `instance.model` and `instance.feature_names` to SHAP's `TreeExplainer`.
- For unsupported models, return a stub result and log a warning.

**Edge Cases & Trade-Offs:**
- If the registry row is missing or malformed, the script raises a `ValueError`.
- The fix ensures that only valid models are analyzed, preventing silent failures and improving observability.
- The trade-off is that linear and ensemble models are excluded from SHAP explainability, but this is necessary due to SHAP's limitations.

**Testing:**
- Mocked registry rows are used to verify correct class resolution and error handling.
- Tests ensure atomic save integrity and absence of leftover temporary files in failure scenarios.

## Key Properties

- **Registry Query Robustness:** Uses suffix-based filtering on `model_name` and correct artifact path resolution to avoid schema drift errors.
- **Model Serialization Awareness:** Handles custom pickled dict format by invoking class-specific `.load()` methods, ensuring compatibility with SHAP.
- **Graceful Handling of Unsupported Models:** Skips SHAP analysis for Ridge and Ensemble models, returning stub results and logging warnings.
- **Improved Observability:** Logs warnings and returns explicit results for skipped analyses, preventing silent workflow failures.

## Limitations

SHAP analysis is limited to tree-based models; Ridge and Ensemble models are excluded due to SHAP's algorithmic constraints. If registry rows are missing or malformed, the script raises errors. The fix does not address explainability for unsupported model types.

## Example

```python
# Example: SHAP analysis dispatch
row = registry.query(ModelRegistry).filter(ModelRegistry.model_name.like('%_pts')).first()
class_name = row.model_name.rsplit('_', 1)[0]
model_class = MODEL_CLASSES[class_name]
instance = model_class()
instance.load(row.artifact_path)
if class_name in ['RidgeModel', 'EnsembleModel']:
    return {'stat': 'pts', 'skipped': True, 'reason': 'TreeExplainer does not support RidgeModel'}
explainer = shap.TreeExplainer(instance.model)
shap_values = explainer.shap_values(X)
```

## Relationship to Other Concepts

- **[[LightGBM Feature Importance and SHAP Values]]** — Both involve SHAP explainability for tree-based models; this concept extends SHAP analysis to a multi-model registry context.
- **[[Ensemble Model Save-Round-Trip Validation Gate]]** — Both address post-training validation and artifact integrity in ensemble workflows.

## Practical Applications

Ensures reliable post-training explainability in production ML pipelines, especially for regulatory or audit requirements. Prevents silent failures in automated model deployment workflows. Enables robust debugging and observability for model selection and artifact management.

## Sources

- [[Copilot Session Checkpoint: Sprint 58 SHAP Bug Planning]] — primary source for this concept
