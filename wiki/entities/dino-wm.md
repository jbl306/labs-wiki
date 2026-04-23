---
title: "DINO-WM"
type: entity
created: 2026-04-20
last_verified: 2026-04-22
source_hash: "9c294439e600a5c5a2e741c8b7994207c1ce7af51793e70b9bb6b664cc642f8b"
sources:
  - raw/2026-04-20-260319312v2pdf.md
quality_score: 75
concepts:
  - dino-wm
related:
  - "[[LeWorldModel: Stable End-to-End Joint-Embedding Predictive Architecture from Pixels]]"
  - "[[LeWorldModel]]"
  - "[[Sketched-Isotropic-Gaussian Regularizer (SIGReg)]]"
  - "[[PLDM]]"
tier: hot
tags: [world-models, JEPA, DINOv2, foundation-model, baseline, planning]
---

# DINO-WM

## Overview

DINO-WM is a foundation-model-based world model that uses a pre-trained DINOv2 vision encoder to mitigate representation collapse. It is compared against LeWorldModel and PLDM in planning performance and speed.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Model |
| Created | 2026 |
| Creator | Unknown |
| URL | https://arxiv.org/pdf/2603.19312 |
| Status | Active |

## Relevance

DINO-WM demonstrates the trade-offs between foundation-based and end-to-end world models, serving as a baseline for evaluating LeWM's efficiency and task-agnostic performance.

## Associated Concepts

- **Joint Embedding Predictive Architecture (JEPA)** — DINO-WM is a JEPA variant using pre-trained encoders.

## Related Entities

- **[[LeWorldModel]]** — DINO-WM is a baseline for comparison.
- **[[Sketched-Isotropic-Gaussian Regularizer (SIGReg)]]** — co-mentioned in source (Tool)
- **[[PLDM]]** — co-mentioned in source (Model)

## Sources

- [[LeWorldModel: Stable End-to-End Joint-Embedding Predictive Architecture from Pixels]] — where this entity was mentioned
