---
title: "Copilot Session Checkpoint: Phase 5 backfill script written"
type: text
captured: 2026-04-18T07:53:30.006999Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, labs-wiki, graph, agents]
checkpoint_class: project-progress
checkpoint_class_rule: "title:phase 5"
retention_mode: compress
status: ingested
---

# Copilot Session Checkpoint Export

**Checkpoint title:** Phase 5 backfill script written
**Session ID:** `dad20dd5-0013-40b5-8fd6-bc371b7bc4d4`
**Checkpoint file:** `/home/jbl/.copilot/session-state/dad20dd5-0013-40b5-8fd6-bc371b7bc4d4/checkpoints/002-phase-5-backfill-script-writte.md`
**Checkpoint timestamp:** 2026-04-18T07:50:03.622663Z
**Exported:** 2026-04-18T07:53:30.006999Z
**Checkpoint class:** `project-progress` (rule: `title:phase 5`)
**Retention mode:** `compress`
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
Implementing Phase 5 of `labs-wiki/plans/copilot-session-checkpoint-curation.md` — a backlog cleanup that retro-classifies the existing 52 Copilot session checkpoint pages, demotes project-progress checkpoints to `tier: archive`, renormalizes their `quality_score`, then evaluates wiki quality, writes a report, and pushes to GitHub. Phases 1–4 already shipped and were merged to local labs-wiki main; homelab phase 1 is already pushed to origin/main.
</overview>

<history>
1. User asked to execute Phase 5, evaluate wiki quality, create a new report, and push to GitHub.
   - Re-read Phase 5 spec from the plan: review 52 existing checkpoints, retro-classify (keep/compress/archive), re-run quality normalization for zero-score pages, build a focused backlog.
   - Investigated existing quality machinery: `_compute_quality_score` in `auto_ingest.py:1529` and the duplicate in `lint_wiki.py:57`. All 52 source pages currently have `quality_score: 0` because post-processing predated the score logic.
   - Inserted Phase 5 + 6 quality gates into SQL tracker (`backfill-script-implemented`, `all-52-checkpoints-classified-in-fm`, `compress-pages-demoted-to-tier-archive`, `quality-scores-renormalized`, `graph-rebuilt-and-health-improved`, `backlog-report-written`). NOTE: SQL insert into `phases` failed with `NOT NULL constraint failed: phases.title` — needs retry with title.
   - Wrote `scripts/backfill_checkpoint_curation.py` — stdlib-only, idempotent backfill that classifies, stamps `checkpoint_class`/`retention_mode`, demotes to `tier: archive` for compress, recomputes `quality_score`. Has `--dry-run` and `--report PATH`.
   - Compaction triggered before running the script.
</history>

<work_done>
Files created:
- `/home/jbl/projects/labs-wiki/scripts/backfill_checkpoint_curation.py` — standalone backfill tool. Uses `checkpoint_classifier`, has `process_page(path)` that returns a diff record, mirrors `_compute_quality_score` logic, supports `--dry-run`/`--report`. Not yet executed.

Files modified:
- None yet in Phase 5.

SQL state:
- phases: phase-1..phase-4 = `done`. phase-5 row insert FAILED (missing `title` column NOT NULL constraint). Phase 5 gates were NOT inserted because the parent insert errored out — need to retry both with proper schema.

Git state:
- labs-wiki: on `main`, merge commit `3daad7a` (Phases 1–4 merged). `checkpoint-curation` branch deleted. Working tree currently has only the new untracked `scripts/backfill_checkpoint_curation.py`.
- homelab: `main` already pushed to `origin/main` (commit `4771537`).

Work completed:
- [x] Read Phase 5 spec
- [x] Inspected existing quality scoring code
- [x] Wrote backfill script
- [ ] Fix SQL phases/gates insert (title constraint)
- [ ] Run backfill `--dry-run` first to preview
- [ ] Run backfill for real (writes 52 files)
- [ ] Rebuild graph and verify `/graph/checkpoints` health improvement
- [ ] Generate backlog report
- [ ] Commit + push to GitHub
</work_done>

