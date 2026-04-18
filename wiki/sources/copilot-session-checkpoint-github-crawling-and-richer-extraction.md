---
title: "Copilot Session Checkpoint: GitHub Crawling and Richer Extraction"
type: source
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "e2f4e2c57a91e050124e6a177d9272a75a50ab4d9ee6cb6bb30f2ad73e5652bb"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-github-crawling-and-richer-extraction-a4ef6de5.md
quality_score: 100
concepts:
  - github-repository-deep-crawling-for-wiki-ingestion
  - image-filtering-for-vision-based-llm-extraction
  - richer-concept-extraction-prompt-for-llm-wiki-pages
related:
  - "[[GitHub Repository Deep Crawling for Wiki Ingestion]]"
  - "[[Image Filtering for Vision-Based LLM Extraction]]"
  - "[[Richer Concept Extraction Prompt for LLM Wiki Pages]]"
  - "[[Labs-Wiki]]"
  - "[[GitHub Trees API]]"
  - "[[GPT-4.1 Vision API]]"
tier: hot
tags: [labs-wiki, llm, docker, agents, auto-ingest, fileback, checkpoint, knowledge-wiki, copilot-session, graph, vision-api, homelab, github, durable-knowledge]
checkpoint_class: durable-architecture
retention_mode: retain
---

# Copilot Session Checkpoint: GitHub Crawling and Richer Extraction

## Summary

This session checkpoint documents enhancements to a personal LLM-powered knowledge wiki's auto-ingest pipeline, focusing on deep GitHub repository crawling, improved image filtering for vision processing, and richer concept extraction for wiki pages. The improvements were deployed in a Docker-based homelab environment, resulting in more comprehensive and higher-quality wiki content.

## Key Points

- Implemented deep GitHub repo crawling using Git Trees API with prioritized file fetching and budget-based limits.
- Fixed private repository access by prioritizing a personal access token with repo scope over the GitHub Models API token.
- Enhanced image filtering to exclude unsupported SVGs and site chrome images, improving ingestion success with vision API.
- Rewrote the extraction prompt to produce richer concept pages with multi-paragraph explanations, examples, limitations, and visual descriptions, increasing LLM processing time but improving output quality.

## Concepts Extracted

- **[[GitHub Repository Deep Crawling for Wiki Ingestion]]** — Deep crawling of GitHub repositories enables comprehensive ingestion of source files beyond shallow metadata and README files, allowing a personal knowledge wiki to capture detailed architecture and documentation content. This approach uses the Git Trees API to fetch the entire file tree in a single request, followed by selective file content retrieval based on relevance and budget constraints.
- **[[Image Filtering for Vision-Based LLM Extraction]]** — Image filtering improves the quality and success of vision-based LLM extraction by excluding unsupported or irrelevant image formats such as SVGs and site chrome images (logos, favicons, badges). This prevents ingestion failures and reduces noise in extracted content.
- **[[Richer Concept Extraction Prompt for LLM Wiki Pages]]** — Enhancing the LLM extraction prompt to demand richer, more detailed concept pages improves the quality and usefulness of generated wiki content. This includes multi-paragraph explanations, specific details, limitations, examples, and visual descriptions, trading off quantity of concepts for depth and clarity.

## Entities Mentioned

- **[[Labs-Wiki]]** — Labs-Wiki is a personal knowledge wiki powered by large language models (LLMs) designed to ingest, process, and organize technical and conceptual content. It supports automated ingestion pipelines, including deep GitHub repository crawling, vision-based image processing, and rich concept extraction to generate detailed wiki pages. Labs-Wiki runs in a Docker-based homelab infrastructure and serves as a living working copy of knowledge for the user.
- **[[GitHub Trees API]]** — The GitHub Trees API provides a way to retrieve the entire file tree of a repository in a single request. The endpoint `GET /repos/{owner}/{repo}/git/trees/HEAD?recursive=1` returns a JSON structure listing all files and directories recursively, enabling efficient enumeration of repository contents for tools and automation.
- **[[GPT-4.1 Vision API]]** — GPT-4.1 Vision API is a multimodal extension of the GPT-4 language model that supports image input processing. It accepts images in specific MIME types (PNG, JPEG, WEBP, GIF) and integrates vision capabilities with natural language understanding to enhance content extraction and reasoning.

## Notable Quotes

> "Richer prompt produces fewer concepts (10 vs 20 from same article) but each is substantially more useful." — Session Summary
> "Wiki provides 'what and why', code provides 'how exactly' — complementary." — User discussion on code repo inclusion

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-github-crawling-and-richer-extraction-a4ef6de5.md` |
| Type | note |
| Author | Unknown |
| Date | 2026-04-18 |
| URL | N/A |
