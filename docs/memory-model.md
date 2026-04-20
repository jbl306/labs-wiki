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
- The `/wiki-lint` skill flags pages with missing provenance as errors

## Staleness Detection

Wiki pages go stale when their source material may have changed or the information hasn't been verified. Tracked via two frontmatter fields:

| Field | Purpose | Updated By |
|-------|---------|-----------|
| `last_verified` | Date the page was last reviewed | `/wiki-update`, Auditor persona |
| `source_hash` | SHA-256 of the raw source content | `/wiki-ingest`, `/wiki-update` |

### Staleness Rules

- Pages not verified in **90+ days** are flagged as stale
- Pages with a `source_hash` mismatch (raw source changed) need re-ingestion
- The Auditor agent runs staleness checks during `/wiki-lint`

### Freshness Decay (Ebbinghaus-Inspired)

Quality score degrades linearly with staleness:

| Age Since Verification | Recency Score (out of 25) |
|----------------------|-------------------------|
| 0-90 days | 25 |
| 91-180 days | 12 |
| 180+ days | 0 |

This is inspired by [agentmemory](https://github.com/rohitg00/agentmemory)'s Ebbinghaus-based memory decay.

## Quality Scoring

Every page gets a 0-100 quality score computed by `/wiki-lint`:

| Dimension | Points | What's Checked |
|-----------|--------|---------------|
| **Completeness** | 25 | All required frontmatter fields present |
| **Cross-references** | 25 | Has `related:` entries and `[[wikilinks]]` in body |
| **Attribution** | 25 | `sources:` has entries, claims traceable |
| **Recency** | 25 | `last_verified` within 90 days |

### Score Thresholds

| Score | Status | Action |
|-------|--------|--------|
| 80-100 | 🟢 Healthy | No action needed |
| 50-79 | 🟡 Needs attention | Review recommended |
| 30-49 | 🟠 Low quality | Flagged in lint report |
| 0-29 | 🔴 Critical | Blocked from index until fixed |

**Note:** `quality_score` measures page structure and linkage, not whether the source reflects executed work versus a tentative plan. That distinction is tracked through checkpoint classification and retention.

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

Tier changes are tracked in `wiki/log.md` and performed by the Curator agent during `/wiki-orchestrate maintenance`.
