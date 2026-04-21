---
title: "NousResearch/autoreason: Autoresearch for Subjective Domains"
type: source
created: 2026-04-21
last_verified: 2026-04-21
source_hash: "f0ccf54adde211ffedb54b1a0f85d4b1c5066e47bbf5b9969689ffa753ca125f"
sources:
  - raw/2026-04-13-nousresearchautoreason-autoresearch-for-subjective-domains.md
quality_score: 100
concepts:
  - autoreason-iterative-self-refinement-framework
related:
  - "[[Autoreason Iterative Self-Refinement Framework]]"
  - "[[Autoreason]]"
  - "[[SHL0MS]]"
  - "[[Hermes Agent]]"
tier: hot
knowledge_state: executed
tags: [blind-judging, agentic-workflows, tournament-evaluation, research-framework, iterative-refinement, subjective-domains, convergence]
---

# NousResearch/autoreason: Autoresearch for Subjective Domains

## Summary

Autoreason is a framework designed to address structural failures in iterative self-refinement for subjective tasks, such as writing and code generation. It introduces a tournament-based approach that produces three competing versions per iteration and employs blind judging to ensure unbiased selection and convergence. The repository contains extensive experimental results, ablation studies, and human evaluation materials, demonstrating Autoreason's superiority over critique-and-revise and single-pass baselines.

## Key Points

- Iterative self-refinement fails due to prompt bias, scope creep, and lack of restraint; Autoreason addresses all three.
- Each iteration generates an unchanged incumbent, adversarial revision, and synthesis, judged via blind Borda count.
- Experimental results show Autoreason outperforms baselines in writing and code tasks, with robust convergence and scalability.

## Concepts Extracted

- **[[Autoreason Iterative Self-Refinement Framework]]** — Autoreason is a structured, tournament-based iterative refinement framework for subjective domains such as writing and code generation. It systematically addresses common failure modes in agentic self-improvement workflows, including prompt bias, scope creep, and lack of restraint, by generating multiple competing versions and employing blind, context-isolated judging.

## Entities Mentioned

- **[[Autoreason]]** — Autoreason is a research framework and repository for iterative self-refinement in subjective domains, such as writing and code generation. It implements a tournament-based approach that generates multiple competing versions per iteration, judged by blind, context-isolated panels to ensure unbiased convergence. The repository includes experiment runners, human evaluation materials, and statistical analysis scripts.
- **[[SHL0MS]]** — SHL0MS is a co-author of the Autoreason framework, contributing to the design and research of iterative self-refinement methodologies for subjective domains. Their work focuses on addressing structural failures in agentic workflows and advancing tournament-based evaluation strategies.
- **[[Hermes Agent]]** — Hermes Agent is a co-author of the Autoreason framework, specializing in agentic workflow design and tournament-based evaluation for subjective task refinement. Their research emphasizes unbiased judging and robust convergence in multi-agent systems.

## Notable Quotes

> "Iterative self-refinement fails for three structural reasons: prompt bias (models hallucinate flaws when asked to critique), scope creep (outputs expand unchecked each pass), and lack of restraint (models never say 'no changes needed'). Autoreason fixes all three." — README
> "Each iteration produces three competing versions — the unchanged incumbent (A), an adversarial revision (B), and a synthesis (AB) — judged by fresh agents with no shared context via blind Borda count. 'Do nothing' is always a first-class option." — README

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-13-nousresearchautoreason-autoresearch-for-subjective-domains.md` |
| Type | repo |
| Author | SHL0MS and Hermes Agent |
| Date | Unknown |
| URL | https://github.com/NousResearch/autoreason |
