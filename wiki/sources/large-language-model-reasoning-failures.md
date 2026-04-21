---
title: "Large Language Model Reasoning Failures"
type: source
created: 2026-04-21
last_verified: 2026-04-21
source_hash: "9b909ca9eada78d8d05ef05a3e511af46402d434c5a0b53123bbb430e41e3e8d"
sources:
  - raw/2026-04-10-260206176v1pdf.md
quality_score: 100
concepts:
  - taxonomy-of-llm-reasoning-failures
  - cognitive-biases-in-large-language-models
  - theory-of-mind-in-large-language-models
  - fundamental-cognitive-skills-executive-function-failures-llms
related:
  - "[[Taxonomy Of LLM Reasoning Failures]]"
  - "[[Cognitive Biases In Large Language Models]]"
  - "[[Theory Of Mind In Large Language Models]]"
  - "[[Fundamental Cognitive Skills And Executive Function Failures In LLMs]]"
  - "[[Awesome LLM Reasoning Failures Repository]]"
  - "[[Peiyang Song]]"
  - "[[Pengrui Han]]"
  - "[[Noah Goodman]]"
tier: hot
knowledge_state: executed
tags: [robustness, social-reasoning, llm, cognitive-bias, reasoning-failure, taxonomy]
---

# Large Language Model Reasoning Failures

## Summary

This paper presents the first comprehensive survey of reasoning failures in Large Language Models (LLMs), introducing a nuanced taxonomy that distinguishes reasoning types and failure categories. It analyzes core cognitive failures, social reasoning limitations, and robustness issues, providing definitions, root causes, and mitigation strategies. The work unifies fragmented research, offers a structured perspective on systemic weaknesses, and releases a curated repository of relevant studies.

## Key Points

- LLM reasoning failures are categorized along two axes: reasoning type (embodied vs. non-embodied, with informal and formal subdivisions) and failure type (fundamental, application-specific, robustness).
- Fundamental failures include deficits in core executive functions (working memory, inhibitory control, cognitive flexibility) and cognitive biases inherited from training data, architecture, and alignment processes.
- Application-specific limitations are prominent in social reasoning tasks such as Theory of Mind and moral reasoning, where LLMs exhibit inconsistent, unreliable, or brittle performance.

## Concepts Extracted

- **[[Taxonomy Of LLM Reasoning Failures]]** — The paper introduces a two-axis taxonomy for reasoning failures in Large Language Models, distinguishing reasoning types (embodied vs. non-embodied, with informal and formal subdivisions) and failure types (fundamental, application-specific, robustness). This structured framework enables systematic analysis and comparison of failure modes across diverse tasks.
- **[[Cognitive Biases In Large Language Models]]** — LLMs exhibit systematic cognitive biases analogous to human biases, affecting reasoning across diverse tasks. These biases are inherited from training data, model architecture, and alignment processes, and manifest as fundamental reasoning failures and robustness vulnerabilities.
- **[[Theory Of Mind In Large Language Models]]** — Theory of Mind (ToM) is the ability to attribute mental states to oneself and others, enabling interpretation and prediction of behaviors. LLMs are evaluated for ToM capacity, but even advanced models struggle with classic ToM tasks and exhibit brittle, inconsistent performance.
- **[[Fundamental Cognitive Skills And Executive Function Failures In LLMs]]** — LLMs systematically fail in fundamental cognitive skills essential for reasoning, including working memory, inhibitory control, cognitive flexibility, and abstract reasoning. These failures are intrinsic to model architecture and training dynamics, manifesting as broad vulnerabilities.

## Entities Mentioned

- **[[Awesome LLM Reasoning Failures Repository]]** — A curated GitHub repository compiling research works on reasoning failures in Large Language Models. It serves as an entry point for researchers and practitioners seeking to understand, analyze, and mitigate systemic weaknesses in LLM reasoning.
- **[[Peiyang Song]]** — Peiyang Song is a researcher affiliated with California Institute of Technology and Stanford University, specializing in Large Language Model reasoning and failure analysis. Song is the lead author of the survey and creator of the Awesome LLM Reasoning Failures repository.
- **[[Pengrui Han]]** — Pengrui Han is a researcher at Carleton College, specializing in reasoning failures and robustness in Large Language Models. Han is a co-author of the survey, contributing to taxonomy development and analysis.
- **[[Noah Goodman]]** — Noah Goodman is a researcher at Stanford University, specializing in cognitive science, reasoning, and Large Language Models. Goodman is a co-author of the survey, contributing expertise in cognitive phenomena and reasoning analysis.

## Notable Quotes

> "Failure is success if we learn from it." — Malcolm Forbes
> "We define LLM reasoning failures as cases where model responses significantly diverge from expected logical coherence, contextual relevance, or factual correctness." — Authors

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-10-260206176v1pdf.md` |
| Type | paper |
| Author | Peiyang Song, Pengrui Han, Noah Goodman |
| Date | Unknown |
| URL | https://arxiv.org/pdf/2602.06176 |
