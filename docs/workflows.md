# Workflows

The auto-ingest service processes pending sources. Run the commands below from the repository root.

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
   - Fetches URL content (for `type: url` sources) and persists a deterministic fetched-content block back into `raw/`
   - Compiles source, concept, entity, and synthesis pages via Codex CLI
   - Generates wiki pages from templates
   - Updates index and log
   - Marks raw source `status: ingested`

3. **Verify:**
   ```bash
   # Check auto-ingest logs
   docker logs wiki-auto-ingest

   # Or run lint
   python3 scripts/lint_wiki.py
   ```

4. **Manual alternative** (if auto-ingest is not running):
   ```bash
   python3 scripts/auto_ingest.py raw/2025-07-17-interesting-article.md
   ```

## 2. Query the Wiki

Use the Wiki MCP tools in a connected client. For a question about positional encoding, call `wiki_search` with `query="positional encoding"`, then call `wiki_read` with a returned page title or path. Cite the pages you used with `[[wikilinks]]` and flag stale or missing evidence. In a local checkout, use `wiki/index.md` to find pages.

## 3. Lint the Wiki

```bash
python3 scripts/lint_wiki.py
```

The report lists frontmatter and link errors, index and staleness warnings, and page scores. To persist recalculated scores during maintenance, run `python3 scripts/lint_wiki.py --write-scores`. Follow the [Wiki Lint persona](../agents/wiki-lint.agent.md) to investigate other findings. Rebuild a stale index with `python3 scripts/compile_index.py`.

## 4. Update a Page

Follow the [Wiki Update persona](../agents/wiki-update.agent.md) for the target page. To find stale pages, start with the lint report. Read the original sources, revise supported claims and cross-references, and record the review in `last_verified`. Update `source_hash` when the source changes and log the revision in `wiki/log.md`.

## 5. Coordinate Maintenance

The [Wiki Orchestrate persona](../agents/wiki-orchestrate.agent.md) describes the audit, maintenance and manual ingest workflows. An audit reports lint findings and proposed repairs. During authorized maintenance, review stale pages and tier changes, apply the selected repairs, then rerun lint. When the watcher is unavailable, use the manual trigger below for the selected sources.

---

## 6. Auto-Ingest (Automated Processing)

New sources added via the API (Android share, bookmarklet, iOS) are automatically
processed by the `wiki-auto-ingest` Docker service.

### How It Works