<technical_details>
- **SQL schema gotcha**: `phases` table has a NOT NULL `title` column. The Phase 1–4 inserts must have provided one. Phase 5 insert needs `(id, title, status)` not `(id, status)`. The phase_gates insert was in the same statement chain so it never ran either.
- **Quality score formula** (mirrored from `auto_ingest._compute_quality_score`, line 1529-1549): 25 pts for required fields ratio (`title`, `type`, `created`, `sources`), 25 pts for has_wikilinks OR has_related, 25 pts for non-empty `sources`, 25 pts for freshness (`last_verified` within 90 days) or 12 pts if just present. Max 100.
- **Backfill idempotency**: `upsert_fm_field` regex-replaces a key line or appends if missing. Skips list-style values (we never set lists). Safe to re-run.
- **Tier demotion**: `compress` → `tier: archive`, which `build_hot.py` already filters out (filters strictly on `tier: hot`). `skip` historically never produced pages; defensive code still archives them.
- **All 52 existing pages have `quality_score: 0`** — that's why Phase 5 includes renormalization. Expectation: most will rise to 50–75 after backfill since they have `title`/`type`/`created`/`sources` plus wikilinks.
- **No pre-existing tests** — verification is dry-run script output and graph metrics.
- **Networkx + FastAPI** for graph builder live in `/tmp/wgapi-venv` (created last session).
- **Plan baseline**: 2/52 = 0.038 synthesis_neighbor_ratio. Phase 5 won't change this directly (no new synthesis pages), but tier demotion will shift the `recommendations` distribution since `keep` requires `synthesis_neighbors>=1` AND `degree>=4`.
- **AGENTS.md commit trailer requirement**: include `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` on every commit.
- **User's "push to GitHub"** likely means `git push origin main` for labs-wiki (currently only local). Need to confirm whether labs-wiki has an origin remote first.
</technical_details>

<important_files>
- `/home/jbl/projects/labs-wiki/scripts/backfill_checkpoint_curation.py`
  - The Phase 5 workhorse. Not yet executed. Operates on `wiki/sources/copilot-session-checkpoint-*.md`.
  - Key entry point: `main()` — supports `--dry-run` and `--report PATH`.
  - `process_page` (~line 156): per-page diff record.
  - `compute_quality_score` (~line 122): mirrors auto_ingest logic.

- `/home/jbl/projects/labs-wiki/scripts/checkpoint_classifier.py`
  - Used by backfill for class/retention. Already shipped.

- `/home/jbl/projects/labs-wiki/scripts/auto_ingest.py`
  - Source of `_compute_quality_score` (line 1529) — mirrored in backfill.

- `/home/jbl/projects/labs-wiki/wiki-graph-api/graph_builder.py`
  - After backfill writes new tier values, rebuild the graph to measure improvement (`_checkpoint_health_report` at ~line 415).
  - Run via `/tmp/wgapi-venv/bin/python` since system python lacks networkx.

- `/home/jbl/projects/labs-wiki/wiki-graph-api/main.py`
  - `GET /graph/checkpoints` endpoint will surface new state.

- `/home/jbl/projects/labs-wiki/plans/copilot-session-checkpoint-curation.md`
  - Phase 5 spec at line 290. Defines success criteria.

- `/home/jbl/projects/labs-wiki/wiki/sources/copilot-session-checkpoint-*.md`
  - 52 target pages. All currently `tier: hot`, `quality_score: 0`, no `checkpoint_class` field.

- `/home/jbl/.copilot/session-state/dad20dd5-0013-40b5-8fd6-bc371b7bc4d4/plan.md`
  - Implementation outline. Update before continuing.
</important_files>

<next_steps>
Remaining work:
- Fix SQL insert for `phases` (provide `title`) and re-insert the 6 Phase 5 gates.
- Run `python3 scripts/backfill_checkpoint_curation.py --dry-run --report /tmp/phase5-dryrun.json` first to preview class/retention/score distribution. Sanity-check that ~23 will move to archive and most pages land 50-75 quality.
- Run for real without `--dry-run` — will modify 52 files.
- Rebuild graph: `/tmp/wgapi-venv/bin/python -m graph_builder --wiki wiki --out wiki/graph/graph.json` (or call build() directly). Verify `/graph/checkpoints` recommendations distribution shifts (expect more `keep` candidates as `quality_score` rises and `compress` candidates already-tagged drop out of hot tier).
- Write a final backlog report — markdown at `labs-wiki/plans/checkpoint-curation-phase5-report.md` listing keep/merge/compress/archive lists, before/after metrics, recommended next actions for the 6 merge clusters.
- Mark Phase 5 gates satisfied in SQL.
- Commit Phase 5 work with co-authored-by trailer.
- Check if labs-wiki has an `origin` remote (`git remote -v`). If yes, push. If not, ask user.

Immediate next steps:
1. Retry SQL with `INSERT INTO phases (id, title, status) VALUES ('phase-5', 'Phase 5: backfill cleanup', 'in_progress')`.
2. Run dry-run to verify backfill output looks sensible.
3. Execute backfill for real if dry-run looks clean.

Open questions:
- Does labs-wiki have a GitHub remote? Need to check before "push to github" step.
- Should the backlog report be committed to `plans/` or `wiki/`? Defaulting to `plans/` since it's a meta-document about the curation effort.
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
