---
title: "Textual Frequency Paired Dataset"
type: concept
created: 2026-04-21
last_verified: 2026-04-21
source_hash: "49f4807ade10bcd1f9d2ef67205cc33240d04aebc0d4d53e1a91fa012cb2f5a3"
sources:
  - raw/2026-04-21-260402176v2pdf.md
quality_score: 100
concepts:
  - textual-frequency-paired-dataset
related:
  - "[[Adam’s Law: Textual Frequency Law on Large Language Models]]"
tier: hot
tags: [dataset, llm-evaluation, frequency-analysis]
---

# Textual Frequency Paired Dataset

## Overview

The Textual Frequency Paired Dataset (TFPD) is a custom dataset created to evaluate the impact of textual frequency on LLM performance. It consists of pairs of paraphrases with identical meaning but varying sentence-level frequency, annotated by experts to ensure semantic equivalence.

## How It Works

TFPD is constructed by rephrasing sentences from existing datasets (GSM8K, FLORES-200, CommonsenseQA) using GPT-4o-mini. Each original sentence is transformed into multiple paraphrases, both common and complex. Three human annotators with English linguistics backgrounds validate that the paraphrases preserve the original meaning.

The dataset includes high-frequency and low-frequency partitions, with statistics reported for sentence count, average length, and maximum/minimum length. Only samples unanimously judged as semantically equivalent are retained. TFPD is used for both prompting and fine-tuning experiments, enabling rigorous comparison of LLM performance across frequency partitions.

TFPD fills a gap in existing resources, providing a controlled benchmark for studying textual frequency effects. It is released for public use and reproducibility.

## Key Properties

- **Semantic Equivalence:** Pairs of paraphrases are validated by human annotators to ensure identical meaning.
- **Frequency Partitioning:** Each pair includes one high-frequency and one low-frequency paraphrase.
- **Diverse Tasks:** Covers math reasoning, machine translation, commonsense reasoning, and tool calling.

## Limitations

TFPD is limited by the accuracy of paraphrase generation and human annotation. Some semantic drift may occur, and the dataset may not cover all linguistic phenomena relevant to LLMs.

## Example

A math reasoning question is rephrased into a common and a complex version. Both are annotated as semantically equivalent, and their frequencies are calculated for use in prompting and fine-tuning experiments.

## Visual

Table 1 presents statistics for TFPD, showing balanced sentence counts and lengths across high- and low-frequency partitions. Figure 2 and 3 illustrate performance differences between partitions.

## Relationship to Other Concepts

- **Textual Frequency Law** — TFPD is used to validate TFL experimentally.
- **Curriculum Textual Frequency Training** — TFPD provides data for CTFT experiments.

## Practical Applications

TFPD is a benchmark for evaluating LLMs’ sensitivity to textual frequency, supporting research in prompt engineering, data selection, and curriculum learning.

## Sources

- [[Adam’s Law: Textual Frequency Law on Large Language Models]] — primary source for this concept
