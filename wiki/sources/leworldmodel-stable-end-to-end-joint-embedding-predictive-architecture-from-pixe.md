---
title: "LeWorldModel: Stable End-to-End Joint-Embedding Predictive Architecture from Pixels"
type: source
created: 2026-04-20
last_verified: 2026-04-20
source_hash: "9c294439e600a5c5a2e741c8b7994207c1ce7af51793e70b9bb6b664cc642f8b"
sources:
  - raw/2026-04-20-260319312v2pdf.md
quality_score: 100
concepts:
  - leworldmodel-architecture
  - sketched-isotropic-gaussian-regularizer-sigreg
  - latent-planning-leworldmodel
related:
  - "[[LeWorldModel Architecture]]"
  - "[[Sketched-Isotropic-Gaussian Regularizer (SIGReg)]]"
  - "[[Latent Planning with LeWorldModel]]"
  - "[[LeWorldModel]]"
  - "[[PLDM]]"
  - "[[DINO-WM]]"
tier: hot
tags: [JEPA, regularization, world-models, planning, latent-space, reinforcement-learning, SIGReg]
---

# LeWorldModel: Stable End-to-End Joint-Embedding Predictive Architecture from Pixels

## Summary

LeWorldModel (LeWM) introduces a robust, end-to-end Joint Embedding Predictive Architecture (JEPA) for learning world models directly from raw pixels. It achieves stable training using only two loss terms—a next-embedding prediction loss and a Sketched-Isotropic-Gaussian Regularizer (SIGReg)—eliminating the need for complex heuristics or multi-term objectives. LeWM demonstrates competitive performance and significant planning speedups across diverse 2D and 3D control tasks, while its latent space encodes meaningful physical structure and reliably detects physically implausible events.

## Key Points

- LeWM is the first JEPA to train stably end-to-end from pixels using only a prediction loss and SIGReg regularization.
- It reduces hyperparameter complexity, requiring only one effective hyperparameter for tuning.
- LeWM outperforms or matches state-of-the-art baselines in planning performance and speed, and its latent space captures physical structure.

## Concepts Extracted

- **[[LeWorldModel Architecture]]** — LeWorldModel (LeWM) is a stable, end-to-end Joint Embedding Predictive Architecture (JEPA) for learning world models directly from raw pixel observations. It consists of an encoder and a predictor, trained jointly with a simple two-term objective, enabling efficient and robust learning of environment dynamics in a compact latent space.
- **[[Sketched-Isotropic-Gaussian Regularizer (SIGReg)]]** — SIGReg is a regularization technique that enforces latent embeddings to follow an isotropic Gaussian distribution, preventing representation collapse in Joint Embedding Predictive Architectures (JEPAs) like LeWorldModel. It operates by projecting embeddings onto multiple random directions and applying a univariate normality test to each projection.
- **[[Latent Planning with LeWorldModel]]** — Latent planning in LeWorldModel leverages the learned latent dynamics to optimize action sequences in the latent space, enabling efficient trajectory optimization for control tasks. Planning is performed via Model Predictive Control (MPC) and the Cross-Entropy Method (CEM), using the world model to forecast future states and minimize a latent goal-matching objective.

## Entities Mentioned

- **[[LeWorldModel]]** — LeWorldModel (LeWM) is a stable, end-to-end Joint Embedding Predictive Architecture for learning world models directly from raw pixel observations. It consists of an encoder and predictor, trained jointly with a two-term objective, enabling efficient planning and robust representation learning in a compact latent space.
- **[[Sketched-Isotropic-Gaussian Regularizer (SIGReg)]]** — SIGReg is a regularization method that enforces latent embeddings to follow an isotropic Gaussian distribution, preventing representation collapse in models like LeWorldModel. It operates by projecting embeddings onto multiple random directions and applying a normality test to each projection.
- **[[PLDM]]** — PLDM is a baseline JEPA-based world model that learns representations end-to-end from pixel observations using a seven-term training objective derived from the VICReg criterion. It is compared against LeWorldModel in planning performance and efficiency.
- **[[DINO-WM]]** — DINO-WM is a foundation-model-based world model that uses a pre-trained DINOv2 vision encoder to mitigate representation collapse. It is compared against LeWorldModel and PLDM in planning performance and speed.

## Notable Quotes

> "LeWM achieves strong control performance across diverse 2D and 3D tasks with a compact 15M-parameter model, surpassing existing end-to-end JEPA-based approach while remaining competitive with foundation-model-based world models at substantially lower cost, enabling planning up to 48× faster." — LeWorldModel paper
> "LeWM addresses the limitations of each category: it is end-to-end, task-agnostic, pixel-based, reconstruction- and reward-free, and requires only a single hyperparameter with provable anti-collapse guarantees." — LeWorldModel paper

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-20-260319312v2pdf.md` |
| Type | paper |
| Author | Lucas Maes, Quentin Le Lidec, Damien Scieur, Yann LeCun, Randall Balestriero |
| Date | 2026-03-24 |
| URL | https://arxiv.org/pdf/2603.19312 |
