---
title: "Adam’s Law: Textual Frequency Law on Large Language Models"
type: source
created: 2026-04-21
last_verified: 2026-04-21
source_hash: "49f4807ade10bcd1f9d2ef67205cc33240d04aebc0d4d53e1a91fa012cb2f5a3"
sources:
  - raw/2026-04-21-260402176v2pdf.md
quality_score: 83
concepts:
  - textual-frequency-law
  - textual-frequency-distillation
  - curriculum-textual-frequency-training
  - textual-frequency-paired-dataset
related:
  - "[[Textual Frequency Paired Dataset]]"
  - "[[Textual Frequency Paired Dataset (TFPD)]]"
  - "[[FaceMind Corporation]]"
  - "[[The Chinese University of Hong Kong]]"
tier: hot
knowledge_state: executed
tags: [frequency-analysis, prompt-engineering, llm-training, dataset, curriculum-learning]
---

# Adam’s Law: Textual Frequency Law on Large Language Models

## Summary

This paper introduces Adam’s Law, which posits that high-frequency textual data should be preferred for both prompting and fine-tuning large language models (LLMs). The authors propose a three-part framework: Textual Frequency Law (TFL), Textual Frequency Distillation (TFD), and Curriculum Textual Frequency Training (CTFT). Experiments on a custom dataset demonstrate that models perform better with high-frequency paraphrases, and curriculum training based on frequency further improves results.

## Key Points

- Textual Frequency Law (TFL): Prefer high-frequency paraphrases for LLM prompting and fine-tuning.
- Textual Frequency Distillation (TFD): Enhance frequency estimation by generating story completions with LLMs.
- Curriculum Textual Frequency Training (CTFT): Fine-tune LLMs in order of increasing sentence-level frequency.

## Concepts Extracted

- **Textual Frequency Law** — Textual Frequency Law (TFL) is a principle stating that, when meaning is preserved, high-frequency textual data should be preferred for both prompting and fine-tuning large language models. This law is motivated by the observation that LLMs are more likely to have encountered high-frequency expressions during pre-training, making them easier for the models to understand and process.
- **Textual Frequency Distillation** — Textual Frequency Distillation (TFD) is a method for refining sentence-level frequency estimation by leveraging LLM-generated story completions. It compensates for the lack of access to actual LLM training data by using model outputs to adjust frequency calculations.
- **Curriculum Textual Frequency Training** — Curriculum Textual Frequency Training (CTFT) is a fine-tuning strategy for LLMs that arranges training data in order of increasing sentence-level frequency. This approach leverages frequency information to optimize learning, extending traditional curriculum learning methods.
- **[[Textual Frequency Paired Dataset]]** — The Textual Frequency Paired Dataset (TFPD) is a custom dataset created to evaluate the impact of textual frequency on LLM performance. It consists of pairs of paraphrases with identical meaning but varying sentence-level frequency, annotated by experts to ensure semantic equivalence.

## Entities Mentioned

- **[[Textual Frequency Paired Dataset (TFPD)]]** — TFPD is a custom dataset designed to evaluate the effect of textual frequency on LLM performance. It consists of pairs of paraphrases with identical meaning but varying sentence-level frequency, validated by expert annotators. The dataset covers math reasoning, machine translation, commonsense reasoning, and agentic tool calling.
- **[[FaceMind Corporation]]** — FaceMind Corporation is a research organization involved in the development and validation of Adam’s Law and the creation of the Textual Frequency Paired Dataset. It collaborates with academic institutions to advance LLM research.
- **[[The Chinese University of Hong Kong]]** — The Chinese University of Hong Kong is an academic institution collaborating on the research and development of Adam’s Law and the Textual Frequency Paired Dataset. It provides expertise in linguistics and machine learning.

## Notable Quotes

> "Frequent textual data should be preferred for LLMs for both prompting and fine-tuning." — Hongyuan Adam Lu et al.
> "Paraphrasing can lead to semantic drift, which is the reason why human annotation is necessary in this process." — Hongyuan Adam Lu et al.

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-21-260402176v2pdf.md` |
| Type | paper |
| Author | Hongyuan Adam Lu et al. |
| Date | Unknown |
| URL | https://arxiv.org/pdf/2604.02176 |
