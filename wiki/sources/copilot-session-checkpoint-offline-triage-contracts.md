---
title: "Copilot Session Checkpoint: Offline Triage Contracts"
type: source
created: '2026-05-31'
last_verified: '2026-05-31'
source_hash: ac2a0a3d9e56d2d9d201b266da04fa315379f6e205476203ef10320f7a42188e
sources:
  - raw/2026-05-31-copilot-session-offline-triage-contracts-f348902c.md
concepts:
  - offline-contract-validation-on-call-triage-artifacts
  - signal-relevance-gate-infrastructure-triage
related:
  - "[[Agentic-Triage]]"
  - "[[Durable Copilot Session Checkpoint]]"
  - "[[Copilot CLI]]"
tags: [copilot-session, checkpoint, on-call-triage, offline-workflow, contract-validation, signal-relevance, cloudstack, pagerduty]
tier: hot
checkpoint_class: durable-architecture
retention_mode: retain
knowledge_state: ingested
ingest_method: copilot-cli-gpt-5.4
quality_score: 76
---

# Copilot Session Checkpoint: Offline Triage Contracts

## Summary

This checkpoint captures the architectural contract for `agentic-triage`: a human-initiated, read-mostly on-call assistant that must prove itself in deterministic offline mode before any live integration is allowed. Its durable lesson is that trustworthy triage depends on typed artifacts, strict validation, conservative resource resolution, and an explicit signal-relevance gate that filters stale or misleading evidence before summarization.

The source also records the product pivot away from autonomous RCA toward operator-invoked workflows, plus the concrete file-level implementation of fixture ingestion, schema validation, CloudStack-aware resource resolution, and regression-tested safety fixes that were still awaiting final commit and push at compaction time.

## Key Points

- The project explicitly moved away from autonomous incident response and toward a **human-initiated, read-mostly on-call workflow** where the operator starts from a PagerDuty alert and the assistant helps collect, filter, and summarize evidence.
- The offline architecture is centered on `bin/triage`, which accepts `--input` fixtures and `--output-dir`, then writes a deterministic run directory containing `incident-envelope.json`, `resource-map.json`, `evidence-bundle.json`, `signal-relevance.json`, `triage-report.md`, and `audit-log.jsonl`.
- The assistant is intentionally **non-live** at this stage: the checkpoint says the offline workflow must not contact production systems, and all P1/P2 work remains read-only even when live integrations eventually arrive.
- `scripts/validate_contract.py` became the core contract gate. It validates a dependency-free subset of JSON Schema, supports `required`, `type`, `properties`, `items`, `enum`, min/max, local `$defs`, `additionalProperties: false`, and now **fails closed** for unsupported schema types.
- Timestamp handling was tightened to strict **RFC3339 date-time**: values must include a `T` separator and timezone (`Z` or explicit offset). Date-only, timezone-less, or space-separated timestamps are rejected before artifacts are written.
- The resource resolver is deliberately conservative for CloudStack incidents. Canonical VM mapping requires **both** `cloudstack_vm_id` and `project_id`; any partial CloudStack clue remains ambiguous and adds a blind-spot warning instead of silently falling back to a host mapping.
- The checkpoint introduces a **Signal Relevance Gate** between evidence collection and report generation so stale Kubernetes events, dead CronJobs, and other background noise do not get elevated into false platform explanations.
- The signal classifier divides evidence into `contributing_signals`, `possibly_related_signals`, `background_noise`, `stale_historical`, and `blind_spots`, with reviewer-driven fixes ensuring declared correlation IDs alone cannot promote stale unrelated CronJobs.
- Event freshness logic was hardened so relevance prefers `last_seen` / `lastTimestamp` over an old first `timestamp`, preventing repeated Kubernetes events from being classified using stale initial times.
- The repo state at compaction was concrete and test-backed: 21 Python stdlib `unittest` cases passed, `py_compile` passed, and the remaining work was operational (`git status`, explicit-path commit, push, and remote verification).

## Key Concepts

- [[Offline Contract Validation for On-Call Triage Artifacts]]
- [[Signal Relevance Gate for Infrastructure Triage]]

## Related Entities

- **[[Agentic-Triage]]** — The repository that implements the fixture-driven offline triage workflow, contract validator, and conservative resolver described in the checkpoint.
- **[[Durable Copilot Session Checkpoint]]** — The artifact type that preserved this partially completed architecture and implementation thread as reusable knowledge.
- **[[Copilot CLI]]** — The agent runtime used to research, implement, review, and checkpoint the work.
