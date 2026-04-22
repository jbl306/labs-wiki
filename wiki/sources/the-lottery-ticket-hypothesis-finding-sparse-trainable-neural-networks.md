---
title: "The Lottery Ticket Hypothesis: Finding Sparse, Trainable Neural Networks"
type: source
created: 2026-04-21
last_verified: 2026-04-21
source_hash: "7dd02169701823b1b12a81026d3d1f736d244060a385045aebe0b8bcec1e1809"
sources:
  - raw/2026-04-10-180303635v5pdf.md
quality_score: 86
concepts:
  - lottery-ticket-hypothesis
  - iterative-pruning-technique
  - initialization-sensitivity-in-sparse-neural-networks
related:
  - "[[Lottery Ticket Hypothesis]]"
  - "[[Iterative Pruning Technique]]"
  - "[[Initialization Sensitivity in Sparse Neural Networks]]"
  - "[[Jonathan Frankle]]"
  - "[[Michael Carbin]]"
tier: hot
knowledge_state: executed
tags: [initialization, optimization, pruning, neural networks, sparsity, deep learning]
---

# The Lottery Ticket Hypothesis: Finding Sparse, Trainable Neural Networks

## Summary

This paper introduces the Lottery Ticket Hypothesis, which posits that dense, randomly-initialized neural networks contain sparse subnetworks ('winning tickets') that, when trained in isolation with their original initialization, can achieve comparable accuracy to the full network in similar training time. The authors present iterative pruning techniques to uncover these subnetworks and demonstrate their effectiveness across fully-connected and convolutional architectures. The findings challenge conventional wisdom about training pruned networks and offer new perspectives on network design, initialization, and theoretical understanding.

## Key Points

- Dense networks contain sparse subnetworks that can be trained effectively if properly initialized.
- Iterative pruning and resetting to original initialization uncovers 'winning tickets' that outperform or match the original network.
- Random reinitialization destroys the winning ticket's effectiveness, highlighting the importance of initialization.

## Concepts Extracted

- **[[Lottery Ticket Hypothesis]]** — The Lottery Ticket Hypothesis asserts that within a dense, randomly-initialized neural network, there exists a sparse subnetwork (a 'winning ticket') whose original initialization enables it to train in isolation to match the performance of the full network. This challenges the notion that pruned networks are inherently harder to train and opens new avenues for efficient network training and design.
- **[[Iterative Pruning Technique]]** — Iterative pruning is a process where a neural network is repeatedly trained, pruned, and reset to its original initialization, enabling the discovery of highly sparse and trainable subnetworks ('winning tickets'). This technique is central to validating the Lottery Ticket Hypothesis and optimizing network efficiency.
- **[[Initialization Sensitivity in Sparse Neural Networks]]** — Initialization sensitivity refers to the critical role of the original weight initialization in enabling sparse subnetworks (winning tickets) to train effectively. The Lottery Ticket Hypothesis demonstrates that proper initialization is essential for the success of pruned networks.

## Entities Mentioned

- **[[Jonathan Frankle]]** — Jonathan Frankle is a researcher at MIT CSAIL and co-author of the Lottery Ticket Hypothesis paper. His work focuses on neural network pruning, optimization, and theoretical understanding of deep learning. Frankle's contributions have significantly advanced the study of sparse, trainable neural networks.
- **[[Michael Carbin]]** — Michael Carbin is a researcher at MIT CSAIL and co-author of the Lottery Ticket Hypothesis paper. His expertise spans neural network optimization, pruning, and theoretical aspects of machine learning. Carbin's collaborative work with Frankle has shaped the understanding of sparse neural networks.

## Notable Quotes

> "A randomly-initialized, dense neural network contains a subnetwork that is initialized such that—when trained in isolation—it can match the test accuracy of the original network after training for at most the same number of iterations." — Jonathan Frankle & Michael Carbin
> "We designate these trainable subnetworks, f(x; m ⊙ θ₀), winning tickets, since those that we find have won the initialization lottery with a combination of weights and connections capable of learning." — Jonathan Frankle & Michael Carbin

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-10-180303635v5pdf.md` |
| Type | paper |
| Author | Jonathan Frankle & Michael Carbin |
| Date | Unknown |
| URL | https://arxiv.org/pdf/1803.03635 |
