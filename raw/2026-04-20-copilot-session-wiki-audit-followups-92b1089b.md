---
title: "Copilot Session Checkpoint: Wiki Audit Followups"
type: text
captured: 2026-04-20T03:15:13.565976Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, labs-wiki, nba-ml-engine, mempalace, graph, agents, dashboard]
checkpoint_class: durable-architecture
checkpoint_class_rule: "body:move to"
retention_mode: retain
status: ingested
---

# Copilot Session Checkpoint Export

**Checkpoint title:** Wiki Audit Followups
**Session ID:** `e4f60aff-3e51-4282-aab3-40c240aad5fa`
**Checkpoint file:** `/home/jbl/.copilot/session-state/e4f60aff-3e51-4282-aab3-40c240aad5fa/checkpoints/002-wiki-audit-followups.md`
**Checkpoint timestamp:** 2026-04-20T03:11:17.592792Z
**Exported:** 2026-04-20T03:15:13.565976Z
**Checkpoint class:** `durable-architecture` (rule: `body:move to`)
**Retention mode:** `retain`
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
The conversation started with operational debugging in `nba-ml-engine` and `homelab`: fix a false training state on the homepage, repair Immich LAN/public DNS, verify and adjust the NBA ML Ofelia scheduler, optimize the NBA ML agent/skill surfaces, merge those changes, and clean up merged branches. It then shifted to knowledge-system work in `labs-wiki`: audit how Copilot session checkpoints are promoted into the wiki and MemPalace, write and push a report aligned with the latest curation plans and Karpathy’s *LLM Wiki* gist, and begin implementing the report’s next steps under a GitHub Models free-tier constraint. The overall approach was: diagnose live behavior first, make targeted code/config fixes, validate with real runtime evidence, document the results, and then move to process hardening in `labs-wiki` using a clean git worktree.
</overview>

<history>
1. The user asked to check the `nba-ml-api` pipeline because the homepage showed stage `2/10` and “shouldn’t be training right now.”
   - Investigated `nba-ml-engine/src/training/status.py`, `src/api/server.py`, trainer hooks, and the homepage service wiring in `homelab/config/homepage/services.yaml`.
   - Verified the live homelab state with a subagent.
   - Found the real issue: a weekly retrain had been killed with exit code `137`, leaving `/tmp/training_status.json` stuck with `running: true`.
   - Fixed stale/dead-run handling in `src/training/status.py`, adjusted stage display formatting in `src/api/server.py`, added `tests/test_training_status.py`, deployed, and confirmed live `/training/status` returned idle again.

2. The user asked to fix Immich DNS for `photos.jbl-lab.com` on LAN and public internet.
   - Inspected `homelab/compose/compose.photos.yml`, `config/adguard/dns-rewrites.json`, and Cloudflare tunnel docs.
   - Determined public DNS and tunnel were already fine; the problem was LAN split-DNS.
   - Added `photos.jbl-lab.com` as a Cloudflare override in `homelab/config/adguard/dns-rewrites.json`, updated `homelab/docs/08-cloudflare-tunnel.md`, synced rewrites, and verified HTTPS worked on LAN and public.

3. The user asked to check that Ofelia cron jobs were enabled for `nba-ml-api`, move props ingest to 4pm EDT, evaluate and optimize skills/agents for NBA ML Engine across VS Code / Copilot CLI / OpenCode, create feature branches, push, and merge.
   - Verified live Ofelia jobs were already enabled and healthy.
   - Updated `homelab/compose/compose.nba-ml.yml` so `props-refresh` runs at `20:00 UTC` (4pm EDT / 3pm EST), and updated docs in `homelab` and `nba-ml-engine`.
   - Audited `nba-ml-engine` agent/skill surfaces and made `.github/skills/` canonical, mirrored them under `.opencode/skills/`, added VS Code settings, and converted the old Copilot prompt into a compatibility shim.
   - Added `tests/test_sprint61.py`, ran code review, fixed a corrupted `dashboard` skill file, synchronized OpenCode skill content, removed a broken symlink, reran tests, and merged/pushed both repos to `main`.

