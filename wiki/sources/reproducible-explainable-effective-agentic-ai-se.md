---
title: "Reproducible, Explainable, and Effective Evaluations of Agentic AI for Software Engineering"
type: source
created: '2026-04-22'
last_verified: '2026-04-22'
source_hash: 5173b70a6725e131573c351830b6c4874521518221c53b9cb004f836568ed255
sources:
  - raw/2026-04-22-260401437v1pdf.md
source_url: https://arxiv.org/abs/2604.01437
concepts:
  - thought-action-result-tar-trajectories
  - agentic-ai-evaluation-software-engineering
related:
  - "[[Reproducible, Explainable, and Effective Evaluations of Agentic AI for Software Engineering]]"
  - "[[Thought-Action-Result (TAR) Trajectories]]"
  - "[[Agentic AI Evaluation for Software Engineering]]"
tags: [arxiv, agentic-ai, software-engineering, evaluation, reproducibility, explainability, tar-trajectories]
tier: hot
knowledge_state: ingested
ingest_method: copilot-cli-gpt-5.4
quality_score: 76
---

# Reproducible, Explainable, and Effective Evaluations of Agentic AI for Software Engineering

## Summary

This April 2026 arXiv position paper argues that software-engineering research on autonomous agents is moving faster than its evaluation practice. After analyzing 18 papers from ICSE 2025-2026, FSE 2025, ASE 2025, and ISSTA 2025, the authors propose guidelines for making agent evaluations reproducible, explainable, and practically comparable. The paper's clearest recommendation is to publish Thought-Action-Result (TAR) trajectories and LLM interaction artifacts, or high-fidelity summaries of them, so later work can inspect how and why an agent succeeded or failed.

## Key Points

- **Core diagnosis**: Agentic AI papers in software engineering often claim strong results while relying on opaque LLM behavior, which makes it hard to explain why an approach outperforms a baseline.
- **Reproducibility gap**: Many evaluations omit crucial details about evaluation design, leaving later researchers unable to reproduce the reported outcomes.
- **Evidence base**: The paper synthesizes 18 Agentic AI for SE papers that were published or accepted at ICSE 2025, ICSE 2026, FSE 2025, ASE 2025, and ISSTA 2025.
- **Position-paper framing**: Rather than introducing a new benchmark or model, the work focuses on strengthening the research methodology used to evaluate agentic systems.
- **Primary recommendation**: Researchers should release **[[Thought-Action-Result (TAR) Trajectories]]** and LLM interaction data, or summarized versions of those artifacts, as part of their evaluation package.
- **Why trajectories matter**: Trajectory records expose intermediate reasoning, tool choices, and environmental feedback, making cross-approach comparison more explainable than final-score reporting alone.
- **Proof of feasibility**: The authors include a proof-of-concept case study showing that TAR trajectories can support structured comparison across different Agentic AI approaches.
- **Scope of impact**: The guidance is targeted specifically at **[[Agentic AI Evaluation for Software Engineering]]**, where tasks are long-horizon, tool-using, and sensitive to evaluation setup details.
- **Venue context**: The paper was accepted to the 2nd International Workshop on Responsible Software Engineering (ResponsibleSE 2026), co-located with FSE.
- **Authorship and date**: arXiv lists Jingyue Li and André Storhaug as authors and records the submission date as 2026-04-01.

## Key Concepts

- [[Agentic AI Evaluation for Software Engineering]]
- [[Thought-Action-Result (TAR) Trajectories]]
- [[The Observability Imperative]]

## Related Entities

- **[[Reproducible, Explainable, and Effective Evaluations of Agentic AI for Software Engineering]]** - Durable entity page for the paper as a position piece about methodology and evaluation evidence.
- **[[Anthropic’s 'Building Effective Agents' Guide]]** - Complementary agent-systems guidance that emphasizes design patterns, whereas this paper emphasizes evaluation transparency and comparability.
- **[[SWE-Bench-Verified]]** - Representative software-engineering benchmark showing why richer evaluation artifacts are useful for understanding agent behavior.
