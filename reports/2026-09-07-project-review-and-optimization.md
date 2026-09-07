# Labs Wiki Review and Optimization — 2026-09-07

Implemented focused fixes for source preservation, local read containment, request privacy, graph cache identity, and repeated corpus scans. The working tree was clean before this review. This report records local verification; service deployment was not tested.

The review covered the capture API, local MCP tools, graph extraction and construction, synthesis auditing, and corpus health. Existing ingestion transaction and CLI tests were also run. This was not a line-by-line audit of the entire project or a live deployment test.

## Findings fixed

| Priority | Finding | Change |
|---|---|---|
| High | Uploads with the same title on the same day overwrote the earlier raw record. Text captures also checked filename availability separately from writing. | Shared `write_raw_source` uses exclusive creation and retries numeric suffixes. Both endpoints return the actual allocated path. Tests preserve separate upload records/assets and exercise concurrent text captures. |
| High | `wiki_read` accepted files outside `wiki/`, and search/list followed external file symlinks. | Local tools admit only Markdown files whose resolved paths stay inside `wiki/`. Tests cover traversal, absolute paths, file/directory symlinks, non-Markdown files, and symlink loops. |
| High | Ingest diagnostics logged content, query values, and cookies; the unauthenticated debug endpoint echoed request headers and body. | Application logs retain operational metadata only. The debug endpoint now requires bearer authentication and returns method and body length. |
| Medium | The graph extraction cache keyed only on bytes but stored path-derived identity and fallback titles. Identical pages collapsed to one node; renamed pages retained old IDs. | Cache keys include the relative path and content hash. Cold/warm extraction tests verify distinct nodes, renamed identities, titles, and current source signatures. Existing caches naturally miss under the new key scheme. |
| Medium | Direct MCP reads scanned every page before opening an already-known path. Unresolved graph links scanned a dictionary whose fallback keys were already indexed. | Resolve direct paths/slugs before title scanning; remove the redundant graph scan. |
| Medium | The full synthesis audit rebuilt wiki provenance once per synthesis page. | Build one fresh provenance map per CLI batch. Standalone ingest checks still build fresh provenance; nothing is cached across audit invocations. |

The ingest API README documents the changed debug contract and collision behavior. No repository dependencies were added.

## Measurements

Local Python 3.11 measurements on this checkout; these are component timings, not deployed latency estimates. Page-read and graph timings are medians of seven calls. Graph construction excludes extraction, layout, and embedding work.

| Operation | Before | After | Output verification |
|---|---:|---:|---|
| Read `wiki/concepts/labs-wiki-architecture.md` through `wiki_read` | 26.081 ms | 0.110 ms | Requested page content retained; explicit-path regression forbids corpus enumeration |
| Construct graph from 980 parsed pages | 11.329 ms | 9.668 ms | 980 nodes and all 3,349 weighted edges unchanged |
| Strict audit of 84 synthesis pages | 84 complete provenance scans; still running at 58 seconds | One scan; 1.24 seconds total | Full JSON output byte-for-byte identical |

## Validation

- Python suite: **97 passed**, no skipped tests, including the installed TF-IDF backend. Existing FastAPI and multipart deprecation warnings remain.
- Graph UI Node tests: **6 passed**.
- `git diff --check`: passed.
- Seven selected new regression checks also failed against the original implementations, confirming that they detect the repaired behavior. The original symlink-loop behavior raised errors; the containment check was additionally verified without that loop and failed seven assertions with no errors.
- Independent read-only review found no correctness or security blocker in the code changes.
- Strict synthesis audit: **84/84 passed**, with all 84 reporting complete claim grounding under the deterministic auditor.

The subsequent integration and documentation merge reran the complete Python
suite: **103 passed**, including six newly versioned durable checkpoint tests.
The native MemPalace transport check also passed against a temporary palace,
including duplicate delivery and the read-only gate. Graph UI tests remained
**6/6**, and the strict synthesis audit remained **84/84**. The versioned
adapter matches the installed runtime source; the test runner resolves that
source from its own directory.

The repository's existing `.venv` lacked pytest, MCP, and python-multipart. Tests ran in `/tmp/labs-wiki-review-venv`, using the existing project packages plus temporary test dependencies, including FastAPI 0.115.0 and MCP 1.30.0. The project environment and dependency files were not changed.

Commands used for the main gates:

```bash
/tmp/labs-wiki-review-venv/bin/python -m pytest -q
node --test wiki-graph-ui/tests/*.test.mjs
/tmp/labs-wiki-review-venv/bin/python scripts/audit_synthesis.py --strict --json-out /tmp/labs-wiki-review-synthesis-after.json
git diff --check
```

## Remaining corpus findings

The general linter scanned 980 pages and reported **zero errors and 1,132 warnings**: 963 stale pages, 163 pages scoring below 50, and six unindexed nested checkpoint summaries.

The stricter shared page validator rejected **139 of 974 top-level canonical pages**. Common findings were missing `concepts` on 110 pages, invalid full SHA-256 hashes on 20, missing `related` on 20, and missing source-summary headings on 12. These categories overlap. Some pages also reference missing raw sources. Thus, a clean general lint result does not establish compliance with the ingest schema.

Recommended follow-up work:

1. Reconcile general lint with the shared schema validator, preserving score calculations and any intentional legacy-page exceptions. This would expose existing schema failures through the routine health command.
2. Curate the 139 failing pages against their raw sources. Restore provenance from evidence; do not invent hashes or substitute source paths.
3. Review stale pages against current sources before changing verification dates. The architecture pages sampled here still describe older backends and planned features that current code already implements.
4. Decide whether the six nested checkpoint summaries belong in the public index or are intentionally archived. The index compiler currently enumerates only top-level category pages.

Corpus audits were read-only. During the review phase, no raw sources, wiki pages, verification dates, scores, memory stores, or live services were changed. The subsequent authorized [Codex checkpoint integration](../docs/codex-durable-memory.md) saved selected results to MemPalace. Browser behavior and deployed API/worker integration remain unverified.
