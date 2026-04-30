---
title: "Copilot Session Checkpoint: GitHub ingest depth — fetcher trim"
type: source
created: '2026-04-30'
last_verified: '2026-04-30'
source_hash: fa0dca993194d7046314a36aee4e5f40c761b7b66efdadb63f2d1d034f7eefdb
sources:
  - raw/2026-04-22-copilot-session-github-ingest-depth-fetcher-trim-732c3907.md
concepts:
  - signal-preserving-github-repository-ingestion
related:
  - "[[Signal-Preserving GitHub Repository Ingestion]]"
  - "[[GitHub Repository Deep Crawling for Wiki Ingestion]]"
  - "[[Richer GitHub Repository Ingestion Workflow]]"
  - "[[Richer Concept Extraction Prompt for LLM Wiki Pages]]"
  - "[[Post-Ingest Quality Fixes in Auto-Ingest Pipelines]]"
  - "[[scripts/auto_ingest.py]]"
  - "[[Labs-Wiki]]"
  - "[[Homelab]]"
tags: [copilot-session, labs-wiki, github-ingestion, auto-ingest, prompt-engineering, technical-briefs]
tier: hot
knowledge_state: ingested
ingest_method: copilot-cli-gpt-5.4
quality_score: 76
checkpoint_class: durable-architecture
checkpoint_class_rule: "body:architecture"
retention_mode: retain
---

# Copilot Session Checkpoint: GitHub ingest depth — fetcher trim

## Summary

This checkpoint captures a design correction for Labs-Wiki's GitHub repository ingest path: simply fetching *more* repository data did not guarantee deeper wiki pages. The session isolates two bottlenecks—activity metadata crowding out architectural substance and a prompt that gave no GitHub-specific structure—then records the fetcher trim and prompt hardening needed to turn repo source pages into technical briefs instead of activity dashboards.

## Key Points

- **Root cause 1: attention pollution from activity dumps** — `scripts/auto_ingest.py` appended `Recent Commits`, `Open Issues`, and `Recently Merged PRs` after the README, which encouraged medium-effort models to mirror those easy, structured lists rather than synthesize architecture from the README and crawled files.
- **Root cause 2: missing GitHub-mode prompt contract** — `scripts/prompts/wiki_ingest_prompt.md` had no repository-specific instructions requiring sections like `Architecture / Technical model`, `How it works`, or `API / interface surface`, so technically rich repos often produced shallow pages.
- **Fetcher trim already implemented** — the GitHub fetcher removed three noisy sections while preserving higher-signal inputs: repository metadata, README content, language breakdown, recent releases, and an 80K-budget tree crawl.
- **Technical signal was already available** — `_crawl_github_tree`, `_should_crawl`, and `_priority_sort_key` prioritized manifests, per-directory READMEs, and `docs/` / `examples/` content, so the limiting factor was curation strategy rather than lack of source material.
- **New target page shape was explicit** — future GitHub repo ingests should generate inline sections for architecture, workflow, API surface, integration notes, caveats, repo metadata, and related concepts, mirroring the stronger repo pages already hand-reprocessed in the wiki.
- **Concept creation needed to be part of repo ingest** — named abstractions such as MemPalace wings/rooms/drawers or MCP tool categories should trigger concept-page creation when they are central to the repository's design.
- **Validation bar shifted from premium rescue to default robustness** — the checkpoint argues that success should be measured with normal `medium`-effort GitHub ingests, not only with one-off premium-model reprocessing.
- **Container constraints remained important context** — the `wiki-auto-ingest` container still lacked `.git` and MemPalace MCP access, so durable commits and KG replay continued to rely on host-side follow-up processes.
- **Manual reprocessing provided the proof point** — eleven GitHub repo sources had already been rewritten to remove commit/PR noise and deepen technical coverage, with `milla-jovovich-mempalace.md` called out as the quality bar.
- **Open decision remained on effort routing** — if `gh copilot -p` at `medium` still underperformed after the prompt hardening, GitHub repos might need the same effort escalation that PDFs already received.

## Key Concepts

- [[Signal-Preserving GitHub Repository Ingestion]]
- [[GitHub Repository Deep Crawling for Wiki Ingestion]]
- [[Richer GitHub Repository Ingestion Workflow]]
- [[Richer Concept Extraction Prompt for LLM Wiki Pages]]
- [[Post-Ingest Quality Fixes in Auto-Ingest Pipelines]]

## Related Entities

- **[[scripts/auto_ingest.py]]** — the ingest entrypoint whose GitHub fetcher was trimmed to remove commit, issue, and PR noise.
- **[[Labs-Wiki]]** — the target knowledge system whose repository source pages needed to become deeper and more durable.
- **[[Homelab]]** — the deployment environment that hosts the `wiki-auto-ingest` container and the redeploy flow for validating the fix.
- **[[Copilot CLI]]** — the compile backend whose medium-effort behavior exposed the difference between high-signal and noisy GitHub source dumps.
- **[[MemPalace]]** — the downstream knowledge graph system whose repository page was used as the exemplar for the desired technical depth.
