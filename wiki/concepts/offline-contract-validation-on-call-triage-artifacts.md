---
title: "Offline Contract Validation for On-Call Triage Artifacts"
type: concept
created: 2026-05-31
last_verified: 2026-05-31
source_hash: ac2a0a3d9e56d2d9d201b266da04fa315379f6e205476203ef10320f7a42188e
sources:
  - raw/2026-05-31-copilot-session-offline-triage-contracts-f348902c.md
quality_score: 86
related:
  - "[[Signal Relevance Gate for Infrastructure Triage]]"
  - "[[Shared Contract Normalization for Dashboard APIs]]"
  - "[[Structured Artifact Chains]]"
tier: hot
tags: [on-call-triage, contract-validation, json-schema, offline-workflow, rfc3339, guardrails]
---

# Offline Contract Validation for On-Call Triage Artifacts

## Overview

Offline contract validation for on-call triage artifacts is the practice of forcing every intermediate object in a triage run to satisfy an explicit schema before the system is allowed to persist results or generate operator-facing conclusions. In the checkpoint, this concept matters because the assistant is intentionally being built in offline mode first: if fixtures, timestamps, resource mappings, and report inputs are not structurally trustworthy, a later live integration would only automate ambiguity faster.

## How It Works

The checkpoint describes a design that treats triage as a typed artifact pipeline rather than a loose sequence of scripts. The central executable is `bin/triage`, which reads an offline fixture and produces a run directory with six named outputs: `incident-envelope.json`, `resource-map.json`, `evidence-bundle.json`, `signal-relevance.json`, `triage-report.md`, and `audit-log.jsonl`. The important architectural point is that those files are not just outputs of convenience. They are contract boundaries. Each one represents a handoff between stages of the workflow, and each handoff is supposed to be machine-checkable before the next stage is allowed to proceed.

That requirement led to `scripts/validate_contract.py`, a dependency-free validator that implements a deliberately limited subset of JSON Schema. The checkpoint calls out the supported surface precisely: `required`, `type`, `properties`, `items`, `enum`, min/max constraints, local `$defs` references, `additionalProperties: false`, and strict `format: date-time`. This is a significant choice. Instead of adopting a broad validation library and inheriting a large behavioral surface, the project narrows the schema language to the exact rules it wants to operationalize during the offline phase. The validator is not "feature incomplete" by accident; it is intentionally constrained so the team can reason about every validation rule in production terms.

The fail-closed behavior is the real contract. Early review found that the validator accepted unsupported schema types. That means a malformed or overly expressive schema could silently degrade the promise that artifacts were validated. The fix was to reject unsupported types outright. In systems language, the checkpoint moves validation from "best effort" to "sound within a defined subset." That shift is crucial for operator trust. A triage assistant should not claim a report is contract-valid because it skipped the parts of the schema it did not understand.

Timestamp validation is another place where the checkpoint turns a vague format expectation into an operational guarantee. The validator now enforces strict RFC3339 date-times with a literal `T` separator and an explicit timezone, either `Z` or an offset. Date-only strings, timezone-less timestamps, or space-separated variants are rejected. This matters because time drives almost every later judgment in the pipeline: event freshness, incident ordering, stale-evidence suppression, and the naming or correlation of artifacts. If time semantics are loose, then downstream logic can appear deterministic while actually running on inconsistent clocks.

The checkpoint also records a critical sequencing choice: artifact validation happens before the system writes run directories. `bin/triage` was modified so invalid incident timestamps or other contract failures do not leave partial run artifacts behind. This is more than cleanup hygiene. Partial directories create a false sense that a run progressed farther than it really did, and they complicate audit trails because later tools may ingest orphaned files as if they were valid evidence. By validating first and only then writing artifacts, the workflow preserves a one-way invariant: persisted runs correspond to contract-satisfying inputs.

Path safety is folded into the same contract mindset. A previous review found a path traversal risk from PagerDuty IDs being used in run directory names. The fix introduced `safe_slug`, and the checkpoint explicitly notes that the run directory name now derives from a sanitized slug rather than trusting incident identifiers verbatim. This is an important design lesson: artifact contracts are not just about JSON structure; they also include filesystem identity, naming boundaries, and the assumptions surrounding operator-provided or third-party identifiers.

Resource resolution sits adjacent to schema validation but participates in the same trust model. `scripts/resolve_resource.py` maps CloudStack VM labels only when `cloudstack_vm_id` and `project_id` are both present. If the evidence is partial, the resolver returns ambiguity and records a blind spot instead of silently downgrading the incident to a host mapping. This is effectively semantic validation. The system is checking not only whether a field exists, but whether the evidence is strong enough to support a canonical interpretation. In other words, the contract extends beyond syntax into the minimum evidence required for safe inference.

The result is an offline workflow that behaves like a staged proof obligation. A fixture is not "good enough" because it can be parsed. It must produce an incident envelope with valid timestamps, a resource map with defensible identity, an evidence bundle that can be classified, and a final report traceable through typed artifacts. That approach makes later live adapters safer to build because each adapter only has one job: generate artifacts that satisfy the preexisting contracts. It does not get to redefine what a valid incident or resource looks like.

## Key Properties

- **Fail-closed schema subset:** Unsupported schema constructs cause validation failure instead of being ignored.
- **Strict temporal semantics:** Timestamps must be RFC3339 with `T` plus timezone, preventing ambiguous freshness calculations.
- **Pre-write validation:** Invalid inputs are rejected before run directories or downstream artifacts are created.
- **Semantic identity gate:** Resource resolution requires enough evidence to justify a canonical CloudStack VM mapping.
- **Filesystem-safe artifact naming:** Sanitized slugs prevent untrusted incident identifiers from escaping the intended run path.

## Limitations

The validator intentionally supports only a subset of JSON Schema, so future artifact types may require either schema redesign or careful extension of the validator. The workflow is also only as good as its schemas: if important domain constraints are not represented there, validation cannot enforce them. Finally, strict failure semantics improve trust but can slow early adoption because every new fixture or adapter must satisfy the contract before it becomes usable.

## Examples

```python
fixture = load_json("pagerduty-alert.json")
incident = pd_incident_context(fixture)
validate_contract("schemas/incident-envelope.schema.json", incident)

resource_map = resolve_resource(incident)
validate_contract("schemas/resource-map.schema.json", resource_map)

evidence = collect_fixture_evidence(incident, resource_map)
validate_contract("schemas/evidence-bundle.schema.json", evidence)

run_dir = make_run_dir(safe_slug(incident["pagerduty_id"]))
write_artifacts(run_dir, incident, resource_map, evidence)
```

In this pattern, each stage has to prove its output before the next stage becomes durable.

## Practical Applications

This concept is valuable anywhere an operations assistant must earn trust before touching live infrastructure: incident triage copilots, security runbook assistants, compliance evidence assemblers, or change-review bots. A schema-first offline lane makes it possible to test real operator workflows against fixtures, catch timestamp and identity ambiguities early, and promote only the adapters that already conform to the system's artifact contracts.

## Related Concepts

- **[[Signal Relevance Gate for Infrastructure Triage]]** — Runs after artifact collection to classify evidence quality rather than merely validate shape.
- **[[Shared Contract Normalization for Dashboard APIs]]** — Solves a similar problem at service boundaries by enforcing one canonical response shape across heterogeneous producers.
- **[[Structured Artifact Chains]]** — Provides the broader systems principle that workflow steps should exchange typed, auditable artifacts rather than hidden in-memory state.

## Sources

- [[Copilot Session Checkpoint: Offline Triage Contracts]] — primary checkpoint defining the validator, pre-write gating, and conservative resolver behavior.
