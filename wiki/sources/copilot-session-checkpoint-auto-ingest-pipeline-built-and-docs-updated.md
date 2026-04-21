---
title: "Copilot Session Checkpoint: Auto-ingest Pipeline Built and Docs Updated"
type: source
created: 2026-04-07
last_verified: 2026-04-21
source_hash: "1e682ce7421bcaeabd752a7742a3c49d999aeb75bc995c31118f12c24d1a690c"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-auto-ingest-pipeline-built-and-docs-updated-f3b54c4f.md
quality_score: 100
concepts:
  - auto-ingest-pipeline-for-wiki-markdown-processing
related:
  - "[[Auto-Ingest Pipeline for Wiki Markdown Processing]]"
  - "[[GitHub Models API]]"
  - "[[Docker]]"
  - "[[Python Watchdog Library]]"
  - "[[Homelab]]"
  - "[[Labs-Wiki]]"
tier: hot
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, labs-wiki, graph, docker, llm, automation, auto-ingest, github-models-api, pipeline]
checkpoint_class: durable-architecture
retention_mode: retain
knowledge_state: validated
---

# Copilot Session Checkpoint: Auto-ingest Pipeline Built and Docs Updated

## Summary

The user wanted to automatically process raw markdown files in their labs-wiki project after they're created via Android share. We built and deployed a complete auto-ingest pipeline: a Docker sidecar service that watches the `raw/` directory for new files, processes them through GPT-4o (GitHub Models API) to extract concepts/entities, generates wiki pages from templates, and updates the index/log. We then updated all project documentation to reflect the new automated flow.

## Key Points

- The user asked how to automatically process raw markdown files created by Android share on their homelab server.
- The user approved the plan and said "build, deploy and validate."
- Created `scripts/auto_ingest.py` — core LLM-powered extraction pipeline.
- Created `scripts/watch_raw.py` — watchdog-based file watcher with 5s debounce.
- Created `scripts/requirements-auto-ingest.txt` — Python dependencies.
- Created `Dockerfile.auto-ingest` — Docker image for the watcher service.

## Execution Snapshot

**Files created:**
- `scripts/auto_ingest.py`: Core LLM extraction pipeline (parse raw → fetch URL → call GPT-4o → generate wiki pages → update log/index)
- `scripts/watch_raw.py`: Watchdog file watcher with debounce, triggers auto_ingest
- `scripts/requirements-auto-ingest.txt`: openai, watchdog, httpx, pyyaml
- `Dockerfile.auto-ingest`: Docker image for the watcher service
- `raw/2026-04-07-llm-wiki.md`: First ingested source (status: ingested)
- `raw/2026-04-07-transformer-architecture-note.md`: Test source via API (status: ingested)
- 10 wiki pages from LLM Wiki gist + 6 wiki pages from Transformer note

**Files modified:**
- `homelab/compose/compose.wiki.yml`: Added `wiki-auto-ingest` service
- `homelab/.env`: Fixed `ITHUB_MODELS_TOKEN` → `GITHUB_MODELS_TOKEN` typo
- `docs/workflows.md`: Added Section 6 (Auto-Ingest) and updated quick reference table
- `README.md`: Updated diagram, quick start, capture sources, skills/services tables
- `docs/architecture.md`: Updated pipeline and capture channel diagrams
- `docs/capture-sources.md`: Updated intro paragraph
- `wiki/index.md`: Auto-rebuilt with 16 entries
- `wiki/log.md`: Two ingest entries appended

**Commits pushed:**
- labs-wiki: `775ca30` feat: add auto-ingest pipeline, `bf9c60a` fix: switch to models.github.ai endpoint, plus doc update commit in progress
- homelab: `4b9e870` feat: add wiki-auto-ingest sidecar

**Deployed:**
- `wiki-auto-ingest` Docker container running and watching `raw/`

**Work in progress:**
- [ ] Still need to update: `docs/tool-setup.md` (lines 127-131, common workflows section), `.github/instructions/raw-sources.instructions.md` (lines 36-40, processing section), `docs/workflows.md` (section 1 header still says manual), `tasks/progress.md` (mark auto-ingest tasks complete)
- [ ] Need to commit and push the remaining doc updates

## Technical Details

