---
title: "WikiSkill"
type: entity
created: 2026-08-28
last_verified: 2026-08-28
source_hash: "609c3adec2ebe732fcc6bf8667864803bf777eb6ef36535bf6abd069390c5206"
sources:
  - raw/2026-08-28-260827454v1pdf.md
quality_score: 89
concepts:
  - wikiskill-framework
  - skill-evolution
  - persistent-knowledge
related:
  - "[[WikiSkill Framework]]"
  - "[[Cross-Model Transfer of Evolved Agent Skills]]"
  - "[[Karpathy LLM Wiki Pattern]]"
tier: hot
tags:
  - wikiskill
  - research-framework
  - agent-skills
  - persistent-knowledge
---

# WikiSkill

## Overview

WikiSkill is a research framework for co-evolving agent skills with a persistent knowledge base compiled from execution experience. It separates raw traces, structured wiki knowledge, and executable skills, then uses a Wiki Maintainer, Skill Proposer, and validation gate to refine procedures across iterations.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Research framework |
| Created | Unknown |
| Creator | Liyan Tang, Cyrus Rashtchian, Chun-Sung Ferng, Andrew Tomkins, Da-Cheng Juan, and Tu Vu |
| URL | https://arxiv.org/pdf/2608.27454 |
| Status | Unknown |

## Relevance

WikiSkill is relevant to persistent agent memory and skill engineering because it makes accumulated experience an explicit intermediate knowledge layer. Its experiments show that the retained wiki materially affects skill evolution and that evolved procedures can transfer between models, subject to source-target compatibility.

## Associated Concepts

- **[[WikiSkill Framework]]** — Describes the three-layer architecture, evolutionary loop, and validation-gated rollback.
- **[[Cross-Model Transfer of Evolved Agent Skills]]** — Describes the framework's cross-model skill-transfer findings.
- **[[Karpathy LLM Wiki Pattern]]** — The paper cites persistent, compounding LLM wiki knowledge as an inspiration.

## Related Entities

No additional related entities are documented in the source.

## Sources

- [[WikiSkill: Compiling Agent Experience into Persistent Knowledge for Skill Evolution]] — Introduces WikiSkill and reports its experiments.