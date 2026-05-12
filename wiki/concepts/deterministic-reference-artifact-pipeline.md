---
title: "Deterministic Reference Artifact Pipeline"
type: concept
created: 2026-05-12
last_verified: 2026-05-12
source_hash: "9c218bc4dd06334dac0cc3734354e440f10b258ad6ca81f29799e18d7980f91a"
sources:
  - raw/2026-05-12-copilot-session-no-llm-reference-workflow-0264677a.md
related:
  - "[[Free-First Vision Pipeline Modes for Spatial Planning Apps]]"
  - "[[Developer-Assisted Vision Workflows for Spatial Planning Apps]]"
  - "[[Review-First Candidate Acceptance for Reference Jobs]]"
tier: hot
tags: [spatial-design-studio, computer-vision, ocr, qr, workflow, no-llm, homelab]
---

# Deterministic Reference Artifact Pipeline

## Overview

The deterministic reference artifact pipeline is the concrete implementation pattern that turns a user-uploaded room or product reference image into reviewable intermediate artifacts without relying on an LLM, paid vision API, or reverse-image search. In this checkpoint, it matters because [[Spatial Design Studio]] stops talking about a local-first vision strategy in the abstract and instead ships a real extraction path with queued jobs, persisted artifacts, OCR/QR enrichment, and acceptance-ready candidates.

At a high level, the concept says that reference-photo processing should produce **structured evidence before editable state**. Instead of immediately inventing furniture objects or trusting a single model output, the system generates deterministic artifacts that a human can inspect: normalized imagery, edges, OCR snippets, link candidates, geometry proposals, and calibration prompts.

## How It Works

The pipeline begins at the API surface, not inside an ad hoc script. A client uploads an asset to `/spaces/{space_id}/assets` and explicitly selects `reference_mode=deterministic` or `reference_mode=extract_links`. That request does not ask a model to "understand the room" in one leap. Instead, it creates an `ai_jobs` row whose semantics are tightly constrained: `type='reference-analysis'`, `provider='local'`, and `model='deterministic-reference-0'`. The naming is important. The existing jobs table is reused for workflow continuity, but the provider/model fields make it clear that this path is not a frontier-model job wearing a different label.

From there, `spatial_api.ai_runner` routes the job into the local reference-processing package rather than the detached AI path. The checkpoint names the package layout explicitly: `quality.py`, `geometry.py`, `proposals.py`, `ocr.py`, `links.py`, and `calibration.py`. That structure reflects a systems decision. The pipeline is decomposed into small deterministic stages so each one can be reasoned about, tested, and swapped independently. A cleanup or normalization stage can improve the image without touching OCR logic. Geometry and edge extraction can evolve without changing the candidate-acceptance contract. URL/QR extraction can be validated separately from object-shape heuristics.

Artifact persistence is a first-class part of the mechanism. Each job writes under `${SPATIAL_DATA_DIR}/reference-jobs/{job_id}` rather than returning only a blob of final JSON. That directory becomes the job's evidence locker. The checkpoint lists the kinds of output that can appear there: normalized previews, edge overlays, optional OCR text dumps, raw candidate geometry, `ocrSnippets`, `productLinkCandidates`, and calibration requirements. Persisting those files is what makes the workflow reviewable. It lets the UI show what the pipeline actually saw and extracted instead of forcing users or future developers to trust an opaque transformation.

OCR and QR extraction are deliberately treated as extensions of the same deterministic pass rather than as a separate magical lookup step. Stage 3 added `pytesseract` and the Docker packages needed to make it work in the container, including `tesseract-ocr`, `libgl1`, and `libglib2.0-0`. The OCR layer is then combined with URL and QR parsing so the system can emit candidate product links from the reference image itself. This is a subtle but important design choice: the pipeline does not need to "know" what object a couch is in a general semantic sense to be useful. If a screenshot or photo contains packaging, labels, or QR codes, deterministic extraction can still surface purchase or catalog clues that anchor later product creation.

The pipeline also encodes a sharp boundary around non-deterministic behavior. The source states multiple negative constraints: no local LLM/VLM, no Copilot/Codex/Claude runtime dependency, no paid cloud vision, and no reverse image search. Those are not footnotes. They are part of the algorithmic contract. In practical terms, that means every pipeline stage has to be explainable in terms of local image transforms, local OCR, local parsing, or explicit heuristics. The reward is operational clarity: if the job output changes, it changed because code or local libraries changed, not because a hosted model silently drifted.

