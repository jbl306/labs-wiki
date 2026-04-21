---
title: "ForecastConfig: Forecasting Configuration Abstraction"
type: concept
created: 2026-04-21
last_verified: 2026-04-21
source_hash: "953a023ae381d64a6a416b274883aa7f90d18bd9eabf91f5d6fa27573c44c032"
sources:
  - raw/2026-04-13-httpsgithubcomgoogle-researchtimesfm.md
quality_score: 100
concepts:
  - forecastconfig-forecasting-configuration-abstraction
related:
  - "[[Continuous Quantile Forecasting in Time-Series Models]]"
  - "[[TimesFM: Time Series Foundation Model (google-research/timesfm)]]"
tier: hot
tags: [configuration, forecasting, dataclass, model-parameters]
---

# ForecastConfig: Forecasting Configuration Abstraction

## Overview

ForecastConfig is a configuration dataclass that encapsulates all major options for TimesFM forecasting, including context length, horizon, normalization, quantile head usage, invariance, and output constraints.

## How It Works

ForecastConfig is defined as a frozen dataclass, ensuring immutability and clarity in model configuration. It provides a unified interface for specifying inference-time options:
- **max_context:** Maximum allowed input sequence length; shorter inputs are zero-padded, longer ones truncated.
- **max_horizon:** Maximum forecast horizon (number of future steps predicted).
- **normalize_inputs:** Whether to normalize input data, useful for handling extreme values and improving numerical stability.
- **window_size:** For decomposed forecasting (currently a TODO/placeholder).
- **per_core_batch_size:** Batch size per device for parallel inference.
- **use_continuous_quantile_head:** Enables the quantile head for uncertainty-aware forecasting.
- **force_flip_invariance:** Ensures the model's outputs respect flip invariance (output scales and shifts with input).
- **infer_is_positive:** Guarantees nonnegative outputs if inputs are nonnegative.
- **fix_quantile_crossing:** Enforces monotonicity in quantile outputs to prevent quantile crossing.
- **return_backcast:** Optionally returns the model's backcast (reconstruction of the input sequence).

This abstraction allows users to easily configure and experiment with different forecasting settings, both programmatically and via agent skill interfaces. The configuration is passed to the model's `compile` method, which sets up the inference pipeline accordingly.

## Key Properties

- **Immutability:** Frozen dataclass ensures configuration cannot be changed after creation.
- **Comprehensive Options:** Covers all major inference-time options for TimesFM.
- **Framework Agnostic:** Used by both PyTorch and Flax/JAX implementations.

## Limitations

Some options (e.g., window_size) are not yet implemented. Incorrect configuration (e.g., mismatched context/horizon with model weights) may lead to runtime errors. Users must understand the implications of each flag for optimal results.

## Example

```python
config = timesfm.ForecastConfig(
    max_context=1024,
    max_horizon=256,
    normalize_inputs=True,
    use_continuous_quantile_head=True,
    force_flip_invariance=True,
    infer_is_positive=True,
    fix_quantile_crossing=True,
)
model.compile(config)
```

## Visual

No diagrams; the code and docstring in configs.py enumerate all configuration options.

## Relationship to Other Concepts

- **[[Continuous Quantile Forecasting in Time-Series Models]]** — ForecastConfig enables and configures quantile forecasting in TimesFM.

## Practical Applications

Allows users to tailor TimesFM's forecasting behavior to specific datasets, tasks, and deployment environments, supporting both research experimentation and production deployment.

## Sources

- [[TimesFM: Time Series Foundation Model (google-research/timesfm)]] — primary source for this concept
