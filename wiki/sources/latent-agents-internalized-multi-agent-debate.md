---
title: "Latent Agents: A Post-Training Procedure for Internalized Multi-Agent Debate"
type: source
created: '2026-04-29'
last_verified: '2026-04-29'
source_hash: a9a46db366eb237bc5197e4bbfcfeb10afd90cf81333ac5446f3e83995f057a1
sources:
  - raw/2026-04-29-260424881v1pdf.md
source_url: https://arxiv.org/abs/2604.24881
tags: [arxiv, llm, multi-agent-debate, activation-steering, post-training, mechanistic-interpretability]
tier: hot
knowledge_state: ingested
ingest_method: copilot-cli-gpt-5.4
quality_score: 78
---

# Latent Agents: A Post-Training Procedure for Internalized Multi-Agent Debate

## Summary

This ACL 2026 paper introduces Internalized Multi-Agent Debate (IMAD), a post-training recipe that compresses explicit multi-agent debate into a single language model. The method first teaches debate structure from full transcripts, then uses reinforcement learning with dynamic reward scheduling and length clipping to force the debate process out of the visible transcript and into latent computation. The paper also shows that the resulting internalized perspectives remain steerable as agent-specific activation subspaces, enabling both cheaper reasoning and more targeted behavior control.

## Key Points

- **Problem framing**: Explicit multi-agent debate improves reasoning quality, but it is expensive because several agents must generate long transcripts before producing a final answer.
- **Core method**: IMAD distills debate into one model with a two-stage pipeline: supervised fine-tuning on full debate traces, followed by reinforcement learning that rewards correctness while progressively penalizing verbose explicit debate.
- **Training data construction**: The paper builds a debate dataset with **944 traces** using the standard debate protocol with **3 agents** and **2 rounds**, starting from arithmetic expressions made of **six randomly generated two-digit numbers**.
- **Structured transcript design**: Debate logs are tagged with markers such as `<|Agent 1|>`, `<|Round 1|>`, `<|Consensus|>`, and `<|endofdebate|>` so the model can learn explicit role and round structure before internalization.
- **RL objective**: The reward mixes a formatting term and a correctness-with-length-clipping term, pushing the model to keep producing correct answers while moving the reasoning process earlier and deeper into the hidden state dynamics.
- **Training schedule**: The paper uses **3-6 SFT epochs**, then **2 GRPO epochs**, with the length limit annealed from **2000 to 500 tokens** and the format reward weight decayed from **1.0 to 0.05**; LoRA adapters are used in both stages.
- **Evaluation scope**: IMAD is evaluated on **GSM8K**, **MMLU-Pro**, and **Big-Bench Hard** across **LLaMA-3.1 8B**, **Qwen 2.5 7B**, and **Mistral Nemo 12B**.
- **Efficiency gain**: Across models, IMAD uses only **6.3%-21.1%** of the tokens consumed by explicit debate, corresponding to roughly **5-16x** inference efficiency improvement and up to **93% fewer tokens**.
- **Mechanistic finding**: Activation steering reveals **agent-specific subspaces** inside the internalized models; steering faithfulness improves by **6.10%-24.97%**, with an average gain of **15.41%** over the base model.
- **Safety/control result**: When one internalized agent is deliberately malicious, negative steering suppresses the encoded trait more cleanly than in the base model; for the "evil" trait, IMAD reaches complete suppression at coefficients from **-3.0 to -5.0** while preserving GSM8K performance more effectively.

## Key Concepts

- [[Multi-Agent Debate]]
- [[Internalized Multi-Agent Debate]]
- [[Agent-Specific Activation Subspaces]]

## Related Entities

- **[[Latent Agents]]** — The research framework introduced by the paper; it packages IMAD and the activation-steering control experiments into a single mechanistic story.
- **[[ReasoningBank]]** — A useful contrast point in the wiki because it improves agent reasoning via external memory and self-evolution, whereas IMAD internalizes collaborative reasoning into one model.
