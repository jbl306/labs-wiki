---
name: wiki-orchestrate
description: Coordinate wiki maintenance — audit, lint, gap analysis, and stale page review.
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

Coordinate wiki maintenance workflows. Ingest is handled automatically by the `wiki-auto-ingest` Docker sidecar.

> **Auto-ingest handles pending sources.** This skill focuses on quality — lint, audit, gap analysis, and stale page review.

## Usage

```
/wiki-orchestrate                    # Audit + maintenance + gap analysis
/wiki-orchestrate audit              # Full audit with auto-fix
/wiki-orchestrate maintenance        # Stale page review + index rebuild
/wiki-orchestrate ingest             # Manual fallback: ingest pending sources
```

## Workflows

### Audit (default)

1. **Run `/wiki-lint`** on all wiki pages
2. **Auto-fix** safe issues (rebuild index, update scores)
3. **Gap analysis** via Curator persona
4. **Report** remaining issues requiring human review
5. **Summary** — pages audited, issues found, issues auto-fixed

### Maintenance

1. Find all stale pages (`last_verified` > 90 days)
2. For each stale page:
   - Re-read the original source(s)
   - If source still valid → bump `last_verified`
   - If source changed → run `/wiki-update`
   - If source missing → flag for human review
3. Review tier promotions (hot → established, established → core)
4. Rebuild `wiki/index.md`
5. Report summary

### Manual Ingest (fallback)

Only use when auto-ingest is unavailable:

1. Check auto-ingest status: `docker ps | grep wiki-auto-ingest`
2. If down, find all `raw/*.md` files with `status: pending`
3. Process each through `/wiki-ingest` (sequentially)
4. Track results: success/skip/fail for each source
5. Rebuild `wiki/index.md` once at the end

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
