---
name: wiki-lint
description: Audit wiki health — broken links, orphan pages, staleness, quality scoring.
allowed-tools:
  - read
  - edit
  - grep
  - glob
  - bash
---

# /wiki-lint

Audit the wiki for health issues. Reports broken links, orphan pages, missing frontmatter, stale pages, and quality scores.

## Usage

```
/wiki-lint                     # Full audit of all wiki pages
/wiki-lint wiki/concepts/      # Audit only concept pages
/wiki-lint --fix               # Auto-fix safe issues (rebuild index, update scores)
```

## Checks Performed

| Check | Severity | Rule |
|-------|----------|------|
| Missing required frontmatter | Error | `title`, `type`, `created`, `sources` must exist |
| Broken wikilinks | Error | Every `[[Link]]` must resolve to an existing page |
| Missing provenance | Error | `sources:` must have at least one entry |
| Orphan pages | Warning | Every page should appear in `wiki/index.md` |
| Stale pages | Warning | `last_verified` > 90 days ago |
| Low quality score | Warning | `quality_score` < 50 flagged for review |
| Invalid page type | Error | `type` must be: source, concept, entity, or synthesis |
| Wrong directory | Error | Page type must match directory (concept → wiki/concepts/) |

## Quality Scoring (0-100)

Score each page against four dimensions:

| Dimension | Points | Criteria |
|-----------|--------|----------|
| Completeness | 25 | All required frontmatter fields present |
| Cross-references | 25 | Has `related:` entries and `[[wikilinks]]` in body |
| Attribution | 25 | `sources:` has entries, claims are traceable |
| Recency | 25 | `last_verified` within 90 days |

### Staleness Detection

Pages with `last_verified` older than 90 days get a `⚠️ STALE` warning. The recency score drops linearly:
- 0-90 days: 25/25 points
- 91-180 days: 12/25 points
- 180+ days: 0/25 points

## Auto-Fix (--fix mode)

Safe to auto-fix:
- ✅ Rebuild `wiki/index.md` from current pages
- ✅ Update `quality_score` in frontmatter based on audit
- ✅ Add missing `last_verified` (set to file modification date)

Requires human review:
- ❌ Broken wikilinks (might be typo or missing page)
- ❌ Missing provenance (need to identify correct source)
- ❌ Content quality issues

## Output Format

```
=== Wiki Lint Report ===
Pages scanned: 15
Errors: 3
Warnings: 5

ERRORS:
  wiki/concepts/rope.md: broken wikilink [[Rotary Encoding]] (no such page)
  wiki/entities/pytorch.md: missing required field 'sources'
  wiki/sources/paper-x.md: page type 'source' in wrong directory 'wiki/concepts/'

WARNINGS:
  wiki/concepts/attention.md: stale (last verified 120 days ago)
  wiki/concepts/attention.md: quality score 42 (below 50 threshold)
  wiki/entities/openai.md: orphan page (not in index.md)

SCORES:
  wiki/concepts/positional-encoding.md: 85/100
  wiki/concepts/attention.md: 42/100
  wiki/entities/pytorch.md: 60/100
```

## Rules

- Use the **Auditor** persona (`agents/auditor.md`) when running lint
- Always report results — never silently pass
- Log audit results to `wiki/log.md`
- Run `scripts/lint_wiki.py` for offline/CI checks (same rules, Python implementation)
