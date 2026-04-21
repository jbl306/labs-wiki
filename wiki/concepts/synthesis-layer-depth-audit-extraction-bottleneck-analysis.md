---
title: "Synthesis-Layer Depth Audit and Extraction Bottleneck Analysis"
type: concept
created: 2026-04-20
last_verified: 2026-04-20
source_hash: "c73306469d0b021d04941005a920130ac9f2aca5d4f041c255bcf45d387eb9f0"
sources:
  - raw/2026-04-20-copilot-session-graph-tracker-and-depth-review-4445c933.md
quality_score: 100
concepts:
  - synthesis-layer-depth-audit-extraction-bottleneck-analysis
related:
  - "[[Quality Evaluation of Auto-Ingested Wiki Content]]"
  - "[[Post-Ingest Quality Fixes in Auto-Ingest Pipelines]]"
  - "[[Copilot Session Checkpoint: Graph Tracker and Depth Review]]"
tier: hot
tags: [synthesis-layer, wiki-extraction, depth-audit, template-design]
---

# Synthesis-Layer Depth Audit and Extraction Bottleneck Analysis

## Overview

The synthesis-layer depth audit is a systematic review of wiki extraction processes, focusing on identifying bottlenecks that limit technical depth in concept/entity/source pages. It distinguishes between checkpoint-derived and URL/tutorial-derived sources, highlighting the impact of raw-capture and template design on downstream wiki quality.

## How It Works

The audit process begins by reviewing synthesis pages and their linked source/concept/entity pages, examining representative raw files, templates, and extraction prompt sections in the ingestion scripts. The reviewer assesses whether enough data is being captured from raw sources, whether page formats are too restrictive, and whether deeper technical detail is needed for high-value wiki artifacts.

A key finding is the distinction between checkpoint-derived and URL/tutorial-derived pages. Checkpoint exports include rich metadata such as overview, history, work_done, technical_details, and important_files, enabling deep concept and source pages. In contrast, many URL/tutorial raw files contain only a URL pointer and minimal frontmatter, with fetched article content used transiently during ingest but not persisted back into raw. This limits downstream extraction depth and makes re-ingest or audit weaker.

The audit also evaluates entity templates, noting that metadata-first designs are suitable for people and organizations but weak for technical tools and frameworks. Synthesis templates are generally adequate but can be over-standardized, especially for checkpoint-cluster syntheses. Some comparison tables render incorrectly, indicating template or rendering bugs.

Quality scoring is found to be structural, not semantic; shallow pages can score highly if frontmatter and links are complete, suggesting the need for a separate depth-sensitive metric. Representative examples illustrate these findings: deep checkpoint-derived pages versus thin URL-only raw files.

The audit concludes with recommendations for improvement, such as preserving fetched content back into raw for URL/article sources, piloting targeted raw/wiki refreshes on representative pages with tables, images, and graphs, and refining templates to support technical depth. The process is iterative, involving researcher subagents and plan updates to track findings and next steps.

## Key Properties

- **Source-Type Differentiation:** Checkpoint-derived sources are rich; URL/tutorial-derived sources are often shallow due to minimal raw capture.
- **Template Impact:** Entity and synthesis templates can restrict technical depth; metadata-first designs are weak for technical tools.
- **Quality Scoring Limitations:** Structural quality scores do not reflect semantic or technical depth; shallow pages can score highly.
- **Audit Process:** Systematic review of representative pages, templates, and extraction prompts to identify bottlenecks.

## Limitations

The audit is descriptive and does not directly remediate extraction bottlenecks. Improvements depend on subsequent implementation of recommendations, such as raw content preservation and template refinement. Rendering bugs and template mismatches require separate technical fixes.

## Example

Example audit finding:
- `raw/2026-04-08-lightgbm-light-gradient-boosting-machine-geeksforgeeks.md` contains only a URL pointer, resulting in a shallow wiki/concept page.
- In contrast, `raw/2026-04-18-copilot-session-sprint-58-shap-bug-planning-...md` includes detailed technical history and work_done, enabling deep extraction.

## Visual

Audit findings are summarized in tables and lists within session plan and MemPalace drawer artifacts. No explicit charts or diagrams are referenced.

## Relationship to Other Concepts

- **[[Quality Evaluation of Auto-Ingested Wiki Content]]** — Both focus on assessing wiki extraction quality and identifying improvement opportunities.
- **[[Post-Ingest Quality Fixes in Auto-Ingest Pipelines]]** — Audit findings inform post-ingest quality remediation strategies.

## Practical Applications

Guides maintainers in identifying and fixing extraction bottlenecks, improving technical depth in wiki pages, and refining templates for better downstream synthesis. Supports pilot-scoping for targeted raw/wiki refreshes and informs durable knowledge architecture.

## Sources

- [[Copilot Session Checkpoint: Graph Tracker and Depth Review]] — primary source for this concept
