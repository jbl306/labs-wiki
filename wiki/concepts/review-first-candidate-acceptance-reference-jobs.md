---
title: "Review-First Candidate Acceptance for Reference Jobs"
type: concept
created: 2026-05-12
last_verified: 2026-05-12
source_hash: "9c218bc4dd06334dac0cc3734354e440f10b258ad6ca81f29799e18d7980f91a"
sources:
  - raw/2026-05-12-copilot-session-no-llm-reference-workflow-0264677a.md
related:
  - "[[Deterministic Reference Artifact Pipeline]]"
  - "[[Free-First Vision Pipeline Modes for Spatial Planning Apps]]"
  - "[[Single-User Local SQLite Migration for Self-Hosted Web Apps]]"
tier: hot
tags: [spatial-design-studio, review-workflow, calibration, scene-objects, product-ingestion, no-llm]
---

# Review-First Candidate Acceptance for Reference Jobs

## Overview

Review-first candidate acceptance is the workflow pattern where extracted geometry, OCR hits, and link candidates remain provisional until a user calibrates, selects, and explicitly promotes them into durable application state. In this checkpoint, the concept matters because [[Spatial Design Studio]] does not stop at deterministic extraction; it also defines how uncertain image-derived suggestions become trustworthy enough to create `scene.objects` and product records.

The key idea is that acceptance, not extraction, is the moment where the app commits to a room model. That makes calibration controls, object-editing affordances, and acceptance endpoints part of the core algorithm rather than mere UI polish.

## How It Works

The workflow starts after the deterministic reference pipeline has already produced candidates and artifact files. At that point, the system has evidence but not yet durable room state. A geometric candidate may describe a plausible rectangle in image space, and OCR or QR extraction may surface a plausible retailer URL, but neither is trusted by default. The checkpoint's design insists on an explicit review boundary because the app's real output is not "an image analysis result"; it is a set of editable scene objects and products that will affect future layout operations in both 2D and 3D.

Calibration is the first major mechanism in that boundary. Stage 4 introduced `reference/calibration.py` with `pixels_per_unit()` and `convert_rectangle_to_scene_object()`. The math is straightforward but important:

$$
\text{pixels\_per\_unit} = \frac{\text{measured pixels}}{\text{real-world units}}
$$

and therefore

$$
\text{real size} = \frac{\text{pixel size}}{\text{pixels\_per\_unit}}
$$

This formula turns image-space rectangles into approximate physical dimensions only after the user or workflow supplies a known measurement. The checkpoint's broader insight is that scale cannot be guessed honestly from many reference images, so the system should expose calibration as a first-class act rather than burying it behind heuristics. A room-planning product is more trustworthy when it says "tell me the scale reference" than when it silently fabricates one.

Once a candidate has enough scale information, the acceptance endpoint becomes the commit step. The source names `POST /reference/jobs/{job_id}/candidates/{candidate_id}/accept` as the path that promotes a reviewed candidate into the scene model. This stage also added `scene.objects` and helper functions like `add_scene_object()`, which means the room planner gained a new state surface distinct from imported product instances. The accepted object is no longer just an overlay from image processing; it becomes something the planner can move, render, duplicate, hide, or delete.

That distinction between **accepted scene object** and **catalog product** is another important part of the concept. The checkpoint implements both, but keeps them separate. A rectangle accepted from a room photo may simply be a useful blocker, cabinet, or furniture proxy inside the plan. By contrast, accepted URL candidates use `POST /reference/jobs/{job_id}/product-candidates/{candidate_id}/accept`, and manually entered candidates use `POST /reference/product-candidates/manual`. Those flows create or import reusable product records through shared helpers instead of pretending every visual candidate is already a canonical product. This preserves modeling honesty. Some extracted items are just geometric placeholders; others can graduate into product-library entries.

