---
name: wiki-update
description: Revise existing wiki pages with new information while maintaining provenance.
allowed-tools:
  - read
  - write
  - edit
  - grep
  - glob
  - bash
---

# /wiki-update

Revise an existing wiki page with new information. Maintains the provenance chain, updates hashes, and preserves existing content.

## Usage

```
/wiki-update wiki/concepts/positional-encoding.md    # Update a specific page
/wiki-update --stale                                  # Update all stale pages (>90 days)
```

## How It Works

1. **Read the target page** and its frontmatter
2. **Check the source** — re-read `sources:` entries in `raw/`
   - Compute new SHA-256 hash of each source
   - Compare with `source_hash` — if changed, the source has been updated
3. **Merge new information:**
   - Add new facts, concepts, or relationships
   - **Never delete existing content** unless it's factually incorrect
   - If source content changed, update the wiki page to reflect changes
4. **Update frontmatter:**
   - `source_hash` → new SHA-256 of source content
   - `last_verified` → today's date
   - `quality_score` → recalculate based on current state
   - `related` → add any new cross-references
   - `sources` → add new sources if information came from additional raw files
5. **Update cross-references** in other pages that link to/from this page
6. **Append to `wiki/log.md`:**
   ```yaml
   - timestamp: 2025-07-17T16:00:00Z
     operation: update
     agent: compiler
     targets:
       - wiki/concepts/positional-encoding.md
     source: raw/2025-07-17-rope-paper.md
     status: success
     notes: "Updated source_hash, added new relationship to [[RoPE]]"
   ```
7. **Rebuild `wiki/index.md`** if the page title, type, or summary changed

## Rules

- **Never delete content** unless provably incorrect — append and attribute instead
- **Always update `last_verified`** even if no content changed (proves the page was reviewed)
- **Maintain provenance** — new facts need new `sources:` entries
- **Update both directions** — if page A now links to page B, page B's `related:` should include A
- **Log every operation** to `wiki/log.md`