- **GitHub Models API**: Free tier with Copilot subscription. GPT-4o is "High" tier: 10 req/min, 50 req/day, 8K in / 4K out tokens. Sufficient for typical usage.
- **Endpoint migration**: `models.inference.ai.azure.com` → `models.github.ai/inference`. Both work. Default now set to new endpoint. Configurable via `GITHUB_MODELS_URL` env var.
- **OpenAI SDK compatibility**: GitHub Models uses OpenAI-compatible API. `openai` Python SDK works with `base_url` override.
- **Raw file permissions**: Files created by `wiki-ingest-api` Docker container are owned by root. Host user `jbl` (uid 1000) can't write them. The `wiki-auto-ingest` container runs as root, so it has no permission issues. This caused a test failure when running `auto_ingest.py` directly on the host — had to use `docker exec` to update the raw file status.
- **Watchdog vs inotify**: Used Python `watchdog` library instead of `inotifywait` — pure Python, no system package dependency, works in Docker.
- **Debounce**: 5-second debounce after file creation before processing, configurable via `DEBOUNCE_SECONDS` env var.
- **URL content fetching**: GitHub gists are handled specially (fetches raw content from `gist.githubusercontent.com`). HTML pages get basic tag stripping. Content capped at 50K chars.
- **LLM structured output**: Uses `response_format={"type": "json_object"}` for reliable JSON extraction. System prompt defines the exact schema.
- **Incremental processing**: SHA-256 hash of source content compared against existing `wiki/sources/` pages. Skips reprocessing if hash matches.
- **ntfy notifications**: Emoji in titles caused ASCII encoding errors. Fixed by removing emoji from title string and using utf-8 encoding for body.
- **Homelab Docker setup**: Compose files in `/home/jbl/projects/homelab/compose/`. Main `docker-compose.yml` includes all stacks. Must use `--env-file /home/jbl/projects/homelab/.env` when running from compose directory. `WIKI_INGEST_PATH` env var points to labs-wiki repo.
- **PAT token scope**: The `GITHUB_MODELS_TOKEN` is a fine-grained PAT (`github_pat_...`). Needs `models:read` permission for GitHub Models API.

## Important Files

- `scripts/auto_ingest.py` (labs-wiki)
- Core of the entire auto-ingest feature. 860+ lines.
- Key functions: `ingest_raw_source()` (main pipeline), `call_llm()` (GitHub Models API), `fetch_url_content()` (URL fetching with gist special-casing), `generate_source_page/concept_page/entity_page()` (wiki page generators)
- Config at top: `GITHUB_MODELS_URL` (line 32-34), `DEFAULT_MODEL` (line 35), `MAX_RETRIES` (line 36)
- LLM system prompt: `SYSTEM_PROMPT` (line ~190-240)

- `scripts/watch_raw.py` (labs-wiki)
- Watchdog-based file watcher. Runs as Docker CMD.
- `RawFileHandler` class with debounce logic
- On startup, processes any existing pending sources before watching

- `Dockerfile.auto-ingest` (labs-wiki)
- Python 3.12-slim, installs requirements, copies scripts + templates
- CMD: `python3 scripts/watch_raw.py`

- `homelab/compose/compose.wiki.yml`
- Defines both `wiki-ingest-api` and `wiki-auto-ingest` services
- Auto-ingest mounts: `raw/`, `wiki/`, `templates/` (ro), `scripts/` (ro)
- Env vars: `GITHUB_MODELS_TOKEN`, `GITHUB_MODELS_MODEL`, `NTFY_SERVER/TOPIC`, `DEBOUNCE_SECONDS`

- `homelab/.env`
- Contains `GITHUB_MODELS_TOKEN`, `WIKI_INGEST_PATH`, `WIKI_API_TOKEN`, `NTFY_SERVER`, `NTFY_TOPIC`
- Gitignored — can't be committed

- `docs/workflows.md` (labs-wiki)
- Section 6 (lines ~152-202): Auto-ingest documentation (complete)
- Sections 1-5: Still reference manual workflow — partially updated in quick reference table

- `README.md` (labs-wiki)
- Updated: mermaid diagram, quick start, capture sources, skills/services tables
- Key change: makes auto-ingest the primary flow, manual skills secondary

- `docs/architecture.md` (labs-wiki)
- Updated: pipeline diagram now shows URL fetching + auto-ingest service
- Updated: capture channel diagram shows auto-ingest between raw/ and wiki/

## Next Steps

**Remaining doc updates (in progress when compaction triggered):**
- `docs/tool-setup.md` line 127-131: "Common Workflows" section still says "Click Ingest into Wiki handoff" — should note auto-ingest handles this
- `.github/instructions/raw-sources.instructions.md` lines 36-40: "Processing" section says "/wiki-ingest pipeline" — should mention auto-ingest
- `docs/workflows.md` line 3: Header still says "five core wiki operations" — should say six (or restructure to lead with auto-ingest)
- `tasks/progress.md`: Mark auto-ingest related tasks as complete

**After doc updates:**
- Commit all remaining doc changes to labs-wiki
- Push to origin
- Rebuild and redeploy `wiki-auto-ingest` container (only needed if scripts changed)

## Related Wiki Pages

- [[Auto-Ingest Pipeline for Wiki Markdown Processing]]
- [[GitHub Models API]]
- [[Docker]]
- [[Python Watchdog Library]]
- [[Homelab]]
- [[Labs-Wiki]]

## Notable Quotes

No notable quotes extracted.

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-auto-ingest-pipeline-built-and-docs-updated-f3b54c4f.md` |
| Type | checkpoint |
| Author | Unknown |
| Date | 2026-04-07 |
| URL | N/A |
