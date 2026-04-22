---
title: "Richer GitHub Repository Ingestion Workflow"
type: concept
created: 2026-04-22
last_verified: 2026-04-22
source_hash: "0a4ff72c02c43a07f603a8baab32716ef2cb63b6d31b3dd941b64676f49cd7bd"
sources:
  - raw/2026-04-22-copilot-session-mobile-node-viewer-and-richer-github-ingestion-8b1dee20.md
quality_score: 100
concepts:
  - richer-github-repository-ingestion-workflow
related:
  - "[[GitHub Repository Deep Crawling for Wiki Ingestion]]"
  - "[[Copilot Session Checkpoint: Mobile Node Viewer And Richer GitHub Ingestion]]"
tier: hot
tags: [github-ingestion, crawler, documentation, activity-snapshot]
---

# Richer GitHub Repository Ingestion Workflow

## Overview

The richer GitHub ingestion workflow expands the scope and depth of repository data captured for wiki pages. It includes additional metadata, files, and activity snapshots, improving the completeness and utility of ingested source pages for technical documentation and knowledge management.

## How It Works

The ingestion workflow is implemented in `scripts/auto_ingest.py`, with enhancements to the GitHub crawler. The `_CRAWL_EXACT` constant now includes common manifest files (e.g., `pyproject.toml`, `package.json`, `go.mod`, `Cargo.toml`, `requirements.txt`, `docker-compose.yml`, `Gemfile`), ensuring these are prioritized alongside per-directory README files. The `_priority_sort_key` is rewritten to sort manifests and READMEs first, followed by priority directories, root files, and the rest.

Crawl budgets are expanded: `_MAX_FILE_CHARS` increases from 8K to 16K, overall crawl budget from 30K to 80K, and output cap from 50K to 140K. The repo handler now issues five additional API calls to fetch `/languages`, `/releases?per_page=5`, `/commits?per_page=20`, `/issues?state=open&per_page=10`, and `/pulls?state=closed&per_page=20` (filtered to merged). This provides a snapshot of repository activity, language breakdown, and release history, which are included in the source page.

Authentication is handled via the `GITHUB_TOKEN` environment variable, with fallback to `GITHUB_MODELS_TOKEN`. Anonymous requests are rate-limited to 60/hr, while authenticated requests allow 5000/hr. The ingestion script skips repos with less than 200 chars of content, avoiding empty or private repositories.

The workflow is validated via smoke tests (e.g., `midudev/autoskills` returns 103k chars with all new sections present). The ingested data is written to deterministic source pages in `wiki/sources/<owner>-<repo>.md`, with sections for Summary, Repository Info, README Excerpt, Activity Snapshot, and Crawled Files. Frontmatter includes `ingest_method: self-synthesis-no-llm` for provenance tracking.

## Key Properties

- **Expanded Crawl Budget:** Allows larger repositories and more files to be ingested, increasing coverage.
- **Manifest and README Prioritization:** Ensures key configuration and documentation files are captured first.
- **Repository Activity Snapshot:** Includes languages, releases, commits, issues, and PRs for a holistic view of repo status.
- **Authenticated API Calls:** Supports higher rate limits and access to private repos with valid tokens.
- **Deterministic Source Page Generation:** Writes structured, reproducible wiki pages for each repo, supporting provenance and audit.

## Limitations

Private repositories may be skipped if no content is accessible (e.g., jbl306/homelab). Rate limits can block ingestion without proper authentication. Multiple raw files for the same repo can collide, resulting in last-write-wins behavior; deduplication is recommended.

## Example

The workflow ingests the 'midudev/autoskills' GitHub repository, fetching its README, manifest files, language stats, recent releases, commits, open issues, and closed PRs. The resulting wiki page contains a summary, repository metadata, an excerpt from the README, a snapshot of activity, and a list of crawled files.

## Visual

No explicit diagrams, but the workflow results in wiki pages with structured sections: summary, repository info, README excerpt, activity snapshot (lists of releases, commits, issues, PRs), and crawled files. These sections are visible in the Content tab of the node viewer.

## Relationship to Other Concepts

- **[[GitHub Repository Deep Crawling for Wiki Ingestion]]** — Extends deep crawling to include more metadata and activity data.

## Practical Applications

Useful for technical documentation, project onboarding, and knowledge management in organizations relying on GitHub. Supports audit, provenance, and richer context for code review, compliance, and research.

## Sources

- [[Copilot Session Checkpoint: Mobile Node Viewer And Richer GitHub Ingestion]] — primary source for this concept