4. The user asked to clean up branches if they were merged to `main`.
   - Listed merged local and remote branches in `homelab` and `nba-ml-engine`.
   - Deleted merged local `feature/*` and `fix/*` branches and removed the corresponding remote branches where present.
   - Pruned stale remote-tracking refs in `homelab`.
   - Left non-feature branches like `cloudflare` and `v2` untouched.

5. The user asked to check that the full retrain for `nba-ml-api` was tonight/tomorrow and turned on.
   - Loaded scheduler context from the repo and MemPalace, then checked live Docker state through a homelab subagent.
   - Verified `nba-ml-scheduler` was running, `ofelia.enabled=true`, and the live labels were:
     - `pipeline-daily = 0 0 7 * * *`
     - `weekly-retrain = 0 0 16 * * 0`
   - Confirmed the next runs from `2026-04-19T21:01 EDT` were:
     - daily pipeline at `2026-04-20 03:00 EDT / 07:00 UTC`
     - weekly retrain at `2026-04-20 12:00 EDT / 16:00 UTC`
   - Reported that the full retrain was enabled, but scheduled for Sunday noon EDT, not overnight.

6. The user asked to review the Copilot sessions added to the wiki “today,” assess whether the right information was being captured, optimize the process, and check whether MemPalace was adding correct details and removing stale memories.
   - Searched `labs-wiki`, `copilot_sessions`, and today’s `raw/` and `wiki/` outputs.
   - Compared the raw session checkpoint exports with the generated wiki source pages and the MemPalace sync scripts.
   - Found that today’s `Sprint 60` and `Sprint 61` checkpoint pages were faithful source summaries, but they were planning-heavy and were being over-promoted into concept/entity pages.
   - Verified `labs_wiki_knowledge` parity was clean (415 wiki pages, 415 collection docs, 0 orphaned docs) but noticed the sync script only upserted and did not prune orphans.
   - Updated `labs-wiki/scripts/auto_ingest.py` to suppress concept/entity/synthesis extraction for planning-only `project-progress` checkpoints and normalize checkpoint source-page metadata.
   - Updated `labs-wiki/scripts/wiki_to_mempalace.py` to prune orphaned drawers for renamed/deleted wiki pages.
   - Updated `labs-wiki/README.md`, `docs/memory-model.md`, and `docs/live-memory-loop.md` to document the revised checkpoint and MemPalace behavior.
   - Validated the planning-only heuristic on today’s three raw checkpoint files and confirmed `wiki_to_mempalace.py --dry-run` still saw 0 orphaned wiki drawers.
   - Tried to apply `scripts/backfill_checkpoint_curation.py` to existing checkpoint pages, but it failed because many `wiki/sources/copilot-session-checkpoint-*.md` files were root-owned by the ingest container.

7. The user then asked to write a report to `labs-wiki/plans` describing what was done, pros/cons based on the latest plans and Karpathy’s gist, and push it to GitHub.
   - Loaded the latest `plans/` files: `copilot-session-checkpoint-curation.md`, `checkpoint-curation-phase5-report.md`, `mempalace-implementation-report.md`, and `mempalace-next-steps.md`, plus Karpathy’s gist.
   - Wrote `labs-wiki/plans/copilot-session-wiki-memory-audit-2026-04-19.md`.
   - Initially committed on the dirty main worktree and hit a non-fast-forward push rejection because `origin/main` moved.
   - Used a clean git worktree `.worktrees/report-sync`, cherry-picked the commit, validated the scripts there, pushed successfully to `origin/main`, and removed the temporary worktree.
   - The pushed commit on `labs-wiki/main` is `c4951aa` with message `docs: report session wiki audit`.

8. The user next asked to implement the audit file’s next steps, with the backfill done in a limited fashion because they are using the GitHub Models API free tier, then create a summary report and evaluation.
   - Created a new clean worktree at `/home/jbl/projects/labs-wiki/.worktrees/audit-followups` on branch `feature/audit-followups` from `origin/main`; baseline `py_compile` checks passed.
   - Loaded the audit report and inspected the likely implementation files:
     - `labs-wiki/Dockerfile.auto-ingest`
     - `homelab/compose/compose.wiki.yml`
     - `labs-wiki/scripts/backfill_checkpoint_curation.py`
     - existing `scripts/backfill_checkpoint_cluster_synthesis.py`
   - Determined the likely ownership bug source: `wiki-auto-ingest` runs as root by default and bind-mounts `raw/` and `wiki/`, which explains root-owned generated files.
   - Confirmed that a cluster-synthesis backfill script already exists, which may be usable for a limited, low-spend Phase 5-style synthesis pass.
   - At the moment of compaction, implementation of these next steps had not started yet; the worktree was prepared and the assessment was underway.
