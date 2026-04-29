---
title: "Internalized Multi-Agent Debate"
type: concept
created: 2026-04-29
last_verified: 2026-04-29
source_hash: "a9a46db366eb237bc5197e4bbfcfeb10afd90cf81333ac5446f3e83995f057a1"
sources:
  - raw/2026-04-29-260424881v1pdf.md
quality_score: 85
related:
  - "[[Multi-Agent Debate]]"
  - "[[Agent-Specific Activation Subspaces]]"
  - "[[Agent Memory Frameworks]]"
tier: hot
tags: [llm, post-training, multi-agent-debate, reinforcement-learning, reasoning]
---

# Internalized Multi-Agent Debate

## Overview

Internalized Multi-Agent Debate is a post-training strategy that teaches a single language model to perform the functional role of multi-agent debate without emitting a full visible debate transcript at inference time. In the Latent Agents paper, the method is abbreviated **IMAD** and framed as a way to keep the error-correcting and perspective-combining benefits of debate while removing most of its token and compute overhead.

The key idea is not merely to compress answers, but to compress *interaction structure*. Rather than fine-tuning on final consensus outputs alone, IMAD first teaches the model to reproduce the entire debate format and only afterward applies optimization pressure that makes explicit debate progressively less reward-compatible. That pressure encourages the debate to migrate from surface text into the model's latent computation.

## How It Works

IMAD begins with a structured debate dataset produced by explicit [[Multi-Agent Debate]]. In the paper's main setup, the authors generate **944** traces using **3 agents** over **2 rounds**, seeded by arithmetic problems built from six randomly generated two-digit numbers. Debates without a final majority consensus are filtered out. The retained traces are then wrapped in explicit markers such as `<|Agent 1|>`, `<|Round 1|>`, `<|Consensus|>`, and `<|endofdebate|>`, so the model sees debate not as generic prose but as a structured computation with named roles and transitions.

The first training stage is supervised fine-tuning (SFT). Here, the goal is not primarily to improve answer correctness; it is to teach the base model to imitate the *shape* of the debate. The model is trained autoregressively over the full trace, learning to generate multiple agent turns, iterative refinements, and a consensus segment. This differs from approaches that fine-tune only on final debate outputs. The paper argues that those compressed targets discard the very interactions that make debate useful in the first place.

After SFT, the model can already emit a plausible debate transcript by itself, but it still externalizes the reasoning and can still hallucinate or misalign agents. The second stage addresses that with reinforcement learning using Group Relative Policy Optimization (GRPO). For a prompt $x$ and model output $y$, the reward is defined as

$$
r(x, y) = w_{fmt} R^{fmt} + w_{clip} R(y; l).
$$

The first term, $R^{fmt}$, rewards adherence to the structured debate format. Early in training, this stabilizes the learned debate scaffold and prevents the model from forgetting the role/round structure learned during SFT. The second term, $R(y; l)$, rewards correctness under a truncation budget:

$$
R(y; l) =
\begin{cases}
1 & \text{if } y^* \in \text{clip}(y, l) \\
0 & \text{otherwise}
\end{cases}
$$

where $y^*$ is the correct answer and `clip(y, l)` keeps only the first $l$ tokens of the model's output. This creates a very specific optimization pressure. The model can still reason at length early on, but it only gets reward if the correct answer appears within the truncated prefix. As the clip length shrinks, verbose visible debate becomes harder to reconcile with reward maximization.

The scheduling policy is the real engine of internalization. During training, the format weight decays from **1.0 to 0.05**, while the length limit is annealed from **2000 to 500 tokens** across **2 GRPO epochs**. SFT itself runs for **3-6 epochs** depending on the base model, and LoRA adapters are used in both stages. The resulting transition is intentional: the model is first encouraged to speak the debate language, then gradually forced to stop externalizing it while still preserving answer quality. The only stable solution is to perform the cross-perspective reasoning internally and emit the answer earlier.

