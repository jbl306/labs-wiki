# Memory Model

> How labs-wiki tracks provenance, staleness, quality, and knowledge consolidation.

## Provenance Chain

Every fact in the wiki traces back to a raw source. This chain is enforced through the `sources:` frontmatter field.

```
raw/2025-07-17-rope-paper.md
  └─ wiki/sources/rope-paper.md (1:1 summary)
       ├─ wiki/concepts/positional-encoding.md (references this source)
       └─ wiki/concepts/rotary-embeddings.md (references this source)
```

**Rules:**
- Every wiki page must have `sources:` with at least one entry
- Sources point to files in `raw/` (relative paths)
- If information comes from multiple sources, list all of them
- The linter flags a missing `sources` field. Review the listed sources to verify provenance.

## Staleness Detection

Wiki pages go stale when their source material may have changed or the information hasn't been verified. Tracked via two frontmatter fields:

| Field | Purpose | Updated By |
|-------|---------|-----------|
| `last_verified` | Date the page was last reviewed | [Wiki Update persona](../agents/wiki-update.agent.md) after source review |
| `source_hash` | SHA-256 of the raw source content | Ingest pipeline or Wiki Update persona after a source change |

### Staleness Rules

- Pages not verified in **90+ days** are flagged as stale
- Pages with a `source_hash` mismatch (raw source changed) need re-ingestion
- Run `python3 scripts/lint_wiki.py` to see staleness warnings.

## Quality Scoring

Run `python3 scripts/lint_wiki.py` from the repository root to calculate page scores. The linter warns on scores below 50. During score maintenance, `--write-scores` writes the calculated values into page frontmatter.

| Signal | Maximum points |
|--------|----------------|
| Inbound wikilinks | 20 |
| Outbound wikilinks | 15 |
| Body length | 15 |
| Number of sources | 15 |
| Recency of verification (full credit through day 30, falling to zero at day 180) | 15 |
| Recorded knowledge state | 10 |
| Specific claim (number, code or quotation) | 10 |

Use `knowledge_state` and the underlying source to distinguish planned, executed and validated work.

## Consolidation Tiers

Pages mature through four tiers over their lifecycle:

```
hot → established → core → workflow
```

| Tier | Criteria | Example |
|------|----------|---------|
| `hot` | Created within 7 days, not yet cross-referenced | New ingest from today |
| `established` | Verified, has cross-references, within 90-day window | Well-linked concept page |
| `core` | Referenced by 3+ other pages, foundational | Architecture patterns |
| `workflow` | Operational procedures, how-tos | Setup guides, processes |

### Promotion Rules

- **hot → established:** Page has been verified at least once, has `related:` entries, and `quality_score` ≥ 50
- **established → core:** Referenced by 3+ other pages, `quality_score` ≥ 70, verified within 90 days
- **workflow:** Manual classification for procedural content (not auto-promoted)

### Copilot Session Checkpoints

- `durable-*` checkpoints remain first-class source pages and can generate concepts, entities, and synthesis pages.
- `project-progress` checkpoints default to `retention_mode: compress` and are archived as source pages.
- Planning-only `project-progress` checkpoints keep the source summary for provenance, but concept/entity extraction is suppressed so future work is not promoted as settled knowledge.
- Checkpoint source pages also carry `knowledge_state: planned | executed | validated` so execution posture is explicit; `quality_score` remains structural and should not be read as implementation certainty.

#### Graph recommendation layer

On every graph build, `wiki-graph-api/graph_builder.py` produces a second editorial recommendation per checkpoint derived from graph position (degree, synthesis-neighbor count, community membership). This recommendation is compared to the heuristic baseline from `checkpoint_class` and `retention_mode`.

The comparison is written to `reports/checkpoint-graph-tracker.md` as a **report-only** artifact — it does not rewrite any wiki page or frontmatter. Its purpose is to surface disagreements between the heuristic classifier and the graph layer so they can be evaluated before any policy change is applied.

During maintenance, the [Wiki Curator](../agents/wiki-curator.agent.md) reviews tier changes. Record approved changes in `wiki/log.md`.

## Codex Durable Session Checkpoints

Codex saves selected Labs Wiki facts to MemPalace with evidence and explicit
execution state; see [Codex durable session memory](codex-durable-memory.md)
for the authorized scope, native hooks, and save receipts.
