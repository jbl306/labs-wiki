---
title: "Agent Skill Integration for Time-Series Forecasting"
type: concept
created: 2026-04-13
last_verified: 2026-04-13
source_hash: "7db9778a42e98d53c01f3f061b1882f3b443288dbd137c0bac910129717f1c39"
sources:
  - raw/2026-04-13-httpsgithubcomgoogle-researchtimesfm.md
quality_score: 76
concepts:
  - agent-skill-integration-for-time-series-forecasting
related:
  - "[[Agent-Ergonomic Tool Design Principles]]"
  - "[[TimesFM: Time Series Foundation Model (google-research/timesfm)]]"
tier: hot
tags: [agent-skills, automation, integration, time-series, forecasting]
---

# Agent Skill Integration for Time-Series Forecasting

## Overview

TimesFM provides a first-party Agent Skill, enabling its forecasting capabilities to be integrated into agentic workflows via the Agent Skills standard. This allows automated agents to discover and use TimesFM for time-series tasks without manual configuration.

## How It Works

The TimesFM repository includes a dedicated skill directory (`timesfm-forecasting/SKILL.md`) that defines the interface and requirements for agent integration. To install the skill, users copy the directory into their agent's skills folder, which can be global (e.g., `~/.cursor/skills/`, `~/.claude/skills/`) or project-level. Agents that support the open Agent Skills standard automatically discover and load the TimesFM skill, making its forecasting functions available as part of their toolset.

This integration is designed for compatibility with popular agentic platforms such as Cursor, Claude Code, OpenCode, and Codex. The skill exposes TimesFM's inference API, allowing agents to perform point and quantile forecasts, configure model parameters, and handle input normalization and invariance flags. Developers working directly with TimesFM can access the source code in `src/timesfm/` and run tests using `pytest`.

The agent skill mechanism abstracts away backend details (PyTorch, Flax, XReg) and hardware dependencies, enabling agents to leverage TimesFM's forecasting power regardless of their underlying infrastructure. This modular approach facilitates automated forecasting in pipelines, dashboards, and decision-support systems.

By adhering to the Agent Skills standard, TimesFM ensures interoperability and ease of adoption in multi-agent environments. Agents can orchestrate forecasting tasks, combine TimesFM outputs with other skills, and automate complex workflows involving time-series analysis.

## Key Properties

- **Agent Skills Standard Compatibility:** TimesFM skill is discoverable and usable by any agent supporting the Agent Skills standard.
- **Modular Installation:** Skill directory can be installed globally or per project, enabling flexible integration.
- **Backend-Agnostic Operation:** Agents can use TimesFM regardless of backend (PyTorch, Flax, XReg) or hardware platform.

## Limitations

Agent skill integration requires agents to support the Agent Skills standard. Some advanced features (e.g., covariate support, custom flags) may need manual configuration or version-specific handling. Skill updates must be managed to ensure compatibility with evolving agent frameworks.

## Example

```bash
cp -r timesfm-forecasting/ ~/.cursor/skills/
cp -r timesfm-forecasting/ ~/.claude/skills/
# Or project-level
cp -r timesfm-forecasting/ .cursor/skills/
```
Any agent supporting Agent Skills standard will discover TimesFM automatically.

## Relationship to Other Concepts

- **[[Agent-Ergonomic Tool Design Principles]]** — TimesFM skill follows ergonomic principles for agent integration.

## Practical Applications

Automated agents in finance, operations, and research can use TimesFM for forecasting tasks, integrating its predictions into larger decision-making workflows. This enables scalable, automated time-series analysis in multi-agent systems.

## Sources

- [[TimesFM: Time Series Foundation Model (google-research/timesfm)]] — primary source for this concept