</history>

<work_done>
Files created/modified/deleted across the conversation:

**`nba-ml-engine`**
- Modified:
  - `src/training/status.py`
  - `src/api/server.py`
  - `AGENTS.md`
  - `.github/copilot-instructions.md`
  - `.github/prompts/execute-sprint-from-report.prompt.md`
  - `README.md`
  - `docs/01-architecture.md`
  - `docs/05-training-pipeline.md`
  - `docs/10-notifications.md`
  - `main.py`
  - `tests/test_sprint61.py`
- Added:
  - `tests/test_training_status.py`
  - `.github/skills/sprint-orchestrator/SKILL.md`
  - `.github/skills/nba-ml-pipeline/SKILL.md`
  - `.github/skills/model-calibration/SKILL.md`
  - `.github/skills/feature-lab/SKILL.md`
  - `.github/skills/data-quality/SKILL.md`
  - `.github/skills/backtest-lab/SKILL.md`
  - `.github/skills/dashboard/SKILL.md`
  - matching mirrors under `.opencode/skills/`
  - `.vscode/settings.json`
  - `.vscode/extensions.json`
- Deleted:
  - `.opencode/skills/execute-sprint-from-report/execute-sprint-from-report` (broken symlink)

**`homelab`**
- Modified:
  - `compose/compose.nba-ml.yml`
  - `config/adguard/dns-rewrites.json`
  - `docs/05-service-guide.md`
  - `docs/08-cloudflare-tunnel.md`

**`labs-wiki`**
- Modified and pushed to `main` in commit `c4951aa`:
  - `README.md`
  - `docs/live-memory-loop.md`
  - `docs/memory-model.md`
  - `scripts/auto_ingest.py`
  - `scripts/wiki_to_mempalace.py`
- Added and pushed:
  - `plans/copilot-session-wiki-memory-audit-2026-04-19.md`

**Session/worktree state**
- Temporary worktree used and removed:
  - `/home/jbl/projects/labs-wiki/.worktrees/report-sync`
- Current active worktree:
  - `/home/jbl/projects/labs-wiki/.worktrees/audit-followups`
  - Branch: `feature/audit-followups`
  - Created from `origin/main`
  - Baseline compile checks passed
- Original `labs-wiki` main worktree is still dirty with many generated `raw/` and `wiki/` files from prior ingestion activity; those were intentionally left out of the pushed report commit.

Completed tasks:
- [x] Diagnose and fix stale NBA ML homepage training status.
- [x] Add regression coverage for stale/dead training status.
- [x] Fix `photos.jbl-lab.com` LAN/public DNS routing.
- [x] Verify Ofelia scheduler was enabled live.
- [x] Move `props-refresh` to `20:00 UTC / 4pm EDT`.
- [x] Optimize NBA ML agent/skill surfaces and merge to `main`.
- [x] Clean up merged `feature/*` and `fix/*` branches.
- [x] Verify the live weekly retrain schedule and enabled state.
- [x] Audit today’s Copilot session wiki promotion behavior.
- [x] Improve `labs-wiki` checkpoint promotion and MemPalace sync logic.
- [x] Write and push the audit report to `labs-wiki/plans`.

Current state:
- `nba-ml-engine/main` and `homelab/main` already include the earlier bugfixes/scheduler/docs/agent-surface work.
- `labs-wiki/main` includes the audit report and the process fixes for planning-only checkpoint suppression and MemPalace orphan pruning.
- The audit follow-up implementation is **in progress** in the clean `labs-wiki` worktree; no new code has been committed there yet.
- A key unresolved operational issue remains: some existing checkpoint pages in `labs-wiki/wiki/sources/` are owned by `root`, which blocks host-side backfill/normalization.

Open issues encountered:
- `backfill_checkpoint_curation.py` cannot rewrite some existing checkpoint source pages because of file ownership (`PermissionError` on root-owned files).
- `labs-wiki` main worktree is dirty, so all new implementation work was moved to a clean worktree.
- `git push origin main` from the original dirty worktree failed once due to non-fast-forward; resolved by using a clean worktree and cherry-picking the commit.
</work_done>

