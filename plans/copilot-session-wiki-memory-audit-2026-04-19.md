# Copilot Session → Wiki → MemPalace Audit Report

**Date:** 2026-04-19  
**Scope:** review today's Copilot session checkpoint ingests, compare the current behavior against the latest `plans/` documents and Karpathy's *LLM Wiki* gist, document the changes made, and judge whether MemPalace is capturing the right details while removing stale memory.

---

## Summary

The pipeline is structurally sound, but it was still too permissive at the point where session checkpoints became durable wiki knowledge.

Today's review found a clean split:

- `Scheduler DNS Agents Cleanup` behaved like a durable debugging checkpoint and deserved first-class wiki treatment.
- `Sprint 60 PTS Feature Planning` and `Sprint 61 Planning + Audit` were useful provenance artifacts, but they were planning-heavy checkpoints that should not have minted standalone concept pages.

That gap mattered because it cut against the direction in [`copilot-session-checkpoint-curation.md`](copilot-session-checkpoint-curation.md) and against Karpathy's central idea: the wiki should be a compounding artifact that preserves durable insight, not a second chat log with nicer formatting.

I tightened the pipeline in two places:

1. **Checkpoint promotion policy**
   - Added planning-only detection for `project-progress` checkpoints.
   - Kept planning-heavy checkpoints as archived source summaries.
   - Suppressed concept, entity, and synthesis extraction for those planning-only checkpoints.

2. **Wiki → MemPalace synchronization**
   - Updated `scripts/wiki_to_mempalace.py` to prune orphaned drawers when wiki pages are renamed or deleted, not just upsert current pages forever.

I also added source-page normalization so checkpoint pages consistently carry `checkpoint_class`, `retention_mode`, and the right `tier`, and I clarified the docs so `quality_score` is no longer mistaken for an execution-confidence signal.

---

## What I did

### 1. Audited today's ingests

I reviewed the raw checkpoint exports created today:

- `raw/2026-04-19-copilot-session-sprint-60-pts-feature-planning-abd21993.md`
- `raw/2026-04-19-copilot-session-sprint-61-planning-audit-6c5cb258.md`
- `raw/2026-04-20-copilot-session-scheduler-dns-agents-cleanup-2222559c.md`

I compared those against the compiled wiki source pages and the current promotion pipeline in:

- `homelab/scripts/mempalace-session-curator.py`
- `labs-wiki/scripts/auto_ingest.py`
- `labs-wiki/scripts/wiki_to_mempalace.py`

### 2. Checked the latest plan intent

I used these plan documents as the baseline:

- [`copilot-session-checkpoint-curation.md`](copilot-session-checkpoint-curation.md)
- [`checkpoint-curation-phase5-report.md`](checkpoint-curation-phase5-report.md)
- [`mempalace-implementation-report.md`](mempalace-implementation-report.md)
- [`mempalace-next-steps.md`](mempalace-next-steps.md)

Those plans already set the right direction:

- keep durable checkpoints,
- compress progress-shaped checkpoints,
- improve graph value,
- preserve provenance without letting session-shaped clutter dominate,
- keep MemPalace and the wiki in sync.

### 3. Implemented process fixes

I changed these files:

- `scripts/auto_ingest.py`
- `scripts/wiki_to_mempalace.py`
- `README.md`
- `docs/memory-model.md`
- `docs/live-memory-loop.md`

#### `scripts/auto_ingest.py`

- Added a planning-only heuristic for compressed `project-progress` checkpoints.
- Suppressed concept/entity/synthesis generation for planning-only checkpoints.
- Added source-page normalization so checkpoint source pages carry:
  - `checkpoint_class`
  - `retention_mode`
  - correct `tier`

#### `scripts/wiki_to_mempalace.py`

- Kept stable-ID upsert behavior.
- Added orphan pruning so renamed/deleted wiki pages are removed from `labs_wiki_knowledge`.
- Added dry-run visibility for the orphan-prune count.

#### Docs

- Clarified that `quality_score` is structural, not a proxy for execution certainty.
- Documented the planning-only checkpoint policy.
- Documented that wiki → MemPalace sync now prunes stale drawers.

---

## Validation

### Checkpoint classification

The new policy classifies today's three checkpoint raws as:

| Raw source | Class | Retention | Planning-only |
|---|---|---|---|
| Sprint 60 PTS Feature Planning | `project-progress` | `compress` | yes |
| Sprint 61 Planning + Audit | `project-progress` | `compress` | yes |
| Scheduler DNS Agents Cleanup | `durable-debugging` | `retain` | no |

This is the behavior we want.

### MemPalace parity

Current `labs_wiki_knowledge` parity is clean:

| Metric | Value |
|---|---|
| Current wiki pages injected | 415 |
| Current collection docs | 415 |
| Orphaned injected docs | 0 |
| Missing injected docs | 0 |

So MemPalace is currently storing the right wiki-derived knowledge set, and after the new pruning logic it has the right long-term deletion behavior too.

---

## Alignment with the checkpoint-curation plan

### Where this work matches the plan well

This audit directly advances the open goals in [`copilot-session-checkpoint-curation.md`](copilot-session-checkpoint-curation.md):

1. **Phase 2 — separate retention from extraction**
   - Now enforced more clearly for planning-heavy `project-progress` checkpoints.

