# Workflows

> Step-by-step guides for wiki operations. Sources are **automatically processed** — manual skills are available for targeted operations.

## 1. Ingest a New Source

Add a raw source — it's automatically processed into wiki pages.

### Steps

1. **Add the source to `raw/`:**
   ```bash
   # Manual: create a markdown file
   cat > raw/2025-07-17-interesting-article.md << 'EOF'
   ---
   title: "Interesting Article About Transformers"
   type: url
   captured: 2025-07-17T10:00:00Z
   source: manual
   url: "https://example.com/article"
   tags: [ml, transformers]
   status: pending
   ---
   
   [Article content or summary here]
   EOF
   
   # Or use the CLI function:
   wa url https://example.com/article "Interesting Article"
   
   # Or upload a file:
   waf ~/Downloads/paper.pdf "Research Paper on Attention"
   ```

2. **Auto-ingest processes it** (within ~5 seconds):
   - The `wiki-auto-ingest` Docker service detects the new file
   - Fetches URL content (for `type: url` sources)
   - Extracts concepts, entities, and facts via GPT-4o
   - Generates wiki pages from templates
   - Updates index and log
   - Marks raw source `status: ingested`

3. **Verify:**
   ```bash
   # Check auto-ingest logs
   docker logs wiki-auto-ingest

   # Or run lint
   /wiki-lint
   ```

4. **Manual alternative** (if auto-ingest is not running):
   ```bash
   python3 scripts/auto_ingest.py raw/2025-07-17-interesting-article.md
   # Or use the Copilot skill:
   /wiki-ingest raw/2025-07-17-interesting-article.md
   ```

## 2. Query the Wiki

Search for information across wiki pages.

### Steps

1. **Ask a question:**
   ```
   /wiki-query What is positional encoding?
   ```

2. **What happens:**
   - Reads `wiki/index.md` to find relevant pages
   - Reads identified pages
   - Synthesizes answer with `[[wikilink]]` citations
   - Warns about stale pages if applicable

3. **Tips:**
   - Be specific — "How does RoPE handle longer sequences?" > "Tell me about encoding"
   - The skill will tell you if information is missing
   - Stale pages are cited with a warning

## 3. Lint the Wiki

Check wiki health and get quality scores.

### Steps

1. **Run a full audit:**
   ```
   /wiki-lint
   ```

2. **Auto-fix safe issues:**
   ```
   /wiki-lint --fix
   ```

3. **Run offline (Python):**
   ```bash
   python3 scripts/lint_wiki.py
   ```

4. **What's checked:**
   - Missing required frontmatter → Error
   - Broken `[[wikilinks]]` → Error
   - Missing provenance → Error
   - Orphan pages → Warning
   - Stale pages (>90 days) → Warning
   - Low quality score (<50) → Warning

## 4. Update a Page

Revise an existing wiki page with new information.

### Steps

1. **Target a specific page:**
   ```
   /wiki-update wiki/concepts/positional-encoding.md
   ```

2. **Or update all stale pages:**
   ```
   /wiki-update --stale
   ```

3. **What happens:**
   - Re-reads source(s) from `raw/`
   - Checks if source content changed (hash comparison)
   - Merges new information (never deletes existing content)
   - Updates `source_hash`, `last_verified`, `quality_score`
   - Updates cross-references
   - Logs the operation

## 5. Orchestrate a Full Pipeline

Run lint → fix → maintenance cycle. (Ingestion is handled automatically by the auto-ingest service.)

### Steps

1. **Full pipeline (most common):**
   ```
   /wiki-orchestrate
   ```

2. **What happens:**
   - Runs lint on all wiki pages
   - Auto-fixes safe issues
   - Reports remaining issues

3. **Other modes:**
   ```
   /wiki-orchestrate audit         # Just full audit
   /wiki-orchestrate maintenance   # Stale page review + index rebuild
   /wiki-orchestrate ingest        # Manually ingest any remaining pending sources
   ```

---

## 6. Auto-Ingest (Automated Processing)

New sources added via the API (Android share, bookmarklet, iOS) are automatically
processed by the `wiki-auto-ingest` Docker service.

### How It Works

