---
title: "NousResearch/autoreason: Autoresearch for Subjective Domains"
type: source
created: 2026-04-13
last_verified: 2026-04-13
source_hash: "3f74fe7844e038b10bfb0f29c9a27acf64d9c65cb9437934aa6cb8cb60254178"
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
tags: [blind evaluation, llm reasoning, subjective domains, self-refinement, agentic workflows]
---

# NousResearch/autoreason: Autoresearch for Subjective Domains

## Summary

Autoreason is a research framework and methodology designed to address iterative self-refinement failures in subjective tasks, such as writing and competitive programming, by introducing structured competition and restraint in revision cycles. The repository provides experimental results, human evaluation materials, and a detailed process for generating, critiquing, and synthesizing outputs using large language models and blind agent panels. Key findings demonstrate Autoreason's superiority over traditional critique-and-revise and single-pass approaches, especially in tasks requiring nuanced judgment.

## Key Points

- Iterative self-refinement fails due to prompt bias, scope creep, and lack of restraint; Autoreason addresses all three.
- Each iteration produces three competing versions (incumbent, adversarial revision, synthesis) judged via blind Borda count.
- Autoreason achieves perfect sweeps and significant accuracy gains in writing and code tasks compared to baselines.

## Concepts Extracted

- **[[Autoreason Iterative Self-Refinement Framework]]** — Autoreason is a structured methodology for iterative self-refinement in subjective domains, such as writing and competitive programming. It addresses fundamental flaws in traditional critique-and-revise cycles by introducing explicit restraint, competitive revision, and blind evaluation, enabling models to know when to stop and avoid unnecessary changes.

## Entities Mentioned

- **[[Autoreason]]** — Autoreason is a research framework and repository for iterative self-refinement in subjective domains, such as writing and code generation. It implements a structured tournament process with blind agent panels and explicit restraint, enabling models to know when to stop revising and avoid unnecessary changes. The repository includes LaTeX papers, experiment scripts, human evaluation materials, and code for running competitive tournaments among agent-generated outputs.
- **[[SHL0MS]]** — SHL0MS is a researcher and co-author of the Autoreason framework, contributing to the design, implementation, and evaluation of iterative self-refinement methodologies for subjective domains. SHL0MS's work focuses on agentic workflows, blind evaluation, and structural remedies for reasoning failures in large language models.
- **[[Hermes Agent]]** — Hermes Agent is a co-author and agentic collaborator in the Autoreason project, involved in the design and experimentation of iterative self-refinement processes for subjective domains. Hermes Agent's role includes both conceptual and technical contributions to the tournament-style revision and blind evaluation methodology.

## Notable Quotes

> "Iterative self-refinement fails for three structural reasons: prompt bias, scope creep, and lack of restraint." — README
> "Autoreason fixes all three. Each iteration produces three competing versions — the unchanged incumbent (A), an adversarial revision (B), and a synthesis (AB) — judged by fresh agents with no shared context via blind Borda count." — README
> ""Do nothing" is always a first-class option." — README

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-13-nousresearchautoreason-autoresearch-for-subjective-domains.md` |
| Type | repo |
| Author | SHL0MS and Hermes Agent |
| Date | 2026 |
| URL | https://github.com/NousResearch/autoreason |
