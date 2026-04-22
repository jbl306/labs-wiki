# Lessons Learned — labs-wiki

<!--
Format:
## YYYY-MM-DD: Short title

- **Pattern**: What went wrong or what was learned
- **Root cause**: Why it happened
- **Prevention rule**: How to avoid it next time
- **Affected files**: Which files were involved
- **Category**: knowledge-curation | auto-ingest | infrastructure | agents
-->

## 2026-04-19: Quality score conflated structural completeness with execution posture

- **Pattern**: Copilot session checkpoints landed in the wiki with `quality_score: 100` regardless of whether they described **planned**, **executed**, or **validated** work. Downstream agents treated the score as a proxy for "this is settled knowledge" and pulled tentative plans into MemPalace as truth.
- **Root cause**: `compute_quality_score` only measured frontmatter completeness, cross-references, source attribution, and recency — none of which capture whether the underlying work actually shipped. The schema had no field to distinguish posture, so the rubric quietly absorbed the question.
- **Prevention rule**: Track execution posture as its own first-class field (`knowledge_state: planned | executed | validated`) and never read `quality_score` as confidence. When introducing a new posture-bearing schema, also update the lint rubric, the auto-ingest path, and the MemPalace export filter in the same change so the three views stay coherent.
- **Affected files**: `scripts/checkpoint_classifier.py`, `scripts/auto_ingest.py`, `scripts/wiki_to_mempalace.py`, `docs/memory-model.md`, `templates/source-summary.md`
- **Category**: knowledge-curation

## 2026-04-20: Second-curation report ran on stale checkpoint state because the audit script hadn't been re-run

- **Pattern**: The second-curation report (`reports/second-curation-report-2026-04-20.md`) was generated against a snapshot of `checkpoint_state` that predated several `retention_mode` flips. Recommendations in the report contradicted what was already on disk, and the agent acted on the stale rows.
- **Root cause**: The curation script defaulted to its cached state file instead of recomputing from the live wiki. There was no freshness assertion before producing recommendations, so a multi-day-old cache silently became the input.
- **Prevention rule**: Any script that produces editorial recommendations must either (a) recompute its inputs from the canonical source on every run, or (b) print a `state generated at: <timestamp>` banner and refuse to emit recommendations if that timestamp is older than the most recent `wiki/log.md` entry. Add the freshness check upstream, not downstream.
- **Affected files**: `scripts/backfill_checkpoint_curation.py`, `scripts/checkpoint_state.py`, `reports/second-curation-report-2026-04-20.md`
- **Category**: tooling

## 2026-04-21: quality_score saturated at 100 across the entire corpus

- **Pattern**: The full review (`reports/full-review-2026-04-21.md`) found 324 of 327 wiki pages pinned at `quality_score: 100`. The score had stopped differentiating thin entity stubs from six-source synthesis pages, breaking the signal that tier promotion (R7) and lint review depend on.
- **Root cause**: The four-bucket rubric (frontmatter complete / has any wikilink / sources non-empty / verified within 90 days) is satisfied by every page on day one of auto-ingest. The rubric measured presence, not quality.
- **Prevention rule**: Any "score" that produces a near-uniform distribution after >100 samples is broken — track the score distribution in CI and alarm when the IQR collapses. Replace presence-checks with continuous signals (graph degree, body length band, citable-claim regex, staleness curve, knowledge_state). R3 in the full review owns the rewrite of `compute_quality_score` and is the prevention.
- **Affected files**: `scripts/lint_wiki.py`, `docs/memory-model.md`, `reports/full-review-2026-04-21.md`
- **Category**: knowledge-curation