1. **Android share / API** creates `raw/YYYY-MM-DD-slug.md` with `status: pending`
2. **File watcher** (watchdog) detects the new file within 5 seconds
3. **LLM pipeline** (GitHub Models API, source-routed):
   - Fetches URL content for `type: url` sources with specialized handlers:
     - **Twitter/X:** extracts tweet text, author, timestamps, and images via fxtwitter API (supports twitter.com, x.com, t.co, vxtwitter, fxtwitter URLs)
     - **GitHub repos:** fetches README, metadata (description, stars, language, topics), and file tree via REST API
     - **HTML pages:** standard fetch with content extraction
    - **Source-aware routing:** Copilot session checkpoint exports and MemPalace bridge exports prefer a lighter text-only model; standard URLs/repos use the default model
    - **Checkpoint classification:** Copilot session checkpoints are classified by `scripts/checkpoint_classifier.py` into one of `durable-architecture`, `durable-debugging`, `durable-workflow`, `project-progress`, or `low-signal`. The class is stamped into raw frontmatter by `homelab/scripts/mempalace-session-curator.py` and propagated into the source page as `checkpoint_class` + `retention_mode`. Retention defaults: durable → `retain`, project-progress → `compress` (page lands in `tier: archive` so it's excluded from hot-tier surfacing), low-signal → `skip`. Override per-class via `LABS_WIKI_CHECKPOINT_RETENTION_OVERRIDES="class=mode,..."`.
    - **Vision support:** downloads images from tweets and pages, analyzes charts/diagrams/screenshots only on the vision-capable lane
   - Auto-follows t.co shortened URLs
   - Extracts concepts, entities, and facts
   - Generates wiki pages from templates
4. **Post-processing**: updates cross-references, log, and index
5. **Notification**: sends ntfy alert on completion

### Manual Trigger

```bash
# Process a specific file
python3 scripts/auto_ingest.py raw/2025-07-17-article.md --project-root .

# Process all pending files
python3 scripts/auto_ingest.py --project-root .
```

### Docker Service

The `wiki-auto-ingest` container runs alongside `wiki-ingest-api` in
`compose.wiki.yml`. It watches the shared `raw/` volume and processes new
sources automatically.

```bash
# View logs
docker logs -f wiki-auto-ingest

# Restart
docker compose -f compose.wiki.yml restart wiki-auto-ingest
```

### Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `GITHUB_MODELS_TOKEN` | — | GitHub PAT with Models API access (required) |
| `GITHUB_MODELS_MODEL` | `gpt-4.1` | Backward-compatible default model fallback |
| `GITHUB_MODELS_MODEL_DEFAULT` | `GITHUB_MODELS_MODEL` | Default text extraction lane |
| `GITHUB_MODELS_MODEL_LIGHT` | `GITHUB_MODELS_MODEL_DEFAULT` | Cheaper lane for session checkpoints / MemPalace exports |
| `GITHUB_MODELS_MODEL_VISION` | `GITHUB_MODELS_MODEL_DEFAULT` | Vision-capable lane for image-bearing sources |
| `GITHUB_MODELS_MODEL_OVERRIDE` | — | Force one model for debugging/manual runs |
| `LABS_WIKI_CHECKPOINT_RETENTION_OVERRIDES` | — | Comma-list `class=mode` overrides for checkpoint retention (e.g. `project-progress=retain,low-signal=compress`) |
| `AUTO_INGEST_MAX_SYNTHESIS_PER_INGEST` | `2` | Cap follow-on synthesis calls per ingest; set `0` for quota-sensitive backlog imports |
| `AUTO_INGEST_INCLUDE_EXISTING_PAGES_CONTEXT` | `1` | Include the existing wiki page list in extraction prompts; set `0` for faster, cheaper backlog imports |
| `DEBOUNCE_SECONDS` | `5` | Wait time after file creation before processing |
| `NTFY_SERVER` | — | ntfy notification server URL |
| `NTFY_TOPIC` | — | ntfy topic for alerts |

---

## Workflow Quick Reference

| I want to... | Command |
|--------------|---------|
| Add and process a new source | Copy to `raw/` → auto-processed, or `/wiki-ingest` |
| Share from Android | Share → HTTP Shortcuts → auto-processed |
| Find information | `/wiki-query <question>` |
| Check wiki health | `/wiki-lint` |
| Fix quality issues | `/wiki-lint --fix` |
| Update a page with new info | `/wiki-update <path>` |
| Process all pending sources | `/wiki-orchestrate` or `python3 scripts/auto_ingest.py` |
| Run offline lint | `python3 scripts/lint_wiki.py` |
| Rebuild index | `python3 scripts/compile_index.py` |
| Check auto-ingest logs | `docker logs -f wiki-auto-ingest` |
