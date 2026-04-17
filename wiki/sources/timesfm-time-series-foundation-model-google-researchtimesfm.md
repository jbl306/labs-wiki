---
title: "TimesFM: Time Series Foundation Model (google-research/timesfm)"
type: source
created: 2026-04-13
last_verified: 2026-04-13
source_hash: "7db9778a42e98d53c01f3f061b1882f3b443288dbd137c0bac910129717f1c39"
sources:
  - raw/2026-04-13-httpsgithubcomgoogle-researchtimesfm.md
quality_score: 100
concepts:
  - time-series-foundation-model-architecture
  - agent-skill-integration-for-time-series-forecasting
  - continuous-quantile-forecasting-in-time-series-models
related:
  - "[[Time Series Foundation Model Architecture]]"
  - "[[Agent Skill Integration for Time-Series Forecasting]]"
  - "[[Continuous Quantile Forecasting in Time-Series Models]]"
  - "[[TimesFM]]"
  - "[[Google Research]]"
tier: hot
tags: [time-series, quantile-prediction, deep-learning, agent-skills, forecasting, transformer]
---

# TimesFM: Time Series Foundation Model (google-research/timesfm)

## Summary

TimesFM is a pretrained foundation model for time-series forecasting developed by Google Research. The repository provides the latest model version (2.5), installation instructions, agent skill integration, and code examples for inference. It supports both PyTorch and Flax backends, and introduces advanced forecasting features such as quantile prediction and long context handling.

## Key Points

- TimesFM is a decoder-only foundation model for time-series forecasting, with open-source code and checkpoints.
- Version 2.5 reduces parameter count, increases context length, and adds continuous quantile forecasting.
- Agent Skill integration allows TimesFM to be used in agentic workflows via the Agent Skills standard.

## Concepts Extracted

- **[[Time Series Foundation Model Architecture]]** — The Time Series Foundation Model (TimesFM) is a decoder-only neural architecture designed for flexible, high-performance time-series forecasting. It leverages transformer-based layers, normalization strategies, and specialized forecasting heads to address diverse forecasting tasks, including point and quantile prediction.
- **[[Agent Skill Integration for Time-Series Forecasting]]** — TimesFM provides a first-party Agent Skill, enabling its forecasting capabilities to be integrated into agentic workflows via the Agent Skills standard. This allows automated agents to discover and use TimesFM for time-series tasks without manual configuration.
- **[[Continuous Quantile Forecasting in Time-Series Models]]** — TimesFM introduces an optional continuous quantile forecasting head, enabling probabilistic predictions across multiple quantiles for future time points. This feature is critical for risk assessment, uncertainty quantification, and robust planning in time-series applications.

## Entities Mentioned

- **[[TimesFM]]** — TimesFM is a pretrained foundation model for time-series forecasting, developed by Google Research. It is designed for flexible, high-performance forecasting tasks, supporting both point and quantile predictions, and is available as open-source with checkpoints and agent skill integration.
- **[[Google Research]]** — Google Research is the research division of Google responsible for developing advanced AI models and technologies, including TimesFM. It drives innovation in machine learning, deep learning, and agentic systems.

## Notable Quotes

> "TimesFM (Time Series Foundation Model) is a pretrained time-series foundation model developed by Google Research for time-series forecasting." — README.md
> "Comparing to TimesFM 2.0, this new 2.5 model: uses 200M parameters, down from 500M; supports up to 16k context length, up from 2048; supports continuous quantile forecast up to 1k horizon via an optional 30M quantile head." — README.md

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-13-httpsgithubcomgoogle-researchtimesfm.md` |
| Type | repo |
| Author | Unknown |
| Date | Unknown |
| URL | https://github.com/google-research/timesfm |
