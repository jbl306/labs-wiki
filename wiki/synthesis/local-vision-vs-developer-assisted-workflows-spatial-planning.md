---
title: "Local Vision vs Developer-Assisted Workflows for Spatial Planning Apps"
type: synthesis
created: 2026-05-12
last_verified: 2026-05-12
source_hash: "synthesis-generated"
sources:
  - raw/2026-05-12-copilot-session-clarifying-vision-options-3cbd5600.md
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-pipeline-enhancements-and-vision-support-deploye-5028ddea.md
concepts:
  - free-first-vision-pipeline-modes-spatial-planning-apps
  - developer-assisted-vision-workflows-spatial-planning-apps
  - vision-support-in-llm-knowledge-ingestion-using-gpt-4-1
related:
  - "[[Free-First Vision Pipeline Modes for Spatial Planning Apps]]"
  - "[[Developer-Assisted Vision Workflows for Spatial Planning Apps]]"
  - "[[Vision Support in LLM Knowledge Ingestion Using GPT-4.1]]"
  - "[[Spatial Design Studio]]"
tier: hot
tags: [vision, synthesis, spatial-design-studio, self-hosting, multimodal, cost-model]
---

# Local Vision vs Developer-Assisted Workflows for Spatial Planning Apps

## Question

When a self-hosted spatial-planning product needs to reason over reference photos, which work should run in the production backend, which work belongs in developer tooling, and when is a paid multimodal API actually justified?

## Summary

The checkpoint's answer is asymmetric: production should default to local extraction, developer tools should help engineers evaluate and refine that pipeline, and paid APIs should remain a clearly gated fallback rather than the hidden default. The older wiki-ingestion vision pipeline shows that multimodal models can be operationalized when the boundary is explicit, but for user-facing spatial planning the privacy and cost bar is higher.

## Comparison

| Dimension | [[Free-First Vision Pipeline Modes for Spatial Planning Apps]] | [[Developer-Assisted Vision Workflows for Spatial Planning Apps]] | [[Vision Support in LLM Knowledge Ingestion Using GPT-4.1]] |
|-----------|---------------------------------------------------------------|-------------------------------------------------------------------|-------------------------------------------------------------|
| Primary role | Production-facing extraction path for end-user reference photos | Human-in-the-loop analysis, debugging, and model comparison | Compile-time enrichment for wiki sources that contain images |
| Default trust boundary | Self-hosted app infrastructure | Individual developer tool session | Explicit external model call inside ingest pipeline |
| Cost model | Hardware-bound, mostly fixed-cost once deployed | Subscription or tooling-budget assisted | Metered model requests at compile time |
| Typical components | OpenCV, Pillow, Depth Anything V2, Grounding DINO, SAM 2, segmentation models | Copilot CLI, Codex CLI, Claude Code used interactively | GPT-4.1 with base64-encoded images in the ingest prompt |
| Failure impact | Directly affects user-visible scene extraction | Affects engineering judgment and iteration speed | Affects wiki page richness, not live product behavior |
| Best use | Stable, privacy-conscious product runtime | Prompt design, edge-case diagnosis, output critique | One-time knowledge compilation from image-bearing raws |

## Analysis

The most important distinction across these pages is that "vision support" is not one thing. The existing [[Vision Support in LLM Knowledge Ingestion Using GPT-4.1]] page describes a compile pipeline where calling an external multimodal model is the point: the system ingests a source once, interprets charts or screenshots, and writes a durable wiki page. That boundary is narrow, observable, and low frequency. A user-facing spatial-planning app has a very different operating environment. It accepts live uploads, may process private room photos, and needs predictable repeated behavior rather than one-off research enrichment.

That difference explains why the new checkpoint shifts the center of gravity toward local extraction. Ingest-time vision can tolerate model-metered calls because the volume is limited and the output is cached as wiki knowledge. Spatial planning cannot assume the same economics or privacy posture. If every room photo silently crosses a cloud boundary, the product has already made a deployment decision whether or not the team documented it. The free-first concept responds by turning that hidden decision into an explicit mode system.

Developer-assisted workflows sit between those two worlds. They borrow multimodal strength from tools like [[Copilot CLI]] and [[Claude Code]] without importing those tools into the runtime contract. This is valuable because it lets engineers benefit from strong image interpretation while building or validating the local stack. But it is a category error to confuse that convenience with a backend. A tool that helps a developer reason about an image is not automatically a service that should process end-user uploads continuously.

The real decision rule, then, is not "Which vision system is best?" but "Which boundary is acceptable for this class of work?" If the work is durable knowledge compilation, a model-backed ingest path may be exactly right. If the work is shipping a self-hosted room planner, local CV plus optional explicitly gated APIs is safer. If the work is engineering evaluation, developer-assisted tooling is ideal. The checkpoint's architecture is strong because it keeps those three roles distinct instead of trying to force one tool surface to do all of them.

## Key Insights

1. **Mode selection is an architecture decision, not a convenience toggle** — the new spatial-planning design encodes privacy and cost boundaries up front in [[Free-First Vision Pipeline Modes for Spatial Planning Apps]].
2. **Developer-tool multimodality is most valuable as critique, not as serving infrastructure** — [[Developer-Assisted Vision Workflows for Spatial Planning Apps]] turns image-capable coding agents into an engineering accelerator without making them the product backend.
3. **The older wiki-ingest vision pipeline remains a valid counterexample, not a contradiction** — [[Vision Support in LLM Knowledge Ingestion Using GPT-4.1]] succeeds because compile-time wiki enrichment has a narrower operational contract than live user-facing spatial inference.

## Open Questions

- What minimum local-hardware profile is acceptable before `local` mode becomes too slow for practical reference-photo workflows?
- Which scene artifacts should be reviewable by users before the app promotes them into editable room objects?
- If a paid API is later approved, which tasks should it own: captions, material inference, depth refinement, or difficult long-tail scenes only?

## Sources

- [[Copilot Session Checkpoint: Clarifying Vision Options]]
- [[Copilot Session Checkpoint: Pipeline Enhancements and Vision Support Deployed]]

