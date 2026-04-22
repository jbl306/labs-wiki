---
title: "Auto-Ingest Pipeline for Wiki Markdown Processing"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "1e682ce7421bcaeabd752a7742a3c49d999aeb75bc995c31118f12c24d1a690c"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-auto-ingest-pipeline-built-and-docs-updated-f3b54c4f.md
quality_score: 79
concepts:
  - auto-ingest-pipeline-for-wiki-markdown-processing
related:
  - "[[Durable Copilot Session Checkpoint Promotion]]"
  - "[[Agentic Wiki Optimization per Karpathy Compile-Once Principles]]"
  - "[[Copilot Session Checkpoint: Auto-ingest Pipeline Built and Docs Updated]]"
tier: hot
tags: [automation, pipeline, wiki-ingestion, docker, github-models-api, llm]
---

# Auto-Ingest Pipeline for Wiki Markdown Processing

## Overview

An automated pipeline designed to watch a directory for new raw markdown files, process them using a large language model via the GitHub Models API, and generate structured wiki pages. This pipeline replaces manual ingestion workflows, improving efficiency and consistency in wiki content creation.

## How It Works

The auto-ingest pipeline operates as a Docker sidecar service running alongside the main wiki system. It continuously monitors the `raw/` directory for newly created markdown files using a Python-based watchdog file watcher with a debounce mechanism to avoid redundant processing. When a new file is detected, the pipeline performs several steps:

1. **File Detection and Debounce:** The watcher waits for a configurable debounce period (default 5 seconds) after file creation to ensure the file is fully written.
2. **Content Fetching:** If the raw markdown references URLs (e.g., GitHub gists), the pipeline fetches the raw content, handling special cases such as gist URLs by fetching from `gist.githubusercontent.com`. For HTML pages, basic tag stripping is applied, and content size is capped at 50,000 characters.
3. **LLM Processing:** The fetched or raw content is sent to the GitHub Models API using GPT-4o with a structured system prompt that instructs the model to extract concepts, entities, and generate wiki page content in a predefined JSON schema (`response_format={"type": "json_object"}`).
4. **Incremental Processing:** The pipeline computes a SHA-256 hash of the source content and compares it against existing wiki source hashes to avoid reprocessing unchanged content.
5. **Wiki Page Generation:** Based on the LLM output, the pipeline generates or updates wiki pages for sources, concepts, and entities using templates.
6. **Index and Log Update:** The wiki index and log files are updated to reflect new or changed content.
7. **Notifications:** The system sends notifications via ntfy, with fixes applied to handle emoji encoding issues.

The pipeline runs inside a Docker container built from a custom Dockerfile (`Dockerfile.auto-ingest`) that installs necessary Python dependencies (`openai`, `watchdog`, `httpx`, `pyyaml`) and runs the watcher script as its command. It integrates tightly with the homelab environment via Docker Compose, mounting necessary volumes and environment variables for tokens and configuration.

This approach leverages the OpenAI-compatible GitHub Models API, using a fine-grained PAT token with `models:read` permission. The pipeline handles endpoint migration transparently, defaulting to the new `models.github.ai/inference` endpoint but allowing configuration via environment variables.

The design choices, such as using Python's watchdog over system tools like inotifywait, ensure compatibility and ease of deployment within Docker. Running the container as root avoids file permission issues with raw files created by other containers.

Overall, this pipeline automates the ingestion and structuring of raw markdown content into a live wiki, enabling a scalable and maintainable knowledge base.

## Key Properties

- **Debounce Time:** Configurable delay (default 5 seconds) after file creation before processing to ensure file stability.
- **GitHub Models API Rate Limits:** Free tier with Copilot subscription allows 10 requests per minute and 50 requests per day for GPT-4o 'High' tier.
- **Content Size Limit:** Fetched URL content is capped at 50,000 characters to control processing load.
- **Incremental Processing:** Uses SHA-256 hash comparison to skip reprocessing unchanged source files.
- **File Permissions:** The auto-ingest container runs as root to avoid permission issues with raw files owned by root.

## Limitations

The pipeline depends on the GitHub Models API rate limits, which can restrict throughput under heavy usage. The use of a debounce timer may delay processing slightly after file creation. The system assumes raw files are well-formed markdown or URLs; malformed inputs may cause extraction errors. Running the container as root may have security implications in some environments. The current implementation handles only markdown files created via Android share and may require adaptation for other sources. Notifications rely on ntfy and require UTF-8 encoding to avoid errors with emoji characters.

## Example

```python
# Simplified pseudocode for the watcher event handler
class RawFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory or not event.src_path.endswith('.md'):
            return
        debounce_wait(DEBOUNCE_SECONDS)
        auto_ingest(event.src_path)

# Core ingestion function

def auto_ingest(filepath):
    content = read_file(filepath)
    if is_url_reference(content):
        content = fetch_url_content(url)
    if sha256(content) == existing_hash:
        return  # Skip
    llm_response = call_github_models_api(content)
    generate_wiki_pages(llm_response)
    update_index_and_log()
    send_ntfy_notification()
```

## Relationship to Other Concepts

- **[[Durable Copilot Session Checkpoint Promotion]]** — The auto-ingest pipeline is a durable checkpoint promoted for Karpathy-style compile-once wiki ingestion.
- **[[Agentic Wiki Optimization per Karpathy Compile-Once Principles]]** — The pipeline supports the compile-once ingestion approach for efficient wiki updates.

## Practical Applications

This pipeline is used to automate the ingestion of raw markdown files created from Android share actions into a structured wiki knowledge base. It enables continuous, real-time updating of wiki content without manual intervention, supporting knowledge management and documentation workflows in homelab or research environments. The approach can be adapted to other content ingestion scenarios requiring LLM-powered extraction and structured content generation.

## Sources

- [[Copilot Session Checkpoint: Auto-ingest Pipeline Built and Docs Updated]] — primary source for this concept
