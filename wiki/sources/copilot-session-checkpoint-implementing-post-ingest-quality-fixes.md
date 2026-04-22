---
title: "Copilot Session Checkpoint: Implementing Post-Ingest Quality Fixes"
type: source
created: 2026-04-10
last_verified: 2026-04-21
source_hash: "b63d1672165b80d7c8439cbcccceb1221f2692ca78875b666163fda03d13e59a"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-implementing-post-ingest-quality-fixes-1de9c8cc.md
quality_score: 84
concepts:
  - post-ingest-quality-fixes-auto-ingest-pipelines
related:
  - "[[Post-Ingest Quality Fixes in Auto-Ingest Pipelines]]"
  - "[[labs-wiki]]"
tier: hot
tags: [copilot-session, checkpoint, fileback, durable-knowledge, labs-wiki, graph, agents, auto-ingest, LLM, post-processing, quality-fixes]
checkpoint_class: durable-architecture
retention_mode: retain
knowledge_state: validated
---

# Copilot Session Checkpoint: Implementing Post-Ingest Quality Fixes

## Summary

The user is working on labs-wiki, a personal LLM-powered knowledge wiki that auto-ingests sources into compiled wiki pages. Across this session: (1) compared labs-wiki against graphify and created an integration plan, (2) pushed it to GitHub, (3) evaluated quality of today's (April 10, 2026) auto-ingested wiki content against raw sources, (4) pushed the evaluation, and (5) began implementing the recommendations from the quality evaluation — fixing the auto-ingest post-processing pipeline. The implementation is mid-way through, with core changes applied to `scripts/auto_ingest.py` but not yet fully tested or committed.

## Key Points

- Deep analysis of graphify codebase
- Feature comparison plan with integration roadmap
- Quality evaluation of today's 5 ingests (29 pages)
- Both plans pushed to GitHub
- LLM prompt hardening (provenance, dates, related_entities)
- Richer entity template with reciprocal linking

## Execution Snapshot

**Files created:**
- `plans/graphify-integration.md`: Full comparison plan (pushed, commit 97eb713)
- `plans/quality-evaluation-2026-04-10.md`: Quality evaluation report (pushed, commit 5859670)

**Files modified (NOT YET COMMITTED):**
- `scripts/auto_ingest.py`: 4 major changes applied

**Changes to auto_ingest.py:**
1. **SYSTEM_PROMPT updated** (~line 576-596): Added "CRITICAL: Provenance & Accuracy" section with 5 new rules:
- No external URLs not in source
- No date fabrication (use null)
- No external source citations
- related_concepts limited to extracted or existing pages
- related_entities from same source

2. **Entity JSON schema updated** (~line 645-660): Added `related_entities` field, made `overview`/`created_year`/`creator`/`url`/`relevance` descriptions more explicit about requiring source grounding

3. **`generate_entity_page()` rewritten** (~line 1050-1120): Now accepts `all_entities` parameter for reciprocal cross-linking. Builds Related Entities section from both LLM-extracted `related_entities` and other entities in same batch

4. **`postprocess_created_pages()` added** (~line 1310-1415): New function that:
- Collects all valid page titles from wiki
- For each created page: removes broken wikilinks from body, removes broken/self-referential/duplicate entries from frontmatter `related:`, computes and writes `quality_score`

5. **Entity generation call updated** (~line 1440): Passes `all_entities=all_entities` to `generate_entity_page()`

6. **Post-process call added** (~line 1540): `postprocess_created_pages()` called before log/index/status update

**Work completed:**
- [x] Deep analysis of graphify codebase
- [x] Feature comparison plan with integration roadmap
- [x] Quality evaluation of today's 5 ingests (29 pages)
- [x] Both plans pushed to GitHub
- [x] LLM prompt hardening (provenance, dates, related_entities)
- [x] Richer entity template with reciprocal linking
- [x] Post-processing function (wikilink cleanup + quality scoring)
- [x] Integration into ingest pipeline
- [x] Syntax verification (ast.parse passes)
- [x] Module import verification (all new functions importable)
- [x] Basic functional test on rlm-qwen3-8b.md (works: deduped related, scored 100)
- [ ] **IN PROGRESS**: Broader validation testing across more pages
- [ ] **NOT STARTED**: Run full lint to compare before/after
- [ ] **NOT STARTED**: Commit and push changes
- [ ] **NOT STARTED**: Consider one-time cleanup of ALL existing 184 broken wikilinks

## Technical Details

