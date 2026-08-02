---
title: "GitHub Ingestion Phase 3 Review Delivery"
type: source
created: '2026-08-02'
last_verified: '2026-08-02'
source_hash: "0662c95f97a999e095421b9c41509fa89d7d7d27f75ce095bf118482790ed0bd"
sources:
  - raw/2026-07-09-github-ingestion-phase-3-delivery.md
tags: [github-ingestion, review-publishing, lifecycle-events, codex-skills, security]
tier: hot
knowledge_state: ingested
ingest_method: codex-cli-gpt-5.6-luna
quality_score: 78
related:
  - "[[Sealed Review Publication]]"
  - "[[Non-Authorizing Lifecycle Records]]"
  - "[[GitHub Repository Deep Crawling for Wiki Ingestion]]"
  - "[[Signal-Preserving GitHub Repository Ingestion]]"
---

# GitHub Ingestion Phase 3 Review Delivery

## Summary

Phase 3 completed the safe delivery loop for sealed GitHub repository reviews. The implementation adds idempotent report pull requests, explicit report-state and adoption commands, append-only lifecycle records, and a narrow credential boundary that covers both REST and Git transport without granting apply authority. Validation passed 206 pytest tests with 96 subtests, 206 unittest tests, compilation, CLI-help, README, skill, and diff checks.

## Key Points

- Phase 2's artifact manifest excludes `evaluation.json`; publication and adoption therefore recompute identity fields and verify a separate hash seal for the complete evaluation record.
- Publication compares the complete report-branch delta with the base branch and permits only `review.md`, `evaluation.json`, and `publication.json` for the exact evaluation, preventing branch pollution.
- GitHub credentials are deliberately narrow: REST and Git use the same limited authority, clean HTTPS remotes, and environment-only extra-header configuration; the operator's broader SSH authority is not used.
- Review publication starts from a pristine base clone because latest-star discovery can mutate local state after review begins.
- Added `publish`, `report-state`, `request-adoption`, and `status` commands; `review --latest --publish` completes the manual report loop.
- Report merges, labels, comments, schedules, and adoption requests are records or intents only. They carry no approval or apply authority.
- Lifecycle retries include prior-event identity, preserving idempotency while allowing legitimate `open -> closed -> open` transitions; merge remains terminal.
- Same-second evaluations use deterministic `(created_at, evaluation_id)` ordering for stale-request invalidation.
- Phase 4 remains focused on a hardened scheduled review-only worker and homelab deployment boundary; Phase 5 covers target-specific multi-file adoption and homelab service pull requests.

## Key Concepts

- [[Sealed Review Publication]]
- [[Non-Authorizing Lifecycle Records]]
- [[GitHub Repository Deep Crawling for Wiki Ingestion]]
- [[Signal-Preserving GitHub Repository Ingestion]]

## Related Entities

- **[[GitHub Copilot]]** — Existing GitHub-adjacent entity; the source concerns repository review delivery rather than the Copilot product itself.
- **[[GitHub Models API]]** — Existing GitHub-adjacent entity; the Phase 3 note instead emphasizes narrow GitHub REST and Git credentials.
