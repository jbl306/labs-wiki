---
title: "Copilot Session Checkpoint: Spatial Studio Production Roadmap"
type: source
created: '2026-05-14'
last_verified: '2026-05-14'
source_hash: "028eef72e54ad8269b0d7824b0cb19ec07877d03e58c629e8af12a3f492bb762"
sources:
  - raw/2026-05-14-copilot-session-spatial-studio-production-roadmap-9170f546.md
concepts:
  - cpu-bound-ai-stack-planning-homelab-spatial-apps
  - free-first-vision-pipeline-modes-spatial-planning-apps
related:
  - "[[Spatial Design Studio]]"
  - "[[Homelab]]"
  - "[[Durable Copilot Session Checkpoint]]"
  - "[[Copilot CLI]]"
  - "[[MemPalace]]"
tags: [copilot-session, checkpoint, durable-knowledge, spatial-design-studio, homelab, roadmap, ai-planning, self-hosting]
tier: hot
checkpoint_class: project-progress
retention_mode: compress
knowledge_state: ingested
ingest_method: copilot-cli-gpt-5.4
quality_score: 75
---

# Copilot Session Checkpoint: Spatial Studio Production Roadmap

## Summary

This checkpoint captures the planning turn where [[Spatial Design Studio]] was reframed from "use interesting local AI tools" to "ship only what the actual [[Homelab]] hardware can sustain." Its durable value is the combination of roadmap structure, concrete homelab constraints, and explicit cost/license notes that turn a broad production-grade ambition into a realistic CPU-first delivery plan.

## Key Points

- **The roadmap scope is product-plus-platform, not just code cleanup:** the session planned code quality, free or self-hosted tooling, UI/UX upgrades, competitive benchmarking against room-planner products, and repository reorganization for agentic sprint execution.
- **The project shape was already mapped:** the source records a monorepo with `apps/api` on FastAPI, `apps/web` on Next.js plus React Three Fiber, a `compose/` layer, a `tasks/features.md` registry, four agents, and a sprint cadence that was extended from S0-S5 into S6-S11.
- **A durable roadmap artifact already exists upstream:** the session wrote a full plan to session state, then committed a slimmer roadmap to `plans/spatial-design-studio-production-grade-roadmap.md` and linked it from the project README.
- **Hardware reality becomes the decision boundary:** the homelab host is a Beelink GTi13 Ultra with an i9-13900HK, 32 GB RAM, 1 TB NVMe, Ubuntu Server 24.04, and Intel Iris Xe graphics already serving Jellyfin workloads, with no discrete NVIDIA GPU.
- **The source sharply separates CPU-feasible and GPU-dependent AI choices:** Depth Anything V2, SAM2 small/base, HorizonNet, RoomFormer, small Ollama LLMs, and Qwen2-VL-2B Q4 are treated as feasible on CPU, while ComfyUI plus Stable Diffusion plus ControlNet are judged too slow or operationally poor without a dedicated GPU.
- **The checkpoint preserves concrete latency expectations instead of vague "might work" language:** it notes roughly 1-3 s CPU depth inference, 5-15 s CPU SAM2 inference for batch use, 10-30 s Qwen2-VL queries through Ollama, and 30-90 s Stable Diffusion 1.5 generation even before ControlNet overhead.
- **Cost discipline is explicit:** the preferred stack stays at $0 through self-hosted Grafana, Loki, Tempo, Prometheus, GlitchTip, Umami or PostHog self-host, Uptime Kuma, MinIO, restic, pgBackRest, Trivy, Semgrep community, gitleaks, Renovate, Storybook, Lost Pixel, Playwright, Ollama, and local CV models.
- **The source records important boundary cases instead of pretending "free" means frictionless:** Cloudflare Access, PostHog Cloud, Renovate hosted, and GitHub Actions free tiers are acceptable but finite, while Chromatic and Sentry SaaS are called out as avoidable paid paths.
- **Licensing is tracked as an engineering constraint alongside cost:** Stable Diffusion's CreativeML Open RAIL-M restrictions and the need to verify research-model licenses such as HorizonNet or RoomFormer are preserved as rollout caveats.
- **The checkpoint also captures operational handoff work still missing:** the full homelab service inventory still needed auditing so the roadmap would not duplicate already deployed observability or storage services.
- **A small but durable tooling quirk was saved:** plain `git` calls through the bash wrapper intermittently failed while `rtk git` worked, which matters for future sessions executing the same repository workflow through [[Copilot CLI]].

## Key Concepts

- [[CPU-Bound AI Stack Planning for Homelab Spatial Apps]]
- [[Free-First Vision Pipeline Modes for Spatial Planning Apps]]

## Related Entities

- **[[Spatial Design Studio]]** — The room-planning application whose roadmap was expanded and then constrained by real homelab deployment conditions.
- **[[Homelab]]** — The runtime environment whose actual CPU, memory, and GPU limits forced the AI stack to be re-prioritized.
- **[[Durable Copilot Session Checkpoint]]** — The artifact type that preserved roadmap intent, hardware facts, and next-step handoff material.
- **[[Copilot CLI]]** — The tool used for the original planning and for the checkpoint capture, including the noted `rtk git` workaround.
- **[[MemPalace]]** — The durable-memory workflow that promoted the checkpoint into labs-wiki raw for long-term reuse.