<technical_details>
- **NBA ML stale training bug**
  - Root cause was not the homepage widget; it was stale state in `/tmp/training_status.json` after a killed retrain.
  - The retrain had died with exit code `137`, leaving `running: true`.
  - The fix added PID tracking, stale/dead-run normalization, and proper failed/non-running persistence in `src/training/status.py`.
  - `/training/status` stage display was normalized to 1-based semantics in `src/api/server.py`.
  - A pre-existing unrelated issue remained in `tests/test_api_auth.py::test_health_no_auth_required`, which already returned 500.

- **Immich split-DNS**
  - Public DNS and Cloudflare tunnel were already healthy.
  - The real issue was missing LAN exact-host overrides, not the tunnel itself.
  - Adding `photos.jbl-lab.com` as a Cloudflare override to AdGuard fixed LAN HTTPS.

- **Ofelia details**
  - Ofelia uses **6-field cron**: `sec min hour day month weekday`.
  - Live scheduler validation showed:
    - `pipeline-daily = 0 0 7 * * *`
    - `weekly-retrain = 0 0 16 * * 0`
  - At `2026-04-19 21:01 EDT`, the next runs were:
    - daily pipeline: `2026-04-20 03:00 EDT / 07:00 UTC`
    - weekly retrain: `2026-04-20 12:00 EDT / 16:00 UTC`
  - The full retrain was enabled, but scheduled for Sunday noon EDT, not overnight.

- **NBA ML agent/skill surface decision**
  - `.github/skills/` is the canonical project skill layer.
  - `.opencode/skills/` mirrors the same content for OpenCode.
  - `.github/prompts/execute-sprint-from-report.prompt.md` is now only a compatibility shim.

- **Labs-wiki audit findings**
  - Today’s `Sprint 60` and `Sprint 61` session checkpoint pages were **faithful source summaries** but **planning-only**, so they should not have minted durable concepts/entities.
  - `Scheduler DNS Agents Cleanup` was the right kind of durable debugging checkpoint and should remain first-class.
  - This aligned with `plans/copilot-session-checkpoint-curation.md`, which already argued for retaining durable checkpoints while compressing `project-progress` material.

- **New `labs-wiki` process logic**
  - `scripts/auto_ingest.py` now:
    - detects planning-only `project-progress` checkpoints,
    - suppresses concept/entity/synthesis extraction for them,
    - still keeps the source summary page,
    - normalizes `checkpoint_class`, `retention_mode`, and `tier` on checkpoint source pages.
  - The heuristic specifically keys off:
    - title hints like `planning`, `audit`, `exploration`,
    - body hints like `<next_steps>`, `open questions`, `plan + tracker`, `sql todos seeded`,
    - “no execution” phrases like `no code changes made this session`,
    - and avoids suppressing content with clear execution hints like completed implementation/tests/deploy/merge.
  - The heuristic was validated on the three current raw checkpoint files and behaved as intended.

- **MemPalace sync details**
  - Before the change, `scripts/wiki_to_mempalace.py` only upserted stable IDs; it did not delete drawers for renamed/deleted wiki pages.
  - After the change, it still upserts stable IDs but also prunes orphaned drawers in `labs_wiki_knowledge`.
  - Validation showed current parity was clean: 415 wiki pages, 415 injected docs, 0 orphaned docs.

- **Quality scoring clarification**
  - `quality_score` in `labs-wiki` is structural: completeness, cross-links, attribution, and recency.
  - It is **not** an “execution certainty” or “this work happened” signal.
  - The pushed docs now state that explicitly.

- **Backfill limitation / free-tier constraint**
  - `scripts/backfill_checkpoint_curation.py` is a **non-LLM** metadata normalizer; it does not spend GitHub Models budget.
  - There is already an existing `scripts/backfill_checkpoint_cluster_synthesis.py` that **does** call the LLM for Phase 5 cluster synthesis.
  - The current implementation request was heading toward a **limited backfill/synthesis pass** to stay within the GitHub Models free tier.
  - At the time of compaction, the likely plan was:
    - fix file ownership first,
    - use cheap/non-LLM backfill widely,
    - and keep any LLM-based synthesis backfill narrowly scoped.

