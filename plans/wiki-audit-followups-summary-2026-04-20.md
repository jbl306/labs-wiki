# Wiki Audit Follow-ups Summary

**Date:** 2026-04-20  
**Scope:** implement the next steps from `copilot-session-wiki-memory-audit-2026-04-19.md`, keep the backfill limited for GitHub Models free-tier usage, and record the outcome.

---

## What shipped

### 1. Explicit checkpoint execution posture

I added a shared `scripts/checkpoint_state.py` helper and used it in both ingest and backfill flows.

- `scripts/auto_ingest.py` now stamps checkpoint source pages with `knowledge_state: planned | executed | validated`.
- `scripts/backfill_checkpoint_curation.py` now:
  - supports targeted runs via `--path` and `--limit`,
  - reads the raw checkpoint body before classifying or deriving `knowledge_state`, so old pages and new ingests use the same evidence,
  - keeps `quality_score` structural rather than overloading it as an execution signal.

### 2. Cost-safe checkpoint synthesis backfill

I hardened `scripts/backfill_checkpoint_cluster_synthesis.py` so it does not spend model calls when the synthesis page already exists.

- Existing cluster syntheses are matched by cluster signature or exact source set before any weaker fallback.
- Existing synthesis pages are stamped with:
  - `checkpoint_cluster_community`
  - `checkpoint_cluster_checkpoint_count`
  - `checkpoint_cluster_signature`
- A token is now required only when the script actually needs to create a new synthesis page.

This closes the main free-tier risk from the earlier one-shot backfill path: duplicate syntheses for the same cluster.

### 3. Wiki ownership fix in homelab

I updated `homelab/compose/compose.wiki.yml` so both wiki services run as `${PUID}:${PGID}` and documented that in `homelab/docs/05-service-guide.md`.

I also applied the live fix:

- redeployed the wiki stack with an absolute `WIKI_INGEST_PATH` override so the worktree deploy used the correct bind mounts,
- confirmed both containers now run as `1000:1000`,
- normalized ownership on the live `labs-wiki/raw` and `labs-wiki/wiki` trees,
- confirmed there are no remaining root-owned files under those directories.

---

## Limited backfill executed

I kept the write path narrow and free-tier-safe.

### Targeted checkpoint curation backfill

Processed three tracked checkpoint source pages in the session-promotion cluster:

1. `wiki/sources/copilot-session-checkpoint-session-wiki-promotion.md`
2. `wiki/sources/copilot-session-checkpoint-auto-ingest-pipeline-built-and-docs-updated.md`
3. `wiki/sources/copilot-session-checkpoint-building-4-copilot-cli-custom-agents.md`

### Result

| Metric | Value |
|---|---|
| Pages processed | 3 |
| Pages changed | 2 |
| Final knowledge-state distribution | `validated=3` |
| Final class distribution | `durable-architecture=2`, `durable-debugging=1` |
| Quality score bucket | `75-100=3` |

The most important correction was `Copilot Session Checkpoint: Session Wiki Promotion`, which moved from `durable-architecture / planned` to `durable-debugging / validated` once the backfill used the raw checkpoint instead of the generated summary page.

### Limited synthesis backfill

I ran the cluster backfill only for community `1`, the Copilot session promotion cluster.

| Metric | Value |
|---|---|
| Cluster processed | `community=1` |
| Checkpoints in cluster | `14` |
| Match result | existing synthesis matched by `signature` |
| New synthesis pages created | `0` |
| GitHub Models calls required | `0` |

The existing synthesis page now carries stable cluster metadata instead of relying on title collision behavior.

---

## Evaluation

### Pros

1. `knowledge_state` now answers the question that `quality_score` never could: whether the checkpoint is planned work, executed work, or validated work.
2. Backfill and ingest now derive that signal from the same source of truth: the raw checkpoint body.
3. The synthesis backfill is now safe to rerun on a free tier because existing clusters are recognized before any LLM call.
4. The wiki stack no longer writes future files as `root`, and the current repo has already been repaired.

### Cons

1. `knowledge_state` is still heuristic. It is more honest than `quality_score`, but it can still be wrong on borderline checkpoints.
2. The limited backfill covered the tracked session-promotion cluster only, not the whole checkpoint corpus.
3. The clean feature worktree does not include today's uncommitted `Sprint 60`, `Sprint 61`, and `Scheduler DNS Agents Cleanup` source pages, so this branch could not rewrite those exact files directly.

### Bottom line

The follow-up work is now in a better operational state:

- execution posture is explicit,
- duplicate checkpoint syntheses are blocked,
- free-tier backfills can be surgical,
- and the live ownership bug is fixed.

The next practical step, after these script changes are merged into the main `labs-wiki` checkout, is a second targeted curation run over today's now-writable source pages.
