---
title: "Auto-Ingest Pipeline for LLM-Powered Knowledge Wiki"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "ef21462a91cbbb64334e1aea7918a68cdf91d2b793139ef7974986c7deb8ef39"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-pipeline-enhancements-and-vision-support-deploye-5028ddea.md
quality_score: 100
concepts:
  - auto-ingest-pipeline-for-llm-powered-knowledge-wiki
related:
  - "[[Karpathy LLM Wiki Pattern]]"
  - "[[Vision-Language-Action (VLA) Models]]"
  - "[[Copilot Session Checkpoint: Pipeline Enhancements and Vision Support Deployed]]"
tier: hot
tags: [auto-ingest, pipeline, LLM, vision, github-models-api]
---

# Auto-Ingest Pipeline for LLM-Powered Knowledge Wiki

## Overview

An automated pipeline designed to watch a directory of raw markdown files and process them into structured wiki pages using large language models. This pipeline automates the ingestion of new content, enabling continuous and scalable knowledge base updates without manual intervention.

## How It Works

The auto-ingest pipeline operates by continuously monitoring a designated raw content directory (`raw/`) using a file watcher implemented with the Python Watchdog library. When new or updated markdown files are detected, the pipeline triggers extraction and processing routines.

The core extraction logic is implemented in `scripts/auto_ingest.py`, which leverages the GitHub Models API to call large language models (LLMs) for content understanding and transformation. The pipeline supports multiple URL handlers to intelligently fetch and parse content from special sources such as Twitter/X tweets and GitHub repositories.

For Twitter/X, the pipeline uses the fxtwitter API to retrieve tweet text, author metadata, media URLs, and quoted tweets. For GitHub repositories, it uses the GitHub REST API to fetch repository metadata and raw README content.

The pipeline also supports vision capabilities by downloading images referenced in content, encoding them in base64, and sending them as multimodal inputs to GPT-4.1, enabling extraction of information from diagrams, charts, and screenshots.

The system is deployed as a Docker container (`wiki-auto-ingest`) running as a sidecar service alongside the wiki ingestion API. It uses a debounce mechanism (default 5 seconds) to batch file changes and avoid redundant processing. The pipeline is configured to use GPT-4.1 as the default model for high throughput and vision support.

This design ensures that raw source documents remain immutable (Layer 1), while the pipeline compiles and updates Layer 2 wiki pages automatically, supporting continuous knowledge base growth with minimal manual effort.

## Key Properties

- **File Watching:** Uses Python Watchdog library to monitor `raw/` directory with a 5-second debounce to detect new or changed markdown files.
- **Smart URL Handlers:** Specialized handlers for Twitter/X (fxtwitter API) and GitHub repos (REST API) to fetch rich metadata and content.
- **Vision Support:** Downloads images, encodes them in base64, and sends to GPT-4.1 multimodal API for content extraction from visuals.
- **Model Usage:** Default model is GPT-4.1, offering 149 requests/min and 148,500 tokens/min throughput, with vision capabilities.
- **Deployment:** Runs as a Docker sidecar container with root permissions to handle file ownership issues and integrates with existing wiki services.

## Limitations

Vision support requires local image download and base64 encoding; remote image URLs cannot be processed directly. The pipeline depends on external APIs (fxtwitter, GitHub REST) which may have rate limits or availability constraints. The file watcher debounce may delay processing slightly. The system assumes raw files are immutable and does not handle manual edits to compiled wiki pages.

## Example

```python
# Simplified pseudocode for file watcher triggering ingest
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class RawFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith('.md'):
            ingest_raw_source(event.src_path)

observer = Observer()
observer.schedule(RawFileHandler(), path='raw/', recursive=False)
observer.start()
```

The `ingest_raw_source` function calls the LLM via GitHub Models API, applying smart URL handlers and vision processing as needed.

## Visual

The source includes a pipeline diagram updated in `docs/architecture.md` showing the flow from raw file detection, through smart URL handling, to LLM processing with vision support, and finally wiki page generation.

## Relationship to Other Concepts

- **[[Karpathy LLM Wiki Pattern]]** — The auto-ingest pipeline implements Layer 1 to Layer 2 ingestion in Karpathy's 3-layer wiki architecture.
- **[[Vision-Language-Action (VLA) Models]]** — The pipeline leverages GPT-4.1's vision capabilities, a form of VLA model, to extract information from images.

## Practical Applications

Automates ingestion of diverse knowledge sources into a personal or organizational LLM-powered wiki, enabling continuous updates from social media, code repositories, and image-rich content without manual curation. Useful for research knowledge bases, technical documentation, and dynamic content aggregation.

## Sources

- [[Copilot Session Checkpoint: Pipeline Enhancements and Vision Support Deployed]] — primary source for this concept
