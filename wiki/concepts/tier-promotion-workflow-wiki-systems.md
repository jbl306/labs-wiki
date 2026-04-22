---
title: "Tier Promotion Workflow in Wiki Systems"
type: concept
created: 2026-04-22
last_verified: 2026-04-22
source_hash: "09970c2d6bf98521e8acf64359beba6cb07e02f1015bc2504f2dd8846bbc0c93"
sources:
  - raw/2026-04-22-copilot-session-labs-wiki-full-review-report-b585f2e1.md
quality_score: 59
concepts:
  - tier-promotion-workflow-wiki-systems
related:
  - "[[Quality Evaluation of Auto-Ingested Wiki Content]]"
  - "[[Durable Copilot Session Checkpoint Promotion]]"
  - "[[Copilot Session Checkpoint: labs-wiki full review report]]"
tier: hot
tags: [workflow, quality-control, wiki-management, tiering]
---

# Tier Promotion Workflow in Wiki Systems

## Overview

Tier promotion is a structured workflow for advancing wiki pages through quality and maturity levels, such as 'hot', 'established', and 'core'. It enforces editorial standards, ensures content validation, and guides curation efforts in persistent knowledge bases.

## How It Works

The tier promotion workflow is defined in `docs/memory-model.md` for labs-wiki, specifying rules for moving pages from 'hot' (newly ingested) to 'established' (validated) and 'core' (canonical, high-quality). However, the review report finds that these rules are not enforced: no cron jobs or agent workflows run the promotion logic, resulting in 602 pages stuck in 'hot', only 2 in 'established', and none in 'core'.

A proper tier promotion system would:
- **Define Promotion Criteria**: Each tier has explicit requirements (e.g., editorial review, synthesis coverage, quality score thresholds).
- **Automate Promotion Checks**: Scheduled jobs or agent workflows periodically evaluate pages against criteria, promoting those that qualify.
- **Editorial Oversight**: Human curators can override or expedite promotion for critical pages.
- **Feedback Loops**: Pages failing promotion are flagged for improvement, and their status is visible in dashboards.

The workflow is typically implemented as a combination of scripts (e.g., cron jobs), agentic review processes, and UI features that surface tier status and allow for manual intervention. Trade-offs include balancing automation with editorial control, and ensuring that promotion criteria are neither too lax (allowing low-quality pages to advance) nor too strict (stalling progress).

The labs-wiki report recommends building and deploying tier-promotion cron jobs (R7), integrating them with the editorial scoring and graph tracker artifacts to drive systematic improvement.

## Key Properties

- **Explicit Tier Criteria:** Each tier ('hot', 'established', 'core') has clear requirements for promotion.
- **Automated Promotion:** Scheduled jobs or agent workflows evaluate and promote pages.
- **Editorial Oversight:** Curators can manually promote, demote, or annotate pages.
- **Feedback and Visibility:** Tier status is surfaced in dashboards and informs curation priorities.

## Limitations

Without enforcement, tier promotion is ineffective, leading to stagnation and lack of differentiation. Overly rigid criteria can bottleneck content flow, while insufficient oversight can degrade quality. Requires ongoing maintenance and adjustment as wiki evolves.

## Example

A page on 'AdaBoost' is initially ingested as 'hot'. After editorial review and synthesis coverage, a cron job promotes it to 'established'. Once further validated and referenced in synthesis pages, it is promoted to 'core', becoming a canonical reference.

## Relationship to Other Concepts

- **[[Quality Evaluation of Auto-Ingested Wiki Content]]** — Tier promotion depends on quality evaluation as a gating mechanism.
- **[[Durable Copilot Session Checkpoint Promotion]]** — Promotion of session checkpoints parallels tier advancement in wiki pages.

## Practical Applications

Used in persistent knowledge bases, technical documentation, and collaborative wikis to ensure content maturity, guide curation, and maintain editorial standards. Supports workflows for onboarding, validation, and canonicalization of knowledge artifacts.

## Sources

- [[Copilot Session Checkpoint: labs-wiki full review report]] — primary source for this concept
