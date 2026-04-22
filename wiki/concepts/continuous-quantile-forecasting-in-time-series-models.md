---
title: "Continuous Quantile Forecasting in Time-Series Models"
type: concept
created: 2026-04-13
last_verified: 2026-04-13
source_hash: "7db9778a42e98d53c01f3f061b1882f3b443288dbd137c0bac910129717f1c39"
sources:
  - raw/2026-04-13-httpsgithubcomgoogle-researchtimesfm.md
quality_score: 76
concepts:
  - continuous-quantile-forecasting-in-time-series-models
related:
  - "[[Time Series Foundation Model Architecture]]"
  - "[[TimesFM: Time Series Foundation Model (google-research/timesfm)]]"
tier: hot
tags: [quantile-forecasting, probabilistic-prediction, time-series, uncertainty]
---

# Continuous Quantile Forecasting in Time-Series Models

## Overview

TimesFM introduces an optional continuous quantile forecasting head, enabling probabilistic predictions across multiple quantiles for future time points. This feature is critical for risk assessment, uncertainty quantification, and robust planning in time-series applications.

## How It Works

The continuous quantile forecasting head in TimesFM is a specialized neural module with 30M parameters, designed to produce quantile predictions for each forecasted time step. Unlike point forecasts, which provide a single deterministic value, quantile forecasts output a range of values corresponding to different probability levels (e.g., 10th to 90th quantiles).

During inference, the quantile head operates alongside the main transformer architecture, processing the encoded sequence and generating quantile outputs for up to 1,000 future steps (horizon). The model can be configured to use the quantile head via the `use_continuous_quantile_head` flag in the `ForecastConfig`. Additional flags such as `fix_quantile_crossing` ensure that quantile outputs remain ordered (i.e., higher quantiles are always greater than lower quantiles), addressing a common issue in quantile regression models.

The quantile head is designed to avoid quantile collapsing, where predicted quantiles converge to similar values, reducing the informativeness of the forecast. By leveraging deep learning and transformer attention, TimesFM maintains separation between quantiles, providing meaningful uncertainty intervals for each forecasted value.

Quantile forecasts are returned as tensors with shape `(batch_size, horizon, num_quantiles)`, allowing users to interpret the mean, median, and various percentile predictions. This is especially useful in domains where understanding the distribution of possible outcomes is more important than a single prediction, such as finance, meteorology, and supply chain management.

The quantile head can be used in conjunction with other model features, including input normalization and invariance flags, to produce robust, interpretable probabilistic forecasts.

## Key Properties

- **30M Parameter Quantile Head:** Dedicated neural module for quantile prediction, supporting up to 1,000 horizon steps.
- **Quantile Crossing Fix:** Ensures predicted quantiles remain ordered, preventing logical inconsistencies.
- **Avoids Quantile Collapsing:** Maintains separation between quantile predictions for meaningful uncertainty intervals.

## Limitations

Quantile forecasting increases computational requirements and may require careful configuration to avoid overfitting. The feature is optional and may not be available in all model versions. Interpretation of quantile outputs requires domain knowledge.

## Example

```python
model.compile(
    timesfm.ForecastConfig(
        use_continuous_quantile_head=True,
        fix_quantile_crossing=True,
    )
)
point_forecast, quantile_forecast = model.forecast(horizon=12, inputs=[...])
# quantile_forecast.shape: (batch_size, horizon, num_quantiles)
```

## Relationship to Other Concepts

- **[[Time Series Foundation Model Architecture]]** — Quantile head is a component of TimesFM's architecture.

## Practical Applications

Quantile forecasting is used in risk management, scenario planning, and uncertainty quantification across finance, weather prediction, and logistics. It enables decision-makers to assess potential outcomes and plan for best/worst-case scenarios.

## Sources

- [[TimesFM: Time Series Foundation Model (google-research/timesfm)]] — primary source for this concept
