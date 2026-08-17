---
title: Scaling Domain Data Repetition in LLM Pretraining
type: source
created: 2026-08-17
last_verified: 2026-08-17
source_hash: f1853c3a9b9d09eea4b11acb9151efaeac67164a0e046eaf93a5d4be19e074cc
sources:
- raw/2026-08-17-260814071-scaling-domain-data-repetition-in-llm-pretraining.md
- raw/2026-08-17-260814071v1pdf.md
quality_score: 90
concepts:
- domain data repetition
- tokens-per-parameter scaling
- repetition-induced overfitting
related:
- '[[Optimal Domain Repetition in LLM Pretraining]]'
tier: hot
tags:
- llm
- pretraining
- data-scaling
- overfitting
---

# Scaling Domain Data Repetition in LLM Pretraining

## Summary

This paper studies how repeatedly sampling scarce, high-quality domain data affects LLM pretraining when the total token budget scales with model size at a fixed tokens-per-parameter ratio. It finds that the optimal repetition count depends strongly on domain validation loss, increases mildly with model size under fixed TPP, and is largely insensitive to the tested fraction of unique domain data.

## Key Points

- Repetition counteracts dilution of scarce domain data as total training-token budgets grow.
- At fixed TPP, optimal repetition increases mildly with model size; this differs from fixed-data-budget scaling, where larger models overfit repeated data earlier.
- Domains with lower minimum validation loss generally tolerate and benefit from more repetitions.
- Optimal repetition is nearly insensitive to the unique high-quality data fraction across the tested range.
- Repeated optimization reduces knowledge-acquisition error but increases noise-fitting error; the optimum occurs where the marginal noise-fitting cost overtakes the acquisition benefit.
- A smaller proxy model trained at the same TPP can provide a conservative repetition estimate for a larger target model.
- Learning-rate schedules affect tolerance: earlier decay causes degradation after fewer repetitions, while delayed or absent decay permits more repetitions.
- The experiments cover Code, Math, Wikipedia, and Medical domains; Math supports the most repetition, while Medical supports the least.

## Concepts Extracted

- **[[Optimal Domain Repetition in LLM Pretraining]]** — Choosing repetition counts for scarce high-quality domains under practical LLM scaling.

## Entities Mentioned

- Jingwei Li, Xinran Gu, Rui Dai, Xintong Hao, Chengyin Xu, Yan Wu, Shuran Zheng, and Jingzhao Zhang — authors.
- Tsinghua University — affiliation for several authors.
- ByteDance Seed — affiliation and workplace noted for the research.

## Source Details

| Field | Value |
|---|---|
| Original | `raw/2026-08-17-260814071-scaling-domain-data-repetition-in-llm-pretraining.md` |
| Type | Research paper |
| Publication date | 2026-08-17 |
| URL | https://arxiv.org/abs/2608.14071 |
| Model-scaling regime | Fixed tokens-per-parameter ratio |
| Domains tested | Code, Math, Wikipedia, Medical |

## Limitations and Future Work

Each training run repeats only one high-quality domain. The paper identifies studying simultaneous repetition of multiple domains and deriving a quantitative large-model scaling rule from small-model results as future work.
