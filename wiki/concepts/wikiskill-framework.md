---
title: "WikiSkill Framework"
type: concept
created: 2026-08-28
last_verified: 2026-08-28
source_hash: "609c3adec2ebe732fcc6bf8667864803bf777eb6ef36535bf6abd069390c5206"
sources:
  - raw/2026-08-28-260827454v1pdf.md
quality_score: 94
concepts:
  - wikiskill-framework
  - persistent-knowledge
  - skill-evolution
  - agent-experience
related:
  - "[[WikiSkill]]"
  - "[[Karpathy LLM Wiki Pattern]]"
  - "[[Agentic Wiki Optimization per Karpathy Compile-Once Principles]]"
tier: hot
tags:
  - wikiskill
  - agent-skills
  - persistent-knowledge
  - evolutionary-agents
  - knowledge-compilation
---

# WikiSkill Framework

## Overview

WikiSkill is a framework for evolving reusable agent skills together with a persistent knowledge base. It addresses a weakness in experience-driven skill optimization: useful observations, recurring failures, and rejected interventions can remain scattered across trajectory histories instead of becoming an explicit representation that later updates can consult.

The framework maintains a joint state of active skills and accumulated wiki knowledge. Skills may be rolled back when validation performance falls, but the wiki persists, allowing later iterations to build on prior evidence rather than restarting from an empty history.

## How It Works

WikiSkill organizes the workspace into three layers:

1. **Raw Layer:** Immutable execution traces contain the agent's observations, actions, tool calls, tool outputs, reasoning, and final answers.
2. **Wiki Layer:** A pattern directory records failure modes, successful strategies, and actionable workarounds. Evolution logs and a programmatic skill-impact tracker preserve proposal history, acceptance outcomes, and recurring errors.
3. **Skills Layer:** Active procedural knowledge is stored in filesystem-based skills. Each skill includes `SKILL.md` for its instructions and `PURPOSE.md` linking the skill to motivating wiki patterns.

The evolutionary loop has four components:

1. The **Inference Agent** performs training rollouts with the active skills. During training, it is restricted from reading the Wiki Layer so that the trajectories reveal what the skills themselves enable.
2. The **Wiki Maintainer** analyzes sampled successful and failing traces, performs root-cause analysis, extracts useful strategies, and incrementally creates or updates pattern pages.
3. The **Skill Proposer** receives the wiki index, skill-impact history, task outcomes, and on-demand access to selected traces. In a ReAct-style process, it proposes one atomic skill creation or edit.
4. **Gating and Rollback** evaluates the candidate skill set on a validation split. An update is accepted only when it improves the best validation score; otherwise the active skills revert while the wiki retains the evidence.

The state transition can be summarized as:

```text
execution traces -> wiki pattern consolidation -> atomic skill proposal
                  -> validation gate -> accept or rollback skill set
                  -> persistent wiki update
```

## Key Properties

- **Separated concerns:** Raw evidence, compiled knowledge, and executable procedures have distinct storage and access roles.
- **Persistent accumulation:** Patterns, rejected proposals, and evolution history survive skill rollback and future iterations.
- **Atomic proposals:** Each iteration targets one skill creation or incremental edit, making validation outcomes easier to attribute.
- **Validation-based control:** Only proposals that exceed the current best validation score become active.
- **Asymmetric rollback:** Skills can revert after degradation, while accumulated wiki knowledge is retained.

## Concrete Example

In the paper's ALFWorld case study with Qwen-3.6-27B, the Wiki Maintainer first records a `take-examine-move-loop` pattern. A `goal-directed-action` proposal fails validation and is rejected. The impact tracker preserves that rejection, after which the proposer creates a `break-repetition-loop` skill containing the rule `Never Return an Item to Its Origin Location`; this update is accepted. Later, new loop evidence leads to a refinement requiring `Each Operation Type ONCE Per Item`.

## Trade-offs and Limitations

The persistent layer improves historical awareness, but it also grows across iterations and currently lacks automated pruning. Strict improvement-only gating protects benchmark performance but rejects neutral changes that might enable later gains. Directly injecting full skills into the inference prompt isolates skill quality from retrieval, but the framework therefore does not evaluate skill triggering or retrieval at scale. The training-time restriction on Wiki access can make trajectories more informative for skill development, yet it differs from an agent that freely consults all accumulated knowledge during task execution.

## Relationship to Other Concepts

- **[[Karpathy LLM Wiki Pattern]]** — The paper explicitly draws on the idea of compiling experience into persistent, compounding wiki knowledge.
- **[[Agentic Wiki Optimization per Karpathy Compile-Once Principles]]** — Provides a related application of compile-once knowledge artifacts and graph-aware wiki maintenance.
- **[[WikiSkill]]** — The named framework implementing this architecture.

## Practical Applications

WikiSkill is applicable when agents repeatedly solve related tasks and need procedural improvements to persist across optimization rounds. Its separation between evidence, knowledge, and active instructions is useful for auditable skill development, failure analysis, benchmark-driven agent improvement, and controlled rollback of candidate procedures.

## Sources

- [[WikiSkill: Compiling Agent Experience into Persistent Knowledge for Skill Evolution]] — Introduces the architecture, loop, ablation, and case study.