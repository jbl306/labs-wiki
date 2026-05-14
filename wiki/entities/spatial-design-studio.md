---
title: "Spatial Design Studio"
type: entity
created: 2026-05-11
last_verified: 2026-05-14
source_hash: "c2c1e0f4ec58dfd8c603b1ce0e4231d656ce300cab8d51853141f3abaa454768"
sources:
  - raw/2026-05-11-copilot-session-spatial-production-deployment-56f1f521.md
  - raw/2026-05-14-copilot-session-implementing-s8-quality-82653c66.md
  - raw/2026-05-14-copilot-session-implementing-s9-features-fe18e8fa.md
concepts:
  - agent-skill-routing-architecture
  - universal-agent-schema-agents-md-for-ai-tool-integration
  - multi-surface-ui-quality-gates-active-product-delivery
  - accessibility-hardening-command-driven-3d-web-interfaces
  - cpu-bound-ai-stack-planning-homelab-spatial-apps
  - metadata-first-local-vision-capability-surfacing
related:
  - "[[Homelab]]"
  - "[[Task Observer]]"
  - "[[Copilot CLI]]"
  - "[[MemPalace]]"
  - "[[Caddy]]"
  - "[[FastAPI]]"
  - "[[PostgreSQL]]"
tier: hot
tags: [spatial-design-studio, room-planner, homelab, nextjs, fastapi, 3d, deployment, local-vision]
---

# Spatial Design Studio

## Overview

Spatial Design Studio is a full-stack room-planning application that is being turned into a production-grade homelab service rather than left as an MVP prototype. In this checkpoint, the project is no longer just a sketchpad for placement ideas; it has explicit deployment surfaces, health-checked production routes, agent-facing repository instructions, and a documented next-phase UI/UX roadmap.

The system matters because it combines several concerns that usually appear separately in hobby projects: an operationally deployable backend and web client, a geometry-aware planning workflow with both 2D and 3D views, retailer/product ingestion surfaces, and AI job orchestration hooks. The checkpoint shows the project settling into a durable architecture where future sessions can iterate on product behavior without having to rediscover deployment and security assumptions.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool |
| Created | Unknown |
| Creator | jbl306 |
| URL | https://github.com/jbl306/Spatial-Design-Studio |
| Status | Active |

## Architecture

The current stack is explicitly split across a Python API and a modern React-based frontend. The API lives under `apps/api` and uses [[FastAPI]] to handle auth, spaces, versions, assets, products, scene edits, AI jobs, and renders. The frontend lives under `apps/web` on Next.js 16.2.6 and carries the main studio experience in `apps/web/app/studio-shell.tsx`, which the checkpoint calls out as large and still "MVP-ish" even after the production increment.

Spatial Design Studio also includes a real geometry and visualization layer instead of a purely CRUD-style interface. The source notes arbitrary-angle fit math, direct 2D drag snapping, fixed-column elements, and a React Three Fiber 3D scene. That means the app's technical center is not only form handling or asset upload but also interactive scene manipulation and layout reasoning.

Persistence is intentionally in transition. Homelab production still runs with `SPATIAL_DB_PATH=/data/spatial.sqlite3`, but the codebase now includes a PostgreSQL-capable wrapper and migrations so the project can evolve toward a multi-environment database story without rewriting all persistence logic at once. This is a useful production seam: local simplicity now, broader DB flexibility later.

## Production Deployment Model

The checkpoint is especially valuable because it records the actual deployment contract instead of only the repo-local development shape. The live stack is driven from the homelab repository's `compose/compose.web.yml`, not from the app repo's own `compose/compose.spatial-design-studio.yml`. Deployments happen through `./scripts/ops/deploy.sh web`, and the validated routes are `spatial.${DOMAIN}` for the web app, `/api` for same-origin API access, and `spatial-api.${DOMAIN}/health` for direct API health checks.

Security and operational settings are also concrete. `SPATIAL_ASSET_SIGNING_SECRET` is present in the homelab environment and must not be exposed; `SPATIAL_COOKIE_SECURE=true` remains required in production; signups should be closed after bootstrap; and `SPATIAL_AI_EXECUTION_MODE=local` is the safe default until there is a trusted detached-worker procedure. Those details make this entity more than a product name; they define how the service is intended to survive real deployment.

