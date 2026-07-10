---
title: "GitHub Ingestion Phase 3 Review Delivery"
type: note
captured: 2026-07-10T01:19:09Z
source: wiki-save
session_client: copilot-cli
tags: [github-ingestion, review-publishing, lifecycle-events, codex-skills, security]
status: pending
---

# GitHub Ingestion Phase 3 Review Delivery

## Context

Phase 3 of the active GitHub ingestion plan required safe GitHub delivery for
sealed repository reviews. The implementation added idempotent report pull
requests, non-authorizing lifecycle records, a stable operator CLI, and concise
documentation.

## Key Findings

- A Phase 2 artifact manifest excludes `evaluation.json`, so publication and
  adoption must recompute identity fields and verify a separate hash seal for
  the complete evaluation record.
- Checking only a report directory cannot prove branch purity. The publisher
  must compare the complete report branch delta with the base branch and allow
  only `review.md`, `evaluation.json`, and `publication.json` for that exact
  evaluation.
- A narrow GitHub credential must cover both REST and Git transport. Git uses
  clean HTTPS remotes and environment-only extra-header configuration; it does
  not use the operator's broader SSH authority or token-bearing arguments.
- Review publication needs a pristine base clone because latest-star discovery
  can update local state after the review command begins.
- Report merges, labels, comments, schedules, and adoption requests carry no
  approval or apply authority. Adoption intent binds the exact evaluation,
  component IDs, target profile, and one of four explicit intents.
- Lifecycle retries need prior-event identity. This preserves idempotency and
  still records legitimate `open -> closed -> open` transitions; merge remains
  terminal.
- Same-second evaluations need a deterministic `(created_at, evaluation_id)`
  order for stale-request invalidation.

## Decisions / Outcomes

- Added `publish`, `report-state`, `request-adoption`, and `status` commands;
  `review --latest --publish` completes the manual report loop.
- Added a dedicated automation checkout, non-force pushes, branch collision and
  pollution checks, remote/repository binding, and mocked GitHub PR create,
  update, closed, and merged behavior.
- Added a strict lifecycle event schema and append-only events that never feed
  the apply path.
- Added an operator README, marked historical plans superseded, completed the
  Phase 3 task record, and updated the installed GitHub ingestion router skill.
- Independent review findings were fixed and converted into regression tests.
- Final validation passed 206 pytest tests with 96 subtests, 206 unittest
  tests, compilation, CLI help, README checks, skill validation, and diff
  checks.

## Open Questions

- Phase 4 still needs the hardened scheduled review-only worker and homelab
  deployment boundary.
- Phase 5 still needs target-specific multi-file adoption and homelab service
  pull-request generation.

## References

- `/home/jbl/projects/github-ingestion/plans/2026-07-09-frictionless-star-review-and-adoption.md`
- `/home/jbl/projects/github-ingestion/tasks/2026-07-09-implement-phase-3-github-delivery.md`
- `/home/jbl/projects/github-ingestion/scripts/github_publisher.py`
- `/home/jbl/projects/github-ingestion/scripts/review_lifecycle.py`
- `/home/jbl/projects/github-ingestion/README.md`
- `/home/jbl/.agents/skills/github-ingestion/SKILL.md`
