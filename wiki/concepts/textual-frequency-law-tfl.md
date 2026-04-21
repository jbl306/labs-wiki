---
title: "Textual Frequency Law (TFL)"
type: concept
created: 2026-04-21
last_verified: 2026-04-21
source_hash: "4ee068b261ce6b20df7021842f1cbae08b0ec5e4124c648f86d6f1e7e50fc275"
sources:
  - raw/2026-04-21-260402176v2pdf.md
quality_score: 100
concepts:
  - textual-frequency-law-tfl
related:
  - "[[Textual Frequency Distillation (TFD)]]"
  - "[[Curriculum Textual Frequency Training (CTFT)]]"
  - "[[Adam’s Law: Textual Frequency Law on Large Language Models]]"
tier: hot
tags: [language-models, prompt-engineering, fine-tuning, frequency-analysis, paraphrasing]
---

# Textual Frequency Law (TFL)

## Overview

The Textual Frequency Law (TFL) is a principle for large language models (LLMs) stating that, when multiple paraphrases of the same meaning are available, those with higher sentence-level frequency should be preferred for both prompting and fine-tuning. This law is grounded in the observation that LLMs are more likely to have encountered high-frequency expressions during pre-training, making them easier for the models to process and understand.

## How It Works

TFL operates on the premise that, for any set of paraphrases conveying the same meaning, the one with the highest sentence-level frequency (as estimated from a large corpus) will yield the best LLM performance. The law is formalized as:

\[
\mathrm{argmax}_{\mathbf{x}\in\mathcal{P}}(\mathrm{sfreq}(\mathbf{x},\mathcal{D})),
\]
where \(\mathcal{P}\) is the set of paraphrases, and \(\mathrm{sfreq}(\mathbf{x},\mathcal{D})\) is the sentence-level frequency of \(\mathbf{x}\) in corpus \(\mathcal{D}\).

Sentence-level frequency is estimated by aggregating word-level frequencies, typically using the geometric mean:

\[
\mathrm{sfreq}(\mathbf{x},\mathcal{D}) = \sqrt[\mathbb{K}]{\frac{1}{\prod_{k=1}^{\mathbb{K}}\mathrm{wfreq}(\mathbf{x}_{k},\mathcal{D})}}
\]
where \(\mathbf{x}_k\) is the k-th word in the sentence and \(\mathbb{K}\) is the sentence length.

For prompting, TFL recommends rephrasing inputs to their most frequent form before submitting to the LLM. For fine-tuning, it suggests using high-frequency paraphrases as training data, under the assumption that these are closer to the model's pre-training distribution.

The intuition is that LLMs, having been trained on massive web-scale corpora, are more familiar with high-frequency expressions, leading to more robust and accurate outputs. Conversely, low-frequency paraphrases may be underrepresented in training data, making them harder for the model to process and more prone to errors or hallucinations.

Empirical results in the paper show that, across tasks such as math reasoning, machine translation, and commonsense reasoning, using high-frequency paraphrases consistently improves accuracy and translation quality (as measured by BLEU, chrF, and COMET scores). Notably, the improvement is most pronounced on samples that the model originally failed to answer correctly with low-frequency paraphrases.

TFL also addresses the practical challenge that LLM training corpora are often closed-source. The law thus relies on frequency estimation from large, publicly available corpora, and is further enhanced by the Textual Frequency Distillation (TFD) method (see below).

## Key Properties

- **Sentence-Level Frequency Estimation:** Calculated as the geometric mean of word-level frequencies from a reference corpus; does not require access to LLM pre-training data.
- **Applicability:** Effective for both prompting (inference) and fine-tuning (training) scenarios.
- **Empirical Effectiveness:** Consistently improves LLM performance across multiple tasks and models, with negligible risk of performance degradation.

## Limitations

TFL assumes that paraphrases are truly semantically equivalent; semantic drift during paraphrasing can introduce errors, necessitating human annotation. The law's effectiveness depends on the accuracy of frequency estimation, which may be imperfect if the reference corpus diverges from the LLM's actual training data. Additionally, TFL may not generalize to tasks where rare or technical language is required.

## Example

Suppose you have two paraphrases for a translation task:

1. 'The boy quickly ran to the store.'
2. 'The lad hastily dashed to the emporium.'

By estimating sentence-level frequency using a large English corpus, TFL would select the first paraphrase (with more common words) for prompting or fine-tuning, leading to better LLM performance.

## Visual

A diagram (Figure 1, top) illustrates the process: given multiple paraphrases, the system selects the prompt with the highest estimated frequency for use in LLM tasks. (Image description from text.)

## Relationship to Other Concepts

- **[[Textual Frequency Distillation (TFD)]]** — TFD refines the frequency estimates used in TFL.
- **[[Curriculum Textual Frequency Training (CTFT)]]** — CTFT extends TFL to training order for fine-tuning.

## Practical Applications

TFL can be applied in prompt engineering for LLMs, data selection for fine-tuning, and automated paraphrase selection in NLP pipelines. It is especially useful in resource-constrained settings where only a subset of possible paraphrases can be used.

## Sources

- [[Adam’s Law: Textual Frequency Law on Large Language Models]] — primary source for this concept
