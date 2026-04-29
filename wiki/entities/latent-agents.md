---
title: Latent Agents
type: entity
created: 2026-04-29
last_verified: 2026-04-29
source_hash: "a9a46db366eb237bc5197e4bbfcfeb10afd90cf81333ac5446f3e83995f057a1"
sources:
  - raw/2026-04-29-260424881v1pdf.md
concepts: [multi-agent-debate, internalized-multi-agent-debate, agent-specific-activation-subspaces]
related:
  - "[[Internalized Multi-Agent Debate]]"
  - "[[Agent-Specific Activation Subspaces]]"
  - "[[Theory Of Mind In Large Language Models]]"
tier: hot
tags: [llm, multi-agent-debate, activation-steering, post-training, acl-2026]
---

# Latent Agents

## Overview

Latent Agents is the research framework introduced in the ACL 2026 paper *Latent Agents: A Post-Training Procedure for Internalized Multi-Agent Debate*. Instead of running several language models in an explicit debate loop at inference time, the framework teaches a single model to reproduce, then internalize, the collaborative reasoning pattern that multi-agent debate normally exposes as text.

The work matters because it reframes debate not as a deployment topology but as a trainable reasoning prior. In the paper's formulation, explicit debate transcripts become supervision, dynamic reward scheduling pushes that debate inward, and the resulting hidden-state geometry preserves agent-like viewpoints that can later be amplified or suppressed with activation steering.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Research Framework |
| Created | 2026-04-27 |
| Creator | John Seon Keun Yi, Aaron Mueller, and Dokyun Lee (Boston University) |
| URL | https://github.com/johnsk95/latent_agents |
| Status | Active |

## Core Concept

Latent Agents centers on the claim that a multi-agent protocol can be distilled into a single model without collapsing the useful diversity that debate provides. The framework operationalizes that claim with [[Internalized Multi-Agent Debate]], where a model first learns the external debate format and then learns to stop verbalizing it while still retaining its performance benefits.

This makes the framework distinct from approaches that simply fine-tune on final answers. The paper argues that the intermediate interactions are the important part: they teach error correction, cross-perspective refinement, and consensus formation, all of which are weakened when only the final output is kept.

## Training Pipeline

The paper's pipeline has three linked stages:

1. **Debate dataset construction** — collect explicit debate traces using the standard [[Multi-Agent Debate]] protocol.
2. **Structure learning via SFT** — train on the full transcript so one model can emit the role markers, rounds, critiques, and consensus pattern.
3. **Internalization via RL** — optimize the model so correct answers appear under progressively tighter length budgets, making visible debate increasingly incompatible with reward maximization.

In the paper's main setup, the dataset contains 944 structured traces generated with three agents and two rounds. The RL stage uses GRPO, decays the format reward, anneals the clip length from 2000 to 500 tokens, and uses LoRA adapters throughout.

## Mechanistic Analysis

Latent Agents is not only a performance paper; it is also a mechanistic interpretability paper. After training, the authors probe the resulting models with activation steering and show that internalization creates [[Agent-Specific Activation Subspaces]] corresponding to different reasoning personas. In the diverse-persona setup, those personas include Chain-of-Thought, Self-Critique, and Program-of-Thought styles.

The steering results support the paper's central thesis: internalized debate is not merely compressed output formatting. Instead, the model appears to preserve separable internal directions for different collaborative roles, which can be recovered with contrastive activation methods and manipulated at inference time.

## Safety Implications

The framework also demonstrates a concrete control use case. By training debates in which one agent expresses malicious behavior, the authors create an internalized harmful trait and then suppress it with negative steering. The most striking result is that the "evil" trait can be driven to zero in the internalized model at strong negative coefficients while preserving downstream reasoning performance better than in the base model.

This makes Latent Agents relevant not only for cheaper inference, but also for controllable reasoning: the same structure that preserves internal perspectives can make unwanted ones easier to isolate.

## Sources

- [[Latent Agents: A Post-Training Procedure for Internalized Multi-Agent Debate]] — Primary source describing the framework, experiments, and mechanistic analysis.