- **File ownership bug**
  - `labs-wiki/wiki/sources/copilot-session-checkpoint-*.md` files like:
    - `copilot-session-checkpoint-sprint-60-pts-feature-planning.md`
    - `copilot-session-checkpoint-sprint-61-planning-audit.md`
    - `copilot-session-checkpoint-scheduler-dns-agents-cleanup.md`
    are owned by `root`.
  - `homelab/compose/compose.wiki.yml` currently runs `wiki-auto-ingest` without a `user:` override.
  - `labs-wiki/Dockerfile.auto-ingest` is a simple Python image and defaults to root.
  - This strongly suggests the container’s default root user is the source of the host-side ownership problem.

- **Git/worktree state**
  - The report commit originally landed on dirty local `main` as `61d2e9f`, but push failed because remote `main` had moved.
  - A clean worktree from `origin/main` was created, the commit was cherry-picked, and pushed successfully as `c4951aa`.
  - Current implementation work is isolated in another clean worktree on branch `feature/audit-followups`.
</technical_details>

<important_files>
- `labs-wiki/plans/copilot-session-wiki-memory-audit-2026-04-19.md`
  - The main audit report the user explicitly requested and that was pushed to GitHub.
  - It documents the Copilot session → wiki → MemPalace audit, pros/cons, Karpathy alignment, and recommended next steps.
  - Key sections: “Summary,” “Validation,” “Recommended next steps,” and “Bottom line.”

- `labs-wiki/scripts/auto_ingest.py`
  - Central file for checkpoint promotion into wiki pages.
  - Modified to add `is_planning_only_checkpoint`, suppress concept/entity/synthesis extraction for planning-only `project-progress` checkpoints, and normalize checkpoint source-page metadata.
  - Important sections:
    - route classification / planning-only helpers near the top after `classify_ingest_route`
    - `generate_source_page`
    - `normalize_checkpoint_source_page`
    - planning-only suppression block in `ingest_raw_source`
    - checkpoint-family synthesis trigger later in the file

- `labs-wiki/scripts/wiki_to_mempalace.py`
  - Controls wiki → MemPalace injection into `labs_wiki_knowledge`.
  - Modified to prune orphaned drawers for renamed/deleted wiki pages while preserving stable-ID upsert behavior.
  - Important sections:
    - module docstring / purpose
    - ChromaDB collection initialization
    - desired ID collection
    - orphan detection and deletion
    - dry-run orphan reporting

- `labs-wiki/scripts/backfill_checkpoint_curation.py`
  - Existing script used to normalize older checkpoint source pages.
  - Important because it was the first attempted backfill path and exposed the root-owned file problem.
  - Key sections:
    - `process_page`
    - frontmatter upsert logic
    - report generation
    - write path near the end (`(ROOT / r["path"]).write_text(...)`), which hit `PermissionError`.

- `labs-wiki/scripts/backfill_checkpoint_cluster_synthesis.py`
  - Existing script for Phase 5-style checkpoint-cluster synthesis backfill.
  - Important for the current in-progress task because it may provide the “limited” LLM-based backfill path under the GitHub Models free tier.
  - Key areas (from grep): cluster discovery, title construction, `call_llm_synthesis`, page generation, and log/report writing.

- `homelab/compose/compose.wiki.yml`
  - Central to the likely ownership fix.
  - Defines `wiki-ingest-api` and `wiki-auto-ingest`.
  - `wiki-auto-ingest` bind-mounts `${WIKI_INGEST_PATH}/raw` and `/wiki` and currently has no `user:` override.
  - Likely place to change runtime UID/GID handling so generated files are not root-owned.

- `labs-wiki/Dockerfile.auto-ingest`
  - Builds the `wiki-auto-ingest` container.
  - Very simple Python image that defaults to running as root.
  - Important for determining whether ownership should be fixed in the container image, the compose file, or both.

- `labs-wiki/README.md`
  - Updated and pushed.
  - Now clarifies that `quality_score` is structural and adds the checkpoint policy summary.

- `labs-wiki/docs/memory-model.md`
  - Updated and pushed.
  - Now documents that `quality_score` is not an execution-confidence signal and explains the Copilot session checkpoint retention policy.

