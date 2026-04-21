---
title: "PLDM"
type: entity
created: 2026-04-20
last_verified: 2026-04-20
source_hash: "9c294439e600a5c5a2e741c8b7994207c1ce7af51793e70b9bb6b664cc642f8b"
sources:
  - raw/2026-04-20-260319312v2pdf.md
quality_score: 100
concepts:
  - pldm
related:
  - "[[LeWorldModel: Stable End-to-End Joint-Embedding Predictive Architecture from Pixels]]"
  - "[[LeWorldModel]]"
  - "[[Sketched-Isotropic-Gaussian Regularizer (SIGReg)]]"
  - "[[DINO-WM]]"
tier: hot
tags: [world-models, JEPA, VICReg, baseline, planning]
---

# PLDM

## Overview

PLDM is a baseline JEPA-based world model that learns representations end-to-end from pixel observations using a seven-term training objective derived from the VICReg criterion. It is compared against LeWorldModel in planning performance and efficiency.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Model |
| Created | Unknown |
| Creator | Unknown |
| URL | N/A |
| Status | Active |

## Relevance

PLDM serves as a benchmark for end-to-end JEPA-based world models, highlighting the advantages of LeWM's simpler, more stable training objective and efficient hyperparameter tuning.

## Associated Concepts

- **Joint Embedding Predictive Architecture (JEPA)** — PLDM is a JEPA variant.

## Related Entities

- **[[LeWorldModel]]** — PLDM is a baseline for comparison.
- **[[Sketched-Isotropic-Gaussian Regularizer (SIGReg)]]** — co-mentioned in source (Tool)
- **[[DINO-WM]]** — co-mentioned in source (Model)

## Sources

- [[LeWorldModel: Stable End-to-End Joint-Embedding Predictive Architecture from Pixels]] — where this entity was mentioned
