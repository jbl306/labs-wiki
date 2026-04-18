---
title: "GitHub Repository Deep Crawling for Wiki Ingestion"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "e2f4e2c57a91e050124e6a177d9272a75a50ab4d9ee6cb6bb30f2ad73e5652bb"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-github-crawling-and-richer-extraction-a4ef6de5.md
quality_score: 0
concepts:
  - github-repository-deep-crawling-for-wiki-ingestion
related:
  - "[[Auto-Ingest Pipeline for Wiki Markdown Processing]]"
  - "[[Durable Copilot Session Checkpoint Promotion]]"
  - "[[Copilot Session Checkpoint: GitHub Crawling and Richer Extraction]]"
tier: hot
tags: [github, wiki-ingestion, auto-ingest, repository-crawling]
---

# GitHub Repository Deep Crawling for Wiki Ingestion

## Overview

Deep crawling of GitHub repositories enables comprehensive ingestion of source files beyond shallow metadata and README files, allowing a personal knowledge wiki to capture detailed architecture and documentation content. This approach uses the Git Trees API to fetch the entire file tree in a single request, followed by selective file content retrieval based on relevance and budget constraints.

## How It Works

The deep crawling process begins with a call to the GitHub Trees API endpoint `GET /repos/{owner}/{repo}/git/trees/HEAD?recursive=1`, which returns the full file tree of the repository in one response. This eliminates the need for multiple paginated requests and enables efficient enumeration of all files and directories.

Once the file tree is obtained, the system applies filters to select relevant files for ingestion. These filters prioritize files in `docs/` directories and include extensions such as `.md`, `.py`, `.yml`, and `Dockerfile`. The filtering ensures that only meaningful documentation and code files are processed, reducing noise.

A crawl budget system is implemented to manage the amount of data fetched and processed, respecting LLM context length limits. The budget allocates 30,000 characters for tree files, 20,000 for README files, and a total cap of 50,000 characters. Individual files are capped at 8,000 characters to avoid oversized inputs.

Selected files are fetched individually via the GitHub Contents API with the header `Accept: application/vnd.github.raw+json` to retrieve raw file content. This content is then passed to the ingestion pipeline for extraction and page generation.

This method supports both public and private repositories, with private repo access requiring a personal access token (PAT) with `repo` scope. The system prioritizes the PAT (`GITHUB_TOKEN`) over the GitHub Models API token (`GITHUB_MODELS_TOKEN`) to avoid 404 errors on private repos.

The deep crawling approach enables the wiki to create many more pages from a repository (e.g., 18 pages from a homelab repo vs. 3 pages shallow crawl), significantly enriching the knowledge base.

## Key Properties

- **API Usage:** Uses GitHub Trees API for full file tree retrieval and GitHub Contents API for file content fetching.
- **Filtering:** Filters files by extension and directory priority (docs/), with crawl budget limits to manage LLM context constraints.
- **Authentication:** Requires GitHub PAT with repo scope for private repo access; token priority ensures correct authentication.
- **Budget System:** Character limits per file and overall to prevent exceeding LLM input size.

## Limitations

The crawl budget may exclude some files if the repository is very large, potentially missing less prioritized content. The system relies on correct token configuration for private repos; misconfiguration leads to access errors. The approach assumes GitHub API availability and rate limits are respected. It does not currently handle non-GitHub repositories or other version control systems.

## Example

Pseudocode for crawling GitHub repo tree:

```python
# Fetch full repo tree
response = github_api.get('/repos/{owner}/{repo}/git/trees/HEAD?recursive=1')
file_tree = response.json()['tree']

# Filter relevant files
relevant_files = [f for f in file_tree if f['path'].endswith(('.md', '.py', '.yml')) or 'docs/' in f['path']]

# Apply crawl budget
selected_files = budgeted_selection(relevant_files, char_limit=30000)

# Fetch file contents
for file in selected_files:
    content = github_api.get(f'/repos/{owner}/{repo}/contents/{file['path']}', headers={'Accept': 'application/vnd.github.raw+json'})
    process_content(content.text)
```

## Relationship to Other Concepts

- **[[Auto-Ingest Pipeline for Wiki Markdown Processing]]** — Deep crawling feeds file content into the auto-ingest pipeline for processing.
- **[[Durable Copilot Session Checkpoint Promotion]]** — Checkpoint promotes durable state of the crawling and ingestion improvements.

## Practical Applications

Useful for personal or organizational knowledge wikis that integrate source code repositories to capture architectural and design knowledge. Enables automated, comprehensive ingestion of documentation and code files from GitHub repos, improving knowledge completeness and searchability.

## Sources

- [[Copilot Session Checkpoint: GitHub Crawling and Richer Extraction]] — primary source for this concept
