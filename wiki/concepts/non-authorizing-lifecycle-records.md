---
title: "Non-Authorizing Lifecycle Records"
type: concept
created: 2026-08-02
last_verified: 2026-08-02
source_hash: "0662c95f97a999e095421b9c41509fa89d7d7d27f75ce095bf118482790ed0bd"
sources:
  - raw/2026-07-09-github-ingestion-phase-3-delivery.md
related:
  - "[[Sealed Review Publication]]"
  - "[[End-To-End Validation In Live Memory Loops]]"
  - "[[Artifact Registry Validation in ML Pipelines]]"
tier: hot
tags: [github, lifecycle-events, auditability, idempotency, authorization]
---

# Non-Authorizing Lifecycle Records

## Overview

Non-authorizing lifecycle records are append-only events that describe what happened in a review and delivery workflow without granting permission to approve, merge, or apply a change. The Phase 3 GitHub-ingestion implementation applies this separation to report merges, labels, comments, schedules, report-state changes, and adoption requests. Records make the workflow observable and retryable while keeping authority in explicit, separately checked operations.

## How It Works

The design begins by separating evidence from authority. A report pull request, a label, or an adoption request can communicate state and intent, but none of those objects is treated as an approval token. In particular, a merged report is still only a published review result. It does not authorize the system to apply the reviewed change. This prevents a convenient GitHub event from silently becoming a privileged control signal.

Lifecycle events are stored append-only. Each event records the transition or action that occurred, and retries carry prior-event identity. Prior-event identity is the key to safe replay: if the same request is delivered twice, the second attempt can be recognized as a retry rather than creating a false second transition. At the same time, the model does not collapse legitimate state changes. The workflow can record `open -> closed -> open`, while merge remains terminal.

The transition model therefore distinguishes idempotency from monotonicity. Idempotency means repeating one event has no additional effect; it does not mean every entity can move only forward once. A review may be reopened after being closed, and that is a new legitimate event with a different identity. Merge is different because the implementation treats it as terminal, preventing later lifecycle events from rewriting the meaning of a completed delivery.

The event stream also supports explicit operator commands. Phase 3 adds `publish`, `report-state`, `request-adoption`, and `status`, while `review --latest --publish` completes the manual report loop. These commands expose delivery and intent as stable interfaces, but they do not collapse review, publication, and adoption into one authorization step. Adoption intent binds the exact evaluation, component IDs, target profile, and one of four explicit intents, making the requested scope inspectable before any future apply path considers it.

Ordering is deterministic even when timestamps are not. Same-second evaluations are ordered by `(created_at, evaluation_id)`, which lets the system invalidate stale requests consistently. Without a tie-breaker, two evaluations created in the same second could produce nondeterministic stale-request behavior depending on storage or API return order. Deterministic ordering turns a timing accident into a stable state-machine decision.

This architecture is useful because auditability and authorization have different failure modes. Audit records should preserve what the system observed, including retries and reopenings. Authorization should be narrow, explicit, and evaluated against current identity and scope. Keeping the two paths separate means a noisy or duplicated lifecycle event can damage neither the audit trail nor the apply boundary.

## Key Properties

- **No implicit approval:** Merges, labels, comments, schedules, and adoption requests do not grant apply authority.
- **Append-only history:** Events preserve the sequence of observed transitions rather than rewriting prior state.
- **Retry identity:** Prior-event identity makes repeated delivery idempotent.
- **Explicit reopen semantics:** `open -> closed -> open` remains representable, while merge is terminal.
- **Deterministic invalidation:** `(created_at, evaluation_id)` provides a stable order for same-second evaluations.
- **Bounded adoption intent:** Requests bind an evaluation, component IDs, target profile, and an explicit intent.

## Limitations

An append-only event stream does not by itself guarantee that every event is authentic or that a consumer interprets it safely. Consumers must preserve the non-authorizing contract and validate event identity, evaluation binding, and current state. The four-intent adoption model is deliberately explicit but can require schema changes when new adoption modes are introduced. The Phase 3 note also leaves scheduled review-only execution and target-specific adoption for later phases.

## Examples

```json
{
  "event": "request-adoption",
  "evaluation_id": "eval-123",
  "component_ids": ["component-a"],
  "target_profile": "homelab",
  "intent": "open_pull_request",
  "prior_event_id": "event-122"
}
```

This object records a narrowly scoped intent. It is not an instruction to apply the component and cannot substitute for a later authorization check.

## Practical Applications

Use non-authorizing lifecycle records in automated code review, deployment previews, compliance workflows, and agentic operations where external systems need a durable audit trail but must not gain authority merely by observing or mutating a status object. The pattern is especially useful when retries, webhook duplication, reopenings, and cross-system synchronization are normal.

## Related Concepts

- **[[Sealed Review Publication]]**: Supplies the integrity and branch-purity checks for the published artifact.
- **[[End-To-End Validation In Live Memory Loops]]**: Illustrates testing of event-driven systems across detection and processing boundaries.
- **[[Artifact Registry Validation in ML Pipelines]]**: Reinforces validation at artifact handoff points.

## Sources

- [[GitHub Ingestion Phase 3 Review Delivery]]