Another mechanism is that the pipeline does not directly produce truthy room objects as its final act. It emits candidates and calibration requirements. In other words, the extracted artifacts are meant to support a later decision layer, not bypass it. The checkpoint makes that clear when it distinguishes artifact generation from the later endpoints that convert accepted candidates into `scene.objects` or imported products. This separation dramatically lowers the blast radius of imperfect extraction. A rectangle proposal can be wrong without corrupting the room plan because it stays a proposal until someone accepts it.

The test strategy in the checkpoint reinforces the concept. OCR is valuable, but it is also operationally brittle because Tesseract may be unavailable or inconsistent in local development. The tests therefore monkeypatch `pytesseract.image_to_string` in cases where OCR output is irrelevant or needs to be deterministic for extraction assertions. That is a design lesson in itself: deterministic pipelines are not achieved simply by banning LLMs; they also require controlled test boundaries around local native dependencies.

Put together, the pipeline forms a compile-before-commit workflow for room references. First normalize the image. Then derive machine-visible evidence. Then persist and expose that evidence. Only after that does the app allow user acceptance and scene mutation. The point is not to eliminate ambiguity from perception; it is to keep ambiguity visible long enough that humans can steer the final result.

## Key Properties

- **Queued local execution:** uploads create `reference-analysis` jobs instead of blocking the request path or calling remote inference.
- **Evidence-first output:** the pipeline writes artifacts and candidates before it creates room objects or products.
- **Composable deterministic stages:** quality cleanup, geometry extraction, OCR, QR/URL parsing, and calibration metadata stay separated.
- **Explicit no-cloud contract:** cloud and LLM flags remain hard-false, preserving privacy and cost predictability.
- **Testable native dependencies:** OCR and related stages are isolated enough to be monkeypatched when local Tesseract availability varies.

## Limitations

A deterministic pipeline is easier to audit than an LLM workflow, but it is not magically correct. OCR quality still depends on image resolution, contrast, viewpoint, and whether Tesseract is available in the environment. Edge- and rectangle-based proposals can fail on cluttered rooms, soft silhouettes, reflective materials, or objects with weak contrast against the background. Local heuristics also struggle when the reference image contains ambiguous scale cues or when the useful signal is semantic rather than geometric. Finally, persisted artifacts improve reviewability, but they also increase storage churn and make cleanup policies more important if many reference jobs accumulate over time.

## Examples

```python
def run_reference_job(asset, mode):
    job = queue_job(
        job_type="reference-analysis",
        provider="local",
        model="deterministic-reference-0",
        reference_mode=mode,
    )
    artifact_dir = f"{SPATIAL_DATA_DIR}/reference-jobs/{job.id}"
    normalized = normalize_image(asset.path)
    edges = extract_edges(normalized)
    text = run_ocr_if_available(normalized)
    links = extract_links_and_qr(text, normalized)
    candidates = propose_rectangles(edges)
    save_artifacts(artifact_dir, normalized, edges, text, links, candidates)
    return job
```

In the checkpoint's implemented form, the pipeline emits enough structure for the UI to show extracted text snippets, candidate product links, and geometric proposals before the user promotes any of them into the editable room model.

## Practical Applications

This concept is useful for self-hosted room planners, renovation tools, furniture-layout systems, and similar products that need to learn from user reference images while keeping privacy and runtime behavior tightly bounded. It is especially appropriate when the highest-value output is not "automatic scene understanding" in the abstract, but a reviewable bundle of candidate objects, link hints, and calibration prompts that a human can validate quickly.

## Related Concepts

- **[[Free-First Vision Pipeline Modes for Spatial Planning Apps]]** — defines the policy-level local-first boundary that this pipeline operationalizes.
- **[[Developer-Assisted Vision Workflows for Spatial Planning Apps]]** — describes the adjacent human tool lane that remains useful for debugging, but not for serving live user uploads.
- **[[Review-First Candidate Acceptance for Reference Jobs]]** — covers the downstream stage where persisted artifacts become accepted scene objects or products.

## Sources

- [[Copilot Session Checkpoint: No-LLM Reference Workflow]] — records the queued job contract, package layout, artifact outputs, OCR/QR additions, and deployment constraints.
