---
title: "Vision Policy vs Extraction vs Acceptance in Spatial Reference Workflows"
type: synthesis
created: 2026-05-12
last_verified: 2026-05-12
source_hash: "synthesis-generated"
sources:
  - raw/2026-05-12-copilot-session-no-llm-reference-workflow-0264677a.md
  - raw/2026-05-12-copilot-session-clarifying-vision-options-3cbd5600.md
concepts:
  - free-first-vision-pipeline-modes-spatial-planning-apps
  - deterministic-reference-artifact-pipeline
  - review-first-candidate-acceptance-reference-jobs
related:
  - "[[Free-First Vision Pipeline Modes for Spatial Planning Apps]]"
  - "[[Deterministic Reference Artifact Pipeline]]"
  - "[[Review-First Candidate Acceptance for Reference Jobs]]"
  - "[[Spatial Design Studio]]"
tier: hot
tags: [spatial-design-studio, synthesis, computer-vision, workflow, homelab, no-llm]
---

# Vision Policy vs Extraction vs Acceptance in Spatial Reference Workflows

## Question

How does a local-first spatial-planning app move from a high-level "no-cloud by default" vision policy to an actually trustworthy workflow for turning reference photos into editable room state?

## Summary

The combined answer across these pages is that policy, extraction, and acceptance are different layers and should stay different. [[Free-First Vision Pipeline Modes for Spatial Planning Apps]] defines the trust boundary, [[Deterministic Reference Artifact Pipeline]] produces reviewable evidence inside that boundary, and [[Review-First Candidate Acceptance for Reference Jobs]] governs when that evidence is allowed to mutate the room model.

## Comparison

| Dimension | [[Free-First Vision Pipeline Modes for Spatial Planning Apps]] | [[Deterministic Reference Artifact Pipeline]] | [[Review-First Candidate Acceptance for Reference Jobs]] |
|-----------|---------------------------------------------------------------|----------------------------------------------|----------------------------------------------------------|
| Main role | Sets runtime trust, privacy, and cost modes | Extracts deterministic artifacts and candidates | Commits reviewed candidates into scene or product state |
| Core question | "Which boundaries are allowed?" | "What evidence can we derive locally?" | "When is the evidence good enough to commit?" |
| Primary outputs | Configuration modes and deployment rules | Job artifacts, OCR snippets, link candidates, geometry proposals | Scene objects, accepted products, editable transforms |
| Failure surface | Accidental cloud drift or unsafe serving mode | Weak OCR, noisy geometry, incomplete artifacts | Bad calibration, wrong acceptance, catalog pollution |
| Human involvement | Architectural decision and mode selection | Artifact review and debugging | Explicit calibration and candidate approval |
| Best use | Before implementation and during deployment design | During queued job execution | During user-facing planning and import workflows |

## Analysis

The most useful insight from the newer checkpoint is that "local-first vision" was necessary but not sufficient. The earlier policy work correctly established that [[Spatial Design Studio]] should not treat developer tools or paid APIs as its default image backend. But a policy alone does not tell the app what to do with a real uploaded image. The no-LLM implementation checkpoint fills that gap by specifying an actual extraction contract: queue a local `reference-analysis` job, run deterministic modules, and persist artifacts under the shared data directory.

That still would not be enough if extraction were allowed to mutate the room model directly. The checkpoint avoids that trap by introducing a review-first acceptance layer. This is a significant architectural refinement. Many vision-heavy products collapse extraction and commitment into one step and then struggle to explain or correct mistakes. Here, the artifact pipeline is intentionally allowed to be broad and heuristic, while acceptance is intentionally narrow and user-mediated. The split preserves speed where uncertainty is acceptable and caution where state mutation matters.

Another way to view the three concepts is as a defense-in-depth stack against different categories of failure. The policy layer prevents privacy, cost, and dependency mistakes. The extraction layer prevents opacity by persisting intermediate evidence instead of only a final answer. The acceptance layer prevents over-automation by requiring calibration and review before durable state changes. Each layer handles a different risk, and the workflow only feels trustworthy when all three are present.

The checkpoint's worker hotfix also reinforces why these layers matter. A missing `PYTHONPATH` broke the worker even though the high-level vision policy was sound. That shows the policy layer does not replace operational rigor. Conversely, once the worker ran, the extraction layer still did not get to "win" on its own; the app still needed acceptance endpoints, object transforms, and manual product review. The broader lesson is that a serious local-first vision workflow is never just a model choice. It is a chain of deployment, evidence, and commitment rules that together make the system usable.

## Key Insights

1. **Local-first policy is only the first layer** — [[Free-First Vision Pipeline Modes for Spatial Planning Apps]] sets the boundary, but the no-LLM checkpoint shows that boundary must be followed by a concrete artifact pipeline.
2. **Evidence is more valuable than premature certainty** — [[Deterministic Reference Artifact Pipeline]] improves trust by persisting previews, overlays, OCR text, and candidate lists before any room mutation happens.
3. **Acceptance is the real modeling step** — [[Review-First Candidate Acceptance for Reference Jobs]] is where the app decides a candidate deserves to become a scene object or product.

## Open Questions

- Which artifact set is sufficient for users to accept a candidate quickly without overwhelming them with debug detail?
- When should calibration be mandatory, and when can safe defaults or prior room measurements reduce user effort?
- If the extraction stack expands later, how should the app decide whether a new stage belongs in deterministic runtime, developer-assisted evaluation, or an explicitly gated paid path?

## Sources

- [[Copilot Session Checkpoint: Clarifying Vision Options]]
- [[Copilot Session Checkpoint: No-LLM Reference Workflow]]
