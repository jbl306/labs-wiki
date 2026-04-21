---
title: "TimesFM: Time Series Foundation Model (google-research/timesfm)"
type: source
created: 2026-04-21
last_verified: 2026-04-21
source_hash: "953a023ae381d64a6a416b274883aa7f90d18bd9eabf91f5d6fa27573c44c032"
sources:
  - raw/2026-04-13-httpsgithubcomgoogle-researchtimesfm.md
quality_score: 100
concepts:
  - timesfm-model-architecture
  - agent-skill-integration-for-timesfm
  - forecastconfig-forecasting-configuration-abstraction
related:
  - "[[TimesFM Model Architecture]]"
  - "[[ForecastConfig: Forecasting Configuration Abstraction]]"
  - "[[TimesFM]]"
  - "[[Google Research]]"
tier: hot
knowledge_state: executed
tags: [agent-skill, open-source, foundation-model, time-series, forecasting, quantile-forecasting]
---

# TimesFM: Time Series Foundation Model (google-research/timesfm)

## Summary

TimesFM is a pretrained, open-source time-series foundation model developed by Google Research, designed for scalable and flexible time-series forecasting. The repository provides the latest TimesFM 2.5 model, supporting long contexts, quantile forecasting, and integration with popular ML frameworks and agentic skill systems. It includes code, installation instructions, fine-tuning examples, and agent skill integration for use in various environments.

## Key Points

- TimesFM 2.5 is a decoder-only, 200M parameter model supporting up to 16k context length and 1k horizon quantile forecasting.
- The model is integrated with Google products (BigQuery ML, Google Sheets, Vertex Model Garden) and supports agent skill standards for plug-and-play use.
- The repository includes examples for fine-tuning (LoRA/PEFT), covariate support (XReg), and agent skill installation, with community contributions and continual updates.

## Concepts Extracted

- **[[TimesFM Model Architecture]]** — TimesFM is a decoder-only, pretrained foundation model for time-series forecasting, designed to handle long contexts and quantile prediction. It is engineered for scalability, flexibility, and integration with both enterprise and agentic environments.
- **Agent Skill Integration for TimesFM** — TimesFM provides a first-party Agent Skill, enabling seamless integration with agentic frameworks that support the open Agent Skills standard. This allows TimesFM to be used as a forecasting skill in agent platforms such as Cursor, Claude Code, OpenCode, and Codex.
- **[[ForecastConfig: Forecasting Configuration Abstraction]]** — ForecastConfig is a configuration dataclass that encapsulates all major options for TimesFM forecasting, including context length, horizon, normalization, quantile head usage, invariance, and output constraints.

## Entities Mentioned

- **[[TimesFM]]** — TimesFM is a pretrained, open-source foundation model for time-series forecasting, developed by Google Research. It is designed for high scalability, long-context support, and robust uncertainty estimation via quantile forecasting. The model is available in both PyTorch and Flax/JAX implementations and is integrated with Google products and agentic skill systems.
- **[[Google Research]]** — Google Research is the research division of Google, responsible for developing and releasing TimesFM. The organization focuses on advancing the state of the art in AI, machine learning, and related fields, and frequently releases open-source models and tools.

## Notable Quotes

> "TimesFM (Time Series Foundation Model) is a pretrained time-series foundation model developed by Google Research for time-series forecasting." — README
> "Any agent that supports the open Agent Skills standard will discover it automatically." — AGENTS.md

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-13-httpsgithubcomgoogle-researchtimesfm.md` |
| Type | repo |
| Author | Google Research (Rajat Sen, Yichen Zhou, Abhimanyu Das, Petros Mol, Michael Chertushkin) |
| Date | Unknown |
| URL | https://github.com/google-research/timesfm |
