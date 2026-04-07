---
name: wiki-orchestrate
description: Coordinate multi-step wiki workflows — bulk ingest, full audit, and maintenance.
allowed-tools:
  - read
  - write
  - edit
  - bash
  - grep
  - glob
  - web_search
---

# /wiki-orchestrate

Coordinate multi-step wiki workflows. This is the meta-skill that chains other skills together for bulk operations.

## Usage

```
/wiki-orchestrate                    # Full pipeline: ingest pending → lint → fix → rebuild
/wiki-orchestrate ingest             # Bulk ingest all pending raw sources
/wiki-orchestrate audit              # Full audit with auto-fix
/wiki-orchestrate maintenance        # Stale page review + index rebuild
```

## Workflows

### Full Pipeline (default)

1. **Scan `raw/`** for sources with `status: pending`
2. **Run `/wiki-ingest`** on each pending source (sequentially to avoid conflicts)
3. **Run `/wiki-lint`** on all wiki pages
4. **Auto-fix** safe issues (rebuild index, update scores)
5. **Report** remaining issues requiring human review
6. **Summary** — pages created, pages updated, issues found, issues auto-fixed

### Bulk Ingest

1. Find all `raw/*.md` files with `status: pending` (or no status)
2. Process each through `/wiki-ingest` (Phase 1 + Phase 2)
3. Track results: success/skip/fail for each source
4. Rebuild `wiki/index.md` once (not after each ingest)
5. Report summary

### Full Audit

1. Run `/wiki-lint` on every page in `wiki/`
2. Use `/wiki-lint --fix` to auto-fix safe issues
3. Run `/wiki-lint` again to verify fixes
4. Report remaining issues with suggested actions
5. Use the **Curator** persona for gap analysis

### Maintenance

1. Find all stale pages (`last_verified` > 90 days)
2. For each stale page:
   - Re-read the original source(s)
   - If source still valid → bump `last_verified`
   - If source changed → run `/wiki-update`
   - If source missing → flag for human review
3. Rebuild `wiki/index.md`
4. Report summary

## Rules

- **Process sources sequentially** during ingest to avoid race conditions on shared pages
- **Always end with index rebuild** — ensures consistency
- **Log each sub-operation** to `wiki/log.md`
- **Report a summary** at the end — total operations, successes, failures, remaining issues
- Use the appropriate agent persona for each sub-task:
  - Researcher for extraction
  - Compiler for page generation
  - Curator for gap analysis
  - Auditor for lint/quality
