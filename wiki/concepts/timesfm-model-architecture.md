---
title: "TimesFM Model Architecture"
type: concept
created: 2026-04-21
last_verified: 2026-04-21
source_hash: "953a023ae381d64a6a416b274883aa7f90d18bd9eabf91f5d6fa27573c44c032"
sources:
  - raw/2026-04-13-httpsgithubcomgoogle-researchtimesfm.md
quality_score: 67
concepts:
  - timesfm-model-architecture
related:
  - "[[Time Series Foundation Model Architecture]]"
  - "[[Continuous Quantile Forecasting in Time-Series Models]]"
  - "[[TimesFM: Time Series Foundation Model (google-research/timesfm)]]"
tier: hot
tags: [time-series, foundation-model, forecasting, transformer, quantile-forecasting]
---

# TimesFM Model Architecture

## Overview

TimesFM is a decoder-only, pretrained foundation model for time-series forecasting, designed to handle long contexts and quantile prediction. It is engineered for scalability, flexibility, and integration with both enterprise and agentic environments.

## How It Works

TimesFM adopts a decoder-only transformer architecture, optimized for time-series forecasting tasks. The 2.5 version of the model reduces parameter count to 200M (from 500M in v2.0) while extending the supported context length to 16,384 (16k), enabling it to process much longer input sequences than prior versions. The model is capable of continuous quantile forecasting for up to 1,000 time steps into the future, using an optional 30M parameter quantile head. This quantile head allows the model to output not just point forecasts but also a range of quantiles (e.g., 10th to 90th percentiles), supporting robust uncertainty estimation.

The model is implemented in both PyTorch and Flax/JAX, with support for fast inference via Flax and flexible deployment on CPU, GPU, or TPU. Key architectural features include:
- **Context Handling:** Inputs shorter than `max_context` are zero-padded; longer inputs are truncated. This ensures consistent tensor shapes for batched inference.
- **Quantile Head:** When enabled, the model outputs a tensor of shape `(batch, horizon, quantiles)`, where quantiles include the mean and specified percentiles.
- **Normalization and Invariance:** The model can normalize inputs, enforce flip invariance (so that scaling and shifting the input series produces corresponding changes in the output), and guarantee nonnegativity of outputs when inputs are nonnegative.
- **Covariate Support (XReg):** TimesFM 2.5 reintroduces support for exogenous covariates, allowing the model to condition forecasts on additional variables.
- **Continuous Quantile Crossing Fix:** The model can enforce monotonicity in quantile outputs to prevent quantile crossing, a common issue in quantile regression.

The model is designed for plug-and-play use in both research and production settings. It is integrated with Google products (BigQuery ML, Google Sheets, Vertex Model Garden) and can be installed and fine-tuned using HuggingFace Transformers and PEFT (LoRA).

## Key Properties

- **Parameter Count:** 200 million parameters in TimesFM 2.5, reduced from 500M in v2.0.
- **Context Length:** Supports up to 16,384 (16k) time steps as input context.
- **Quantile Forecasting:** Supports continuous quantile forecasting up to 1,000 steps with an optional 30M parameter quantile head.
- **Covariate Support:** Supports exogenous covariates via XReg.
- **Frameworks:** Implements both PyTorch and Flax/JAX backends for broad hardware compatibility.

## Limitations

The open-source version is not an officially supported Google product. Some features (e.g., windowed decomposition) are marked as TODO or experimental. Quantile crossing fixes and invariance options may introduce additional computational overhead. The model may require substantial memory for very long contexts or large batch sizes.

## Example

```python
import torch
import numpy as np
import timesfm

torch.set_float32_matmul_precision("high")

model = timesfm.TimesFM_2p5_200M_torch.from_pretrained("google/timesfm-2.5-200m-pytorch")

model.compile(
    timesfm.ForecastConfig(
        max_context=1024,
        max_horizon=256,
        normalize_inputs=True,
        use_continuous_quantile_head=True,
        force_flip_invariance=True,
        infer_is_positive=True,
        fix_quantile_crossing=True,
    )
)
point_forecast, quantile_forecast = model.forecast(
    horizon=12,
    inputs=[
        np.linspace(0, 1, 100),
        np.sin(np.linspace(0, 20, 67)),
    ],  # Two dummy inputs
)
point_forecast.shape  # (2, 12)
quantile_forecast.shape  # (2, 12, 10): mean, then 10th to 90th quantiles.
```

## Visual

No diagrams or charts are present in the source. The code example illustrates the API usage and expected output shapes.

## Relationship to Other Concepts

- **[[Time Series Foundation Model Architecture]]** — TimesFM is a concrete implementation and extension of this architectural concept.
- **[[Continuous Quantile Forecasting in Time-Series Models]]** — TimesFM 2.5 implements and extends continuous quantile forecasting.

## Practical Applications

TimesFM is used for forecasting in enterprise analytics (BigQuery ML), spreadsheet-based forecasting (Google Sheets), and as a dockerized endpoint for agentic workflows (Vertex Model Garden). It is suitable for demand forecasting, anomaly detection, financial time-series prediction, and any scenario requiring robust, scalable, and uncertainty-aware time-series forecasts.

## Sources

- [[TimesFM: Time Series Foundation Model (google-research/timesfm)]] — primary source for this concept
