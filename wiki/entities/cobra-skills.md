---
title: "COBRA-Skills"
type: entity
created: 2026-09-15
last_verified: 2026-09-15
source_hash: "dd436547ea18eace6464dcb20b924f525790f07a573a0b502cac2f52c5f89682"
sources:
  - raw/2026-09-15-260911682v1pdf.md
quality_score: 90
concepts:
  - contextual-bandit-guided-agent-skill-optimization
  - evidence-grounded-skill-evolution
related:
  - "[[Contextual-Bandit-Guided Agent Skill Optimization]]"
  - "[[Cross-Model Transfer of Evolved Agent Skills]]"
  - "[[WikiSkill]]"
tier: hot
tags:
  - agent-skills
  - contextual-bandits
  - optimization-framework
  - llm-agents
---

# COBRA-Skills

## Overview

COBRA-Skills is a research framework for optimizing reusable skills for large-language-model agents under a limited evaluation budget. It combines contextual-bandit prioritization with evidence-grounded evolutionary operators that generate, refine, and replace candidate skills.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Research framework |
| Created | Unknown |
| Creator | Pingchen Lu, Xiangyi Wang, Xiang Li, Jie Mao, Zikun Qu, Junfeng Luo, Yao Shu, Bryan Kian Hsiang Low, and Zhongxiang Dai |
| URL | https://github.com/Jerry-LuP/COBRA-Skills |
| Status | Research prototype; code available |

## Relevance

COBRA-Skills is a concrete implementation of [[Contextual-Bandit-Guided Agent Skill Optimization]]. It treats each candidate skill as a contextual arm, uses execution reward to train a lightweight predictor, and uses uncertainty to decide which candidate should receive the next expensive evaluation. Its evolutionary operators connect evaluation feedback to continued skill-population refinement.

The framework is also relevant to [[Cross-Model Transfer of Evolved Agent Skills]] because its experiments found that 34 of 36 cross-model transfers improved over the corresponding target-model no-skill baseline.

## Associated Concepts

- **[[Contextual-Bandit-Guided Agent Skill Optimization]]** — Describes COBRA-Skills’ selection, evaluation, and population-evolution mechanism.
- **[[Cross-Model Transfer of Evolved Agent Skills]]** — Covers the reported transfer of optimized skills between target models.
- **[[WikiSkill Framework]]** — A related framework for persistent, experience-driven skill evolution.

## Related Entities

- **[[WikiSkill]]** — Another research framework for evolving reusable agent skills from execution experience.

## Sources

- [[COBRA-Skills: Contextual Bandit-Guided Evolution for Agent Skill Optimization]] — Introduces the framework, its algorithm, and experimental evaluation.