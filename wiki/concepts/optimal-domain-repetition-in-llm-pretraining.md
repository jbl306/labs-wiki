---
title: "Optimal Domain Repetition in LLM Pretraining"
type: concept
created: 2026-08-17
last_verified: 2026-08-17
source_hash: "f1853c3a9b9d09eea4b11acb9151efaeac67164a0e046eaf93a5d4be19e074cc"
sources:
  - raw/2026-08-17-260814071-scaling-domain-data-repetition-in-llm-pretraining.md
quality_score: 90
concepts:
  - domain data repetition
  - tokens-per-parameter scaling
  - repetition-induced overfitting
related:
  - "[[Scaling Domain Data Repetition in LLM Pretraining]]"
  - "[[Transformer Architecture]]"
tier: hot
tags:
  - llm
  - pretraining
  - data-scaling
  - overfitting
---

# Optimal Domain Repetition in LLM Pretraining

## Overview

Optimal domain repetition is the repetition count that minimizes validation loss when scarce, high-quality domain data is reused during LLM pretraining. Repetition increases a domain's effective presence in the training mixture, but eventually trades knowledge acquisition for noise fitting and overfitting.

## How It Works

Let model size be N and let the total training-token budget be D = TPP × N, with TPP held constant. A domain contributes a unique-token fraction α and is repeated e times. The repeated domain therefore receives eαD token presentations, while the remaining budget is filled with non-repeated web data.

Increasing e gives the model more opportunities to learn domain signal and can counteract dilution when the overall training budget grows. However, repeated examples also make it easier to fit sample-specific noise. The useful repetition point is where the marginal reduction in knowledge-acquisition error is balanced by the increasing noise-fitting error.

The paper reports that domain characteristics dominate the choice of e. Optimal repetition is strongly negatively correlated with a domain's minimum validation loss: domains with lower loss generally support more repetition. At fixed TPP, the optimum rises mildly with model size and is nearly unchanged across the tested unique-data fractions.

## Trade-offs and Limitations

Repetition is useful when high-quality domain data is scarce, but it consumes training-token budget that could otherwise be spent on fresh data. Excessive repetition eventually degrades validation performance. The result also depends on the scaling convention: fixed-data-budget experiments can show the opposite model-size trend from fixed-TPP experiments.

Learning-rate schedules introduce another dependency. Earlier decay causes validation loss to deteriorate after fewer repetitions, while delayed decay or a constant learning rate permits more repetitions. The reported experiments repeat only one high-quality domain per run, so interactions among simultaneously repeated domains remain unresolved.

## Practical Procedure

1. Select a smaller proxy model and preserve the target model's tokens-per-parameter ratio.
2. Sweep repetition counts for the target domain while holding the total token budget and other training settings fixed.
3. Choose the repetition count near the proxy model's validation-loss minimum, treating it as a conservative estimate for the larger model.
4. Recheck the choice when the learning-rate schedule, domain, or scaling regime changes.

## Concrete Example

In the paper's experiments, Math generally reaches its validation-loss minimum after roughly 5–6 repetitions, Code after roughly 4–5, and Wikipedia and Medical after roughly 3–4. These counts are illustrative experimental findings rather than universal defaults; the optimum shifts with domain, model size, and training schedule.

## Sources

- [[Scaling Domain Data Repetition in LLM Pretraining]] — empirical results and theoretical explanation of repetition under fixed-TPP scaling.