## Agent and Workflow Surface

Another durable part of the project is its explicit agent surface. The repository now contains `AGENTS.md`, `.github/copilot-instructions.md`, and specialized agent definition files for orchestration, UI/UX, API work, and homelab deployment. That places the project squarely inside the wiki's existing body of knowledge around [[Agent Skill Routing Architecture]] and [[Universal Agent Schema (AGENTS.md) for AI Tool Integration]].

The checkpoint also records a live workflow limitation: context-engineering skill calls like `context-fundamentals`, `tool-design`, `filesystem-context`, and `multi-agent-patterns` returned "Skill not found" through the Copilot CLI Skill tool, and that observation was logged separately. Preserving that constraint helps future sessions reason about which abstractions exist in documentation versus which are actually callable in the working toolchain.

## Current Roadmap

The major unfinished area is the user experience of the main studio shell. The checkpoint says the next session should start by loading the plan at `plans/spatial-design-studio-production-ui-ux-and-feature-plan.md`, extracting reusable UI primitives into `apps/web/app/components/`, and refactoring the monolithic shell into clearer surfaces with production-grade loading, empty, and error states.

Later phases are already named: better 2D planner pan/zoom and scale affordances, improved 3D camera/material polish, stronger product ingestion workflow, AI workflow refinements, collaboration and sharing, and operational cleanup. That gives the project a durable next-step hierarchy rather than a vague "polish later" placeholder.

## Quality-System Maturation

The S8 quality checkpoint moves Spatial Design Studio from "deployed and structurally safer" toward "safe to evolve at the interface layer." The product now has a concrete UI quality stack: Storybook 10 for isolated component rendering, Lost Pixel visual baselines, Playwright coverage for a mocked core flow, a WCAG-oriented accessibility pass across forms, 3D scenes, and media panels, plus a keyboard-first command palette wired into `StudioShell` and `StudioWorkspace`. That matters because the project now preserves more than architectural and deployment truth; it also preserves evidence about what a healthy user-facing slice should look and feel like.

The checkpoint is especially durable because it records the exact compatibility seams that made the stack work. Storybook 8 was rejected by Next 16 peer dependencies, so the repo advanced to Storybook 10 and used `@storybook/addon-docs` plus `@storybook/addon-a11y` instead of the unavailable `@storybook/addon-essentials@10`. Lost Pixel still needed `lostpixel.config.ts`, so the repo kept a re-export next to `lost-pixel.config.ts`. Playwright e2e moved to port `3107` to avoid a local AdGuard collision on `3000`, and Lost Pixel required an older Chromium build through `playwright-core@1.47.2`. Those details make [[Copilot Session Checkpoint: Implementing S8 Quality]], [[Multi-Surface UI Quality Gates for Active Product Delivery]], and [[Accessibility Hardening for Command-Driven 3D Web Interfaces]] useful as operational references instead of vague "we improved quality" notes.

## S9 Feature Delivery

The S9 checkpoint shows the project maturing from quality hardening into feature-delivery under production constraints. On the user-facing side, `Scene3D.tsx` gained cutaway-wall controls, sun-position tuning, camera and panorama presets, local PNG/JSON exports, and accessible scene summaries. That is an important product signal: the 3D surface is no longer just a viewer attached to the plan; it is becoming a real planning workstation with export and inspection affordances.

The same checkpoint also refines how AI-adjacent spatial edits become durable state. Reviewed wall proposals now flow through `POST /reference/jobs/{job_id}/wall-proposals/accept`, creating a new annotated version while preserving the original target version instead of mutating the latest scene implicitly. At the same time, the app adds [[Metadata-First Local Vision Capability Surfacing]] through seeded local model profiles, `localVision` worker metadata, env and compose wiring, capability badges, and license warnings, while still blocking unsafe cloud mode in production. This makes the project's AI story more honest: more visible and structured than a roadmap note, but still explicit about what remains deferred or metadata-only.

## Impact

Spatial Design Studio is an example of a project that has crossed the boundary from exploratory feature-building into maintainable, reproducible deployment. The checkpoint captures a rare combination of product-level work, infrastructure-level deployment truth, and agent-level documentation scaffolding, which makes the entity useful both as a project reference and as a pattern for future self-hosted application hardening.
