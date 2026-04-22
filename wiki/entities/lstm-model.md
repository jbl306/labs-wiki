---
title: "LSTM Model"
type: entity
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "7947d08e9a063fe0b24b8984da65f96b90179927fffc01c1f05927569f503763"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-11-evaluation-and-report-5b560f0f.md
quality_score: 61
concepts:
  - lstm-model
related:
  - "[[Copilot Session Checkpoint: Sprint 11 Evaluation and Report]]"
  - "[[NBA ML Engine]]"
  - "[[Holdout Evaluator CLI Command]]"
tier: hot
tags: [LSTM, neural networks, time series]
---

# LSTM Model

## Overview

The LSTM (Long Short-Term Memory) model is a recurrent neural network architecture included optionally in the NBA ML Engine. It is gated via a configuration flag `USE_LSTM` which defaults to false in Sprint 11, reflecting its disabled status in production. LSTM model files exist on disk but are not included in the active model classes unless explicitly enabled.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Model |
| Created | Unknown |
| Creator | Unknown |
| URL | N/A |
| Status | Inactive by default |

## Relevance

Represents a potential advanced modeling approach for temporal sequence data in NBA stat prediction, gated off during Sprint 11 to focus on other models and evaluation infrastructure.

## Associated Concepts

No associated concepts documented.

## Related Entities

- **[[NBA ML Engine]]** — Optional model within the engine
- **[[Holdout Evaluator CLI Command]]** — co-mentioned in source (Tool)

## Sources

- [[Copilot Session Checkpoint: Sprint 11 Evaluation and Report]] — where this entity was mentioned
