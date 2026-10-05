---
title: "WikiSkill: Compiling Agent Experience into Persistent Knowledge for Skill Evolution"
type: source
created: 2026-08-28
last_verified: 2026-08-28
source_hash: "609c3adec2ebe732fcc6bf8667864803bf777eb6ef36535bf6abd069390c5206"
sources:
  - raw/2026-08-28-260827454v1pdf.md
quality_score: 92
concepts:
  - wikiskill-framework
  - cross-model-transfer-of-evolved-agent-skills
related:
  - "[[WikiSkill Framework]]"
  - "[[Cross-Model Transfer of Evolved Agent Skills]]"
  - "[[Karpathy LLM Wiki Pattern]]"
tier: hot
tags:
  - wikiskill
  - agent-skills
  - skill-evolution
  - persistent-knowledge
  - agent-memory
---

# WikiSkill: Compiling Agent Experience into Persistent Knowledge for Skill Evolution

## Summary

This paper introduces WikiSkill, a framework that co-evolves reusable agent skills with a persistent knowledge base compiled from execution experience. Its three-layer workspace separates immutable raw traces, a compounding Wiki Layer, and executable Skills, while an orchestrated loop consolidates patterns, proposes skill updates, and gates them with validation performance.

Across five benchmarks and five models, WikiSkill generally outperforms competing skill-evolution methods and no-skill baselines. The study also reports that persistent wiki knowledge is critical to continued skill refinement, that stronger models often benefit more from evolved skills, and that skills can transfer across model families—although model-specific workarounds can cause negative transfer.

## Key Points

- The Raw Layer stores immutable, step-by-step execution traces.
- The Wiki Layer preserves patterns, recurring errors, rejected proposals, evolution history, and skill-impact records across iterations.
- The Skills Layer contains executable procedural instructions in `SKILL.md` and purpose mappings in `PURPOSE.md`.
- The Inference Agent, Wiki Maintainer, Skill Proposer, and Gating and Rollback mechanism form the evolutionary loop.
- WikiSkill reaches the highest five-benchmark average for each evaluated model in the main comparison table.
- Persistent wiki access improves the Gemini-3.5-Flash ablation average from 48.7% to 63.7% when the Inference Agent lacks wiki access.
- Transferred skills can outperform self-evolved skills, but low-level workarounds and fragmented procedures can produce negative transfer.

## Concepts Extracted

- **[[WikiSkill Framework]]** — A three-layer architecture and iterative orchestration loop for compiling agent experience into persistent knowledge that guides skill evolution.
- **[[Cross-Model Transfer of Evolved Agent Skills]]** — The transfer of evolved procedural skills between source and target models, including both positive transfer and model-specific negative transfer.

## Entities Mentioned

- **[[WikiSkill]]** — Research framework introduced by Liyan Tang, Cyrus Rashtchian, Chun-Sung Ferng, Andrew Tomkins, Da-Cheng Juan, and Tu Vu.

## Notable Quotes

> "The wiki is not reset between iterations, but rather accumulates and compiles knowledge continuously throughout the evolution process." — WikiSkill paper

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-08-28-260827454v1pdf.md` |
| Type | paper |
| Author | Liyan Tang, Cyrus Rashtchian, Chun-Sung Ferng, Andrew Tomkins, Da-Cheng Juan, Tu Vu |
| Date | Unknown |
| URL | https://arxiv.org/pdf/2608.27454 |