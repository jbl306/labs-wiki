---
title: "Copilot Session Checkpoint: No-LLM Reference Workflow"
type: source
created: '2026-05-12'
last_verified: '2026-05-12'
source_hash: "9c218bc4dd06334dac0cc3734354e440f10b258ad6ca81f29799e18d7980f91a"
sources:
  - raw/2026-05-12-copilot-session-no-llm-reference-workflow-0264677a.md
concepts:
  - deterministic-reference-artifact-pipeline
  - review-first-candidate-acceptance-reference-jobs
related:
  - "[[Spatial Design Studio]]"
  - "[[Spatial Design Studio Reference Worker]]"
  - "[[Homelab]]"
  - "[[Copilot CLI]]"
  - "[[MemPalace]]"
  - "[[Free-First Vision Pipeline Modes for Spatial Planning Apps]]"
  - "[[Developer-Assisted Vision Workflows for Spatial Planning Apps]]"
  - "[[Vision Policy vs Extraction vs Acceptance in Spatial Reference Workflows]]"
tags: [copilot-session, checkpoint, durable-knowledge, spatial-design-studio, homelab, no-llm, computer-vision, ocr]
tier: hot
checkpoint_class: durable-workflow
retention_mode: retain
knowledge_state: ingested
ingest_method: copilot-cli-gpt-5.4
quality_score: 79
---

# Copilot Session Checkpoint: No-LLM Reference Workflow

## Summary

This checkpoint captures the full implementation of a deterministic, no-LLM reference-photo workflow for [[Spatial Design Studio]], turning an earlier local-first vision policy into an actual production path. The durable value is not just that the feature shipped, but that the checkpoint records the full contract: local `reference-analysis` jobs, review-first calibration and candidate acceptance, editable scene/object transforms, product-candidate import, and a dedicated internal worker deployed on [[Homelab]].

It also preserves the most important operational lesson from deployment: the worker is intentionally private and cloud-disabled, but it still needed an explicit `PYTHONPATH=/app/apps/api` hotfix to import `spatial_api` correctly after rollout.

## Key Points

- **The written plan was implemented end to end:** stages 0 through 7 of the no-LLM reference asset production plan were completed, merged through sequential PRs, deployed, and partially validated on homelab.
- **The pipeline is explicitly deterministic and local:** uploads with `reference_mode=deterministic` or `extract_links` queue `reference-analysis` jobs with `provider='local'`, `model='deterministic-reference-0'`, and both cloud/LLM flags hard-false.
- **The extraction stack is concrete, not aspirational:** `OpenCV`, `Pillow`, `pytesseract`, QR/URL extraction, calibration helpers, and proposal generation now live under `apps/api/spatial_api/reference/`.
- **Artifact output is reviewable:** each job writes into `${SPATIAL_DATA_DIR}/reference-jobs/{job_id}` and can return normalized previews, edge overlays, OCR text paths, `ocrSnippets`, `productLinkCandidates`, and calibration requirements.
- **The workflow is intentionally review-first:** extracted rectangles are not treated as truth; users calibrate scale, accept candidates, and then convert them into editable `scene.objects` through `pixels_per_unit()` and `convert_rectangle_to_scene_object()`.
- **Reference-derived objects remain editable after acceptance:** the API and UI added scene object update/duplicate/delete endpoints, `SceneObjectUpdate`, per-instance product dimension edits, a 2D drag surface, and primitive 3D rendering.
- **Product ingestion became part of the same path:** accepted OCR/QR URL candidates and manual candidate entry both create products through reusable API helpers instead of forcing a separate catalog workflow.
- **The deployed worker has a narrow runtime contract:** `spatial-design-studio-reference-worker` runs `python -m spatial_api.worker --interval 2 --limit 1`, has 2 CPU / 2 GB limits, shares the Spatial data volume, has no Caddy labels, and stays internal-only.
- **A real deployment gotcha was captured:** after the first rollout, the worker crash-looped with `ModuleNotFoundError: No module named 'spatial_api'` until a hotfix added `PYTHONPATH=/app/apps/api` in `compose/compose.web.yml`.
- **The checkpoint connects implementation to prior architecture work:** it operationalizes [[Free-First Vision Pipeline Modes for Spatial Planning Apps]] by replacing abstract local-first guidance with a shipped extraction-and-acceptance workflow.

## Key Concepts

- [[Deterministic Reference Artifact Pipeline]]
- [[Review-First Candidate Acceptance for Reference Jobs]]
- [[Free-First Vision Pipeline Modes for Spatial Planning Apps]]

## Related Entities

- **[[Spatial Design Studio]]** — The application that now owns the deterministic reference upload, review, and object/product creation flow.
- **[[Spatial Design Studio Reference Worker]]** — The internal worker service that executes queued reference-analysis jobs on homelab.
- **[[Homelab]]** — The deployment environment where the API, web app, and worker were rolled out and validated.
- **[[Copilot CLI]]** — The tool surface used to implement the staged plan, manage PRs, and record this durable checkpoint.
- **[[MemPalace]]** — Part of the checkpoint-promotion path that preserved this implementation as reusable knowledge.
