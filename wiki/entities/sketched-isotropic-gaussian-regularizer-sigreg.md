---
title: "Sketched-Isotropic-Gaussian Regularizer (SIGReg)"
type: entity
created: 2026-04-20
last_verified: 2026-04-22
source_hash: "9c294439e600a5c5a2e741c8b7994207c1ce7af51793e70b9bb6b664cc642f8b"
sources:
  - raw/2026-04-20-260319312v2pdf.md
quality_score: 69
concepts:
  - sketched-isotropic-gaussian-regularizer-sigreg
related:
  - "[[LeWorldModel Architecture]]"
  - "[[LeWorldModel: Stable End-to-End Joint-Embedding Predictive Architecture from Pixels]]"
  - "[[LeWorldModel]]"
  - "[[PLDM]]"
  - "[[DINO-WM]]"
tier: hot
tags: [regularization, latent-space, SIGReg, Gaussian-distribution, JEPA, anti-collapse]
---

# Sketched-Isotropic-Gaussian Regularizer (SIGReg)

## Overview

SIGReg is a regularization method that enforces latent embeddings to follow an isotropic Gaussian distribution, preventing representation collapse in models like LeWorldModel. It operates by projecting embeddings onto multiple random directions and applying a normality test to each projection.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool |
| Created | Unknown |
| Creator | Unknown |
| URL | https://arxiv.org/abs/2604.02176 |
| Status | Active |

## Relevance

SIGReg provides a principled, efficient, and scalable solution to the representation collapse problem in JEPA-based world models, enabling robust end-to-end training without heuristic tricks or auxiliary supervision.

## Associated Concepts

- **Sketched-Isotropic-Gaussian Regularizer (SIGReg)** — This entity implements the concept.
- **[[LeWorldModel Architecture]]** — SIGReg is the regularization component in LeWM.

## Related Entities

- **[[LeWorldModel]]** — SIGReg is used in LeWorldModel for regularization.
- **[[PLDM]]** — co-mentioned in source (Model)
- **[[DINO-WM]]** — co-mentioned in source (Model)

## Sources

- [[LeWorldModel: Stable End-to-End Joint-Embedding Predictive Architecture from Pixels]] — where this entity was mentioned
