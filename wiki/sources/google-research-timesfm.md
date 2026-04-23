---
title: google-research/timesfm
type: source
created: '2026-04-21'
last_verified: '2026-04-22'
source_hash: fd7cfe463512c7b0734b9ec2e0b54e50c1919080501f414032e485e14bbf3d22
sources:
- raw/2026-04-13-httpsgithubcomgoogle-researchtimesfm.md
source_url: https://github.com/google-research/timesfm
tags:
- github
- python
tier: warm
knowledge_state: ingested
ingest_method: manual-deepen-github-2026-04-22
quality_score: 65
concepts:
- timesfm-model-architecture
- continuous-quantile-forecasting-in-time-series-models
- forecastconfig-forecasting-configuration-abstraction
- agent-skill-integration-for-time-series-forecasting
- patched-decoder-forecasting
---

# google-research/timesfm

## What it is

TimesFM (Time Series Foundation Model) is a pretrained, decoder-only foundation model for univariate time-series forecasting from Google Research, published at ICML 2024. It provides zero-shot forecasts without per-dataset training and ships PyTorch and Flax inference plus an optional 30M-parameter quantile head for continuous quantile forecasts. The current model is TimesFM 2.5 — 200M parameters, 16k context, no frequency indicator.

## Why it matters

Direct candidate for nba-ml-engine prediction features that are currently per-stat ARIMA/LSTM ensembles. A pretrained foundation model gives a strong zero-shot baseline to compare custom models against, and the LoRA fine-tuning example via HuggingFace Transformers + PEFT is exactly what you'd need for league-specific calibration. Also relevant for any forecasting work in the homelab monitoring stack (Prometheus → Grafana) where short-horizon prediction would help with alert tuning.

## Architecture / Technical model

- **Decoder-only foundation model** — Treats time series forecasting like next-token prediction; input patches are processed through a standard transformer decoder stack to produce output patches. Model pretrained on a large corpus of real time series across multiple domains (finance, weather, web traffic, etc.).
> See [[timesfm-model-architecture]] and [[patched-decoder-forecasting]] for the technical design.

- **Patched-decoder forecasting** — Input time series is divided into fixed-length patches (patch_len), each encoded as a single token. The decoder processes these tokens autoregressively and outputs a sequence of predicted patches, which are then reshaped into the final forecast horizon.
> See [[patched-decoder-forecasting]] for the patch-based encoding approach.

- **TimesFM 2.5 architecture** — 200M parameters, 16k max context length, no frequency indicator (removed in v2.5). Supports PyTorch and Flax (JAX) runtimes. Input patches default to length 32; output patches depend on `max_horizon` config.

- **Continuous quantile forecasting** — Optional 30M-parameter quantile head produces mean + 10th–90th quantiles (in 10% increments) up to 1k horizon. `use_continuous_quantile_head=True` enables this; output shape becomes `(batch, horizon, 10)` for quantile forecasts.
> See [[continuous-quantile-forecasting-in-time-series-models]] for the quantile head design.

- **`ForecastConfig`** — Per-call configuration object specifying `max_context`, `max_horizon`, `normalize_inputs`, `force_flip_invariance`, `infer_is_positive`, `fix_quantile_crossing`. Compiled once before inference; can be reused for multiple forecast calls.
> See [[forecastconfig-forecasting-configuration-abstraction]] for config flags and their effects.

- **XReg covariate support** — Per-input ridge regression regressors added back in v2.5 (removed in v2.0). Covariates are passed as an optional `covariates` array; model performs per-input ridge regression to align covariate influence.

- **Internal instance normalization (RevIN)** — TimesFM 2.5 applies its own reversible instance normalization internally. **Do not** externally normalize your inputs — feed raw values and let the model handle it.

- **Zero-shot inference** — No per-dataset training required; pretrained checkpoints work out-of-the-box on new series. For domain-specific calibration, use the LoRA fine-tuning pipeline under `timesfm-forecasting/examples/finetuning/`.

