---
title: "Textual Frequency Distillation (TFD)"
type: concept
created: 2026-04-21
last_verified: 2026-04-21
source_hash: "4ee068b261ce6b20df7021842f1cbae08b0ec5e4124c648f86d6f1e7e50fc275"
sources:
  - raw/2026-04-21-260402176v2pdf.md
quality_score: 72
concepts:
  - textual-frequency-distillation-tfd
related:
  - "[[Textual Frequency Law (TFL)]]"
  - "[[Adam’s Law: Textual Frequency Law on Large Language Models]]"
tier: hot
tags: [language-models, frequency-estimation, data-selection, model-adaptation]
---

# Textual Frequency Distillation (TFD)

## Overview

Textual Frequency Distillation (TFD) is a method for refining sentence-level frequency estimates by leveraging LLM-generated data. It addresses the challenge that frequency estimates from public corpora may not match the LLM's actual training distribution, especially for closed-source models.

## How It Works

TFD supplements corpus-based frequency estimation by generating new data via the target LLM. The process involves prompting the LLM to complete stories or extend sentences from the training set, thereby producing a 'distilled' dataset that reflects the LLM's generative tendencies. The frequency of a sentence in this distilled dataset (\(\mathcal{D}'\)) is then computed as:

\[
\mathcal{F}_2 = \mathrm{sfreq}(\mathbf{x}, \mathcal{D}')
\]

The final frequency estimate combines the original corpus-based frequency (\(\mathcal{F}_1\)) and the distilled frequency (\(\mathcal{F}_2\)) using a weighted sum:

\[
\mathcal{F}(x) = \alpha \mathcal{F}_1(x) + (1 + \zeta \mathbbm{1}(\mathcal{F}_1(x) = 0)) \beta \mathcal{F}_2(x)
\]

Here, \(\alpha\), \(\beta\), and \(\zeta\) are hyperparameters, and \(\mathbbm{1}(\mathcal{F}_1(x) = 0)\) is an indicator function that boosts the influence of \(\mathcal{F}_2\) when the original frequency is zero.

The rationale is that LLM-generated completions are more likely to reflect the model's internal distribution, thus providing a more accurate estimate of what the model 'knows' or finds familiar. This is particularly valuable when the public corpus is a poor proxy for the LLM's training data.

TFD is computationally expensive, as it requires generating large amounts of data from the LLM. However, it is optional; the framework remains effective with corpus-based frequency alone, but TFD can further enhance performance, especially for closed-source or domain-specific models.

In practice, TFD is used to adjust the frequency scores that guide paraphrase selection (in TFL) and training order (in CTFT).

## Key Properties

- **Model-Specific Frequency Estimation:** Incorporates LLM-generated data to better match the model's internal distribution.
- **Weighted Combination:** Final frequency is a weighted sum of corpus-based and distilled frequencies, with a boosting factor for unseen sentences.
- **Optional Enhancement:** TFD is not required for TFL to be effective, but it can yield further gains.

## Limitations

TFD is computationally intensive, as it requires generating and processing large datasets via the LLM. Its effectiveness depends on the quality and diversity of the LLM's completions. If the LLM is biased or limited in its generative capacity, TFD may reinforce those biases. Additionally, TFD may not be feasible for very large or proprietary models with limited API access.

## Example

Suppose a sentence's frequency in the public corpus is zero, but the LLM frequently generates similar completions. TFD assigns a higher frequency to this sentence, allowing it to be selected for prompting or fine-tuning despite its rarity in external data.

## Visual

No explicit diagram for TFD, but Figure 1 (middle/bottom) in the paper conceptually shows how frequency estimation is enhanced using LLM outputs. (Image description from text.)

## Relationship to Other Concepts

- **[[Textual Frequency Law (TFL)]]** — TFD refines the frequency estimates used in TFL.

## Practical Applications

TFD is useful for adapting frequency-based selection to closed-source or domain-specific LLMs, improving prompt engineering and fine-tuning in settings where the training distribution is unknown or mismatched.

## Sources

- [[Adam’s Law: Textual Frequency Law on Large Language Models]] — primary source for this concept
