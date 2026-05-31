---
title: Agentic-Triage
type: entity
created: 2026-05-31
last_verified: 2026-05-31
source_hash: ac2a0a3d9e56d2d9d201b266da04fa315379f6e205476203ef10320f7a42188e
sources:
  - raw/2026-05-31-copilot-session-offline-triage-contracts-f348902c.md
concepts: [offline-contract-validation-on-call-triage-artifacts, signal-relevance-gate-infrastructure-triage]
related:
  - "[[Durable Copilot Session Checkpoint]]"
  - "[[Copilot CLI]]"
  - "[[Offline Contract Validation for On-Call Triage Artifacts]]"
  - "[[Signal Relevance Gate for Infrastructure Triage]]"
tier: hot
tags: [on-call-triage, offline-workflow, contract-validation, cloudstack, kubernetes, pagerduty]
---

# Agentic-Triage

## Overview

Agentic-Triage is a private repository for a human-initiated on-call triage assistant aimed at a mixed CloudStack and Kubernetes platform. The checkpoint shows that the project deliberately narrowed its scope from an autonomous root-cause-analysis and response system into a read-mostly operator aid that starts from PagerDuty incidents, assembles evidence through deterministic scripts, and produces structured offline artifacts before any live collection or action path is trusted.

What makes the repository notable is not just that it stores scripts, but that it encodes an operational safety model. The repo's `bin/triage` entry point, contract schemas, fixture inputs, signal classifier, and conservative resource resolver all work together to make ambiguous infrastructure evidence explicit rather than silently guessed. In other words, Agentic-Triage treats correctness and auditability as product features, not cleanup work to add later.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool / Repository |
| Created | 2026-05-31 |
| Creator | jbl306 |
| URL | https://github.com/jbl306/agentic-triage |
| Status | Active |

## Purpose and Workflow

The checkpoint describes a staged operating model:

1. The on-call human receives a PagerDuty alert and initiates the workflow.
2. Fixture ingestion converts the alert into an `incident-envelope.json`.
3. Resource resolution maps evidence to the most defensible target, preferring ambiguity over false certainty.
4. Evidence is scored by a signal-relevance classifier before report generation.
5. The system emits a typed run directory and markdown triage report without touching live systems.

This matters because the target environment mixes Kubernetes, CloudStack, host diagnostics, metrics, and logs. The repository is designed so that every later live adapter must conform to the same artifact contracts already proven in offline mode.

## Safety Model

The checkpoint makes several hard constraints explicit. P1 and P2 behavior remain read-only. Even the future P3 action surface is limited to approved CloudStack VM lifecycle actions such as `live-migrate`, `start`, and `stop`, and those are still gated behind explicit safety checks. The source also notes that CloudStack guest VMs have no in-guest access, so diagnosis must stay outside-in through APIs, host context, metrics, and shipped logs.

The repository therefore emphasizes fail-closed validation, strict timestamp parsing, path-safe run directory creation, and blind-spot reporting whenever the evidence is incomplete. Those design choices are central to why the project can evolve toward production without normalizing unsafe operator assumptions.

## Current State

By the time of compaction, the repository already contained a working offline pipeline, new N1/N2 helpers (`validate_contract.py`, `pd_incident_context.py`, `resolve_resource.py`), new fixtures, and expanded regression coverage. Verification had passed with 21 tests plus `py_compile`; the only unfinished work was operational hygiene around staging explicit paths, committing, and pushing the latest branch state.

## Related Work

- **[[Offline Contract Validation for On-Call Triage Artifacts]]** — Describes the schema-first gate that keeps the repository's offline run artifacts trustworthy.
- **[[Signal Relevance Gate for Infrastructure Triage]]** — Explains the deterministic evidence filter that separates contributing signals from stale or irrelevant noise.
- **[[Durable Copilot Session Checkpoint]]** — The knowledge artifact category that preserved this repo state for wiki ingestion.
