---
title: "LeWorldModel"
type: entity
created: 2026-04-20
last_verified: 2026-04-20
source_hash: "9c294439e600a5c5a2e741c8b7994207c1ce7af51793e70b9bb6b664cc642f8b"
sources:
  - raw/2026-04-20-260319312v2pdf.md
quality_score: 100
concepts:
  - leworldmodel
related:
  - "[[LeWorldModel Architecture]]"
  - "[[Sketched-Isotropic-Gaussian Regularizer (SIGReg)]]"
  - "[[Latent Planning with LeWorldModel]]"
  - "[[LeWorldModel: Stable End-to-End Joint-Embedding Predictive Architecture from Pixels]]"
  - "[[PLDM]]"
  - "[[DINO-WM]]"
tier: hot
tags: [world-models, JEPA, latent-space, SIGReg, planning, reinforcement-learning]
---

# LeWorldModel

## Overview

LeWorldModel (LeWM) is a stable, end-to-end Joint Embedding Predictive Architecture for learning world models directly from raw pixel observations. It consists of an encoder and predictor, trained jointly with a two-term objective, enabling efficient planning and robust representation learning in a compact latent space.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Model |
| Created | 2026 |
| Creator | Lucas Maes, Quentin Le Lidec, Damien Scieur, Yann LeCun, Randall Balestriero |
| URL | N/A |
| Status | Active |

## Relevance

LeWM advances the state-of-the-art in world model learning by providing a principled, stable, and efficient architecture that eliminates the need for complex heuristics or multi-term objectives. It achieves competitive performance and significant planning speedups across diverse control tasks, with its latent space encoding meaningful physical structure.

## Associated Concepts

- **[[LeWorldModel Architecture]]** — LeWM is the implementation of this architecture.
- **[[Sketched-Isotropic-Gaussian Regularizer (SIGReg)]]** — SIGReg is the regularization method used in LeWM.
- **[[Latent Planning with LeWorldModel]]** — LeWM enables efficient latent planning.

## Related Entities

- **[[PLDM]]** — Baseline JEPA model for comparison.
- **[[DINO-WM]]** — Foundation-model-based world model baseline.
- **[[Sketched-Isotropic-Gaussian Regularizer (SIGReg)]]** — co-mentioned in source (Tool)

## Sources

- [[LeWorldModel: Stable End-to-End Joint-Embedding Predictive Architecture from Pixels]] — where this entity was mentioned
