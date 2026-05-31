---
title: "Deterministic Evidence Gates in Offline On-Call Triage"
type: synthesis
created: 2026-05-31
last_verified: 2026-05-31
source_hash: "synthesis-generated"
sources:
  - raw/2026-05-31-copilot-session-offline-triage-contracts-f348902c.md
concepts: [offline-contract-validation-on-call-triage-artifacts, signal-relevance-gate-infrastructure-triage]
related:
  - "[[Offline Contract Validation for On-Call Triage Artifacts]]"
  - "[[Signal Relevance Gate for Infrastructure Triage]]"
  - "[[Shared Contract Normalization for Dashboard APIs]]"
  - "[[LLM-Powered Noise Filtering]]"
tier: hot
tags: [on-call-triage, deterministic-gates, contract-validation, signal-relevance, offline-workflow]
---

# Deterministic Evidence Gates in Offline On-Call Triage

## Question

Which deterministic gates should an offline on-call triage assistant apply before it summarizes an incident or recommends action?

## Summary

The checkpoint argues for two different but complementary gates. [[Offline Contract Validation for On-Call Triage Artifacts]] decides whether the pipeline's intermediate objects are structurally trustworthy enough to persist, while [[Signal Relevance Gate for Infrastructure Triage]] decides whether the evidence inside those objects is causally relevant enough to shape the operator's incident narrative.

## Comparison

| Dimension | [[Offline Contract Validation for On-Call Triage Artifacts]] | [[Signal Relevance Gate for Infrastructure Triage]] |
|-----------|--------------------------------------------------------------|-----------------------------------------------------|
| Primary question | "Is this artifact valid enough to exist?" | "Is this signal relevant enough to matter?" |
| Main input | Incident envelopes, resource maps, evidence bundles, report contracts | Collected events, metrics, logs, resource clues, blind spots |
| Failure mode prevented | Partial artifacts, schema drift, invalid timestamps, unsafe path names | Stale CronJobs, old K8s events, weak correlations, noisy summaries |
| Typical output | Pass/fail validation plus only durable typed artifacts | Ranked buckets: contributing, possible, noise, stale, blind spots |
| Pipeline position | Before writing run directories and before downstream handoffs | After evidence collection, before markdown report generation |
| Human benefit | Trust that the workflow is operating on well-formed state | Trust that the report emphasizes causally plausible evidence |

## Analysis

These two gates solve different trust problems, and the checkpoint is valuable because it separates them cleanly. Contract validation protects the shape of the workflow. It ensures the assistant does not produce misleadingly durable artifacts from malformed fixtures, invalid RFC3339 timestamps, unsafe PagerDuty-derived paths, or ambiguous CloudStack identities. Without that gate, even a careful relevance classifier would still be operating on untrustworthy inputs.

The signal relevance gate protects interpretation. Even perfectly valid JSON can encode bad operational judgment if stale or weakly connected evidence is promoted into the incident story. The checkpoint's CronJob and timestamp regressions show why this matters: the system was not failing because the data was malformed; it was failing because temporally and causally weak evidence was being ranked too highly. That is a different class of bug, so it needs a different class of deterministic control.

Together, the gates create a layered discipline: first make the evidence pipeline well-typed, then make the evidence ranking defensible. This echoes [[Shared Contract Normalization for Dashboard APIs]], where correctness depends on one canonical shape before presentation, and it also parallels [[LLM-Powered Noise Filtering]], where semantic filtering happens before retrieval or summarization quality can improve. The difference is that on-call triage adds stronger safety stakes because bad filtering can alter operator actions during a live incident.

The broader systems lesson is that "use an LLM to summarize the incident" is too late to be the first quality boundary. Deterministic gates should narrow both the *form* and the *meaning* of evidence before any generative layer touches it. In practical terms, contract validation keeps the assistant from persisting garbage, and relevance gating keeps it from telling persuasive stories about garbage that happened to be well-formed.

## Key Insights

1. **Artifact correctness and signal correctness are separate problems** — [[Offline Contract Validation for On-Call Triage Artifacts]] solves the first, while [[Signal Relevance Gate for Infrastructure Triage]] solves the second.
2. **A trustworthy offline lane needs both gates before any live rollout** — the checkpoint's strategy is to prove schemas, timestamps, identities, and evidence ranking under fixtures before touching production systems.
3. **Deterministic pre-LLM filtering improves auditability** — the more meaning that is settled in explicit artifacts and buckets, the easier it is for a human to review the system's judgment path.

## Open Questions

- How should the relevance gate evolve once Prometheus, OpenSearch, Kubernetes, and CloudStack collectors move from fixtures to live read-only adapters?
- Which additional contract checks will be needed when the workflow expands from read-only diagnosis to explicitly approved CloudStack action prechecks?

## Sources

- [[Copilot Session Checkpoint: Offline Triage Contracts]]
- [[Shared Contract Normalization for Dashboard APIs]]
- [[LLM-Powered Noise Filtering]]
