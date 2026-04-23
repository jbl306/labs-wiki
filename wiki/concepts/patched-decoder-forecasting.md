---
title: "Patched-Decoder Forecasting"
type: concept
created: '2026-04-22'
last_verified: '2026-04-22'
sources:
  - raw/2026-04-13-httpsgithubcomgoogle-researchtimesfm.md
quality_score: 75
concepts:
  - patched-decoder-forecasting
related:
  - "[[google-research/timesfm]]"
  - "[[TimesFM Model Architecture]]"
  - "[[Continuous Quantile Forecasting in Time-Series Models]]"
tier: warm
tags: [time-series, forecasting, transformer, decoder-only, foundation-model]
---

# Patched-Decoder Forecasting

## Overview

Patched-decoder forecasting is an architectural pattern for time-series foundation models where the input series is divided into fixed-length patches, each encoded as a single token, and processed through a decoder-only transformer. This approach is inspired by language modeling (where sentences are tokenized into words) and enables long-context forecasting by treating time series as sequences of patches rather than individual time steps. TimesFM 2.5 (Google Research) is a canonical implementation of this pattern.

## How It Works

In traditional sequence-to-sequence forecasting, each time step is a separate token, leading to very long sequences (e.g., 1024 time steps = 1024 tokens). Patched-decoder forecasting reduces this by treating consecutive time steps as a single patch:

1. **Input patching** — The input time series `x[0..N]` is divided into non-overlapping patches of length `patch_len` (default 32 in TimesFM 2.5). Each patch is encoded as a single embedding vector via a linear projection or convolutional layer.

2. **Patch tokenization** — The `N / patch_len` patch embeddings are treated as tokens and fed into a decoder-only transformer. This reduces the sequence length by a factor of `patch_len`, enabling longer context windows (TimesFM 2.5 supports 16k time steps → 512 patch tokens).

3. **Autoregressive decoding** — The decoder processes the patch sequence autoregressively (like a language model predicting next tokens) and outputs a sequence of predicted patches for the horizon.

4. **Output un-patching** — The predicted patch embeddings are decoded back into individual time steps via a linear projection or deconvolutional layer, producing the final forecast.

5. **Quantile head** — Optionally, a separate quantile head processes the patch embeddings to produce quantile forecasts (10th–90th percentiles) rather than just point forecasts.

**Key insight:** Patching trades off temporal resolution (individual time steps) for sequence length efficiency. By encoding 32 time steps as 1 patch, the model can process 32× more history in the same context window.

**Patch size trade-off:**
- **Small patches** (e.g., patch_len=8) → finer temporal resolution, shorter context
- **Large patches** (e.g., patch_len=64) → coarser resolution, longer context

TimesFM 2.5 uses patch_len=32 as a balance between resolution and context length.

**Relation to language modeling:** This pattern directly mirrors how large language models work:
- Language models: sentence → words → tokens → embeddings → decoder → predicted tokens
- Patched-decoder forecasting: time series → patches → patch tokens → embeddings → decoder → predicted patches

## Key Properties

- **Context length amplification** — Patching reduces the sequence length by `patch_len`, enabling models to process longer input series within the same token budget.
- **Decoder-only architecture** — Uses a standard transformer decoder stack (no encoder), enabling autoregressive generation and easier pretraining on large corpora.
- **Patch-level attention** — The model attends to patches, not individual time steps, so fine-grained temporal patterns within a patch are captured by the patch encoder (linear/conv layer), not the transformer.
- **Zero-shot transfer** — Because patches are domain-agnostic (any series can be patched), pretrained models can zero-shot forecast on new domains without retraining.

## Trade-offs

**Benefits:**
- Enables very long context windows (16k time steps in TimesFM 2.5)
- Reduces computational cost (512 patch tokens vs 16k time-step tokens)
- Allows pretraining on diverse series (patches are a universal abstraction)

**Drawbacks:**
- Loss of fine-grained temporal resolution (within-patch patterns are compressed)
- Patch boundaries can introduce artifacts if not carefully aligned
- Requires careful tuning of patch_len for the target domain (32 may not be optimal for all series)

## Example

**Input series** (100 time steps):
```
x = [1.2, 1.3, 1.5, 1.4, ..., 2.1, 2.0]  # 100 values
```

**Patching** (patch_len=32):
```
patches = [
    [1.2, 1.3, 1.5, 1.4, ...],  # first 32 steps → patch 0
    [...],                       # next 32 steps → patch 1
    [...],                       # final 36 steps → patch 2 (padded)
]
# 100 steps → 3 patches (or 4 with padding)
```

**Patch embeddings** → fed to decoder → produces predicted patches → un-patched back to time steps:
```
forecast = [2.2, 2.3, 2.4, ...]  # 12 steps
```

**Code example** (TimesFM 2.5):
```python
import timesfm, numpy as np

model = timesfm.TimesFM_2p5_200M_torch.from_pretrained("google/timesfm-2.5-200m-pytorch")
model.compile(timesfm.ForecastConfig(max_context=1024, max_horizon=256))

# Input: 100 time steps → internally patched to ~3 patches
point_forecast, _ = model.forecast(horizon=12, inputs=[np.linspace(0, 1, 100)])
# point_forecast.shape: (1, 12)
```

## Relationship to Other Concepts

- **[[TimesFM Model Architecture]]** — TimesFM 2.5 is the reference implementation of patched-decoder forecasting.
- **[[google-research/timesfm]]** — The open-source project that introduced this pattern.
- **[[Continuous Quantile Forecasting in Time-Series Models]]** — The quantile head operates on patch embeddings, not individual time steps.

## Practical Applications

Patched-decoder forecasting is useful for:
- **Long-context forecasting** — Scenarios requiring 1000+ time steps of input history (e.g., hourly data over months).
- **Multi-domain pretraining** — Patching enables training a single model on diverse time series (finance, weather, web traffic) without domain-specific feature engineering.
- **Zero-shot forecasting** — Pretrained patch-based models can forecast new series without fine-tuning, useful for ad-hoc analytics or cold-start scenarios.
- **Efficient inference** — Patching reduces the transformer's sequence length, speeding up inference on CPU/GPU/TPU.

Specific use cases:
- Demand forecasting (retail, supply chain) with long seasonal patterns
- Financial time series (high-frequency trading data compressed into patches)
- IoT sensor data (thousands of time steps from distributed sensors)
- Energy grid forecasting (hourly load data over years)

## Sources

- [[google-research/timesfm]] — introduces patched-decoder forecasting for TimesFM 2.5