1. **Android share / API** creates `raw/YYYY-MM-DD-slug.md` with `status: pending`
2. **File watcher** (watchdog) detects the new file within 5 seconds
3. **LLM pipeline** (Codex CLI, source-routed):
   - Fetches URL content for `type: url` sources with specialized handlers:
     - **Twitter/X:** extracts tweet text, author, timestamps, and images via fxtwitter API (supports twitter.com, x.com, t.co, vxtwitter, fxtwitter URLs)
     - **GitHub repos:** fetches README, metadata (description, stars, language, topics), and file tree via REST API
      - **HTML pages:** structure-aware fetch with headings/lists/code/table preservation
    - **Source-aware routing:** agent-session checkpoint exports and MemPalace bridge exports prefer lower reasoning effort; standard URLs/repos use medium effort; PDFs and complex inputs use high effort
    - **Checkpoint classification:** Copilot session checkpoints are classified by `scripts/checkpoint_classifier.py` into one of `durable-architecture`, `durable-debugging`, `durable-workflow`, `project-progress`, or `low-signal`. The class is stamped into raw frontmatter by `homelab/scripts/mempalace-session-curator.py` and propagated into the source page as `checkpoint_class` + `retention_mode`. Retention defaults: durable → `retain`, project-progress → `compress` (page lands in `tier: archive` so it's excluded from hot-tier surfacing), low-signal → `skip`. Override per-class via `LABS_WIKI_CHECKPOINT_RETENTION_OVERRIDES="class=mode,..."`.
    - **Vision support:** downloads images from tweets and pages, analyzes charts/diagrams/screenshots only on the vision-capable lane
   - Auto-follows t.co shortened URLs
   - Extracts concepts, entities, and facts
   - Generates wiki pages from templates
4. **Validation/finalization**: validates Codex's schema-constrained status,
   reported paths, source provenance, and any new synthesis page; only then the
   orchestrator updates raw status, log, and index
5. **Notification**: sends ntfy alert on completion

### Manual Trigger

```bash
# Process a specific file
python3 scripts/auto_ingest.py raw/2025-07-17-article.md --project-root .

# Reprocess an already-ingested file using the persisted fetched-content block
python3 scripts/auto_ingest.py raw/2025-07-17-article.md --project-root . --force

# Re-fetch the URL and replace the persisted fetched-content block
python3 scripts/auto_ingest.py raw/2025-07-17-article.md --project-root . --force --refresh-fetch

# Quota-safe targeted rerun
AUTO_INGEST_MAX_SYNTHESIS_PER_INGEST=0 python3 scripts/auto_ingest.py raw/2025-07-17-article.md --project-root . --force

# Validation rerun — update raw snapshot and pages; skip wiki/log.md and notifications
AUTO_INGEST_MAX_SYNTHESIS_PER_INGEST=0 python3 scripts/auto_ingest.py raw/2025-07-17-article.md --project-root . --force --refresh-fetch --validation-run

# Process all pending files
python3 scripts/auto_ingest.py --project-root .

# Measure synthesis quality across the corpus
python3 scripts/audit_synthesis.py --json-out reports/synthesis-audit.json

# Gate a newly created synthesis page
python3 scripts/audit_synthesis.py --page wiki/synthesis/example.md --strict
```

### Validation-Run Policy

Use `--validation-run` (requires `--force`) when you want to verify extraction quality on a single
already-ingested file without generating audit noise. A validation run:

- re-fetches the URL (with `--refresh-fetch`) or reuses the persisted block
- rewrites the raw snapshot and wiki source pages normally
- **does not** append an entry to `wiki/log.md`
- **does not** send an ntfy notification
- **does not** auto-commit the review output

The Codex ingest transaction also updates the index, graph, and checkpoint tracker and can replay pending knowledge-graph facts. For an isolated extraction check, use a disposable project root with external services isolated.

### Docker Service

Source-page reconciliation identifies arXiv abstract, PDF, and HTML URLs and
Hugging Face `/papers/<arxiv-id>` listings by their validated arXiv ID. A later
full-paper capture can enrich the existing source page while preserving both
raw references. Different IDs, other hosts, and unrecognized paths remain
distinct; a matching title alone never authorizes a merge. If reconciliation
fails, the raw source stays pending and canonical wiki state is unchanged.
Every proposed page update must use the orchestrator's current `SOURCE_HASH`,
including multi-source canonical pages; earlier provenance stays in `sources`.

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
| `WIKI_INGEST_BACKEND` | `codex-cli` | Processing backend; legacy `copilot-cli` and API backends remain explicit compatibility options |
| `WIKI_INGEST_MODEL` | `gpt-5.6-luna` | Default Codex model when no override is supplied |
| `WIKI_INGEST_MODEL_OVERRIDE` | — | Force one model for debugging/manual runs |
| `CODEX_HOME` | `~/.codex` | Writable Codex auth/config directory; treat `auth.json` as a secret and persist refreshed auth securely |
| `GITHUB_MODELS_TOKEN` | — | Required only for the explicit legacy GitHub Models backend |
| `LABS_WIKI_CHECKPOINT_RETENTION_OVERRIDES` | — | Comma-list `class=mode` overrides for checkpoint retention (e.g. `project-progress=retain,low-signal=compress`) |
| `AUTO_INGEST_MAX_SYNTHESIS_PER_INGEST` | `1` | Cap follow-on synthesis creation per ingest; set `0` for quota-sensitive backlog imports |
| `AUTO_INGEST_INCLUDE_EXISTING_PAGES_CONTEXT` | `1` | Include the existing wiki page list in extraction prompts; set `0` for faster, cheaper backlog imports |
| `AUTO_INGEST_CHECKPOINT_FAMILY_MIN` | `3` | Minimum checkpoints (incl. the new one) sharing concepts that triggers a "recurring patterns" synthesis suggestion |
| `AUTO_INGEST_CHECKPOINT_FAMILY_SHARED` | `1` | Minimum number of concepts a checkpoint must share with the new one to count as a family member |
| `DEBOUNCE_SECONDS` | `5` | Wait time after file creation before processing |
| `NTFY_SERVER` | — | ntfy notification server URL |
| `NTFY_TOPIC` | — | ntfy topic for alerts |

---

## 7. Build the Knowledge Graph

Rebuild the graph artifact and generate the checkpoint graph tracker report.

### Command

```bash
python3 wiki-graph-api/graph_builder.py \
  --wiki wiki \
  --cache wiki-graph-api/.cache \
  --out wiki/graph/graph.json
```

This writes two artifacts:

- `wiki/graph/graph.json` — node-link graph for the WebGL and Canvas renderers and the graph API
- `reports/checkpoint-graph-tracker.md` — **report-only** tracker comparing graph recommendations to heuristic frontmatter baselines

### Checkpoint graph tracker

The tracker is auto-generated on every build. It:

- Compares the graph-derived recommendation (`keep` / `compress` / `merge` / `archive`) to the heuristic baseline from each checkpoint's `checkpoint_class` + `retention_mode` frontmatter
- Shows disagreement counts and a breakdown by transition type (e.g. `compress→keep`)
- Lists every disagreeing checkpoint with path, class, retention, recommendations, degree, and neighbor counts
- Surfaces merge-cluster candidates (communities with ≥ 3 checkpoints)

It does **not** rewrite any wiki page, tier, or frontmatter field. Use it to evaluate whether the graph and heuristic layers agree before making any policy change.

---

## Workflow Quick Reference

| Task | Entry point |
|--------------|---------|
| Add and process a new source | Capture a pending source for the watcher, or run `python3 scripts/auto_ingest.py raw/example.md` |
| Share from Android | Share → HTTP Shortcuts → auto-processed |
| Find information | Wiki MCP tools `wiki_search` and `wiki_read` |
| Check wiki health | `python3 scripts/lint_wiki.py` |
| Update a page with new info | [Wiki Update persona](../agents/wiki-update.agent.md) |
| Process all pending sources | `python3 scripts/auto_ingest.py --project-root .` |
| Rebuild index | `python3 scripts/compile_index.py` |
| Build knowledge graph + checkpoint tracker | `python3 wiki-graph-api/graph_builder.py --wiki wiki --cache wiki-graph-api/.cache --out wiki/graph/graph.json` |
| Check auto-ingest logs | `docker logs -f wiki-auto-ingest` |
