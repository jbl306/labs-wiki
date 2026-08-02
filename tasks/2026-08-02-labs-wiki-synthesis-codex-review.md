# Labs Wiki synthesis and Codex review

## Goal

Comprehensively review Labs Wiki and improve its ability to compile durable, cross-source synthesis after the ingest backend moved from a GitHub Copilot subscription to Codex CLI.

## Constraints

- Preserve unrelated untracked work under `.o11y/` and `tasks/sevenrooms-doordash-going-out-browser-to-api.md`.
- Keep raw-source provenance intact and avoid rewriting generated knowledge without source evidence.
- Prefer the Codex subscription path; retain compatibility backends only where they have a tested operational purpose.
- Do not change live homelab services or restart the ingest stack as part of the repository review.

## Plan

- [x] Audit repository instructions, architecture, pipeline code, prompts, graph, current corpus, tests, and existing evaluations.
- [x] Verify the current Codex CLI configuration and official capabilities relevant to unattended compilation.
- [x] Establish a measurable synthesis-quality baseline: coverage, evidence breadth, duplication, title quality, graph connectivity, and retrieval usefulness.
- [x] Implement the highest-value narrowly scoped synthesis improvements with regression tests.
- [x] Run focused tests, full tests/lint/evaluation where feasible, inspect the final diff, and record results.

## Success criteria

- Synthesis creation is explicitly cross-source and evidence-aware rather than an incidental output of single-source ingest.
- Generated synthesis has deterministic eligibility gates, bounded context selection, and machine-checkable provenance requirements.
- Codex execution is configured and documented for reliable non-interactive use under the current subscription path.
- A repeatable evaluation reports synthesis quality separately from structural wiki quality.
- Existing compatibility and unrelated working-tree artifacts are preserved.

## Review / results

Completed 2026-08-02.

### Implemented

- Added a deterministic strict synthesis auditor and 83-page corpus baseline.
- Added evidence scope/count plus claim-level Evidence Maps for new synthesis.
- Replaced concept-count triggering with a decision/trade-off/contradiction value
  gate, bounded evidence packets, existing-page search, and one-page cap.
- Added Codex JSON Schema output, ephemeral execution, user-config isolation,
  strict created/updated path and provenance validation, pre/post checkout manifest
  enforcement, deterministic checkpoint preflight, validation-run isolation, and
  orchestrator-owned raw/log finalization with manifest-scoped git staging.
- Enforced the same JSON Schema for every agent backend, made commit finalization
  path-limited even when unrelated files are pre-staged, and moved index rebuilds
  before success status/log/notification finalization.
- Contained strict provenance to existing repository `raw/*.md` files, required
  each Evidence Map row to match its Key Insight's named existing wiki pages and
  use provenance belonging to every supporting page, emitted per-insight
  provenance, and applied the strict audit to checkpoint-backfill output.
- Removed unstable community-ID cluster matching, versioned cluster signatures,
  bounded recorded provenance to actual model inputs, prevented one page from
  satisfying two clusters, and repaired post-write log call sites.
- Pinned Codex CLI 0.145.0, set the reviewed default model to `gpt-5.6-luna`,
  hardened container permissions, and verified the image as uid 1000.
- Fixed fenced-code false wikilinks and the stale Karpathy evaluation slug.
- Documented architecture, workflow, deployment boundary, costs, privacy,
  reliability, maintenance, and the graph/session-capture roadmap.

### Principal findings

- Codex remains write-first: schema/path/audit gates prevent false finalization,
  but failed runs can leave files for review and the agent path still bypasses the
  legacy deterministic renderer. A read-only typed-proposal architecture is the
  remaining core refactor.

- Live `wiki-auto-ingest` is still Copilot CLI and failed the July pending raw
  after Copilot access ended; the reviewed Codex image/config is not deployed.
- The systemd session curator still watches Copilot checkpoints, while active
  Codex sessions are not promoted; this breaks the historically largest source
  channel.
- Of 83 synthesis pages, 17 have incomplete insight grounding, 68 rely on one
  source family, and 13 have mechanism-shaped/overlong titles.
- Tier/staleness maintenance is not operating: 863/958 pages remain hot and 866
  are stale.

### Verification

- Unit tests: **31 passed**.
- Ingest evaluation: **3/3 fixtures passed** after correcting the stale expected
  slug.
- Wiki lint: **964 pages, 0 errors, 974 warnings, 0 contradictions**. The warnings
  are corpus maintenance debt (866 stale, 106 low quality, 2 unindexed cluster
  summaries), not regressions from this change.
- Graph rebuild: **964 nodes, 3,304 edges, 23 communities**, TF-IDF backend.
- Synthesis audit: **83 pages**; mean 95.6, 17 below 90, 17 not fully grounded,
  13 mechanism-shaped titles, and 0 legacy pages yet on the new strict contract.
- Codex structured-output smoke: authenticated host call returned schema-valid
  `{"status":"ok"}`; a dedicated container request proved live
  `gpt-5.6-luna` availability under the subscription login.
- Container build/runtime smoke: passed with `codex-cli 0.145.0`, required
  `pages_updated`, strict JSON Schema/audit enforcement, path-limited commits, and
  an isolated writable uid-1000 Codex home.
- Checkpoint-cluster dry run: five planned, one exact-source match, zero
  community-number fallback matches.
- Python compilation, Markdown fence balance, and `git diff --check`: passed.

### Deployment follow-up

The first container rollout exposed a nested bubblewrap namespace failure. The
runtime now executes image-owned scripts from `/opt/labs-wiki`, mounts the Git
worktree separately, and selects `danger-full-access` only for the inner Codex
CLI while retaining the capability-dropped, no-new-privileges container as the
outer sandbox. A real containerized shell/read schema smoke returned
`{"status":"ok"}`.

The first full ingest exposed a second runtime-only issue: the JSON scanner
returned a nested `duplicates_avoided` entry instead of the outer typed result.
It now prefers objects carrying the top-level `status`; a regression test covers
the exact nested-object shape.

### Safety boundary

During the review implementation phase, no live homelab compose file, OAuth
secret, running container, systemd unit, or raw/wiki corpus page was changed or
restarted. Deployment was handled afterward under the separate homelab task.

The comprehensive review is
`reports/full-review-2026-08-02-codex-synthesis.md`.
