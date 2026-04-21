---
title: "LeWorldModel: Stable End-to-End Joint-Embedding Predictive Architecture from Pixels"
type: source
created: 2026-04-21
last_verified: 2026-04-21
source_hash: "dbe880f9912188cd26d152ae99593297fed0011190420927082c774d79faa155"
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
knowledge_state: executed
tags: [latent-dynamics, JEPA, planning, SIGReg, end-to-end-learning, regularization, world-models]
---

# LeWorldModel: Stable End-to-End Joint-Embedding Predictive Architecture from Pixels

## Summary

This paper introduces LeWorldModel (LeWM), a novel Joint Embedding Predictive Architecture (JEPA) for learning world models directly from raw pixels in a stable, end-to-end manner. LeWM uses only two loss terms—a next-embedding prediction loss and a Sketched-Isotropic-Gaussian Regularizer (SIGReg)—to avoid representation collapse, reducing hyperparameter complexity and enabling efficient training on a single GPU. The model demonstrates competitive performance across diverse 2D and 3D control tasks and encodes meaningful physical structure in its latent space, with robust detection of physically implausible events.

## Key Points

- LeWM is the first JEPA trained stably end-to-end from raw pixels with only two loss terms.
- It eliminates the need for pre-trained encoders, auxiliary supervision, or heuristic tricks, reducing hyperparameters from six to one.
- LeWM achieves strong control performance and efficient planning speeds, with provable anti-collapse guarantees via SIGReg.

## Concepts Extracted

- **[[LeWorldModel Architecture]]** — LeWorldModel (LeWM) is a Joint Embedding Predictive Architecture (JEPA) designed for stable, end-to-end learning of world models directly from raw pixel observations. It consists of an encoder and a predictor, both optimized jointly with a streamlined two-term loss, enabling robust representation learning without pre-trained encoders or heuristic stabilization.
- **[[Sketched-Isotropic-Gaussian Regularizer (SIGReg)]]** — SIGReg is a regularization technique that enforces Gaussian-distributed latent embeddings in high-dimensional spaces, preventing representation collapse in JEPA models. It operates by projecting embeddings onto multiple random directions and optimizing normality tests on these projections.
- **[[Latent Planning with LeWorldModel]]** — Latent planning in LeWorldModel refers to optimizing action sequences in the learned latent space, enabling efficient trajectory planning and control without explicit reward signals or pixel-space simulation. This approach leverages the compact, predictable latent dynamics modeled by LeWM.

## Entities Mentioned

- **[[LeWorldModel]]** — LeWorldModel (LeWM) is a Joint Embedding Predictive Architecture for learning world models directly from raw pixels in a stable, end-to-end manner. It consists of an encoder (Vision Transformer) and a predictor (transformer network), both trained jointly with a two-term loss that includes a prediction objective and SIGReg regularization.
- **[[Sketched-Isotropic-Gaussian Regularizer (SIGReg)]]** — SIGReg is a regularization method that enforces Gaussian-distributed latent embeddings, preventing representation collapse in JEPA models. It operates by projecting embeddings onto random directions and optimizing normality tests on these projections.
- **[[PLDM]]** — PLDM is a JEPA-based world model baseline that learns representations end-to-end using VICReg with additional regularization terms. It requires multiple hyperparameters and is prone to training instabilities.
- **[[DINO-WM]]** — DINO-WM is a foundation-model-based world model that avoids representation collapse by freezing a pre-trained vision encoder. It does not support end-to-end learning and is bounded by the expressivity of the pre-trained encoder.

## Notable Quotes

> "LeWM plans up to 48× faster than foundation-model-based world models while remaining competitive across diverse 2D and 3D control tasks." — Abstract
> "LeWM addresses the limitations of each category: it is end-to-end, task-agnostic, pixel-based, reconstruction- and reward-free, and requires only a single hyperparameter with provable anti-collapse guarantees." — Section 1 Introduction

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-20-260319312v2pdf.md` |
| Type | paper |
| Author | Lucas Maes*, Quentin Le Lidec*, Damien Scieur, Yann LeCun, Randall Balestriero |
| Date | Unknown |
| URL | https://arxiv.org/pdf/2603.19312 |
