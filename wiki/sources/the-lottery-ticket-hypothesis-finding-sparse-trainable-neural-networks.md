---
title: "The Lottery Ticket Hypothesis: Finding Sparse, Trainable Neural Networks"
type: source
created: 2026-04-10
last_verified: 2026-04-10
source_hash: "bd2046c48eb130a120593477f3fc9678dc18e4c8014a3f9bf5361937812db817"
sources:
  - raw/2026-04-10-180303635v5pdf.md
quality_score: 100
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
tags: [training-efficiency, sparsity, initialization, neural-networks, pruning, generalization]
---

# The Lottery Ticket Hypothesis: Finding Sparse, Trainable Neural Networks

## Summary

This paper introduces the Lottery Ticket Hypothesis, which posits that dense, randomly-initialized neural networks contain smaller subnetworks ('winning tickets') that, when trained in isolation from their original initialization, can match the performance of the full network. The authors present iterative pruning techniques to identify these winning tickets and demonstrate their existence across fully-connected and convolutional architectures, including VGG and ResNet variants. The paper explores the implications for training efficiency, network design, and theoretical understanding of neural networks.

## Key Points

- Pruning uncovers sparse subnetworks that can be trained to match or exceed the original network's accuracy.
- Initialization is critical: winning tickets only succeed when trained from their original initial weights.
- Iterative pruning is more effective than one-shot pruning in finding smaller, high-performing winning tickets.

## Concepts Extracted

- **[[Lottery Ticket Hypothesis]]** — The Lottery Ticket Hypothesis asserts that within a dense, randomly-initialized neural network, there exist smaller subnetworks—called 'winning tickets'—that, when trained from their original initialization, can achieve comparable performance to the full network. This challenges the prevailing notion that pruned networks are harder to train from scratch and suggests that certain initializations are uniquely conducive to effective learning.
- **[[Iterative Pruning Technique]]** — Iterative pruning is a method for identifying winning tickets in neural networks by repeatedly training, pruning, and resetting the network over multiple rounds. This approach uncovers smaller, highly trainable subnetworks compared to one-shot pruning and is central to validating the Lottery Ticket Hypothesis.
- **[[Initialization Sensitivity in Sparse Neural Networks]]** — Initialization sensitivity refers to the critical dependence of sparse neural networks (winning tickets) on their original weight initialization. The Lottery Ticket Hypothesis demonstrates that only subnetworks retaining their original initialization can achieve high performance; random reinitialization leads to poor learning and generalization.

## Entities Mentioned

- **[[Jonathan Frankle]]** — Jonathan Frankle is a researcher at MIT CSAIL and co-author of the Lottery Ticket Hypothesis paper. His work focuses on neural network pruning, sparse architectures, and theoretical understanding of deep learning.
- **[[Michael Carbin]]** — Michael Carbin is a faculty member at MIT CSAIL and co-author of the Lottery Ticket Hypothesis paper. His research spans programming languages, systems, and machine learning.

## Notable Quotes

> "Dense, randomly-initialized, feed-forward networks contain subnetworks (winning tickets) that—when trained in isolation—reach test accuracy comparable to the original network in a similar number of iterations." — Jonathan Frankle & Michael Carbin
> "Initialization is crucial for the efficacy of a winning ticket." — Jonathan Frankle & Michael Carbin

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-10-180303635v5pdf.md` |
| Type | paper |
| Author | Jonathan Frankle & Michael Carbin |
| Date | 2019-04-07 |
| URL | https://arxiv.org/pdf/1803.03635 |