2. **Phase 4 — make the graph checkpoint-aware**
   - The system now treats planning checkpoints as provenance-first rather than concept-first, which improves graph quality indirectly.

3. **Budget discipline**
   - Fewer low-value concepts means less downstream churn and less model spend on content that should never have become canonical.

4. **Karpathy alignment**
   - This moves the system closer to "compile once, reuse many" and farther from "promote every compacted chat milestone."

### Where the plan is still ahead of the implementation

The latest plans still call for more than this audit delivered:

1. **Synthesis-first compression is not complete**
   - The Phase 5 report still recommends generating synthesis pages for checkpoint clusters.
   - Today's fix reduces clutter, but it does not author those syntheses.

2. **Graph-aware ranking is still heuristic**
   - Planning-only detection is rule-based, not graph-scored or model-scored.

3. **Backlog normalization is blocked operationally**
   - Existing checkpoint source pages under `wiki/sources/` are root-owned from the ingest container.
   - That blocked automatic backfill of older pages even though the code path is now correct.

---

## Alignment with Karpathy's LLM Wiki gist

Karpathy's gist says the wiki should sit between the raw sources and future queries as a persistent, maintained, compounding artifact. The wiki should preserve synthesis, contradictions, cross-references, and durable structure so the model does not have to rediscover the same knowledge each time.

### Pros

1. **The raw/wiki/schema split is correct**
   - `raw/` is immutable source input.
   - `wiki/` is the compiled artifact.
   - `AGENTS.md` and the wiki docs act as the schema.

2. **Checkpoint promotion uses the right unit**
   - Durable checkpoint markdown is much closer to Karpathy's ideal than transcript JSON.
   - The system already promotes distilled summaries instead of raw chat logs.

3. **Provenance is strong**
   - Checkpoint source pages preserve where concepts came from.
   - MemPalace and the wiki both keep that traceability.

4. **The wiki compounds better after this change**
   - Planning-only checkpoints stop turning future work into fake present-tense knowledge.
   - Durable debugging sessions still enrich the wiki.

5. **MemPalace is now safer as a mirror**
   - Upsert-only behavior is no longer the whole story.
   - Renames and deletes can now be reflected in `labs_wiki_knowledge`.

### Cons

1. **Heuristics still stand in for editorial judgment**
   - A planning checkpoint may contain one durable idea.
   - The new suppression rule may be too blunt in borderline cases.

2. **Checkpoint pages still risk becoming a holding area**
   - This was the main issue in the Sprint 60/61 pages.
   - The fix reduces the problem, but the stronger answer is still more synthesis and more canonical workflow pages.

3. **`quality_score` still looks stronger than it is**
   - A planning page can still score well structurally.
   - The score is useful, but it does not answer "is this executed knowledge?"

4. **Container ownership is undermining maintenance**
   - Root-owned generated pages block backfill, normalization, and batch curation from the host user.
   - This is now the main process bug.

5. **The system is still better at provenance than abstraction**
   - The curation plan already spotted this in the low synthesis-link rate.
   - This audit improved the boundary, but not the deeper synthesis problem.

---

## Is MemPalace adding the correct details?

**Mostly yes.**

For the wiki-derived side of the system, MemPalace currently reflects the right set of concept, entity, and synthesis pages. The collection is in parity with the filesystem, and the new prune logic closes the deletion gap that existed before.

For session-derived material, the stronger answer is:

- **good at storing detail,**
- **good at retrieval,**
- **needs the wiki promotion layer to be selective.**

That matches the intended split:

- `copilot_sessions` = raw conversational/session memory
- `labs-wiki` = compiled durable knowledge
- `labs_wiki_knowledge` = searchable mirror of the compiled wiki

That split is consistent with both the latest plans and Karpathy's gist.

---

## Is stale memory being removed?

**Now yes for wiki-derived MemPalace knowledge, but not yet fully for existing root-owned checkpoint pages.**

### Fixed in code

- `scripts/wiki_to_mempalace.py` now prunes stale drawers for renamed/deleted wiki pages.

### Still weak operationally

- existing root-owned files in `wiki/sources/` blocked the automatic backfill pass,
- which means some already-generated checkpoint pages still need a one-time ownership fix and curation rerun.

So the design is now correct, but the backlog still needs one operational cleanup pass.

---

## Recommended next steps

1. **Fix file ownership in the ingest container**
   - Generated wiki files should be written as the host user, not `root`.

2. **Re-run checkpoint backfill**
   - After ownership is fixed, rerun `scripts/backfill_checkpoint_curation.py` to normalize old checkpoint pages.

3. **Add an explicit execution-status signal**
   - Example: `knowledge_state: planned | executed | validated`
   - This would make the distinction clearer than relying on `quality_score`.

4. **Do the synthesis work Phase 5 still calls for**
   - The biggest remaining gap is still upward compression into synthesis pages.

5. **Track planning-only suppression impact**
   - Review whether the rule suppresses any checkpoint that should still mint a workflow or architecture concept.

---

## Bottom line

The system is closer to the right shape after this audit.

It now does a better job of keeping planning checkpoints as provenance and keeping durable debugging sessions as knowledge. That is more faithful to the checkpoint-curation plan, more faithful to Karpathy's gist, and safer for MemPalace as a durable mirror.

The remaining weak point is no longer classification logic. It is operational ownership and backlog cleanup.
