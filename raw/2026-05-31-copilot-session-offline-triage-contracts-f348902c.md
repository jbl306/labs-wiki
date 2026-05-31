---
title: "Copilot Session Checkpoint: Offline Triage Contracts"
type: text
captured: 2026-05-31T23:07:45.741410Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, graph, agents, dashboard]
checkpoint_class: durable-architecture
checkpoint_class_rule: "body:integration"
retention_mode: retain
status: pending
---

# Copilot Session Checkpoint Export

**Checkpoint title:** Offline Triage Contracts
**Session ID:** `b7d55107-cb09-4910-b448-7fde6b456831`
**Checkpoint file:** `/home/jbl/.copilot/session-state/b7d55107-cb09-4910-b448-7fde6b456831/checkpoints/001-offline-triage-contracts.md`
**Checkpoint timestamp:** 2026-05-31T22:48:10.265988Z
**Exported:** 2026-05-31T23:07:45.741410Z
**Checkpoint class:** `durable-architecture` (rule: `body:integration`)
**Retention mode:** `retain`
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
The user is building a repo for a human-initiated on-call triage assistant for a complex CloudStack/Kubernetes platform. The work pivoted from an autonomous RCA/response system to a read-mostly, on-call-invoked workflow with deterministic offline scripts, schemas, signal relevance filtering, and fixture-based tests before any live integrations.
</overview>

<history>
1. User asked for deep research and a world-class agentic triage system plan for CloudStack, FreeIPA, MySQL, Prometheus/Grafana, QEMU/KVM, OpenSearch, HPE/NFS, and Kubernetes.
   - Ran parallel research agents on RCA state of the art, token optimization, and stack integration.
   - Created `~/projects/agentic-triage/` with `README.md`, `docs/PLAN.md`, and research appendices under `docs/research/`.
   - Initial design was a token-optimized RCA funnel with deterministic prefiltering, specialist agents, causal graph, and budgeted frontier model.

2. User asked for a roadmap to improve the triage system.
   - Added `docs/ROADMAP.md` with L0→L5 maturity ladder, workstreams, horizons, metrics, and risks.
   - Linked it from README.

3. User clarified the system should be an on-call triage/response workflow.
   - Added `docs/ONCALL-WORKFLOW.md` describing an AI on-call first responder lifecycle.
   - Repositioned README around AI on-call responder framing.

4. User said the plan was too autonomous and described the actual workflow: on-call receives PagerDuty alert, initiates flow, checks Prometheus/Grafana, OpenSearch, kubectl, ssh; for CloudStack guest VMs no in-guest access, but can live-migrate/start/stop resources.
   - Moved autonomous workflow to `docs/backlog/ONCALL-WORKFLOW.md`.
   - Created active plan `docs/ACTIVE-PLAN.md` for human-initiated, read-mostly triage.
   - Updated README and `PLAN.md` scope note.
   - Seeded deferred autonomy todos for auto-ack, alert ingest/dedup, auto-severity/paging, gated auto-remediation, autonomy ladder.

5. User asked to review the active on-call plan.
   - Reviewed for operational gaps.
   - Identified need for resource resolution, diagnostic order, ssh/kubectl allow-lists, guest VM wording, CloudStack action gates, report schema, PagerDuty behavior, adapter limits.

6. User asked to make recommended plan updates and evaluate repeatable scripts.
   - Updated `docs/ACTIVE-PLAN.md`.
   - Added sections for Resource Identity Resolution, Diagnostic Order, Guardrails, CloudStack Action Safety Gates, Adapter Output Limits, Triage Report Contract, and Repeatable Scripts/Runbooks Evaluation.
   - Recommended deterministic scripts under `bin/`, `scripts/`, `runbooks/`, `schemas/`.

7. User asked how to distinguish true platform errors from dead CronJobs/old K8s events.
   - Proposed a Signal Relevance Gate between evidence collection and report generation.
   - Recommended deterministic relevance scoring before LLM summarization.

8. User asked to implement the plan and push all commits, then reevaluate repo/workflow efficiency.
   - Initialized git repo, created private GitHub repo `jbl306/agentic-triage`, pushed `main`.
   - Implemented `scripts/assess_signal_relevance.py` using TDD.
   - Added `tests/test_signal_relevance.py`, `schemas/signal-relevance.schema.json`, `runbooks/k8s-signal-relevance.yaml`.
   - Added `docs/NEXT-STEPS.md`.
   - Code review found two bugs: stale unrelated CronJob could be promoted by declared correlation; repeated K8s events used old timestamp before `last_seen`. Added regression tests and fixed.
   - Commit pushed: `20222b0 Add on-call triage signal relevance gate`.

9. User asked to implement next steps that do not require live system.
   - Implemented fixture-only offline workflow with TDD.
   - Added `bin/triage`, core schemas, sample fixture, report renderer, audit helper, config example, GitHub Actions tests.
   - Code review found path traversal risk from PagerDuty ID in run dir; added regression test and fixed with `safe_slug`.
   - Commit pushed: `a9f459f Add offline triage fixture workflow`.

