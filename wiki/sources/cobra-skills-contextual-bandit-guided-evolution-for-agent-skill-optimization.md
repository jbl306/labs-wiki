---
title: "COBRA-Skills: Contextual Bandit-Guided Evolution for Agent Skill Optimization"
type: source
created: 2026-09-15
last_verified: 2026-09-15
source_hash: "dd436547ea18eace6464dcb20b924f525790f07a573a0b502cac2f52c5f89682"
sources:
  - raw/2026-09-15-260911682v1pdf.md
quality_score: 92
concepts:
  - contextual-bandit-guided-agent-skill-optimization
  - evidence-grounded-skill-evolution
  - cross-model-skill-transfer
related:
  - "[[Contextual-Bandit-Guided Agent Skill Optimization]]"
  - "[[COBRA-Skills]]"
  - "[[Cross-Model Transfer of Evolved Agent Skills]]"
tier: hot
tags:
  - agent-skills
  - contextual-bandits
  - skill-optimization
  - evolutionary-optimization
  - llm-agents
---

# COBRA-Skills: Contextual Bandit-Guided Evolution for Agent Skill Optimization

## Summary

This paper introduces COBRA-Skills, a framework that treats reusable agent-skill optimization as budgeted sequential optimization over a changing candidate population. It combines contextual-bandit prioritization with evidence-grounded skill evolution so target-agent evaluations are allocated to promising or uncertain candidates while execution trajectories are reused to refine the population.

Across six heterogeneous agent benchmarks and three target models, COBRA-Skills achieved the highest average performance among the compared methods, reduced optimization cost by 55–58% relative to SkillOpt, and used only 50 unique optimization examples per benchmark.

## Key Points

- Candidate skills are represented by semantic embeddings and ranked with a neural reward predictor plus a LinearUCB-style uncertainty bonus.
- The selected candidate is evaluated by the target agent on a fixed optimization set, and the resulting reward and trajectories update the optimization history.
- Scheduled population updates prune low-priority candidates and introduce new candidates through regeneration, rollout mutation, and crossover.
- Regeneration creates an independent skill from no-skill trajectories; rollout mutation revises the currently evaluated skill using successful and failed trajectories; crossover combines evidence from strong and weak evaluated skills.
- The final output is the evaluated skill with the highest mean observed reward.
- The default experiments used 30 rounds, a population of 10, 50 optimization examples, and a held-out test set of 100 examples per benchmark.
- COBRA-Skills remained effective under Claude Code and Codex harnesses, and self-teaching reduced optimization cost by roughly half with only a small average-score decrease.

## Concepts Extracted

- **[[Contextual-Bandit-Guided Agent Skill Optimization]]** — A budget-aware loop for selecting, evaluating, pruning, and evolving reusable agent skills.
- **[[Cross-Model Transfer of Evolved Agent Skills]]** — The paper reports that 34 of 36 cross-model transfers improved over the target model’s no-skill baseline.

## Entities Mentioned

- **[[COBRA-Skills]]** — The named research framework introduced by the paper.
- **SkillOpt** — A skill-optimization baseline used for performance and cost comparison; no canonical wiki page was found.

## Notable Quotes

> “COBRA-Skills couples contextual-bandit-guided prioritization with evidence-grounded skill evolution.” — paper abstract

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-09-15-260911682v1pdf.md` |
| Type | paper |
| Author | Pingchen Lu, Xiangyi Wang, Xiang Li, Jie Mao, Zikun Qu, Junfeng Luo, Yao Shu, Bryan Kian Hsiang Low, and Zhongxiang Dai |
| Date | Unknown |
| URL | https://arxiv.org/pdf/2609.11682 |