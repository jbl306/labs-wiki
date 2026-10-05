---
title: 'Agentic Artifact Creation: Systems, Evaluation, Principles, and Opportunities'
type: source
created: 2026-08-31
last_verified: 2026-09-08
source_hash: 6f27d7396f1d3d162817128cbc62d1215a0096b0d9c17dfcee9b67a34b9c1cb3
sources:
- raw/2026-08-31-paper-page-agentic-artifact-creation-systems-evaluation-prin.md
- raw/2026-08-31-260828122v1pdf.md
quality_score: 84
concepts:
- agentic-artifact-creation
- runtime-verification-stateful-artifact-construction
related:
- '[[Agentic Artifact Creation]]'
- '[[Runtime Verification for Stateful Artifact Construction]]'
- '[[Evaluator-Optimizer Workflow]]'
- '[[Structured Artifact Chains]]'
tier: hot
tags:
- agentic-ai
- artifact-creation
- evaluation
- runtime-verification
- accountability
---

# Agentic Artifact Creation: Systems, Evaluation, Principles, and Opportunities

## Summary

This survey defines agentic artifact creation as stateful construction in which an AI system materially constructs or revises a deliverable, carries artifact or process state across decisions, and uses intermediate observations to redirect later artifact-related work. It reviews 259 works available through August 20, 2026: 230 systems and 29 benchmarks.

The survey organizes the paradigm around three functional roles: an Operational Representation of the evolving artifact, a Construction Policy that selects actions from task requirements, state, and feedback, and Runtime Verification that turns observations into feedback. It compares textual, 2D visual, audio, video, spatial, and behavioral artifacts, then examines applications and evaluation as separate dimensions.

## Key Points

- Complete deliverables are harder than isolated drafts because their requirements and component decisions interact.
- Agentic creation is distinguished by persistent construction state and intermediate observations that redirect subsequent actions, revision targets, branches, or stopping decisions.
- Representational and edit granularity determine whether failures can be localized and repaired without discarding accepted work.
- Decomposition may reduce local complexity while increasing coordination, handoff, and reassembly costs.
- Evaluation should distinguish delivered-artifact quality, construction-trajectory behavior, and agentic-system properties such as reliability, robustness, efficiency, controllability, and update stability.
- Learned judges may provide limited independent evidence when they share generator preferences or blind spots.
- The survey proposes four principles: Externalize Commitments, Define Control Boundaries, Make Feedback Actionable, and Revalidate Affected State.

## Concepts Extracted

- **[[Agentic Artifact Creation]]** — Stateful construction and revision of deliverables driven by intermediate observations and feedback.
- **[[Runtime Verification for Stateful Artifact Construction]]** — In-loop verification that redirects construction, scopes repair, and revalidates affected state.
- **[[Evaluator-Optimizer Workflow]]** — An adjacent iterative feedback pattern already represented in the wiki.
- **[[Structured Artifact Chains]]** — An adjacent approach for making intermediate artifacts inspectable and auditable.

## Entities Mentioned

- No separate tool, organization, dataset, or model page is required for this source-grounded update. The paper and its authors are documented as source metadata.

## Review Scope and Limitations

The authors searched arXiv, Google Scholar, Semantic Scholar, ACM Digital Library, and IEEE Xplore using agentic-process terms crossed with the six artifact families, supplemented by citation tracing and venue audits. After deduplication and screening, they retained 230 systems and 29 benchmarks. Database-specific query exports, per-source yields, and pre-reconciliation labels were not retained, and benchmark maturity is uneven across artifact families.

## Source Details

| Field | Value |
|-------|-------|
| Original title | Agentic Artifact Creation: Systems, Evaluation, Principles, and Opportunities |
| Authors | Tianfu Wang; Zhezheng Hao; Xilin Xia; Lixin Liu; Mengkang Hu; Hongzhang Liu; Xi Chen; Ziyan Liu; Xiankun Lin; Weijia Zhang; Nicholas Jing Yuan; Hui Xiong |
| Date | 2026-08-28 |
| arXiv | 2608.28122 |
| Source URL | https://arxiv.org/pdf/2608.28122 |
| Companion source URL | https://huggingface.co/papers/2608.28122 |
| Project website | https://agentic-creation.github.io |
| Curated repository | https://github.com/GeminiLight/awesome-agentic-artifact-creation |