- `labs-wiki/docs/live-memory-loop.md`
  - Updated and pushed.
  - Now states that `wiki_to_mempalace.py` prunes orphaned drawers so `labs_wiki_knowledge` stays aligned with the filesystem.

- `labs-wiki/plans/copilot-session-checkpoint-curation.md`
  - Baseline plan that guided the audit and still guides the current follow-up implementation.
  - Important sections:
    - goals and Karpathy alignment
    - Phase 2 (retention vs extraction)
    - Phase 3 (synthesis)
    - Phase 4 (graph-aware curation)

- `labs-wiki/plans/checkpoint-curation-phase5-report.md`
  - Existing evaluation report for backlog checkpoint curation.
  - Important because it recommends synthesis pages for merge clusters and is the source for the “limited backfill” follow-up work.

- `homelab/config/homepage/services.yaml`
  - Important earlier in the conversation for diagnosing the false NBA ML homepage training state.
  - Confirmed the homepage Training Pipeline widget reads `http://nba-ml-api:8000/training/status`.

- `nba-ml-engine/src/training/status.py`
  - Important earlier fix: stale/dead training run normalization with PID tracking and stale status cleanup.

- `nba-ml-engine/src/api/server.py`
  - Important earlier fix: corrected failed stage display and normalized `/training/status` output.

- `homelab/compose/compose.nba-ml.yml`
  - Important earlier fix: updated `props-refresh` schedule and verified live Ofelia labels.
  - Also served as the source-of-truth when checking retrain schedule and enabled state.
</important_files>

<next_steps>
Remaining work:
- Implement the next steps from `plans/copilot-session-wiki-memory-audit-2026-04-19.md` in the clean `labs-wiki` worktree.
- Keep the backfill limited enough to respect GitHub Models free-tier usage.
- Create the requested follow-up summary report and evaluation after implementation.

Immediate next steps:
1. **Decide exact implementation scope for the audit follow-ups**
   - Likely minimum set:
     - fix file ownership for generated wiki files,
     - add an explicit execution-status / knowledge-state signal,
     - implement a limited backfill path,
     - produce a summary/evaluation report.
   - The synthesis step should probably be limited, not full-cluster across the whole backlog.

2. **Implement the ownership fix**
   - Most likely in `homelab/compose/compose.wiki.yml` by running `wiki-auto-ingest` as `${PUID}:${PGID}` or similar.
   - Possibly adjust `labs-wiki/Dockerfile.auto-ingest` if needed.
   - Because this touches homelab deployment, the `homelab-deploy` skill was invoked and the relevant source-of-truth files were read.

3. **Add a limited backfill mechanism**
   - `scripts/backfill_checkpoint_curation.py` already performs metadata-only normalization without LLM cost.
   - The likely next step is to extend it to support targeted subsets (specific pages, recent pages, changed pages, or a limit count) so it can be run cheaply and surgically.
   - For any LLM-backed synthesis backfill, inspect and potentially constrain `scripts/backfill_checkpoint_cluster_synthesis.py` with filters like top N clusters / max clusters / dry-run review before spending requests.

4. **Add an explicit execution-status signal**
   - The audit suggested something like `knowledge_state: planned | executed | validated`.
   - This likely belongs in generated checkpoint source-page frontmatter and in docs.
   - It may also require a classification helper or source-page normalization path in `auto_ingest.py`.

5. **Consider updating the session `plan.md`**
   - Reminder was present, but `plan.md` still reflects the earlier NBA ML work.
   - It has not yet been updated for the new `labs-wiki` audit-followup task.

6. **After implementation, validate and report**
   - Re-run baseline compile checks.
   - Run dry-run backfill / limited synthesis previews.
   - If the ownership fix is applied locally/deployed, retry the previously blocked backfill on the relevant checkpoint source pages.
   - Then write the follow-up summary report and evaluation in `labs-wiki/plans/`, commit, and push.

Blockers / open questions:
- Whether the user wants only the **low-cost metadata/backfill + ownership** next steps, or also a **small LLM-backed synthesis batch** in the same pass.
- Whether the ownership fix should be made only in repo config or also deployed live to the homelab during this task.
- Whether the explicit execution-status field should apply only to checkpoint source pages or also to concepts derived from them.
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
