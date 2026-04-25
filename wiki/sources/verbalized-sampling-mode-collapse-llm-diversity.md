---
title: "Verbalized Sampling: How to Mitigate Mode Collapse and Unlock LLM Diversity"
type: source
created: '2026-04-25'
last_verified: '2026-04-25'
source_hash: "31baf54a0ffb96c571203e5c35d3defc247078c20d39650279674699bd41c656"
sources:
  - raw/2026-04-25-251001171v3pdf.md
source_url: https://arxiv.org/abs/2510.01171
tags: [arxiv, llm, alignment, prompting, mode-collapse, diversity, preference-data]
tier: warm
knowledge_state: ingested
ingest_method: copilot-cli-gpt-5.4
quality_score: 78
---

# Verbalized Sampling: How to Mitigate Mode Collapse and Unlock LLM Diversity

## Summary

This paper argues that alignment-induced diversity loss in large language models is not just an optimization artifact; it is also driven by **typicality bias** in preference data, where annotators systematically favor familiar and predictable text. It introduces **[[Verbalized Sampling]]**, a training-free prompting method that asks the model to state a distribution over candidate responses, then shows that this recovers substantially more of the base model's latent diversity across creative writing, dialogue simulation, open-ended QA, and synthetic data generation.

## Key Points

- **Problem framing**: Post-training alignment methods such as RLHF can trigger [[Mode Collapse in Aligned LLMs]], causing the model to repeatedly produce a narrow set of stereotypical responses even when many answers would be acceptable.
- **Core diagnosis**: The paper identifies **[[Typicality Bias in Preference Data]]** as a data-level driver of collapse, grounded in cognitive-psychology effects such as familiarity preference, processing fluency, and schema congruity.
- **Formalization**: The reward model is written as $r(x,y)=r_{\\text{true}}(x,y)+\\alpha\\log \\pi_{\\mathrm{ref}}(y\\mid x)+\\epsilon(x)$, where positive $\\alpha$ means more typical completions receive higher reward even when true task utility is unchanged.
- **Method**: [[Verbalized Sampling]] asks the model to generate multiple candidate responses plus probabilities, e.g. "generate 5 jokes about coffee and their corresponding probabilities," rather than directly returning a single completion.
- **Creative-writing setup**: The paper evaluates poem continuation, story generation, and joke writing using PoemHunter.com, BookMIA, and 100 thematic prompts from Reddit r/DadJokes; semantic diversity is measured as $1-\\bar{s}$ from text-embedding-3-small embeddings, lexical diversity via ROUGE-L, and quality with Claude-3.7-Sonnet as judge.
- **Main result**: In creative writing, verbalized sampling improves diversity by roughly **1.6-2.1x** over direct prompting while preserving output quality.
- **Dialogue simulation**: On PersuasionForGood, the method yields more human-like multi-turn behavior and can approach the realism of a dedicated fine-tuned simulator.
- **Open-ended QA**: On CoverageQA-style questions with many valid answers, the method lowers KL divergence to a realistic reference distribution, improves coverage, and keeps precision near 1.0.
- **Synthetic data generation**: Using GPT-4.1 and Gemini-2.5-Flash to generate 1,000 synthetic competition-math questions, then Qwen3-32B to produce reasoning traces, yields downstream gains on MATH500, OlympiadBench, and Minerva Math after fine-tuning smaller Qwen models.
- **Limitations**: The method increases inference-time latency/token cost and works better on stronger models, since they are more capable of estimating probabilities and following structured-distribution prompts.

## Key Concepts

- [[Typicality Bias in Preference Data]]
- [[Mode Collapse in Aligned LLMs]]
- [[Cognitive Biases In Large Language Models]]

## Related Entities

- **[[Verbalized Sampling]]** — Training-free prompting method introduced by the paper to recover the broader response distribution learned during pretraining.