- **Agent skill integration** — Ships a first-party `timesfm-forecasting` Agent Skill (`SKILL.md` / `AGENTS.md`) for tool-using agents. The skill defines tool signatures for `forecast`, `forecast_with_covariates`, and `evaluate_model`.
> See [[agent-skill-integration-for-time-series-forecasting]] for the skill interface.

- **Multi-backend support** — PyTorch (GPU/CPU), Flax (GPU/TPU/CPU), and XReg extras. Flax backend is faster for inference on CPU and TPU; PyTorch backend supports PEFT (LoRA/DoRA) fine-tuning via HuggingFace Transformers.

## How it works

1. **Install and select backend**: Clone the repo, install `[torch]`, `[flax]`, or `[xreg]` extras, and optionally install backend-specific accelerators (e.g., `pip install torch --index-url ...` for CUDA).
2. **Load pretrained checkpoint**: Use `TimesFM_2p5_200M_torch.from_pretrained("google/timesfm-2.5-200m-pytorch")` or the Flax equivalent. Checkpoints hosted on HuggingFace.
3. **Compile ForecastConfig**: Call `model.compile(ForecastConfig(...))` once to set context/horizon limits and inference flags (normalization, flip invariance, quantile head, etc.).
4. **Forecast**: Pass a list of 1-D numpy arrays to `model.forecast(horizon=H, inputs=[...])`. Returns `(point_forecast, quantile_forecast)` where:
   - `point_forecast` shape: `(batch, horizon)`
   - `quantile_forecast` shape: `(batch, horizon, 10)` if quantile head is enabled (mean + 9 quantiles)
5. **Optional: covariates**: Use `model.forecast_with_covariates(horizon=H, inputs=[...], covariates=[...])` to include exogenous regressors. Covariates must align with the input series length + horizon.
6. **Optional: fine-tuning**: For domain-specific adaptation, use the LoRA/DoRA pipeline under `timesfm-forecasting/examples/finetuning/`. This requires the PyTorch backend, HuggingFace Transformers, and PEFT. Training uses random window sampling (Chronos-2 style) and supports multi-GPU via `accelerate`.
7. **Benchmarking**: Extended benchmarks on Monash/ETT datasets are provided in `v1/experiments/extended_benchmarks/` and `v1/experiments/long_horizon_benchmarks/`. TimesFM 1.0 (200M) achieved best MASE/SMAPE across 27 datasets, 600× faster than StatisticalEnsemble baseline.

## API / interface surface

### Core Classes (PyTorch)

| Class | Description |
|-------|-------------|
| `TimesFM_2p5_200M_torch` | PyTorch model wrapper; load with `.from_pretrained(...)` |
| `ForecastConfig` | Configuration object for inference (context, horizon, normalization flags) |

### Core Classes (Flax)

| Class | Description |
|-------|-------------|
| `TimesFM_2p5_200M_flax` | Flax (JAX) model wrapper; load with `.from_pretrained(...)` |
| `ForecastConfig` | Same config object as PyTorch backend |

### Methods

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `compile(config)` | `config: ForecastConfig` | None | Compile model with context/horizon limits and flags |
| `forecast(horizon, inputs)` | `horizon: int`, `inputs: List[np.ndarray]` | `(point, quantile)` | Point + quantile forecasts |
| `forecast_with_covariates(horizon, inputs, covariates)` | `horizon: int`, `inputs: List[np.ndarray]`, `covariates: List[np.ndarray]` | `(point, quantile)` | Forecast with exogenous regressors |

### ForecastConfig Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `max_context` | int | 1024 | Max input series length |
| `max_horizon` | int | 256 | Max forecast horizon |
| `normalize_inputs` | bool | True | Apply internal RevIN normalization |
| `use_continuous_quantile_head` | bool | False | Enable 30M quantile head for uncertainty |
| `force_flip_invariance` | bool | False | Enforce forecast symmetry (useful for series with no known direction) |
| `infer_is_positive` | bool | False | Constrain forecasts to non-negative values |
| `fix_quantile_crossing` | bool | False | Post-process quantiles to prevent crossing |

