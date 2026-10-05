---
title: Cross-Model Transfer of Evolved Agent Skills
type: concept
created: 2026-08-28
last_verified: 2026-09-15
source_hash: dd436547ea18eace6464dcb20b924f525790f07a573a0b502cac2f52c5f89682
sources:
- raw/2026-08-28-260827454v1pdf.md
- raw/2026-09-15-260911682v1pdf.md
quality_score: 91
concepts:
- cross-model-skill-transfer
- skill-evolution
- procedural-knowledge
- negative-transfer
- contextual-bandit-guided-agent-skill-optimization
related:
- '[[WikiSkill Framework]]'
- '[[WikiSkill]]'
- '[[Skill Design Framework for AI Agents]]'
- '[[Contextual-Bandit-Guided Agent Skill Optimization]]'
- '[[COBRA-Skills]]'
tier: hot
tags:
- agent-skills
- skill-transfer
- model-capability
- negative-transfer
- wikiskill
- cobra-skills
---

# Cross-Model Transfer of Evolved Agent Skills

## Overview

Cross-model skill transfer is the use of a procedural skill evolved by one inference model as the active skill for another model. The WikiSkill transfer experiments show that skills are not necessarily tied to the model that discovered them: transferred procedures can improve both smaller and larger target models, and can sometimes outperform a target model’s self-evolved skill.

COBRA-Skills provides complementary evidence from a different optimization procedure. While keeping GPT-5.5 fixed as the teaching model, its experiments found that 34 of 36 transfers between the three evaluated target models improved over the corresponding target-model no-skill baseline.

Transfer quality depends on the abstraction level of the procedure and on the target model’s ability to execute it. General workflows tend to transfer better, while low-level workarounds, model-specific assumptions, or fragmented tool procedures can constrain a stronger target model and cause negative transfer.

## How It Works

1. WikiSkill evolves a skill using a source model on training tasks.
2. The resulting skill is injected into the target model’s system prompt at inference time.
3. Performance is compared with the target’s no-skill baseline and, when available, its self-evolved skill.
4. Transfer is analyzed by task and source-target pair to distinguish general procedures from source-model-specific behavior.

The method separates two capabilities that ordinary self-evolution can conflate:

- **Skill discovery:** extracting useful procedures from experience.
- **Skill execution:** reliably applying those procedures during inference.

A target model may therefore benefit more from a skill discovered elsewhere than from its own skill, especially when it can execute structured instructions more reliably.

## Evidence and Examples

| Source skill | Target model and task | Result |
|---|---|---|
| Qwen-3.6-27B | Qwen-3.5-9B on SpreadSheet | 50.5%, versus 24.3% with no skill and 33.6% with its self-evolved skill |
| Qwen-3.6-27B | Gemma-4-31B on LiveMath | 73.7%, versus 33.9% with no skill and 56.7% with its self-evolved skill |
| Qwen-3.5-4B | Gemma-4-31B on LiveMath and ALFWorld | 73.1% and 66.9%, respectively |
| Qwen-3.5-4B | Gemini-3.5-Flash on SpreadSheet | 18.1%, down from the 50.5% no-skill baseline |

LiveMath skills transfer particularly well: Qwen-3.5-4B and Qwen-3.6-27B skills raise Gemini-3.5-Flash from 33.0% to 67.5% and 73.9%. SpreadSheet shows the opposite possibility: a Qwen-3.5-4B skill reduces Gemini-3.5-Flash performance because it encodes restrictive single-line commands, string-conversion rules, and fragmented diagnostics that consume interaction budget.

## Additional Evidence from COBRA-Skills

COBRA-Skills optimized skills on six heterogeneous benchmarks using Qwen3.6-35B-A3B, GPT-5.4-Nano, and Gemma4-26B-A4B-it as target models. Across its cross-model transfer matrix, 34 of 36 transfers improved over the corresponding evaluation model’s no-skill baseline. The authors interpret this as evidence that the optimized skills capture reusable task-level strategies rather than being tightly coupled to the model used for optimization.

## Key Properties

- **Asymmetric benefit:** A skill can help a target model more than the source model that created it.
- **Cross-scale transfer:** Transfer can work from smaller to larger models as well as in the opposite direction.
- **Procedure sensitivity:** General procedures transfer more reliably than model-specific workarounds.
- **Execution dependence:** The target must be capable of following the skill’s structure; long-context navigation is especially sensitive to execution ability.
- **Task dependence:** Transfer quality varies substantially across benchmarks and source-target pairs.
- **Empirical robustness:** COBRA-Skills reports mostly positive transfer across its evaluated target-model pairs, but not universal improvement.

## Trade-offs and Limitations

Transfer provides a way to reuse the cost of skill discovery across models, but it introduces a source-target compatibility problem. A procedure that prevents execution failures for a small model may unnecessarily constrain a stronger model. Detailed or fragmented instructions can also increase tool calls and exhaust a target’s interaction budget.

The COBRA-Skills transfer result is benchmark-based and includes two non-improving transfers, so it does not establish universal transfer rules or replace evaluation on the intended target model. The WikiSkill evidence likewise varies substantially by task and source-target pair.

## Practical Example

For OfficeQA, Qwen-3.5-4B’s skill lowers its own performance from 30.2% to 28.5%, yet raises Qwen-3.6-27B from 42.1% to 52.9%. The paper attributes this asymmetry to long-context behavior: the smaller model can lose focus in lengthy documents and revert to default reading, whereas the stronger model more reliably executes the skill’s structured search procedure.

## Relationship to Other Concepts

- **[[WikiSkill Framework]]** — Provides the persistent evolution loop that generated the original cross-model transfer findings.
- **[[Skill Design Framework for AI Agents]]** — Addresses the structure and specificity of reusable skills; the transfer evidence shows why overly model-specific structure can harm portability.
- **[[WikiSkill]]** — The research framework used for the earlier transfer experiments.
- **[[Contextual-Bandit-Guided Agent Skill Optimization]]** — Describes the adaptive evaluation and evolution procedure used for the additional transfer evidence.
- **[[COBRA-Skills]]** — The named framework reporting 34 improving transfers out of 36 evaluated cross-model pairs.

## Sources

- [[WikiSkill: Compiling Agent Experience into Persistent Knowledge for Skill Evolution]] — Reports cross-model transfer results, failure analysis, and the distinction between skill discovery and execution.
- [[COBRA-Skills: Contextual Bandit-Guided Evolution for Agent Skill Optimization]] — Reports cross-model transfer results from contextual-bandit-guided skill optimization.
