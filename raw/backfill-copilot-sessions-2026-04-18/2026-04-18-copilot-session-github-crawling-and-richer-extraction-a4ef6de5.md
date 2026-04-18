---
title: "Copilot Session Checkpoint: GitHub crawling and richer extraction"
type: text
captured: 2026-04-18T03:23:51.483387Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, labs-wiki, graph, agents]
status: ingested
---

# Copilot Session Checkpoint Export

**Checkpoint title:** GitHub crawling and richer extraction
**Session ID:** `7ccd0122-adc4-4b81-b65b-098fa0804cde`
**Checkpoint file:** `/home/jbl/.copilot/session-state/7ccd0122-adc4-4b81-b65b-098fa0804cde/checkpoints/002-github-crawling-and-richer-ext.md`
**Checkpoint timestamp:** 2026-04-08T01:07:15.867696Z
**Exported:** 2026-04-18T03:23:51.483387Z
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
The user is building a personal LLM-powered knowledge wiki (labs-wiki) and needed several enhancements to the auto-ingest pipeline: fixing Android share issues (prior session), adding deep GitHub repo crawling, fixing image format filtering for vision processing, and improving LLM extraction quality to produce richer concept pages. All changes were deployed to a Docker-based homelab infrastructure.
</overview>

<history>
1. (Prior session) User debugged Android share 422/400 errors from HTTP Shortcuts app
   - Added universal body parsing, auto-type detection, debug endpoint to wiki-ingest-api
   - Root cause was user clicking wrong share button; docs reverted to scripting shortcut
   - Server-side improvements remain deployed

2. User shared a VS Code custom agents URL and asked to validate the auto-ingest pipeline
   - Confirmed full pipeline worked: raw source captured via Android share → auto-ingest processed → 9 wiki pages created (6 concepts, 2 entities, 1 source)
   - Status: ingested, log entry present

