---
title: "Curriculum Textual Frequency Training (CTFT)"
type: concept
created: 2026-04-21
last_verified: 2026-04-21
source_hash: "4ee068b261ce6b20df7021842f1cbae08b0ec5e4124c648f86d6f1e7e50fc275"
sources:
  - raw/2026-04-21-260402176v2pdf.md
quality_score: 100
concepts:
  - curriculum-textual-frequency-training-ctft
related:
  - "[[Textual Frequency Law (TFL)]]"
  - "[[Textual Frequency Distillation (TFD)]]"
  - "[[Adam’s Law: Textual Frequency Law on Large Language Models]]"
tier: hot
tags: [curriculum-learning, fine-tuning, language-models, frequency-analysis]
---

# Curriculum Textual Frequency Training (CTFT)

## Overview

Curriculum Textual Frequency Training (CTFT) is a fine-tuning strategy for LLMs that orders training samples by increasing sentence-level frequency. The method is motivated by curriculum learning principles, aiming to expose the model to more diverse (low-frequency) expressions first, then gradually shift to more common (high-frequency) ones.

## How It Works

CTFT extends the TFL framework to the order in which training data is presented during fine-tuning. For a dataset \(\mathcal{T}\) of \(\mathbb{N}\) samples, each sample \(x_n\) is assigned a frequency score \(\mathcal{F}(x_n)\) (as computed by TFL/TFD). At each epoch, the training samples are sorted from lowest to highest frequency:

\[
\mathrm{sort}_{x_n \in \mathcal{T}}(\mathcal{F}(x_n))
\]

The intuition is that low-frequency samples are more diverse and challenging, so exposing the model to them first encourages broader generalization. As training progresses, the model sees increasingly frequent (and thus more familiar) samples, consolidating its ability to handle common expressions.

CTFT is empirically compared to other curriculum strategies, such as easy-to-hard (where 'easy' is defined by syntactic simplicity), and to random or reversed frequency orderings. Results show that CTFT yields superior fine-tuning outcomes, particularly in translation tasks, as measured by BLEU and chrF scores.

This approach is especially valuable in resource-constrained settings, where only a subset of paraphrases can be used for fine-tuning. By prioritizing diversity early and familiarity later, CTFT strikes a balance between coverage and model comfort.

## Key Properties

- **Frequency-Based Curriculum:** Orders training samples from low to high frequency, rather than by syntactic complexity or random order.
- **Improved Fine-Tuning Performance:** Outperforms traditional curriculum learning and random orderings in empirical benchmarks.
- **General Applicability:** Can be applied to any LLM fine-tuning scenario where sentence-level frequency can be estimated.

## Limitations

CTFT requires accurate frequency estimation for all training samples, which may be challenging for under-resourced languages or domains. The method assumes that diversity is best captured by low-frequency expressions, which may not hold in all tasks. Additionally, CTFT may not be optimal for tasks where rare or technical language is essential.

## Example

In fine-tuning a translation model, CTFT would first train on paraphrases with rare wordings, then gradually introduce more common paraphrases, leading to improved BLEU scores compared to random or reversed orderings.

## Visual

No explicit diagram for CTFT, but the training order is described in the text and illustrated in experimental tables.

## Relationship to Other Concepts

- **[[Textual Frequency Law (TFL)]]** — CTFT builds on TFL's frequency estimation.
- **[[Textual Frequency Distillation (TFD)]]** — CTFT can use TFD-refined frequencies for ordering.

## Practical Applications

CTFT is applicable in LLM fine-tuning for translation, reasoning, and any scenario where paraphrase diversity and model familiarity are both important. It is especially useful when training resources are limited.

## Sources

- [[Adam’s Law: Textual Frequency Law on Large Language Models]] — primary source for this concept
