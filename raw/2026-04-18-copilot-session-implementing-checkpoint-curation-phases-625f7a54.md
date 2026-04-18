---
title: "Copilot Session Checkpoint: Implementing checkpoint curation phases"
type: text
captured: 2026-04-18T07:39:27.069087Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, labs-wiki, mempalace, graph]
checkpoint_class: durable-architecture
checkpoint_class_rule: "body:graph-api"
retention_mode: retain
status: pending
---

# Copilot Session Checkpoint Export

**Checkpoint title:** Implementing checkpoint curation phases
**Session ID:** `dad20dd5-0013-40b5-8fd6-bc371b7bc4d4`
**Checkpoint file:** `/home/jbl/.copilot/session-state/dad20dd5-0013-40b5-8fd6-bc371b7bc4d4/checkpoints/001-implementing-checkpoint-curati.md`
**Checkpoint timestamp:** 2026-04-18T07:31:48.538086Z
**Exported:** 2026-04-18T07:39:27.069087Z
**Checkpoint class:** `durable-architecture` (rule: `body:graph-api`)
**Retention mode:** `retain`
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
The user asked me to invoke the `executing-plans` superpower skill and implement `labs-wiki/plans/copilot-session-checkpoint-curation.md`, a 5-phase plan to make Copilot session checkpoint promotion align with Karpathy's "compile once, reuse many" LLM Wiki pattern. After clarifying scope, I'm implementing Phases 1–4 (deferring Phase 5's 52-page backlog cleanup) on a feature branch `checkpoint-curation`, with cross-repo edits spanning `labs-wiki` and `homelab`. The user requested a progress tracker with quality gates per phase, which I'm maintaining in SQL.
</overview>

<history>
1. User asked me to invoke the `executing-plans` skill and implement the curation plan with quality gates per phase.
   - Loaded the skill and read the full plan from `labs-wiki/plans/copilot-session-checkpoint-curation.md`.
   - Surveyed labs-wiki repo (dirty tree on main, ~150 untracked auto-ingest files; on branch `main`).
   - Queried MemPalace `labs_wiki` wing for prior context.

2. I raised concerns and asked three scoping questions:
   - Branch handling → user chose: create feature branch `checkpoint-curation`, commit dirty state as WIP first.
   - Scope → user chose: Phases 1–4, defer Phase 5.
   - Cross-repo → user chose: yes, edit `homelab/scripts/mempalace-session-curator.py`.

3. Set up infrastructure:
   - Created branch `checkpoint-curation`, committed dirty WIP state (commit `9d396b5`).
   - Created SQL `phases` + `phase_gates` tables tracking 4 phases with 3–5 gates each.
   - Wrote plan summary to session `plan.md`.

4. Explored relevant code: `auto_ingest.py` (2010 lines), `watch_raw.py`, `build_hot.py`, `snapshot_hot.py`, `mempalace-session-curator.py` (370 lines), `wiki-graph-api/graph_builder.py` (514 lines), `wiki-graph-api/main.py`. Confirmed no existing tests in repo.

5. Started Phase 1 (in progress): Created shared `checkpoint_classifier.py` module, wired it into both the homelab curator and `auto_ingest.py`'s `classify_ingest_route`. Mid-implementation when compaction triggered.
</history>

<work_done>
Files created:
- `/home/jbl/projects/labs-wiki/scripts/checkpoint_classifier.py` — Shared, stdlib-only classifier with 5 classes (`durable-architecture`, `durable-debugging`, `durable-workflow`, `project-progress`, `low-signal`) and 3 retention modes (`retain`, `compress`, `skip`). Exposes `classify_checkpoint(title, content) -> CheckpointClassification` and `resolve_retention(cls, env=None) -> str`. Heuristic ordering: debugging → architecture → workflow → progress, with title-priority then body-fallback, and `_LOW_SIGNAL_MIN_CHARS=600`. Env override via `LABS_WIKI_CHECKPOINT_RETENTION_OVERRIDES="class=mode,..."`.
- `/home/jbl/.copilot/session-state/dad20dd5-0013-40b5-8fd6-bc371b7bc4d4/plan.md` — Implementation outline for all 4 phases.

Files modified:
- `/home/jbl/projects/homelab/scripts/mempalace-session-curator.py` — Added `sys.path` insert for `~/projects/labs-wiki/scripts`, imported classifier with stub fallback, added `checkpoint_class`/`checkpoint_class_rule`/`retention_mode` to `Candidate` dataclass, updated `build_raw_content` to emit those into raw frontmatter and body header, classified during `collect_candidates`, persisted class+retention into state file, updated dry-run print to show `[class/retention]`.
- `/home/jbl/projects/labs-wiki/scripts/auto_ingest.py` — Imported classifier, extended `IngestRoute` dataclass with `checkpoint_class: str = ""` and `retention_mode: str = RETAIN`, rewrote the `copilot-session-curator` branch in `classify_ingest_route` to honour fm-supplied class or re-classify via `body` arg; signature gained `body: str | None = None`.

Git state:
- Branch `checkpoint-curation`, one commit ahead of `main` (`9d396b5` — WIP snapshot).
- Phase 1 changes are NOT yet committed.

SQL tracker state:
- `phases`: phase-1 = `in_progress`; phase-2/3/4 = `pending`. No gates marked satisfied yet.

Work completed:
- [x] Branch + WIP commit + SQL tracker
- [x] Phase 1: classifier module
- [x] Phase 1: curator integration (homelab)
- [x] Phase 1: `IngestRoute` extended + `classify_ingest_route` honours class
- [ ] Phase 1: callers of `classify_ingest_route` need to pass `body=` (currently still call without it — re-classification fallback won't trigger for legacy raw files)
- [ ] Phase 1: `generate_source_page` should emit `checkpoint_class` in source-page frontmatter
- [ ] Phase 1: dry-run verification across existing 52 checkpoints (the gate)
- [ ] Phase 1: docs update in `labs-wiki/docs/workflows.md`
- [ ] Phases 2, 3, 4 not started
</work_done>

<technical_details>
- **Classifier design**: pure stdlib, regex-based, deterministic. Title-only match wins over body match. Order matters in `_PATTERNS`: debugging first (most specific), then architecture, workflow, progress. Below `_LOW_SIGNAL_MIN_CHARS=600` with no signal → low-signal; otherwise fallback → project-progress (errs toward compression, not retention).
- **Retention defaults**: durable-* → retain, project-progress → compress, low-signal → skip. Override via env `LABS_WIKI_CHECKPOINT_RETENTION_OVERRIDES`.
- **Cross-repo sharing**: homelab curator imports the classifier by `sys.path.insert(0, ~/projects/labs-wiki/scripts)` with a try/except stub fallback so curator still works if labs-wiki is missing. Avoids duplicating taxonomy in two repos.
- **`classify_ingest_route` callers**: `auto_ingest.py` calls it twice in `ingest_raw_source` (lines ~1683 and ~1702 pre-edit, now shifted) and once in `watch_raw.py:_process_pending` (line 95). All currently call without `body=` — need updating so the re-classification fallback works on legacy raw files that lack `checkpoint_class` in frontmatter.
- **Source-page generation**: `generate_source_page` (line ~1004) currently produces frontmatter with `tier: hot` hardcoded and `quality_score: 0`. Phase 2 will need this to write `tier: archive` for `compress` mode and possibly emit `checkpoint_class`. The function's signature would need to accept the route or class.
- **`build_hot.py` filtering**: `hot_tier_pages()` (line 114) regexes `tier: hot` from fm — Phase 2 needs to also exclude `tier: archive`. Trivial.
- **Graph builder**: `Page` dataclass already carries `page_type`, `tier`, `quality_score`, `tags`. Phase 4 can detect checkpoints by `page_type=='source'` and title prefix `Copilot Session Checkpoint`. Need new metric pass + serialization fields.
- **No tests exist** — verification will be dry-run scripts that print classifier output / graph metrics.
- **Dirty WIP commit**: `9d396b5` includes prior auto-ingest output and unrelated edits to `auto_ingest.py`/`workflows.md`. The Phase 1 edits are layered on top of it.
- **Open assumption**: heuristics in `_PATTERNS` are first-pass; need to validate against all 52 existing checkpoints during the Phase 1 quality gate. May need tuning.
</technical_details>

<important_files>
- `/home/jbl/projects/labs-wiki/scripts/checkpoint_classifier.py`
  - Shared classifier — single source of truth for class taxonomy and retention policy.
  - Newly created. Read top-level docstring for design constraints.

- `/home/jbl/projects/labs-wiki/scripts/auto_ingest.py`
  - Main ingest pipeline. Phase 1 partially wired.
  - Imports added near line 27. `IngestRoute` extended (~line 72). `classify_ingest_route` rewritten (~line 81). `ingest_raw_source` calls at lines ~1683 and ~1702 still need `body=body` arg. `generate_source_page` at line ~1004 needs Phase 2 changes.

- `/home/jbl/projects/labs-wiki/scripts/watch_raw.py`
  - Calls `classify_ingest_route` at line 95 — needs `body=` once we pass it through.

- `/home/jbl/projects/labs-wiki/scripts/build_hot.py`
  - `hot_tier_pages()` line 114: Phase 2 needs to exclude `tier: archive`.

- `/home/jbl/projects/homelab/scripts/mempalace-session-curator.py`
  - Promotes checkpoints into labs-wiki/raw. Phase 1 fully wired: imports classifier, classifies + writes class/retention into raw frontmatter and state.

- `/home/jbl/projects/labs-wiki/wiki-graph-api/graph_builder.py`
  - Graph extraction. Phase 4 will add checkpoint health metrics — extend `analyze_graph` and `to_node_link` (~line 365 and ~417).

- `/home/jbl/projects/labs-wiki/wiki-graph-api/main.py`
  - FastAPI service. Phase 4 will add `GET /graph/checkpoints` endpoint.

- `/home/jbl/projects/labs-wiki/plans/copilot-session-checkpoint-curation.md`
  - The plan being executed. Phase definitions, success criteria, and Karpathy alignment standard.

- `/home/jbl/.copilot/session-state/dad20dd5-0013-40b5-8fd6-bc371b7bc4d4/plan.md`
  - My implementation outline. Reference for resuming.
</important_files>

<next_steps>
Resume Phase 1:
1. Pass `body=body` (or `body=content`) into the second `classify_ingest_route` call inside `ingest_raw_source` (after URL fetch) so re-classification works on legacy raws. Also update the call in `watch_raw.py` (uses parsed fm but no body — body would need to be re-read; alternative: skip body fallback there since priority sort doesn't need class).
2. Modify `generate_source_page` to accept (or read from extraction context) the `checkpoint_class` and emit it in frontmatter when present.
3. Run the Phase 1 quality gate: write a small dry-run script that walks `wiki/sources/copilot-session-checkpoint-*.md`, reads the raw they came from (`sources:` field), classifies, and prints class distribution. Mark gates satisfied in SQL.
4. Update `labs-wiki/docs/workflows.md` with the classification step.
5. Commit Phase 1 with co-authored-by trailer.

Then Phase 2:
- Implement retention behaviour in `ingest_raw_source`: `skip` short-circuits before LLM call (mark raw `ingested-skipped`); `compress` proceeds but writes source page with `tier: archive`.
- Update `build_hot.py` `hot_tier_pages()` to exclude `tier: archive`.
- Dry-run gate: simulate retention on the 52 existing checkpoints and confirm `archive` pages drop from `build_hot.py` output.

Then Phases 3 (synthesis triggers from checkpoint families) and 4 (graph health endpoint) per the session `plan.md`.

After all phases: invoke `superpowers:finishing-a-development-branch` per executing-plans skill.

Blockers / open questions:
- None blocking. The heuristic taxonomy may need tuning after the Phase 1 dry-run reveals class distribution.
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
