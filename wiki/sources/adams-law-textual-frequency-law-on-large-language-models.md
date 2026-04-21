---
title: "Adam’s Law: Textual Frequency Law on Large Language Models"
type: source
created: 2026-04-21
last_verified: 2026-04-21
source_hash: "4ee068b261ce6b20df7021842f1cbae08b0ec5e4124c648f86d6f1e7e50fc275"
sources:
  - raw/2026-04-21-260402176v2pdf.md
quality_score: 100
concepts:
  - textual-frequency-law-tfl
  - textual-frequency-distillation-tfd
  - curriculum-textual-frequency-training-ctft
related:
  - "[[Textual Frequency Law (TFL)]]"
  - "[[Textual Frequency Distillation (TFD)]]"
  - "[[Curriculum Textual Frequency Training (CTFT)]]"
  - "[[Textual Frequency Paired Dataset (TFPD)]]"
  - "[[FaceMind Corporation]]"
  - "[[The Chinese University of Hong Kong]]"
tier: hot
tags: [paraphrasing, language-models, fine-tuning, prompt-engineering, curriculum-learning, frequency-analysis]
---

# Adam’s Law: Textual Frequency Law on Large Language Models

## Summary

This paper introduces the Textual Frequency Law (TFL), which posits that, for both prompting and fine-tuning large language models (LLMs), higher-frequency textual data—when meaning is held constant—should be preferred over lower-frequency paraphrases. The authors propose a comprehensive framework that includes frequency estimation, frequency distillation, and curriculum training based on sentence-level frequency. Experiments across math reasoning, machine translation, and commonsense reasoning demonstrate that high-frequency inputs consistently yield better LLM performance.

## Key Points

- Textual Frequency Law (TFL) argues for prioritizing high-frequency paraphrases in LLM training and inference.
- Textual Frequency Distillation (TFD) refines frequency estimates by leveraging LLM-generated completions.
- Curriculum Textual Frequency Training (CTFT) further improves fine-tuning by ordering samples from low to high frequency.

## Concepts Extracted

- **[[Textual Frequency Law (TFL)]]** — The Textual Frequency Law (TFL) is a principle for large language models (LLMs) stating that, when multiple paraphrases of the same meaning are available, those with higher sentence-level frequency should be preferred for both prompting and fine-tuning. This law is grounded in the observation that LLMs are more likely to have encountered high-frequency expressions during pre-training, making them easier for the models to process and understand.
- **[[Textual Frequency Distillation (TFD)]]** — Textual Frequency Distillation (TFD) is a method for refining sentence-level frequency estimates by leveraging LLM-generated data. It addresses the challenge that frequency estimates from public corpora may not match the LLM's actual training distribution, especially for closed-source models.
- **[[Curriculum Textual Frequency Training (CTFT)]]** — Curriculum Textual Frequency Training (CTFT) is a fine-tuning strategy for LLMs that orders training samples by increasing sentence-level frequency. The method is motivated by curriculum learning principles, aiming to expose the model to more diverse (low-frequency) expressions first, then gradually shift to more common (high-frequency) ones.

## Entities Mentioned

- **[[Textual Frequency Paired Dataset (TFPD)]]** — The Textual Frequency Paired Dataset (TFPD) is a curated benchmark introduced in this paper to evaluate the impact of sentence-level frequency on LLM performance. It consists of pairs of paraphrases—one high-frequency, one low-frequency—for each original sentence, with human annotation ensuring semantic equivalence.
- **[[FaceMind Corporation]]** — FaceMind Corporation is one of the organizations affiliated with the authors of this paper. It is involved in research and development in the field of artificial intelligence and large language models.
- **[[The Chinese University of Hong Kong]]** — The Chinese University of Hong Kong is a major academic institution and a co-affiliation for several authors of this paper. It is recognized for its contributions to computational linguistics and artificial intelligence.

## Notable Quotes

> "We propose Textual Frequency Law (TFL), which suggests that high-frequency textual data should be preferred for LLMs when conducting prompting and fine-tuning, when the meaning of the data is kept the same." — Hongyuan Adam Lu et al.
> "Our results suggest that high-frequency paraphrases should be preferred under both prompting and fine-tuning scenarios." — Hongyuan Adam Lu et al.

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-21-260402176v2pdf.md` |
| Type | paper |
| Author | Hongyuan Adam Lu, Z.L., Victor Wei, Zefan Zhang, Zhao Hong, Qiqi Xiang, Bowen Cao, Wai Lam |
| Date | 2026-04-07 |
| URL | https://arxiv.org/pdf/2604.02176 |
