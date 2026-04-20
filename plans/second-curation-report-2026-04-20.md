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

### Bottom line

The second curation pass supports the original audit: checkpoint curation is working best when it preserves durable debugging and architecture work while aggressively demoting planning checkpoints out of the hot path.
