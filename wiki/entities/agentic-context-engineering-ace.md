---
title: "Agentic Context Engineering (ACE)"
type: entity
created: 2026-04-20
last_verified: 2026-04-20
source_hash: "477e5dbd4d13659cf31de2992a6be546df5c474c80638069dbeef4368ec4bba0"
sources:
  - raw/2026-04-19-6372438pdf.md
  - raw/2026-04-16-251004618v3pdf.md
quality_score: 88
concepts:
  - agentic-context-engineering-ace
related:
  - "[[Brevity Bias and Context Collapse in LLM Context Adaptation]]"
  - "[[Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models]]"
  - "[[AppWorld Benchmark]]"
  - "[[FiNER]]"
  - "[[DeepSeek-V3.1]]"
tier: hot
tags: [context-adaptation, llm-agents, framework, self-improvement]
---

# Agentic Context Engineering (ACE)

## Overview

ACE is a modular framework for context adaptation in large language model applications, treating contexts as evolving playbooks that accumulate, refine, and organize strategies through structured generation, reflection, and curation. It addresses key limitations like brevity bias and context collapse, enabling scalable, self-improving LLM systems.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Framework |
| Created | 2026 |
| Creator | Qizheng Zhang, Changran Hu, Shubhangi Upasani, Boyuan Ma, Fenglu Hong, Vamsidhar Kamanuru, Jay Rainton, Chen Wu, Mengmeng Ji, Hanchen Li, Urmish Thakker, James Zou, Kunle Olukotun |
| URL | https://ace-agent.github.io |
| Status | Active |

## Relevance

ACE is central to the paper's contributions, offering a scalable, efficient, and interpretable solution for context adaptation in LLM agents and domain-specific reasoning tasks. It consistently outperforms strong baselines, reduces adaptation latency and cost, and enables self-improvement without labeled supervision.

## Associated Concepts

- **Agentic Context Engineering (ACE) Framework** — ACE is the implementation of the framework described.
- **[[Brevity Bias and Context Collapse in LLM Context Adaptation]]** — ACE is designed to mitigate these failure modes.

## Related Entities

- **Dynamic Cheatsheet** — ACE builds on the memory entry concept from Dynamic Cheatsheet.
- **[[AppWorld Benchmark]]** — co-mentioned in source (Dataset)
- **[[FiNER]]** — co-mentioned in source (Dataset)
- **[[DeepSeek-V3.1]]** — co-mentioned in source (Model)

## Sources

- [[Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models]] — where this entity was mentioned
- [[6372438.pdf]] — additional source
