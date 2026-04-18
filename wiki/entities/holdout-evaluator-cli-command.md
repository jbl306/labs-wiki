---
title: "Holdout Evaluator CLI Command"
type: entity
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "7947d08e9a063fe0b24b8984da65f96b90179927fffc01c1f05927569f503763"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-11-evaluation-and-report-5b560f0f.md
quality_score: 100
concepts:
  - holdout-evaluator-cli-command
related:
  - "[[Holdout Evaluator Module]]"
  - "[[Copilot Session Checkpoint: Sprint 11 Evaluation and Report]]"
  - "[[NBA ML Engine]]"
  - "[[LSTM Model]]"
tier: hot
tags: [CLI, evaluation, automation]
---

# Holdout Evaluator CLI Command

## Overview

A command-line interface (CLI) command added to the NBA ML Engine's main script to facilitate running the holdout evaluator module. The command `python main.py evaluate` supports options to specify the statistic to evaluate, toggle calibration and feature importance analyses, restrict to production models, and save results as JSON files.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool |
| Created | Unknown |
| Creator | Unknown |
| URL | N/A |
| Status | Active |

## Relevance

Enables reproducible and flexible evaluation runs from the command line, supporting integration into CI/CD pipelines and automated reporting.

## Associated Concepts

- **[[Holdout Evaluator Module]]** — CLI interface to run evaluation

## Related Entities

- **[[NBA ML Engine]]** — Part of the engine's tooling
- **[[LSTM Model]]** — co-mentioned in source (Model)

## Sources

- [[Copilot Session Checkpoint: Sprint 11 Evaluation and Report]] — where this entity was mentioned
