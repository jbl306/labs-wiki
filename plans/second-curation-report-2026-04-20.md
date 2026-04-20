# Second Curation Report

**Date:** 2026-04-20  
**Scope:** run a second targeted checkpoint curation pass after the wiki ownership fix, record the resulting checkpoint classes and retention decisions, and capture the script fix needed to run that pass against the live wiki checkout.

---

## Summary

The second curation pass confirmed the split from the first audit:

- `Sprint 60 PTS Feature Planning` and `Sprint 61 Planning + Audit` are planning checkpoints and should be compressed.
- `Scheduler DNS Agents Cleanup` is a durable debugging checkpoint and should remain first-class.
- `Wiki Audit Followups` is a durable architecture checkpoint and should remain first-class.

The pass also exposed a real bug in `scripts/backfill_checkpoint_curation.py`: the new `--wiki` option changed file discovery, but the script still assumed the repo root when resolving raw sources and writing result paths. I fixed that in this branch so targeted curation can run against an external wiki checkout instead of only the local repo root.

---

## What I ran

I used the updated curation script from a clean worktree and pointed it at the live `labs-wiki/wiki` tree:

```bash
python3 scripts/backfill_checkpoint_curation.py \
  --wiki /home/jbl/projects/labs-wiki/wiki \
  --path wiki/sources/copilot-session-checkpoint-sprint-60-pts-feature-planning.md \
  --path wiki/sources/copilot-session-checkpoint-sprint-61-planning-audit.md \
  --path wiki/sources/copilot-session-checkpoint-scheduler-dns-agents-cleanup.md \
  --path wiki/sources/copilot-session-checkpoint-wiki-audit-followups.md
```

---

## Results

| Checkpoint | Class | Retention | Knowledge state | Tier after |
|---|---|---|---|---|
| `Sprint 60 PTS Feature Planning` | `project-progress` | `compress` | `planned` | `archive` |
| `Sprint 61 Planning + Audit` | `project-progress` | `compress` | `planned` | `archive` |
| `Scheduler DNS Agents Cleanup` | `durable-debugging` | `retain` | `validated` | `hot` |
| `Wiki Audit Followups` | `durable-architecture` | `retain` | `validated` | `hot` |

Aggregate outcome:

| Metric | Value |
|---|---|
| Checkpoints processed | 4 |
| Pages changed | 4 |
| `retain` | 2 |
| `compress` | 2 |
| `planned` | 2 |
| `validated` | 2 |

This is the result we wanted. The two sprint-planning checkpoints no longer read as durable completed knowledge, and the two durable checkpoints keep their first-class status.

---

## Implementation note

The changes to the live checkpoint pages were applied in the host checkout because those generated pages are present there but are not part of `origin/main` yet. This branch does **not** try to publish those generated checkpoint files. It captures:

1. the curation outcome in this report, and
2. the script fix that makes `--wiki` work correctly for future targeted runs.

That keeps the merge small and safe while still recording the second-pass decision.

---

## Evaluation

### Pros

1. The second pass validates the policy on real follow-up pages, not just the earlier session-promotion cluster.
2. Planning-heavy sprint checkpoints are now explicitly marked `planned` and archived.
3. Durable operational checkpoints still surface as hot, reusable knowledge.
4. The `--wiki` path fix makes the curation tooling usable from clean worktrees against the live checkout.

### Cons

1. The curated checkpoint pages themselves still live only in the host checkout, not in the tracked repo state.
2. The current classifier still relies on heuristic titles and body signals rather than graph-aware editorial scoring.

## Options for graph-aware editorial scoring

The current classifier is good at the first cut, but it still decides mostly from title and body text. The next step is to let graph position influence whether a checkpoint is worth keeping hot, compressing, or archiving.

### Option 1 — Add a graph-aware recommendation layer after the current classifier

Keep the current `checkpoint_classifier.py` classes, then add a second pass that reads graph features from `wiki/graph/graph.json` or `GET /graph/checkpoints` and emits an editorial recommendation such as `keep`, `compress`, `merge`, or `archive`.

Suggested signals:

- checkpoint degree
- number of synthesis neighbors
- community concentration
- repeated-cluster membership
- concept overlap with existing durable pages
- whether the page is acting only as provenance

**Pros**

1. Smallest change to ship.
2. Keeps the current heuristic classifier stable.
3. Easy to run in report-only mode before enforcing thresholds.

**Cons**

1. Leaves classification and editorial scoring split across two systems.
2. Can drift if the heuristic class and graph recommendation disagree often.

### Option 2 — Replace binary heuristics with a weighted editorial score

Compute a single editorial score per checkpoint from both text and graph features, then map score bands to retention behavior.

Example inputs:

- text class: `durable-*`, `project-progress`, `low-signal`
- `knowledge_state`
- `quality_score`
- checkpoint degree percentile
- synthesis-neighbor count
- bridge score across communities
- cluster recurrence
- freshness / recency

Example output:

- `80-100` → retain as first-class checkpoint
- `50-79` → retain as provenance, but compress upward
- `20-49` → compress / archive
- `<20` → skip or archive-only

**Pros**

1. Gives one explicit editorial decision surface.
2. Makes the reasoning more measurable and tunable.
3. Fits the Karpathy goal better than title-only routing.

**Cons**

1. Needs threshold tuning.
2. Harder to explain if too many weak signals get mixed together.

### Option 3 — Score checkpoint families, not just individual pages

Move part of the decision from page level to cluster level. If a checkpoint belongs to a repeated sprint/status family with low synthesis lift, score the family first and demote later members more aggressively. If a checkpoint belongs to a root-cause or architecture cluster with strong bridge behavior, bias toward retention.

**Pros**

1. Better match for repeated sprint checkpoints, where the problem is often the family, not the single page.
2. Encourages synthesis-first compression after repeated similar ingests.

**Cons**

1. Depends on stable enough cluster detection.
2. Weaker for one-off checkpoints with no family yet.

### Option 4 — Add editorial overrides and learn from them

Keep the scoring deterministic, but let curated outcomes become training data. Store explicit overrides such as:

- `editorial_recommendation`
- `editorial_reason`
- `editorial_reviewed_at`

Over time, use those labeled decisions to tune weights or train a small reranker.

**Pros**

1. Lets the system learn from actual curation outcomes.
2. Keeps human judgment in the loop for borderline cases.

**Cons**

1. Slower to mature.
2. Requires disciplined labeling to be useful.

## Recommended path

The best next move is **Option 1 first, then Option 2**.

1. Add a graph-aware recommendation layer now, but run it in report-only mode.
2. Track where graph recommendations disagree with the current classifier.
3. Once the disagreements are understandable, fold the strongest graph signals into a weighted editorial score.
4. Use checkpoint-family scoring as a second-stage upgrade for repeated sprint/status clusters.

That path is safer than jumping straight to a fully weighted classifier, and it gives us real disagreement data before we start moving thresholds.

### Bottom line

The second curation pass supports the original audit: checkpoint curation is working best when it preserves durable debugging and architecture work while aggressively demoting planning checkpoints out of the hot path.
