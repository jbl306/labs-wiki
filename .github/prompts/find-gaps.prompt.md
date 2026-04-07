---
agent: 'wiki-curator'
description: "Analyze wiki coverage and identify missing concepts, broken links, and synthesis opportunities"
---

Perform a comprehensive gap analysis of the wiki:

1. Find all `[[wikilinks]]` that don't resolve to existing pages
2. Scan `concepts:` fields for concepts without dedicated pages
3. Identify clusters of 3+ related concepts that lack a synthesis page
4. Check for concept pages that are referenced nowhere (isolated knowledge)
5. Find raw sources that were ingested but produced no concept/entity pages

Report findings grouped by priority:
- 🔴 Broken wikilinks (errors)
- 🟡 Missing concept pages (coverage gaps)
- 🔵 Synthesis opportunities (coherence improvements)
- ⚪ Isolated pages (connectivity issues)