3. User asked whether wiki should be pushed to GitHub
   - Checked Karpathy's LLM wiki gist — no mention of git pushing
   - Advised keeping wiki local (it's a living working copy), commit periodically for snapshots

4. User shared their private homelab GitHub repo and asked if all files including docs/ were processed
   - Found auto-ingest only fetched repo metadata + README (shallow) — produced 3 generic pages
   - User requested the GitHub handler crawl all subdirectories automatically

5. Implemented GitHub repo deep crawling in auto_ingest.py
   - Added `_crawl_github_tree()` function using Git Trees API (single request for full tree)
   - Filters for relevant files (.md, .py, .yml, Dockerfile, etc.), prioritizes docs/ directories
   - Budget-based fetching (30K chars) to stay within LLM context limits
   - Tested against public repo (astral-sh/uv) — worked: 10 files fetched, docs/ prioritized

6. Fixed private repo access
   - `GITHUB_MODELS_TOKEN` lacks `repo` scope → 404 on private repos
   - User created `WIKI_GITHUB_PAT` in homelab .env
   - Added `GITHUB_TOKEN=${WIKI_GITHUB_PAT}` to compose.wiki.yml
   - Changed token priority: `GITHUB_TOKEN` preferred over `GITHUB_MODELS_TOKEN` for GitHub API
   - Re-ingested homelab repo: 96 crawlable files found, 7 docs/ files fetched, **18 pages created** (vs 3 before)
   - Committed compose change to homelab repo

7. User discussed whether code repos should be added to wiki
   - Advised: add repos where architecture/design knowledge matters, skip simple/fast-changing repos
   - Wiki provides "what and why", code provides "how exactly" — complementary

8. User shared a GeeksforGeeks ML algorithms article and asked to evaluate quality
   - Ingest **failed** with 400 error: SVG image (`gfg-gg-logo.svg`) rejected by GPT-4.1 vision API
   - Fixed: whitelist vision-compatible MIME types (png/jpeg/webp/gif only)
   - Added URL-level filtering to skip logos/icons/favicons/badges/SVGs during image collection
   - Re-triggered: **22 pages created** successfully with 5 images processed
   - Quality assessment: structure solid but concept pages were thin (glossary-level, 5-6 sentences each)
   - Images processed via vision but didn't visibly enrich the output

9. User asked to tune extraction for richer concept pages
   - Rewrote SYSTEM_PROMPT: demands 3-5 paragraphs in how_it_works, specifics over summaries
   - Added new extraction fields: `limitations`, `example` (with code blocks), `visual_description`
   - Updated concept page template to render optional sections conditionally
   - Bumped max_tokens from 8K to 16K
   - Re-ingested ML article: 12 pages (10 concepts + 1 entity + 1 source) — fewer but much richer
   - Linear Regression page now has: multi-paragraph explanation, O(n×d²) complexity, sklearn code example, visual description of scatter plot, limitations section
   - LLM processing time increased (~90s vs ~50s) due to richer output
</history>

<work_done>
Files updated:
- `scripts/auto_ingest.py`: Major enhancements — GitHub tree crawling, SVG/logo image filtering, richer extraction prompt, new concept page fields, 16K max_tokens
- `wiki-ingest-api/app.py`: (Prior session) Universal ingest handler, debug endpoint, auto-type-detection
- `/home/jbl/projects/homelab/compose/compose.wiki.yml`: Added `GITHUB_TOKEN=${WIKI_GITHUB_PAT}` env var

Commits pushed to main (this session):
- `a3b0ef6` feat(ingest): crawl GitHub repo subdirectories on ingest
- `d14cef9` fix(ingest): prefer GITHUB_TOKEN over GITHUB_MODELS_TOKEN for repo API
- `0df677d` fix(ingest): filter SVG and site chrome from vision pipeline
- `0177987` feat(ingest): deeper extraction — richer concept pages
- `165e90e` (homelab repo) feat(wiki): add GITHUB_TOKEN for private repo crawling

Deployed state:
- wiki-auto-ingest container is running with all improvements
- wiki-ingest-api container unchanged this session (still has prior session's universal parser)
- ML article successfully re-ingested with richer output (12 pages)
- Homelab repo fully crawled (18 pages including all docs/)

Wiki state:
- 69 total entries in index.md
- Several old shallow ML concept pages remain as orphans (e.g., `linear-regression.md` vs new `linear-regression-algorithm.md`) — not cleaned up
</work_done>

<technical_details>
- **GitHub Trees API**: `GET /repos/{owner}/{repo}/git/trees/HEAD?recursive=1` returns full file tree in one request. Individual files fetched via `/repos/{owner}/{repo}/contents/{path}` with `Accept: application/vnd.github.raw+json` header.
- **Token priority for GitHub API**: `GITHUB_TOKEN` (PAT with repo scope) must be preferred over `GITHUB_MODELS_TOKEN` (GitHub Models API key without repo scope). Private repos return 404 with the Models token.
- **Crawl budget system**: 30K char budget for tree files, 20K for README, 50K total cap. Priority: docs/ dirs → root files → everything else. Individual files capped at 8K chars.
- **Vision API format restriction**: GPT-4.1 via GitHub Models only accepts png/jpeg/webp/gif. SVGs cause 400 errors that fail all retries since the same images are sent each time.
- **Image filtering**: Two layers — URL patterns (skip logo/icon/favicon/badge/avatar/svg) and MIME whitelist (only `_VISION_MIMES = {"image/png", "image/jpeg", "image/webp", "image/gif"}`).
- **Extraction depth tradeoff**: Richer prompt produces fewer concepts (10 vs 20 from same article) but each is substantially more useful. LLM processing takes ~90s vs ~50s. The 16K max_tokens accommodates this.
- **File watcher behavior**: `watch_raw.py` uses `on_modified` events from inotify. Files owned by root (created by Docker) need `docker exec touch` to trigger re-processing since host-level `touch` may need sudo.
- **Orphan page issue**: Re-ingesting with the new prompt creates pages with different slugs (e.g., `linear-regression-algorithm.md` vs `linear-regression.md`). Old pages are not automatically cleaned up.
- **Homelab deployment**: `docker compose --env-file ../.env` from `compose/` dir. Wiki services defined in `compose.wiki.yml`, included from main `docker-compose.yml`. `.env` at `/home/jbl/projects/homelab/.env`.
- **og:image still collected from sites**: The first image URL comes from og:image meta tags (not filtered by the logo/icon pattern). The `gfg_200x200-min.png` (GeeksforGeeks favicon) passed because it doesn't match the skip pattern — it's a 200x200 PNG. Could add size-based filtering in the future.
</technical_details>

<important_files>
- `scripts/auto_ingest.py`
   - Core auto-ingest pipeline — all extraction, page generation, URL fetching
   - Added: `_crawl_github_tree()` (~lines 130-245), `_should_crawl()`, `_priority_sort_key()`
   - Modified: `SYSTEM_PROMPT` (~lines 527-600) — richer extraction with new fields
   - Modified: `generate_concept_page()` (~lines 754-850) — renders limitations, example, visual sections
   - Modified: `download_images_as_base64()` (~lines 450-480) — MIME whitelist instead of prefix check
   - Modified: HTML handler image collection (~lines 430-440) — skip logo/icon/favicon patterns
   - Modified: GitHub token priority (~line 330) — `GITHUB_TOKEN` before `GITHUB_MODELS_TOKEN`
   - Modified: `max_tokens=16000` (~line 651)

- `scripts/watch_raw.py`
   - File watcher that triggers auto_ingest.py on new/modified raw sources
   - Not modified this session but important for understanding trigger behavior

- `/home/jbl/projects/homelab/compose/compose.wiki.yml`
   - Docker compose for wiki services (not in labs-wiki repo)
   - Added `GITHUB_TOKEN=${WIKI_GITHUB_PAT}` to wiki-auto-ingest environment (~line 52)

- `wiki-ingest-api/app.py`
   - FastAPI capture service — receives sources from Android/browser/CLI
   - Modified in prior session (universal parser, debug endpoint) — not touched this session

- `wiki/index.md`
   - Auto-generated wiki index — currently 69 entries
   - Contains orphan entries from old shallow ML concept pages
</important_files>

<next_steps>
Potential cleanup/improvements:
- **Orphan page cleanup**: Old shallow ML concept pages (e.g., `linear-regression.md`, `decision-trees.md`) still exist alongside new richer versions (`linear-regression-algorithm.md`). Should delete old ones and rebuild index.
- **og:image filtering**: Small site favicons/logos that come via og:image meta tags still pass through (e.g., gfg_200x200-min.png). Could add minimum dimension check or URL heuristic.
- **Remove debug endpoint**: `/api/debug` in app.py still deployed (no auth required). Should remove once Android share is confirmed stable.
- **Remove unused IngestRequest model**: Pydantic model in app.py no longer referenced by any endpoint.
- **Clean up verbose INGEST DEBUG logging**: Still active in app.py from prior debugging session.

No immediate user request pending — all tasks from this session are complete.
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
