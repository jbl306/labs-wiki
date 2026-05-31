---
title: "Signal Relevance Gate for Infrastructure Triage"
type: concept
created: 2026-05-31
last_verified: 2026-05-31
source_hash: ac2a0a3d9e56d2d9d201b266da04fa315379f6e205476203ef10320f7a42188e
sources:
  - raw/2026-05-31-copilot-session-offline-triage-contracts-f348902c.md
quality_score: 87
related:
  - "[[Offline Contract Validation for On-Call Triage Artifacts]]"
  - "[[LLM-Powered Noise Filtering]]"
  - "[[Structured Artifact Chains]]"
tier: hot
tags: [on-call-triage, signal-relevance, noise-filtering, kubernetes, cloudstack, deterministic-gates]
---

# Signal Relevance Gate for Infrastructure Triage

## Overview

A signal relevance gate is a deterministic classification stage that decides which observed events, alerts, logs, or metrics should influence an incident narrative and which should be treated as background, stale history, or unresolved blind spots. In the checkpoint, this concept matters because noisy infrastructure evidence can easily overwhelm an on-call assistant: without an explicit gate, dead CronJobs, old Kubernetes events, and weak correlations can be promoted into false explanations that waste operator attention.

## How It Works

The checkpoint places the signal relevance gate between evidence collection and report generation. That placement is the main design decision. Instead of letting an LLM read everything and infer what matters, the workflow first produces a structured evidence bundle and then runs `scripts/assess_signal_relevance.py` to sort the contents into named buckets. The output categories are explicit: `contributing_signals`, `possibly_related_signals`, `background_noise`, `stale_historical`, and `blind_spots`. This means the system does not merely compress observations into one summary; it preserves the reason each observation was accepted, deferred, or rejected.

The gate exists because infrastructure evidence is temporally messy. A Kubernetes cluster can carry historical events long after they stop reflecting the present incident. CronJobs are especially dangerous: a failed job may still appear in logs or events even though it is unrelated to the current outage, and the presence of a correlation ID or nearby namespace match can tempt a naïve workflow to over-credit it. The checkpoint documents a concrete bug of exactly this kind: a stale unrelated CronJob could be promoted by declared correlation alone. The fix established a stronger rule that declared correlation IDs are not sufficient by themselves to make stale noise relevant.

That change reveals the deeper mechanism. Relevance is treated as a conjunction of evidence dimensions, not a single boolean tag. A signal becomes genuinely contributing only when timing, resource proximity, and incident context line up strongly enough to justify causal attention. Weak matches can still be preserved, but they are downgraded into `possibly_related_signals` instead of being allowed to rewrite the incident narrative. This is important operationally because on-call work is not just about finding data; it is about ranking hypotheses under uncertainty.

Freshness logic is the second core mechanism. The checkpoint records another review-found bug: repeated Kubernetes events were using an old first `timestamp` instead of the more recent `last_seen` or `lastTimestamp`. That produces a subtle but severe distortion. If the system anchors on the first observation, a currently active repeated event can look historical; if it anchors on the last observation, the same event can correctly register as current evidence. The fix therefore prefers `last_seen` / `lastTimestamp` over the original first timestamp. In effect, the gate computes recency using the most operationally meaningful clock available rather than the earliest clock present in the object.

The bucket structure also lets the workflow handle absence honestly. `blind_spots` are not errors thrown away by the classifier; they are an explicit output class. This matters for the hybrid CloudStack/Kubernetes environment described in the checkpoint. For example, a CloudStack guest VM may have no in-guest access, and application logs may only exist if they were shipped to OpenSearch. When the workflow lacks those views, the system should not silently compensate with stronger claims from weaker evidence. A blind-spot bucket preserves the fact that the operator is reasoning with incomplete observability.

The gate is deterministic on purpose. The checkpoint explicitly says the user asked how to distinguish true platform errors from dead CronJobs or old Kubernetes events, and the response was to add a deterministic relevance-scoring layer before LLM summarization. The reason is practical: summarizers are good at narrative compression but weak as policy boundaries. If the LLM decides both what evidence exists and what evidence matters, a later reviewer cannot separate hallucinated reasoning from real upstream classification. By computing relevance first, the system hands the model a better-bounded input: "these are the likely contributors, these are ambiguous, these are noise, and these are blind spots."

This does not mean the gate eliminates judgment. It externalizes judgment into inspectable rules and testable categories. That is why the checkpoint emphasizes TDD and reviewer-found regressions. The quality bar is not whether the model can usually summarize incidents plausibly; it is whether the relevance boundary remains stable when new fixtures introduce old CronJob noise, repeated events, or partial correlations. In operational systems, that kind of stability is often more valuable than raw cleverness because it keeps the assistant from oscillating between over-alarm and under-alarm as the evidence surface changes.

## Key Properties

- **Category-preserving output:** Signals are classified into five semantic buckets instead of being flattened into one narrative.
- **Freshness-aware ranking:** Repeated-event relevance prefers `last_seen` / `lastTimestamp` over first-observed timestamps.
- **Correlation is insufficient alone:** Declared correlation IDs cannot promote stale unrelated CronJob evidence by themselves.
- **Blind-spot reporting:** Missing or weak observability is preserved as a first-class output rather than hidden.
- **Deterministic pre-LLM filter:** Relevance is computed before report generation so later summarization starts from bounded evidence.

## Limitations

A deterministic gate can only score what the evidence bundle captures, so missing collectors or weak schemas still limit its usefulness. Hand-tuned relevance rules may also require adjustment as the platform grows beyond the current CloudStack and Kubernetes scope. Finally, some incidents genuinely involve weak, indirect, or delayed signals, which means the `possibly_related_signals` bucket can still require careful human interpretation rather than automated promotion or dismissal.

## Examples

```yaml
contributing_signals:
  - current_k8s_event: pod restart loop seen at lastTimestamp=2026-05-31T22:40:00Z
possibly_related_signals:
  - delayed_opensearch_error: same service namespace but weak temporal alignment
background_noise:
  - old_cronjob_failure: namespace match only
stale_historical:
  - deleted_cronjob_warning: last seen 3 days ago
blind_spots:
  - no_guest_vm_logs: CloudStack guest has no in-guest access
```

This structure gives the on-call human a ranked evidence map instead of an undifferentiated dump.

## Practical Applications

Signal relevance gates are useful in any operational workflow where raw observability data is plentiful but causality is scarce: incident triage, SIEM alert enrichment, SRE retrospectives, synthetic-monitor debugging, or platform health dashboards that need to separate real regressions from background churn. The concept is especially valuable when the final consumer is an LLM, because it lets deterministic logic do the filtering work and reserves generation for explanation rather than evidence arbitration.

## Related Concepts

- **[[Offline Contract Validation for On-Call Triage Artifacts]]** — Ensures the artifacts entering the gate are structurally trustworthy before relevance scoring begins.
- **[[LLM-Powered Noise Filtering]]** — Shares the goal of removing distracting information, but applies it to document indexing rather than live infrastructure evidence.
- **[[Structured Artifact Chains]]** — Explains why the relevance output should remain an auditable intermediate artifact instead of an invisible internal decision.

## Sources

- [[Copilot Session Checkpoint: Offline Triage Contracts]] — primary checkpoint defining the gate, its output buckets, and the regression fixes around stale CronJobs and timestamp precedence.
