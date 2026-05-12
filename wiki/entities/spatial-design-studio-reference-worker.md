---
title: "Spatial Design Studio Reference Worker"
type: entity
created: 2026-05-12
last_verified: 2026-05-12
source_hash: "9c218bc4dd06334dac0cc3734354e440f10b258ad6ca81f29799e18d7980f91a"
sources:
  - raw/2026-05-12-copilot-session-no-llm-reference-workflow-0264677a.md
concepts:
  - deterministic-reference-artifact-pipeline
  - review-first-candidate-acceptance-reference-jobs
related:
  - "[[Spatial Design Studio]]"
  - "[[Homelab]]"
  - "[[Deterministic Reference Artifact Pipeline]]"
  - "[[Review-First Candidate Acceptance for Reference Jobs]]"
  - "[[Free-First Vision Pipeline Modes for Spatial Planning Apps]]"
tier: hot
tags: [spatial-design-studio, worker, homelab, computer-vision, no-llm, ocr]
---

# Spatial Design Studio Reference Worker

## Overview

Spatial Design Studio Reference Worker is the internal background service that executes queued `reference-analysis` jobs for [[Spatial Design Studio]] without using an LLM or paid cloud vision backend. In this checkpoint it becomes the concrete runtime embodiment of the app's local-first reference-photo plan: it polls the job queue, runs deterministic extraction code from `spatial_api.reference`, and writes reviewable artifacts into the shared Spatial data directory.

What makes the worker important is that it turns the earlier "keep vision local" policy into an operationally separable service. Rather than doing all image work inline with user requests or delegating it to opaque external tooling, the app now has a dedicated homelab process with explicit resource limits, explicit no-cloud flags, and a narrow command surface that can be deployed, observed, and hotfixed independently.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Service |
| Created | 2026-05-12 |
| Creator | Unknown |
| URL | N/A |
| Status | Active |

## Runtime Contract

The worker runs as container `spatial-design-studio-reference-worker` with command `python -m spatial_api.worker --interval 2 --limit 1`. The source is explicit that this service is for `reference-analysis` jobs only, not for generic detached AI execution. Its job loop wakes up every two seconds, processes at most one queued job per iteration, and relies on the API package mounted inside the same image layout used by the rest of the Spatial stack.

That contract is reinforced by configuration. `SPATIAL_REFERENCE_ALLOW_CLOUD=false` and `SPATIAL_REFERENCE_ALLOW_LLM=false` remain hard-false in the deployed compose service. The worker therefore exists to operationalize deterministic extraction, OCR, QR/URL discovery, calibration metadata, and candidate generation, not to sneak a cloud dependency back into the product under a different service name.

## Deployment Topology

The worker is defined in `compose/compose.web.yml` inside the [[Homelab]] repository. It shares the Spatial data volume, has no Caddy labels, and is attached only to the network surface needed to reach the API and shared storage. The checkpoint also records its resource envelope: memory limit `2G` and CPU limit `2.0`. Those values matter because they tell future sessions this is meant to be a bounded internal helper, not a general-purpose GPU inference box.

The artifact directory is also part of the topology. Reference-job output lands under `/opt/homelab/data/spatial-design-studio/reference-jobs` on the host, exposed to the app through `${SPATIAL_DATA_DIR}/reference-jobs/{job_id}`. That shared location is what lets the worker produce normalized previews, overlays, OCR text, and candidate payloads that the API and UI can later expose for user review.

## Operational Gotchas

The source preserves one especially valuable failure mode: after the initial deploy, the worker entered a restart loop because Python could not resolve `spatial_api`. The eventual fix was not a code rewrite but an environment correction—`PYTHONPATH=/app/apps/api` had to be set in the worker service. This is a durable deployment fact because the API package lives under `/app/apps/api` inside the image, so `python -m spatial_api.worker` depends on module path wiring rather than only the container's working directory.

The checkpoint also distinguishes the worker's own problem from unrelated homelab noise. `scripts/ops/setup.sh` failed while trying to `chown` a Riven FUSE mount, but that happened after the required Spatial directory had already been created and was treated as a separate setup bug rather than a blocker for the worker rollout.

## Impact

This worker is the service boundary that makes the no-LLM reference flow credible. It gives [[Spatial Design Studio]] a repeatable place to run deterministic extraction, keeps user-facing uploads off developer tooling and paid APIs, and makes failures observable at the compose-service level. In other words, it turns a vision-policy preference into a deployable part of the system.

## Sources

- [[Copilot Session Checkpoint: No-LLM Reference Workflow]] — records the worker's command, limits, volume layout, and PYTHONPATH hotfix.