This two-stage design also explains why IMAD can outperform naive compression approaches. DebateGPT-style distillation, as summarized in the source, uses only final consensus outputs and indeed consumes very few tokens, but it underperforms both explicit debate and IMAD. Without access to the intermediate interactions, the distilled model cannot inherit the error-correction dynamics that make multi-agent debate strong. IMAD keeps those interactions during training, then removes them only at deployment time.

The paper evaluates IMAD on **GSM8K**, **MMLU-Pro**, and **Big-Bench Hard**, using **LLaMA-3.1 8B**, **Qwen 2.5 7B**, and **Mistral Nemo 12B** as base models. Across those settings, IMAD uses only **6.3%-21.1%** of explicit debate's tokens, equivalent to about **5-16x** inference efficiency improvement and up to **93% fewer tokens**. The source also notes that IMAD generalizes beyond the arithmetic domain used during training, suggesting that what transfers is a reusable reasoning structure rather than benchmark-specific memorization.

An especially interesting result is that SFT alone can already outperform explicit debate in some cases. The paper attributes this to an information advantage: the single SFT model sees the entire prior transcript as it generates each token, while explicit debate agents only see prior rounds at discrete turns. RL then takes this already-strong structured reasoner and compacts it, cutting token usage by up to **66%** relative to the SFT stage while preserving or improving accuracy. This makes IMAD a blend of distillation, post-training compression, and mechanistic structure learning rather than a simple decoding trick.

## Key Properties

- **Trace-preserving distillation**: Learns from full debate transcripts rather than only final answers.
- **Dynamic reward scheduling**: Internalization is produced by decaying format reward and shrinking length budget together.
- **Single-model deployment**: Shifts compute from inference-time agent orchestration to post-training.
- **Transfer beyond training domain**: Arithmetic debate traces still improve performance on broader reasoning benchmarks.
- **Mechanistically interpretable outcome**: Internalization leaves behind steerable role-specific directions instead of collapsing everything into one undifferentiated policy.

## Limitations

IMAD requires a nontrivial post-training pipeline, including curated debate traces and an RL stage, so it is not a zero-cost replacement for debate. Its benefits may also depend on having clean structure tags and tasks where role-based critique is genuinely useful. The paper's control experiments further show that not every harmful trait becomes perfectly localized: hallucination remains more distributed than the deliberately "evil" trait, which means internalization improves controllability without guaranteeing complete disentanglement.

## Examples

```python
def train_imad(base_model, debate_dataset):
    sft_model = supervised_finetune(
        base_model,
        debate_dataset,  # full structured traces
        objective="next_token_prediction",
    )

    for step in grpo_steps(sft_model):
        l = anneal_length(step, start=2000, end=500)
        w_fmt = decay(step, start=1.0, end=0.05)
        candidates = sample_outputs(step.model, k=step.k)
        rewards = [
            w_fmt * format_reward(y) + correctness_under_clip(y, l)
            for y in candidates
        ]
        step.update_from_preferences(candidates, rewards)

    return step.model
```

In practice, the visible debate becomes shorter and shorter during training until the model is effectively forced to "think debate" internally and answer directly.

## Practical Applications

Internalized multi-agent debate is useful when a team wants debate-quality reasoning but cannot afford explicit multi-agent inference in production. It is also valuable for research on controllable reasoning because the method creates structured internal roles that can later be analyzed or steered. Relative to external memory approaches such as [[Agent Memory Frameworks]], IMAD pushes more of the reasoning improvement into the model itself rather than relying on a runtime retrieval loop.

## Related Concepts

- **[[Multi-Agent Debate]]** — The explicit teacher protocol that IMAD learns and then compresses.
- **[[Agent-Specific Activation Subspaces]]** — Evidence that internalized roles remain recoverable after compression.
- **[[Agent Memory Frameworks]]** — A contrasting strategy for improving agent reasoning through externalized experience rather than latent internalization.

## Sources

- [[Latent Agents: A Post-Training Procedure for Internalized Multi-Agent Debate]] — Introduces IMAD, details the training objective, and reports efficiency and generalization results.