The acceptance workflow is only credible because editability follows immediately after promotion. Stage 5 extended `ProductInstanceUpdate` with per-instance width, depth, height, and unit overrides so users can tune a placed object without mutating the product library's global definition. It also added `SceneObjectUpdate` plus scene-object update/duplicate/delete endpoints. In the frontend, `Plan2D.tsx` renders, selects, and drags reference objects; `Scene3D.tsx` renders them as primitives; and `ObjectTransformPanel.tsx` exposes x/y/z position, dimensions, rotation, visibility, and lock state. This is not an incidental convenience. It is what transforms acceptance from a fragile one-shot import into an iterative modeling step.

Review-first acceptance also provides a safer answer to imperfect OCR and link extraction. OCR can hallucinate or misread characters, and QR or URL heuristics can surface noisy candidates. By forcing user review before product creation, the system reduces the risk that a bad parse silently pollutes the product catalog. The human review step becomes a semantic firewall: extraction can be broad and opportunistic, while acceptance remains selective and intentional.

Another subtle mechanism is that the acceptance workflow keeps the product and scene paths convergent where that is useful. The checkpoint notes a reusable `_create_imported_product()` helper in the API. That matters because it prevents the reference-derived product flow from becoming a second-class, inconsistent import path. Once a user accepts a candidate, it should enter the same durable product machinery used by the rest of the app, not a parallel subsystem with weaker guarantees.

The overall result is a room-planning workflow that treats computer-vision output as a starting point for user-guided model construction. First extract evidence. Then calibrate and review. Then promote selected candidates into scene objects or products. Then let normal editing tools take over. The concept works because it preserves uncertainty until the last responsible moment and then hands the result to standard application surfaces instead of a special "AI object" limbo.

## Key Properties

- **Calibration before commitment:** image measurements become room dimensions only after explicit scale input.
- **Separate acceptance paths:** scene-object promotion and product creation use different endpoints because they represent different kinds of truth.
- **Post-acceptance editability:** accepted objects immediately join the normal 2D/3D editing workflow.
- **Human semantic firewall:** OCR and link suggestions are filtered through explicit user review before they affect durable state.
- **Reuse of core app helpers:** accepted product candidates flow through shared creation logic instead of a sidecar import path.

## Limitations

Review-first workflows trade automation speed for trust. Users must spend time calibrating and accepting candidates, which can feel slower than a push-button "auto furnish" flow. Calibration is only as good as the reference measurement supplied, so bad user input can still create distorted room objects. Some candidates will also fall into an awkward middle ground: useful enough to keep as a rough blocker, but too ambiguous to map confidently to a product or canonical object type. Finally, richer editability increases state complexity, which means the app has to keep API, 2D rendering, and 3D rendering behavior aligned as new object properties are introduced.

## Examples

```python
def accept_reference_candidate(job_id, candidate, measured_pixels, real_units):
    ppu = measured_pixels / real_units
    width = candidate.pixel_width / ppu
    depth = candidate.pixel_depth / ppu
    scene_object = convert_rectangle_to_scene_object(candidate, width=width, depth=depth)
    add_scene_object(job_id.space_id, scene_object)
    return scene_object
```

A parallel flow applies to a product-link candidate: inspect the OCR/QR-derived URL, confirm it is meaningful, then accept it through the product-candidate endpoint so the API can create a reusable product record rather than only a temporary image annotation.

## Practical Applications

This concept fits applications where image-derived suggestions need to become editable domain objects without pretending the extraction is perfect. Room planners, CAD-adjacent annotation tools, and industrial inspection systems can all benefit from the same pattern: persist candidates, let humans calibrate and choose, then convert accepted items into standard application entities with normal editing controls.

## Related Concepts

- **[[Deterministic Reference Artifact Pipeline]]** — produces the evidence, candidates, and calibration prompts that acceptance consumes.
- **[[Free-First Vision Pipeline Modes for Spatial Planning Apps]]** — explains why this review-heavy local workflow is preferable to silently outsourcing end-user images.
- **[[Single-User Local SQLite Migration for Self-Hosted Web Apps]]** — another example of preserving operational honesty by aligning the data model with the actual deployment boundary.

## Sources

- [[Copilot Session Checkpoint: No-LLM Reference Workflow]] — records the calibration helpers, acceptance endpoints, scene-object model, product-candidate flow, and 2D/3D editing surfaces.
