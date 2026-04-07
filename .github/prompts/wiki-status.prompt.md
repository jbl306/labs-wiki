---
agent: 'ask'
description: "Show wiki health dashboard — pending sources, stale pages, lint issues, coverage stats"
---

Generate a wiki status dashboard by checking:

1. **Pending Sources**: Count files in `raw/` with `status: pending` in frontmatter
2. **Wiki Pages**: Count pages by type (concepts, entities, sources, synthesis) and tier (hot, established, core, workflow)
3. **Stale Pages**: Find pages where `last_verified` is more than 90 days ago
4. **Quality Issues**: Find pages with `quality_score` < 50
5. **Recent Activity**: Show the last 5 entries from `wiki/log.md`

Format as a concise dashboard:
```
📊 WIKI STATUS
──────────────
Sources: N pending | N ingested
Pages:   N concepts | N entities | N sources | N synthesis
Tiers:   N hot | N established | N core | N workflow
Health:  N stale | N low-quality | N errors
Recent:  [last 5 log entries]
```
