---
title: "Copilot Session Checkpoint: Mobile Node Viewer And Richer GitHub Ingestion"
type: source
created: 2026-04-22
last_verified: 2026-04-22
source_hash: "0a4ff72c02c43a07f603a8baab32716ef2cb63b6d31b3dd941b64676f49cd7bd"
sources:
  - raw/2026-04-22-copilot-session-mobile-node-viewer-and-richer-github-ingestion-8b1dee20.md
quality_score: 85
concepts:
  - mobile-first-node-viewer-wiki-graph-ui
  - richer-github-repository-ingestion-workflow
  - self-synthesizing-github-source-re-ingestion-workflow
related:
  - "[[Mobile-First Node Viewer For Wiki Graph UI]]"
  - "[[Richer GitHub Repository Ingestion Workflow]]"
  - "[[Self-Synthesizing GitHub Source Re-Ingestion Workflow]]"
  - "[[auto_ingest.py]]"
  - "[[refresh_github_sources.py]]"
tier: hot
checkpoint_class: durable-architecture
retention_mode: retain
tags: [agents, github-ingestion, copilot-session, durable-knowledge, mobile-ui, mempalace, labs-wiki, provenance, homelab, wiki-graph, graph, documentation, fileback, checkpoint]
---

# Copilot Session Checkpoint: Mobile Node Viewer And Richer GitHub Ingestion

## Summary

This checkpoint documents the completion and deployment of three major improvements to the labs-wiki system: a mobile-friendly node viewer in the graph UI, enhanced GitHub repository ingestion, and a self-synthesizing re-ingest workflow for existing GitHub-sourced wiki pages without LLM or GitHub Models API calls. All workstreams were merged as PR #18 and validated in production.

## Key Points

- Mobile node viewer enables wiki page content display in a bottom-sheet, tabbed UI optimized for phones.
- GitHub repo ingestion now includes manifests, languages, releases, commits, issues, and PRs, with expanded crawl budgets.
- A new script re-ingests GitHub sources using skills, bypassing the GitHub Models API and supporting deterministic, self-synthesizing source pages.

## Concepts Extracted

- **[[Mobile-First Node Viewer For Wiki Graph UI]]** — The mobile-first node viewer is a UI enhancement for the labs-wiki graph interface, allowing users to click on any node and view its wiki page content in a responsive, tabbed bottom-sheet layout. This design addresses usability and accessibility on mobile devices, providing a richer, more interactive experience for navigating wiki content.
- **[[Richer GitHub Repository Ingestion Workflow]]** — The richer GitHub ingestion workflow expands the scope and depth of repository data captured for wiki pages. It includes additional metadata, files, and activity snapshots, improving the completeness and utility of ingested source pages for technical documentation and knowledge management.
- **[[Self-Synthesizing GitHub Source Re-Ingestion Workflow]]** — This workflow enables deterministic, skill-driven re-ingestion of GitHub-sourced wiki pages without relying on LLMs or the GitHub Models API. It refreshes content blocks, ensures provenance, and supports reproducible documentation for knowledge graphs.

## Entities Mentioned

- **wiki-graph-api** — The wiki-graph-api is the backend API for the labs-wiki knowledge graph system, responsible for serving node content, neighbors, and supporting mobile-friendly UI enhancements. It provides endpoints for retrieving wiki page content and metadata, enabling interactive graph navigation.
- **wiki-graph-ui** — The wiki-graph-ui is the frontend interface for the labs-wiki knowledge graph, featuring a mobile-friendly, tabbed node viewer for displaying wiki page content. It handles markdown rendering, tab logic, and interactive navigation via clickable wikilinks.
- **[[auto_ingest.py]]** — auto_ingest.py is the script responsible for crawling and ingesting GitHub repositories for the labs-wiki system. It prioritizes key files, expands crawl budgets, and fetches additional metadata and activity snapshots to enrich wiki source pages.
- **[[refresh_github_sources.py]]** — refresh_github_sources.py is a new script for deterministic, skill-driven re-ingestion of GitHub-sourced wiki pages. It refreshes content blocks, ensures provenance, and writes structured source pages without LLM or GitHub Models API calls.

## Notable Quotes

> "Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion." — Session summary
> "All three workstreams completed, deployed, and merged to main as PR #18 (squash 58059ff)." — Session summary

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-22-copilot-session-mobile-node-viewer-and-richer-github-ingestion-8b1dee20.md` |
| Type | note |
| Author | Unknown |
| Date | 2026-04-22 |
| URL | N/A |
