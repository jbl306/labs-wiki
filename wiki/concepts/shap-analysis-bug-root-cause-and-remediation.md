---
title: "SHAP Analysis Bug Root Cause and Remediation"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "924e132f95d9fa94650d78f540b91683d2ddb7c4f20d9fb9d776cf74f1885c5a"
sources:
  - raw/2026-04-18-copilot-session-sprint-58-shap-bug-planning-dfccfb5c.md
quality_score: 76
concepts:
  - shap-analysis-bug-root-cause-and-remediation
related:
  - "[[LightGBM Feature Importance and SHAP Values]]"
  - "[[Copilot Session Checkpoint: Sprint 58 SHAP Bug Planning]]"
tier: hot
tags: [ml-engineering, explainability, bug-fix, schema-mapping, shap]
---

# SHAP Analysis Bug Root Cause and Remediation

## Overview

The SHAP analysis bug in the NBA ML Engine was caused by schema drift and a custom model serialization format, leading to failures in post-training explainability routines. Fixing this bug requires careful mapping between database schema, model class resolution, and SHAP's requirements for tree-based models.

## How It Works

The SHAP bug emerged during post-training analysis when the SHAP script attempted to load production models from the registry. The registry schema had changed: the expected `stat_name` and `model_path` columns no longer existed. Instead, the statistical target (e.g., 'pts', 'reb') was encoded as a suffix in the `model_name` field (e.g., `EnsembleModel_pts`). The artifact path was stored in `artifact_path`, not `model_path`. This required updating the filtering logic in the SHAP script to use `model_name.like(f"%_{stat_name}")` and to read the correct column for file paths.

A deeper issue was the custom serialization format: each model's `save()` method pickled a dictionary containing keys like `model`, `feature_names`, `params`, and `residuals`, rather than a raw sklearn estimator. As a result, `joblib.load(pkl)` returned a dict, not a regressor object. SHAP's `TreeExplainer` expects a tree-based model object (e.g., XGBoost, LightGBM, CatBoost, RandomForest), so the script needed to instantiate the correct model class, call its `.load(path)` method, and then pass the inner `.model` attribute to SHAP.

Model class resolution was handled by parsing the `model_name` prefix (before the underscore) and mapping it to a class using a lookup dictionary built from the `MODEL_CLASSES` list in the training module, supplemented with custom classes like `EnsembleModel` and `MinutesModel`. If the resolved class was not supported by SHAP (e.g., RidgeModel or EnsembleModel), the script would log a warning and return a stub result indicating the analysis was skipped.

The fix plan involved:
- Updating the database query and file path resolution in the SHAP script.
- Building a robust class lookup for model instantiation.
- Ensuring only supported models were passed to SHAP, with graceful skipping for unsupported types.
- Adding comprehensive tests to verify correct class resolution, error handling, and atomic save integrity.

This approach ensured that SHAP analysis would work reliably for tree-based models, while providing clear diagnostics and fallback behavior for unsupported cases.

## Key Properties

- **Schema-Aware Model Resolution:** Model class and stat are inferred from the `model_name` field, not separate columns. Filtering uses SQL LIKE patterns.
- **Custom Serialization Format:** Models are saved as pickled dictionaries with keys for estimator, features, parameters, and residuals, requiring class-specific loading.
- **SHAP Support Constraints:** Only tree-based models (CatBoost, XGBoost, LightGBM, RandomForest) are supported by SHAP's TreeExplainer. Ridge and Ensemble models are skipped.
- **Graceful Skipping:** Unsupported models are detected and analysis is skipped with a warning and stub result.

## Limitations

SHAP analysis is limited to tree-based models; linear and meta-ensemble models are not supported and must be skipped. The fix relies on correct parsing of `model_name` and assumes consistent naming conventions. Any further schema drift or changes in serialization format could require additional updates.

## Example

```python
# Example: Loading a production model for SHAP
stat_name = 'pts'
model_row = session.query(ModelRegistry).filter(ModelRegistry.model_name.like(f'%_{stat_name}'), ModelRegistry.is_production==True).first()
class_name = model_row.model_name.rsplit('_', 1)[0]
model_class = MODEL_CLASSES[class_name]
instance = model_class()
instance.load(model_row.artifact_path)
if class_name in ['RidgeModel', 'EnsembleModel']:
    return {'stat': stat_name, 'skipped': True, 'reason': f'TreeExplainer does not support {class_name}'}
explainer = shap.TreeExplainer(instance.model)
```

## Relationship to Other Concepts

- **[[LightGBM Feature Importance and SHAP Values]]** — Both involve SHAP explainability, but this concept focuses on bug remediation and schema mapping.

## Practical Applications

Ensures robust post-training explainability for production ML models, allowing for accurate feature importance analysis and diagnostics. The approach is applicable to any ML pipeline with evolving schemas and custom serialization formats, especially in ensemble and tree-based modeling contexts.

## Sources

- [[Copilot Session Checkpoint: Sprint 58 SHAP Bug Planning]] — primary source for this concept