### CLI (LoRA Fine-Tuning)

```bash
python timesfm-forecasting/examples/finetuning/finetune_lora.py \
    --model_id google/timesfm-2.5-200m-transformers \
    --context_len 64 \
    --horizon_len 13 \
    --epochs 10 \
    --batch_size 32 \
    --lr 1e-4 \
    --lora_r 4 \
    --lora_alpha 8 \
    --output_dir my-adapter
```

## Setup

```bash
git clone https://github.com/google-research/timesfm.git
cd timesfm
uv venv && source .venv/bin/activate
uv pip install -e .[torch]   # or .[flax] / .[xreg]
```

```python
import timesfm, numpy as np, torch
torch.set_float32_matmul_precision("high")
model = timesfm.TimesFM_2p5_200M_torch.from_pretrained("google/timesfm-2.5-200m-pytorch")
model.compile(timesfm.ForecastConfig(
    max_context=1024, max_horizon=256,
    normalize_inputs=True, use_continuous_quantile_head=True,
    force_flip_invariance=True, infer_is_positive=True,
    fix_quantile_crossing=True,
))
point, quantile = model.forecast(horizon=12, inputs=[np.linspace(0,1,100)])
```

## Integration notes

Plug-in candidate for nba-ml-engine alongside the existing per-stat models — useful as a zero-shot prior or a baseline in `walk-forward-stability-analysis-backtesting-nba-ml-engine`. The `[flax]` install path gives the fastest CPU/TPU inference; PyTorch path is fine on the homelab Beelink. The first-party Agent Skill could be wired into the `nba-sprint` custom agent.

## Caveats / Gotchas

- **Not an officially supported Google product** — The README is explicit about this; use at your own risk for production forecasting.
- **Versions 1.0 and 2.0 archived** — Older checkpoints live in `v1/`; pin `timesfm==1.3.0` to load them. Current checkpoints (2.5) are incompatible with the v1 API.
- **Frequency indicator removed in v2.5** — Code expecting a `frequency` parameter must be migrated. The model now infers temporal patterns from the raw series.
- **Do not normalize inputs externally** — TimesFM 2.5 applies internal RevIN normalization. Feeding pre-normalized data will degrade performance.
- **TimesFM 2.5 PyTorch checkpoint format issue** — The `google/timesfm-2.5-200m-pytorch` checkpoint downloads as `model.safetensors`, but the loader expects `torch_model.ckpt`. This causes a `FileNotFoundError`. Workaround: use TimesFM 1.0 PyTorch or Flax backend until resolved.
- **Random window sampling in fine-tuning** — The LoRA pipeline samples random `(context, horizon)` windows from each series, not fixed windows. This is more data-efficient but means each epoch sees different slices of the same series.
- **LoRA rank = 4 is ~0.6% trainable params** — With `r=4`, LoRA adds only ~1.4M trainable params out of ~232M total. This is enough for domain adaptation but may not capture highly dataset-specific patterns.
- **Quantile head not calibrated post-pretraining** — The 30M quantile head is included in the pretrained model but was not calibrated on a hold-out set. For production use, consider calibrating or conformalizing on your validation data.
- **Benchmark results use the median quantile head** — MASE/SMAPE scores reported in the extended benchmarks use the 0.5 quantile (median) as the point forecast, not the mean.
- **Long-horizon benchmarks use stride=horizon** — ETT dataset benchmarks use disjoint test windows (stride = horizon) rather than rolling validation (stride = 1) to keep baseline runtime tractable.
- **Apache-2.0 license** — Per Google Research convention; verify in repo before redistribution.

## Related concepts

- [[timesfm-model-architecture]]
- [[patched-decoder-forecasting]]
- [[continuous-quantile-forecasting-in-time-series-models]]
- [[forecastconfig-forecasting-configuration-abstraction]]
- [[agent-skill-integration-for-time-series-forecasting]]

## Source

- Raw dump: `raw/2026-04-13-httpsgithubcomgoogle-researchtimesfm.md`
- Upstream: https://github.com/google-research/timesfm