- **URL fetchers** (lines ~250-495): Smart handlers for arXiv (HTML→abstract fallback), Twitter/X (fxtwitter API), GitHub repos (REST API + tree crawl), GitHub gists, generic HTML with vision support
- **LLM extraction** (lines ~570-730): SYSTEM_PROMPT defines JSON schema for concepts/entities/synthesis. Uses OpenAI client against GitHub Models API (GPT-4.1). Temperature 0.3, max 16K tokens, json_object response format
- **Page generators** (lines ~850-1230): `generate_source_page()`, `generate_concept_page()`, `generate_entity_page()`, `generate_synthesis_page()` — each returns (filename, content) tuple
- **Post-processing** (lines ~1310-1415): NEW — `postprocess_created_pages()` validates wikilinks, removes self-refs/dupes, computes quality scores
- **Main pipeline** `ingest_raw_source()` (lines ~1440-1570): Orchestrates: parse raw → fetch URL → hash check → LLM extract → generate pages → POST-PROCESS → log → index → status → notify ### Quality Evaluation Findings (April 10 ingests)
- **29 pages from 5 sources**, overall grade B+
- Best: Lottery Ticket Hypothesis (A) — accurate math notation, 3 good concept decompositions
- Worst issues: 8+ broken wikilinks, thin entity pages, quality_score always 0
- Root cause of broken links: LLM generates related: wikilinks to conceptually related topics without checking existence
- Root cause of thin entities: template is minimal, LLM not prompted for related_entities ### Wiki-wide Link Health (pre-fix)
- 185 valid page titles total
- 184 broken wikilinks across entire wiki (not just today's)
- 11 self-referential links
- 7 duplicate related: entries ### Key Quirks
- Wiki files created by Docker sidecar are owned by root — `sudo chown -R jbl:jbl wiki/` needed before local scripts can modify them
- The `parse_frontmatter()` in auto_ingest.py is a custom YAML parser (not yaml.safe_load) — handles lists and inline arrays but has edge cases
- lint_wiki.py has its own separate `parse_frontmatter()` and `compute_quality_score()` — the new `_compute_quality_score()` in auto_ingest.py mirrors it but is independent
- `_compute_quality_score` gives 25 points each for: required fields, cross-references, source attribution, staleness (new pages always get staleness points = 100 max for well-linked pages)
- The entity page test showed 3 remaining `[[Recursive Language Models]]` links after processing — 1 in related (correct), 1 in Associated Concepts body, 1 in Sources body. The duplicate was removed from related: frontmatter. This is correct behavior. ### SQL Todo Tracking 7 todos created with dependencies:
- prompt-hardening → done (implemented)
- richer-entities → done (implemented)
- wikilink-postprocessor → done (depends on prompt-hardening)
- self-ref-removal → done (part of postprocessor)
- dedup-related → done (part of postprocessor)
- reciprocal-entities → done (depends on richer-entities)
- quality-scoring → done (part of postprocessor) ### Environment
- Docker sidecar (`wiki-auto-ingest`) watches raw/ and runs auto_ingest.py
- Deployed at wiki-ingest.jbl-lab.com via Caddy proxy
- Model: GPT-4.1 via GitHub Models API (GITHUB_MODELS_TOKEN env var)
- Python dependencies: httpx, openai (in requirements-auto-ingest.txt)

## Important Files

- `scripts/auto_ingest.py`
- Core of the auto-ingest pipeline — ALL implementation changes are here
- 4 major modifications: prompt hardening (~line 576), entity schema (~line 645), generate_entity_page (~line 1050), postprocess_created_pages (~line 1310), pipeline integration (~line 1440, 1540)
- NOT YET COMMITTED — changes are in working tree only

- `scripts/lint_wiki.py`
- Quality scoring logic that the post-processor mirrors
- NOT modified — read-only reference
- compute_quality_score at line 57-82

- `plans/graphify-integration.md`
- Comparison plan: labs-wiki vs graphify, 3-phase integration roadmap
- Committed and pushed (97eb713)

- `plans/quality-evaluation-2026-04-10.md`
- Quality evaluation of today's 5 ingests → 29 pages
- Recommendations section (lines 187-210) is what we're implementing
- Committed and pushed (5859670)

- `wiki/entities/rlm-qwen3-8b.md`
- Used as test target for post-processor — was modified during testing
- Now has quality_score: 100 and deduplicated related: field
- This test modification should be part of the commit or reverted

## Next Steps

**Remaining work:**
1. **Broader validation** — Run post-processor on more of today's pages (especially ones with known broken links like autoskills, axi, llm-reasoning) to verify it handles all edge cases
2. **Consider one-time wiki-wide cleanup** — 184 broken wikilinks exist across entire wiki, not just today's. Could run postprocess on all pages, or add a `--fix-all` mode to the script
3. **Run lint before/after** — `python3 scripts/lint_wiki.py --wiki-dir .` to measure improvement
4. **Commit and push** — All auto_ingest.py changes + any wiki page fixes
5. **Update SQL todos** — Mark all as done
6. **Docker rebuild consideration** — The auto-ingest Docker sidecar needs to be rebuilt to pick up these changes. User may need to rebuild the container image.

**Immediate next actions:**
- Run the post-processor on all of today's 29 pages to validate
- Run lint_wiki.py to see error count reduction
- Decide whether to do wiki-wide cleanup now or just commit the pipeline fix
- Git commit with descriptive message + push

**Open questions:**
- Should we fix ALL 184 broken links wiki-wide, or only apply fixes to new ingests going forward?
- Does the Docker sidecar auto-rebuild, or does user need to manually rebuild?
- The test modified wiki/entities/rlm-qwen3-8b.md — should this be committed as-is or reverted to keep the commit clean (pipeline-only)?

## Related Wiki Pages

- [[Post-Ingest Quality Fixes in Auto-Ingest Pipelines]]
- [[labs-wiki]]

## Notable Quotes

No notable quotes extracted.

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-implementing-post-ingest-quality-fixes-1de9c8cc.md` |
| Type | checkpoint |
| Author | Unknown |
| Date | 2026-04-10 |
| URL | N/A |