10. User asked to implement N1 and N2, review code, and fix using best practices.
   - Began implementing N1: schema validation helper.
   - Began implementing N2: PagerDuty fixture ingestion and conservative resource resolver.
   - Added tests first:
     - `tests/test_contract_validation.py`
     - `tests/test_pd_resource_scripts.py`
   - Added implementation:
     - `scripts/validate_contract.py`
     - `scripts/pd_incident_context.py`
     - `scripts/resolve_resource.py`
     - `fixtures/pagerduty-cloudstack-vm-alert.json`
   - Updated `bin/triage` to validate fixture artifacts before writing run dirs.
   - Updated README and `docs/NEXT-STEPS.md`.
   - First code review found:
     - Validator accepted unsupported schema types.
     - Invalid incident timestamps could create partial run artifacts.
   - Added regression tests; fixed validator to fail closed and enforce date-time.
   - Second review found:
     - Date-time validation accepted date-only/timezone-less/non-`T` values.
     - Partial CloudStack labels could downgrade to host mapping without ambiguity.
   - Added regression tests; fixed strict RFC3339 timestamp validation and partial CloudStack ambiguity.
   - Final review found:
     - Single partial CloudStack label was treated as resolved.
   - Added regression test; fixed resolver so any partial CloudStack clue remains ambiguous.
   - Latest verification run passed 21 tests, but commit/push had not happened before compaction.
</history>

<work_done>
Current repo: `/home/jbl/projects/agentic-triage`, remote `git@github.com:jbl306/agentic-triage.git`, private GitHub repo `https://github.com/jbl306/agentic-triage`, branch `main`.

Already committed/pushed:
- `20222b0 Add on-call triage signal relevance gate`
- `a9f459f Add offline triage fixture workflow`

Uncommitted/in-progress N1/N2 work at compaction:
- Added `scripts/validate_contract.py`
- Added `scripts/pd_incident_context.py`
- Added `scripts/resolve_resource.py`
- Added `fixtures/pagerduty-cloudstack-vm-alert.json`
- Added `tests/test_contract_validation.py`
- Added `tests/test_pd_resource_scripts.py`
- Modified `bin/triage` to validate artifacts before writing run dirs and return `SystemExit(main())`.
- Modified `README.md` with offline helper commands.
- Modified `docs/NEXT-STEPS.md` marking N1/N2 complete and adjusting next implementation order.
- Modified `tests/test_offline_triage.py` with invalid fixture/timestamp validation tests.
- Modified `scripts/validate_contract.py` through review fixes.
- Modified `scripts/resolve_resource.py` through review fixes.

Latest verification before compaction:
- `python3 -m unittest discover -s tests -v` passed 21 tests.
- `python3 -m py_compile bin/triage scripts/*.py` passed.
- `rm -rf bin/__pycache__ scripts/__pycache__ tests/__pycache__` was run.
- Final diff was being inspected with `rtk git --no-pager diff ...`; commit/push still pending.
</work_done>

<technical_details>
- Active scope is explicitly human-initiated/read-mostly:
  - No auto-ack, auto-page, auto-resolve, auto-escalate, or unattended remediation.
  - P1/P2 read-only.
  - P3 may only perform approved CloudStack VM lifecycle actions: `live-migrate`, `start`, `stop`.
- CloudStack guest VMs have no in-guest access:
  - Diagnosis must be outside-in via CloudStack API, KVM host, metrics/logs.
  - Guest app logs only available if shipped to OpenSearch.
- Signal Relevance Gate:
  - Script: `scripts/assess_signal_relevance.py`
  - Classifies signals into `contributing_signals`, `possibly_related_signals`, `background_noise`, `stale_historical`, `blind_spots`.
  - Handles stale K8s events, dead CronJobs, current correlated CronJob failures, and declared blind spots.
  - Reviewer-found fixes:
    - Declared correlation IDs alone cannot promote stale unrelated CronJob.
    - Event relevance prefers `last_seen` / `lastTimestamp` over old first `timestamp`.
- Offline `bin/triage`:
  - Takes `--input` fixture and `--output-dir`.
  - Writes run dir with:
    - `incident-envelope.json`
    - `resource-map.json`
    - `evidence-bundle.json`
    - `signal-relevance.json`
    - `triage-report.md`
    - `audit-log.jsonl`
  - Does not contact live systems.
  - Run dir name uses `safe_slug` to prevent PagerDuty ID path traversal.
- N1 validator:
  - `scripts/validate_contract.py` is dependency-free and supports subset of JSON Schema: `required`, `type`, `properties`, `items`, `enum`, min/max, local `$defs` refs, `additionalProperties: false`, and strict `format: date-time`.
  - It now fails closed for unsupported schema types.
  - It enforces strict RFC3339 date-time with `T` separator and timezone (`Z` or offset); date-only, timezone-less, and space-separated values are invalid.
