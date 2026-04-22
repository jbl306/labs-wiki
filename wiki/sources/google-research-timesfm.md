---
title: google-research/timesfm
type: source
created: '2026-04-21'
last_verified: '2026-04-21'
source_hash: fd7cfe463512c7b0734b9ec2e0b54e50c1919080501f414032e485e14bbf3d22
sources:
- raw/2026-04-13-httpsgithubcomgoogle-researchtimesfm.md
source_url: https://github.com/google-research/timesfm
tags:
- github
- python
tier: warm
knowledge_state: ingested
ingest_method: self-synthesis-no-llm
quality_score: 50
---

# google-research/timesfm

## Summary

TimesFM (Time Series Foundation Model) is a pretrained time-series foundation model developed by Google Research for time-series forecasting.

## Repository Info

- **Source URL**: https://github.com/google-research/timesfm
- **Stars**: 18302
- **Primary language**: Python

## README Excerpt

# TimesFM

TimesFM (Time Series Foundation Model) is a pretrained time-series foundation
model developed by Google Research for time-series forecasting.

*   Paper:
    [A decoder-only foundation model for time-series forecasting](https://arxiv.org/abs/2310.10688),
    ICML 2024.
*   All checkpoints:
    [TimesFM Hugging Face Collection](https://huggingface.co/collections/google/timesfm-release-66e4be5fdb56e960c1e482a6).
*   [Google Research blog](https://research.google/blog/a-decoder-only-foundation-model-for-time-series-forecasting/).
*   TimesFM in Google 1P Products:
    *   [BigQuery ML](https://cloud.google.com/bigquery/docs/timesfm-model): Enterprise level SQL queries for scalability and reliability.
    *   [Google Sheets](https://workspaceupdates.googleblog.com/2026/02/forecast-data-in-connected-sheets-BigQueryML-TimesFM.html): For your daily spreadsheet. 
    *   [Vertex Model Garden](https://pantheon.corp.google.com/vertex-ai/publishers/google/model-garden/timesfm): Dockerized endpoint for agentic calling.

This open version is not an officially supported Google product.

**Latest Model Version:** TimesFM 2.5

**Archived Model Versions:**

-   1.0 and 2.0: relevant code archived in the sub directory `v1`. You can `pip
    install timesfm==1.3.0` to install an older version of this package to load
    them.

## Activity Snapshot

### Recent Releases

### v1.2.6 (2024-12-31)

Changes:
----
1. Add support for TimesFM-2.0 models.
2. Set the median head as the default point forecaster.

PyPI Release:
----
v1.2.6: Support for TimesFM-2.0 models.
- Add hparam support for TimesFM-2.0 models.
- Some bug fixes in pytorch decoding.
- Right now we do not support cached decoding in both jax and pytorch.

Checkpoints:
----
The TimesFM-2.0 checkpoints are available on Hugging Face:
- https://huggingface.co/google/timesfm-2.0-500m-jax
- https://huggingface.co/google/timesfm-2.0-500m-pytorch

Full Changelog:
----
https://github.com/google-research/timesfm/commits/v1.2.6

### v1.2.1 (2024-10-18)

Changes:
----
- PyTorch support for TimesFM inference.

PyPI Release:
----

v1.2.1: Support separate dependencies for `pax` and `torch` versions of TimesFM:
  - `pip install timesfm[pax]` for the `pax` version and `jax` checkpoints.
  - `pip install timesfm[torch]` for the `torch` version and checkpoints.
  - See the updated [README](https://github.com/google-research/timesfm?tab=readme-ov-file#usage) for the usage.

Checkpoints:
----
The PyTorch checkpoint for the 200m model is available on Hugging Face:
- https://huggingface.co/google/timesfm-1.0-200m-pytorch

Full Changelog:
----
https://gi…
### Recent Commits

- 2026-04-15 d720daa Yichen Zhou: Update README.md
- 2026-04-15 eacf761 Yichen Zhou: Merge pull request #398 from darkpowerxo/feat/peft-finetuning-pipeline-2.5
- 2026-04-10 6ae67d4 darkpowerxo: revert: drop PR #393 (xreg batch behavior) and PR #390 (SKILL.md link) per maintainer feedback
- 2026-04-09 caddef1 darkpowerxo: refactor: replace custom PEFT pipeline with Transformers+PEFT example
- 2026-04-09 18d5eb2 darkpowerxo: fix: improve PEFT device consistency and XReg output slicing
- 2026-04-08 ad192b7 darkpowerxo: docs: update README — replace 'under construction' with completed status
- 2026-04-08 54f5405 darkpowerxo: docs: fix swapped xreg_mode descriptions and typo in error message
- 2026-04-08 13a8eb2 darkpowerxo: ci: upgrade GitHub Actions to v6
- 2026-04-08 30f28a1 darkpowerxo: fix: correct SKILL.md link in README
- 2026-04-08 1bb44d5 darkpowerxo: fix: respect batch_size in v1 data_loader when permute=False
- 2026-04-08 a63360a darkpowerxo: fix: per-input ridge regression to prevent data leakage in xreg
- 2026-04-08 c10494a darkpowerxo: test: add unit tests for configs, torch layers, utils, and base utils
- 2026-04-08 bc03b77 darkpowerxo: fix: correct 'complied' typo and replace print with logging
- 2026-04-08 b6ac2b3 darkpowerxo: docs: add README for the PEFT fine-tuning pipeline
- 2026-04-08 a67eeb2 darkpowerxo: feat: add CLI entry-point and launch script for PEFT fine-tuning
- 2026-04-08 eca7ca3 darkpowerxo: feat: add multi-GPU PEFT trainer for TimesFM 2.5
- 2026-04-08 9875d92 darkpowerxo: feat: add TimeSeriesDataset for PEFT fine-tuning
- 2026-04-08 7357458 darkpowerxo: feat: add LoRA/DoRA adapter layers for TimesFM 2.5 (PyTorch)
- 2026-04-08 aa2b17f darkpowerxo: chore: update .gitignore for egg-info, uv.lock, peft_checkpoints
- 2026-04-03 f085b90 Yichen Zhou: Update README.md
### Recently Merged PRs (top 10)

- #398 feat: PEFT fine-tuning pipeline (LoRA/DoRA, multi-GPU) for TimesFM 2.5 (merged 2026-04-15)
- #376 docs: fix swapped xreg_mode descriptions in forecast_with_covariates (merged 2026-03-19)
- #369 feat(skill): ship first-party timesfm-forecasting Agent Skill (agentskills.io) (merged 2026-03-19)
- #372 [HF] use the ModelHubMixin api (merged 2026-03-11)
- #341 [TimesFMv1] fix variance calculation (merged 2026-02-19)
- #360 Update pyproject.toml (merged 2026-01-27)

## Crawled Files

Source dump in `raw/2026-04-13-httpsgithubcomgoogle-researchtimesfm.md` includes:

- `.gitignore`
- `LICENSE`
- `pyproject.toml`
- `requirements.txt`
- `timesfm-forecasting/examples/finetuning/README.md`
- `timesfm-forecasting/examples/global-temperature/README.md`
- `v1/experiments/extended_benchmarks/README.md`
- `v1/experiments/long_horizon_benchmarks/README.md`
- `v1/LICENSE`
- `v1/peft/README.md`
- `v1/pyproject.toml`
- `v1/README.md`
- `timesfm-forecasting/examples/anomaly-detection/detect_anomalies.py`
- `timesfm-forecasting/examples/anomaly-detection/output/anomaly_detection.json`
