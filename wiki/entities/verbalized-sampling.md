---
title: Verbalized Sampling
type: entity
created: '2026-04-25'
last_verified: '2026-04-25'
source_hash: "31baf54a0ffb96c571203e5c35d3defc247078c20d39650279674699bd41c656"
sources:
  - raw/2026-04-25-251001171v3pdf.md
concepts: [typicality-bias-preference-data, mode-collapse-aligned-llms]
related:
  - "[[Typicality Bias in Preference Data]]"
  - "[[Mode Collapse in Aligned LLMs]]"
  - "[[Cognitive Biases In Large Language Models]]"
tier: warm
tags: [llm, prompting, alignment, mode-collapse, diversity, inference-time]
quality_score: 76
---

# Verbalized Sampling

## Overview

Verbalized Sampling is a training-free prompting method introduced in the 2025 arXiv paper *Verbalized Sampling: How to Mitigate Mode Collapse and Unlock LLM Diversity*. It is designed for aligned LLMs whose outputs have become overly concentrated around a single stereotypical answer after post-training.

Instead of asking the model for one completion, Verbalized Sampling asks it to verbalize a small response distribution: multiple candidate outputs plus estimated probabilities. The method matters because it targets diversity loss at inference time, without retraining the model or changing the alignment pipeline, and the paper shows that this simple reformulation can recover much of the diversity suppressed by direct prompting.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Prompting Method |
| Created | 2025-10-01 |
| Creator | Jiayi Zhang, Simon Yu, Derek Chong, Anthony Sicilia, Michael R. Tomz, Christopher D. Manning, and Weiyan Shi |
| URL | https://github.com/CHATS-lab/verbalized-sampling |
| Status | Active |

## Core Idea

The paper's central claim is that different prompts can collapse to different modes of the underlying pretraining distribution. A standard prompt like "tell me a joke about coffee" tends to elicit the most stereotypical coffee joke. Verbalized Sampling changes the task: it asks for several jokes and their probabilities, which shifts the model toward representing a broader slice of the distribution it learned before alignment narrowed it.

That makes the method a practical response to [[Mode Collapse in Aligned LLMs]]. Rather than trying to undo preference optimization directly, it changes the observable interface the model is asked to satisfy. In the paper's framing, the prompt steers the model away from the single highest-probability aligned response and toward an approximate distributional summary of plausible responses.

## Prompt Structure

The paper studies several variants:

- **VS-Standard** — ask for `k` candidate responses and their probabilities in a single call.
- **VS-CoT** — ask the model to think step by step before producing the candidate list and probabilities.
- **VS-Multi** — extend the same logic to multi-turn settings such as dialogue simulation, where each turn requires selecting a continuation from a verbalized candidate set.

For dialogue simulation, the paper explores two design axes: whether the number of candidates is model-decided or fixed (for example, `k = 5`), and whether the next utterance is sampled according to the verbalized probabilities or uniformly at random. The reported best trade-offs come from model-decided random sampling and human-fixed probability-weighted sampling, depending on the setting.

## Performance & Evaluation

The method is evaluated across four application families:

1. **Creative writing** — poem continuation, story generation, and joke writing. Diversity is measured semantically with embedding similarity and lexically with ROUGE-L; quality is judged with Claude-3.7-Sonnet. The headline result is a **1.6-2.1x** diversity improvement over direct prompting.
2. **Dialogue simulation** — PersuasionForGood, with a GPT-4.1-based persuader and LLM-based persuadee. Verbalized Sampling produces more human-like response patterns and competitive realism.
3. **Open-ended QA** — CoverageQA-style questions with many valid answers. The method improves coverage and KL divergence to a realistic reference distribution while keeping precision near 1.0.
4. **Synthetic data generation** — GPT-4.1 and Gemini-2.5-Flash generate 1,000 competition-math problems; Qwen3-32B supplies reasoning traces; fine-tuning smaller Qwen models on the resulting data improves downstream benchmark performance.

## Limitations

The paper highlights two main caveats. First, generating a response distribution costs more tokens and latency than asking for a single output, so the approach is less attractive in highly latency-sensitive systems. Second, benefits scale with model capability: weaker models are less reliable at probability verbalization and may not consistently improve under the method.

## Sources

- [[Verbalized Sampling: How to Mitigate Mode Collapse and Unlock LLM Diversity]]