- N2 PagerDuty/resource path:
  - `scripts/pd_incident_context.py` converts PagerDuty-shaped fixture to incident envelope.
  - `scripts/resolve_resource.py` maps CloudStack VM labels when `cloudstack_vm_id` and `project_id` are both present.
  - Resolver is conservative:
    - Multiple possible resources produce `resource_type: ambiguous`.
    - Partial CloudStack labels (`cloudstack_vm_id` without `project_id`, etc.) always remain ambiguous and include a blind spot.
    - It must not silently fallback to host mapping when partial CloudStack evidence exists.
- Testing:
  - Uses Python stdlib `unittest`, no external test dependencies.
  - Current test count after N1/N2 is 21.
- Tooling quirk:
  - Some shell output shows `rtk git` / `rtk find`, but normal git commands work. Earlier `find -prune` through wrapper behaved oddly; use normal shell carefully.
- Git workflow:
  - User memory says stage only task-authored files explicitly, never `git add -A`.
  - Need to commit N1/N2 with explicit paths and push.
</technical_details>

<important_files>
- `README.md`
  - Entry point and quickstart.
  - Now documents offline fixture workflow and helper scripts.
  - Modified in N1/N2, not yet committed.

- `docs/ACTIVE-PLAN.md`
  - Primary active plan: human-initiated assistive triage copilot.
  - Contains resource resolution, diagnostic order, signal relevance gate, guardrails, report contract, scripts/runbooks evaluation.

- `docs/NEXT-STEPS.md`
  - Current implementation roadmap.
  - Updated to mark N1 schema validation and N2 PagerDuty/resource resolver complete.
  - Next items are fixture collectors and pluggable collector stages.
  - Modified in N1/N2, not yet committed.

- `bin/triage`
  - Fixture-only offline orchestrator.
  - Now validates incident/resource/evidence before creating run dir.
  - Uses `assess_signal_relevance` before rendering report.
  - Important fixes: `safe_slug`, `raise SystemExit(main())`, pre-write validation.

- `scripts/validate_contract.py`
  - New N1 validation helper.
  - Fail-closed subset validator with strict RFC3339 date-time.
  - Central for contract enforcement.

- `scripts/pd_incident_context.py`
  - New N2 fixture ingestion script.
  - Converts PagerDuty-shaped fixture to incident envelope.

- `scripts/resolve_resource.py`
  - New N2 conservative resolver.
  - CloudStack VM requires both VM ID and project ID to be canonical.
  - Partial CloudStack clues are ambiguous with blind spot.

- `fixtures/pagerduty-cloudstack-vm-alert.json`
  - New PagerDuty-shaped fixture for N2.

- `fixtures/sample-pagerduty-k8s-cronjob-noise.json`
  - Existing offline fixture for `bin/triage`.

- `tests/test_contract_validation.py`
  - New N1 tests.
  - Covers valid envelope, missing required field, unsupported schema type, invalid date-time, strict RFC3339 variants.

- `tests/test_pd_resource_scripts.py`
  - New N2 tests.
  - Covers PagerDuty fixture conversion, CloudStack mapping, ambiguous mapping, partial CloudStack ambiguity, single partial CloudStack ambiguity.

- `tests/test_offline_triage.py`
  - Existing offline orchestrator tests.
  - Modified to ensure invalid fixture/timestamp rejected before run artifacts are written.

- `scripts/assess_signal_relevance.py`
  - Existing signal relevance implementation.
  - Important dependency of `bin/triage`.

- `schemas/*.schema.json`
  - Contract schemas for incident envelope, resource map, evidence bundle, triage report, audit event, signal relevance.
</important_files>

<next_steps>
Immediate pending actions:
1. Re-run final verification if needed:
   - `cd /home/jbl/projects/agentic-triage`
   - `python3 -m unittest discover -s tests -v`
   - `python3 -m py_compile bin/triage scripts/*.py`
   - `rm -rf bin/__pycache__ scripts/__pycache__ tests/__pycache__`
2. Inspect git status/diff.
3. Commit N1/N2 changes with explicit paths only:
   - `README.md`
   - `docs/NEXT-STEPS.md`
   - `bin/triage`
   - `scripts/validate_contract.py`
   - `scripts/pd_incident_context.py`
   - `scripts/resolve_resource.py`
   - `fixtures/pagerduty-cloudstack-vm-alert.json`
   - `tests/test_contract_validation.py`
   - `tests/test_pd_resource_scripts.py`
   - `tests/test_offline_triage.py`
4. Suggested commit message: `Add offline contract validation and resource resolution`
5. Push to `origin/main`.
6. Verify remote after push:
   - `git status --short --branch`
   - `git log --oneline --decorate -2`
   - `gh repo view jbl306/agentic-triage --json nameWithOwner,visibility,url,defaultBranchRef`

Remaining planned work after N1/N2:
- Build read-only fixture collectors in order:
  1. Prometheus + OpenSearch fixture collectors
  2. Kubernetes fixture collector
  3. CloudStack fixture/read context
  4. Host ssh read-only diagnostics fixture mode
  5. CloudStack action precheck (no mutation)
  6. Refactor `bin/triage` to pluggable collector stages while preserving offline mode.
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
