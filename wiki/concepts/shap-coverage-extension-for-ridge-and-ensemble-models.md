---
title: "SHAP Coverage Extension for Ridge and Ensemble Models"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "8e3ec5b24e92a02a9a1b03fb00f1bdd35fbc8dbe8d7723b1a284751ce576ff29"
sources:
  - raw/2026-04-18-copilot-session-sprint-59-shap-coverage-implementation-9a231f70.md
quality_score: 100
concepts:
  - shap-coverage-extension-for-ridge-and-ensemble-models
related:
  - "[[LightGBM Feature Importance and SHAP Values]]"
  - "[[SHAP Analysis Bug Resolution In NBA ML Engine]]"
  - "[[Copilot Session Checkpoint: Sprint 59 SHAP Coverage Implementation]]"
tier: hot
tags: [shap, ridge, ensemble-model, explainability, nba-ml-engine]
---

# SHAP Coverage Extension for Ridge and Ensemble Models

## Overview

This concept details the extension of SHAP (SHapley Additive exPlanations) coverage to Ridge regression models and ensemble models within the NBA ML Engine. The implementation leverages SHAP's LinearExplainer for Ridge models, ensuring proper handling of feature scaling, and introduces a weighted aggregation approach for ensemble models, projecting base model SHAP values onto a unified feature axis.

## How It Works

SHAP explainability provides per-feature attribution for model predictions, crucial for understanding and debugging machine learning models in production. In Sprint 59, SHAP coverage was extended to two new model types: Ridge regression (via LinearExplainer) and ensemble models (via weighted aggregation).

**Ridge LinearExplainer Path:**
RidgeModel wrappers in the NBA ML Engine include both a StandardScaler (`self.scaler`) and the Ridge estimator (`self.model`). For SHAP analysis, the input features (`X`) must be transformed using the scaler before passing to SHAP's LinearExplainer. The explainer is instantiated as `shap.LinearExplainer(estimator, background)`, where `background` consists of the first 100 rows of the scaled feature matrix. If the SHAP API version is older, an exception fallback uses `LinearExplainer((coef_, intercept_), bg)`. This ensures SHAP values are computed in the same feature space as model inference, maintaining fidelity.

**Ensemble SHAP Aggregation:**
EnsembleModel objects contain a list of base models organized by fold and index (`List[List[BaseModel]]`). The ensemble prediction is computed as a weighted average of base model predictions across folds, with weights determined by inverse mean absolute error (MAE) performance. SHAP's additivity property allows for linear aggregation: each base model's SHAP values are weighted identically to its prediction weight. However, base models may have differing feature sets, so their SHAP matrices (shape: n_samples × n_base_features) must be projected onto the ensemble's feature axis. This is achieved using pandas DataFrame's `reindex(columns=feat_axis, fill_value=0.0)`, aligning features and filling missing values with zero. The helper function `wrapper._align_for_base(X, base_model)` ensures proper alignment.

**Performance and Sampling:**
Ensemble SHAP computation is significantly more expensive than single-model SHAP due to the need to aggregate across multiple base models and folds. To mitigate this, the implementation subsamples input data, setting `effective_max = min(max_samples, 300)`. This reduces computational load but still results in SHAP analysis being roughly five times slower than a single TreeExplainer run.

**Dispatch Architecture:**
The rewritten `scripts/shap_analysis.py` organizes models into four class sets: `_TREE_MODEL_CLASSES`, `_LINEAR_MODEL_CLASSES`, `_ENSEMBLE_MODEL_CLASSES`, and `_UNSUPPORTED_MODEL_CLASSES`. Dispatch logic in `run_shap_analysis` routes each model to the appropriate SHAP helper based on its class name. Unsupported models (e.g., MinutesModel) are skipped with a status message.

**CLI and Registry Integration:**
A new `--model` CLI flag allows users to force analysis on a specific model class, bypassing production status checks in the registry. This ensures flexibility in testing and debugging SHAP coverage across different model variants.

**Edge Cases and Trade-Offs:**
The aggregation method assumes linearity in SHAP values, which holds for weighted averages but does not account for meta-learner coefficients in stacking ensembles. This approximation matches the ensemble's prediction logic but omits nuanced meta-model effects. Additionally, subsampling may reduce SHAP fidelity, especially for rare features or highly variable predictions.

## Key Properties

- **LinearExplainer Scaling Fidelity:** Ensures SHAP values for Ridge models are computed on scaled features, matching inference logic.
- **Weighted SHAP Aggregation:** Aggregates base model SHAP values using performance-based weights and projects onto unified feature axis.
- **Subsampling for Performance:** Limits SHAP computation to 300 samples for ensembles to control runtime and resource usage.
- **Dispatch Architecture:** Model classes are routed to specific SHAP computation branches based on taxonomy.

## Limitations

The ensemble SHAP aggregation treats the ensemble as a weighted average of base predictions, ignoring meta-learner coefficients (e.g., Ridge stacking weights). This means the SHAP values do not fully capture meta-model effects. Subsampling may miss important feature interactions. Unsupported models are skipped entirely, reducing coverage. The approach assumes feature alignment across base models, which may not hold in highly heterogeneous ensembles.

## Example

```python
# Ridge SHAP example
X_scaled = scaler.transform(X)
explainer = shap.LinearExplainer(ridge_model, X_scaled[:100])
shap_values = explainer.shap_values(X_scaled)

# Ensemble SHAP aggregation
ensemble_shap = np.zeros((n_samples, n_features))
for i, base_model in enumerate(base_models):
    base_shap = compute_shap(base_model, X)
    base_shap_df = pd.DataFrame(base_shap, columns=base_model.feature_names)
    aligned_shap = base_shap_df.reindex(columns=ensemble_feature_axis, fill_value=0.0)
    ensemble_shap += performance_weights[i] * aligned_shap.values
ensemble_shap /= n_folds
```

## Visual

No diagrams or charts included in the source; all technical details are described in text.

## Relationship to Other Concepts

- **[[LightGBM Feature Importance and SHAP Values]]** — Both use SHAP for model explainability; this concept extends coverage to Ridge and Ensemble models.
- **[[SHAP Analysis Bug Resolution In NBA ML Engine]]** — Sprint 59 builds upon prior bug resolution to expand SHAP coverage.

## Practical Applications

This approach enables robust feature attribution for Ridge and ensemble models in production ML pipelines, supporting model debugging, regulatory compliance, and user-facing interpretability. It is particularly valuable for sports analytics, where model transparency and rapid iteration are critical.

## Sources

- [[Copilot Session Checkpoint: Sprint 59 SHAP Coverage Implementation]] — primary source for this concept
