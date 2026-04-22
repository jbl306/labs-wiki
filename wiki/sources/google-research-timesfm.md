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
ingest_method: manual-reprocess-github-2026-04-22
quality_score: 80
concepts:
- timesfm-model-architecture
- continuous-quantile-forecasting-in-time-series-models
- forecastconfig-forecasting-configuration-abstraction
- agent-skill-integration-for-time-series-forecasting
---

# google-research/timesfm

## What it is

TimesFM (Time Series Foundation Model) is a pretrained, decoder-only foundation model for univariate time-series forecasting from Google Research, published at ICML 2024. It provides zero-shot forecasts without per-dataset training and ships PyTorch and Flax inference plus an optional 30M-parameter quantile head for continuous quantile forecasts. The current model is TimesFM 2.5 — 200M parameters, 16k context, no frequency indicator.

## Why it matters

Direct candidate for nba-ml-engine prediction features that are currently per-stat ARIMA/LSTM ensembles. A pretrained foundation model gives a strong zero-shot baseline to compare custom models against, and the LoRA fine-tuning example via HuggingFace Transformers + PEFT is exactly what you'd need for league-specific calibration. Also relevant for any forecasting work in the homelab monitoring stack (Prometheus → Grafana) where short-horizon prediction would help with alert tuning.

## Key concepts

- **Decoder-only forecasting transformer** — Treats time series like a language-modeling problem; pretrained on a large corpus of real series. See [[timesfm-model-architecture]].
- **Continuous quantile forecasting** — Optional 30M quantile head returns mean + 10th–90th quantiles up to a 1k horizon. See [[continuous-quantile-forecasting-in-time-series-models]].
- **`ForecastConfig`** — Per-call configuration: `max_context`, `max_horizon`, `normalize_inputs`, `force_flip_invariance`, `infer_is_positive`, `fix_quantile_crossing`. See [[forecastconfig-forecasting-configuration-abstraction]].
- **XReg covariates** — Per-input ridge regression covariate support added back in v2.5.
- **PEFT / LoRA fine-tuning** — Multi-GPU LoRA / DoRA adapter pipeline for TimesFM 2.5 via HuggingFace Transformers + PEFT.
- **Agent skill** — Ships a first-party `timesfm-forecasting` Agent Skill (SKILL.md / AGENTS.md) for tool-using agents. See [[agent-skill-integration-for-time-series-forecasting]].
- **Multi-runtime** — PyTorch, Flax (faster inference), or `[xreg]` extras.

## How it works

- Load a pretrained checkpoint from the HuggingFace `google/timesfm-*` collection.
- Compile the model with a `ForecastConfig` (sets context/horizon and inference flags).
- Call `model.forecast(horizon, inputs)` with a list of 1-D arrays; returns a `(batch, horizon)` point forecast and optionally a `(batch, horizon, 10)` quantile forecast.
- For fine-tuning: clone the repo, install `[torch]` extras, run the LoRA pipeline under `timesfm-forecasting/examples/finetuning/`.
- Also exposed in Google products: BigQuery ML, Connected Sheets, Vertex Model Garden.

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

- Versions 1.0 and 2.0 are archived in `v1/`; pin `timesfm==1.3.0` to load older checkpoints.
- "This open version is not an officially supported Google product."
- TimesFM 2.5 dropped the `frequency` indicator; downstream code expecting it must be migrated.
- Apache-2.0 license per Google Research convention (verify in repo before redistribution).

## Repo metadata

| Field | Value |
|---|---|
| Stars | 18,302 |
| Primary language | Python |
| Topics | (none) |
| License | Apache-2.0 (per Google Research convention) |

## Source

- Raw dump: `raw/2026-04-13-httpsgithubcomgoogle-researchtimesfm.md`
- Upstream: https://github.com/google-research/timesfm
