---
title: "Copilot Session Checkpoint: Clarifying Vision Options"
type: source
created: '2026-05-12'
last_verified: '2026-05-12'
source_hash: "47cdb90273c4de212de47aaf8fde339926e688cd13758b8166d01787137e4145"
sources:
  - raw/2026-05-12-copilot-session-clarifying-vision-options-3cbd5600.md
concepts:
  - free-first-vision-pipeline-modes-spatial-planning-apps
  - developer-assisted-vision-workflows-spatial-planning-apps
related:
  - "[[Spatial Design Studio]]"
  - "[[Copilot CLI]]"
  - "[[Claude Code]]"
  - "[[Vision Support in LLM Knowledge Ingestion Using GPT-4.1]]"
  - "[[Durable Copilot Session Checkpoint]]"
tags: [copilot-session, checkpoint, durable-knowledge, spatial-design-studio, vision, self-hosting, multimodal, homelab]
tier: hot
checkpoint_class: durable-debugging
retention_mode: retain
knowledge_state: ingested
ingest_method: copilot-cli-gpt-5.4
quality_score: 77
---

# Copilot Session Checkpoint: Clarifying Vision Options

## Summary

This checkpoint refines the reference-photo roadmap for [[Spatial Design Studio]] by separating three roles that are easy to conflate: free self-hosted computer-vision backends, developer-facing coding tools that can look at images, and paid production APIs. Its durable contribution is a deployment rule: default the app to local or disabled vision modes, treat tools like [[Copilot CLI]] and [[Claude Code]] as developer assistance rather than backend infrastructure, and gate cloud inference behind explicit configuration.

## Key Points

- **The checkpoint starts from a production constraint, not a model benchmark:** the app needs a realistic reference-photo-to-scene roadmap that works in a homelab and does not quietly depend on paid cloud inference.
- **The prior production increment is preserved as context:** mobile rendering fixes, editable product dimensions, PR merge, and homelab deployment were already complete before this research pass began.
- **The key architectural distinction is tool surface vs backend surface:** Copilot CLI, Codex CLI, and Claude Code can analyze images for development and workflow design, but they are not stable free APIs for user-uploaded production traffic.
- **The recommended default is explicitly local-first:** `SPATIAL_VISION_MODE` should prefer `disabled` or `local`, with `SPATIAL_VISION_ALLOW_CLOUD=false` and explicit provider keys required before any paid path is enabled.
- **The proposed self-hosted stack is modular rather than monolithic:** OpenCV, Pillow, and scikit-image handle cleanup; Depth Anything V2 or DPT/MiDaS provide depth cues; Grounding DINO plus SAM 2 handle open-set detection and masks; Mask2Former or MMSegmentation provide semantic segmentation.
- **Lightweight multimodal models are optional interpretation layers, not mandatory core infrastructure:** Qwen2.5-VL, LLaVA, and BLIP-2 can help with captions or material guesses, but the plan does not require them for the first extraction pass.
- **3D proxy generation is intentionally secondary:** TripoSG is mentioned as an optional mesh-proxy stage rather than a prerequisite for the first usable version of the pipeline.
- **Licensing is treated as a first-class engineering constraint:** GPL or non-commercial models should be excluded unless explicitly acceptable, and even promising open models need per-model license checks before production adoption.
- **The checkpoint keeps infrastructure scope narrow:** the work is a documentation and architecture correction, not a request to add new homelab services or deploy cloud dependencies.
- **The durable lesson generalizes beyond this app:** developer tools with image input are valuable for prototyping and evaluation, but production systems still need their own explicit runtime, privacy, cost, and failure boundaries.

## Key Concepts

- [[Free-First Vision Pipeline Modes for Spatial Planning Apps]]
- [[Developer-Assisted Vision Workflows for Spatial Planning Apps]]
- [[Vision Support in LLM Knowledge Ingestion Using GPT-4.1]]
- [[Source-Aware Model Routing in Wiki Ingestion Pipelines]]

## Related Entities

- **[[Spatial Design Studio]]** — The homelab room-planning application whose reference-photo pipeline is being redesigned around local-first constraints.
- **[[Copilot CLI]]** — A developer tool that can inspect images during implementation work, but should not be treated as the app's backend inference layer.
- **[[Claude Code]]** — Another developer-facing coding agent with image capabilities that belongs in the development loop rather than the production request path.
- **[[Durable Copilot Session Checkpoint]]** — The artifact type that preserved this design clarification as reusable knowledge.

