---
title: "Initialization Sensitivity in Sparse Neural Networks"
type: concept
created: 2026-04-10
last_verified: 2026-04-10
source_hash: "bd2046c48eb130a120593477f3fc9678dc18e4c8014a3f9bf5361937812db817"
sources:
  - raw/2026-04-10-180303635v5pdf.md
quality_score: 64
concepts:
  - initialization-sensitivity-in-sparse-neural-networks
related:
  - "[[Lottery Ticket Hypothesis]]"
  - "[[The Lottery Ticket Hypothesis: Finding Sparse, Trainable Neural Networks]]"
tier: hot
tags: [initialization, sparse-networks, generalization, optimization]
---

# Initialization Sensitivity in Sparse Neural Networks

## Overview

Initialization sensitivity refers to the critical dependence of sparse neural networks (winning tickets) on their original weight initialization. The Lottery Ticket Hypothesis demonstrates that only subnetworks retaining their original initialization can achieve high performance; random reinitialization leads to poor learning and generalization.

## How It Works

The process of identifying winning tickets involves pruning a trained network and resetting the surviving weights to their original initialization. Experiments show that these subnetworks, when retrained from their original initialization, achieve comparable or superior performance to the full network. However, if the surviving weights are randomly reinitialized, performance drops sharply, both in learning speed and test accuracy.

This sensitivity arises because the original initialization provides a fortuitous combination of weights that are uniquely suited to learning the task at hand. The structure alone (i.e., the subnetwork defined by the mask) is insufficient; the specific values of the initial weights are necessary for effective training. This finding challenges the assumption that network architecture alone determines trainability and highlights the importance of initialization in optimization and generalization.

Empirical results show that randomly reinitialized winning tickets learn slower and achieve lower test accuracy, even as training accuracy remains high. The gap between training and test accuracy widens, indicating poorer generalization. This pattern is consistent across fully-connected and convolutional architectures, reinforcing the centrality of initialization.

## Key Properties

- **Critical Dependence on Initialization:** Sparse subnetworks only succeed when trained from their original initialization; random reinitialization leads to poor performance.
- **Generalization:** Original initialization yields better generalization, with smaller gaps between training and test accuracy.
- **Architecture-Initialization Interaction:** The combination of subnetwork structure and initialization is necessary for success.

## Limitations

The sensitivity to initialization limits the transferability of winning tickets across tasks unless initialization is preserved. Random reinitialization negates the benefits of pruning, and the approach may not generalize to all architectures or tasks.

## Example

For a Conv-6 network on CIFAR10, a winning ticket at 15.1% of original size learns 2.5x faster and is 3.3 percentage points more accurate than the original network. If the surviving weights are randomly reinitialized, learning slows and test accuracy drops below the original network.

## Visual

Figures in the source (e.g., Figure 3 and Figure 5) compare learning curves for winning tickets and randomly reinitialized subnetworks, showing stark differences in learning speed and accuracy.

## Relationship to Other Concepts

- **[[Lottery Ticket Hypothesis]]** — Initialization sensitivity is a core component of the hypothesis.
- **SGD Optimization** — SGD interacts with initialization to determine which weights are trainable.

## Practical Applications

Understanding initialization sensitivity informs the design of initialization schemes and training protocols for sparse networks. It suggests that preserving initialization is critical for effective pruning and transfer learning.

## Sources

- [[The Lottery Ticket Hypothesis: Finding Sparse, Trainable Neural Networks]] — primary source for this concept
