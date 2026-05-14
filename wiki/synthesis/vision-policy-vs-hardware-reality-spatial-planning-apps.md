---
title: "Vision Policy vs Hardware Reality in Spatial Planning Apps"
type: synthesis
created: 2026-05-14
last_verified: 2026-05-14
source_hash: "synthesis-generated"
sources:
  - raw/2026-05-14-copilot-session-spatial-studio-production-roadmap-9170f546.md
  - raw/2026-05-12-copilot-session-clarifying-vision-options-3cbd5600.md
concepts:
  - free-first-vision-pipeline-modes-spatial-planning-apps
  - cpu-bound-ai-stack-planning-homelab-spatial-apps
related:
  - "[[Free-First Vision Pipeline Modes for Spatial Planning Apps]]"
  - "[[CPU-Bound AI Stack Planning for Homelab Spatial Apps]]"
  - "[[Spatial Design Studio]]"
tier: hot
tags: [spatial-design-studio, synthesis, self-hosting, vision, homelab, hardware-constraints]
---

# Vision Policy vs Hardware Reality in Spatial Planning Apps

## Question

How should a self-hosted spatial-planning product move from a sound local-first vision policy to a roadmap that actually matches the hardware it runs on?

## Summary

The earlier policy work explains **which boundaries are acceptable**: local by default, developer-assisted for engineering, and cloud only by explicit opt-in. The newer roadmap checkpoint explains **which local options remain credible on the real machine**: small CPU-feasible models and asynchronous processing are viable, while GPU-hungry generation stacks should be deferred or explicitly gated.

## Comparison

| Dimension | [[Free-First Vision Pipeline Modes for Spatial Planning Apps]] | [[CPU-Bound AI Stack Planning for Homelab Spatial Apps]] |
|-----------|---------------------------------------------------------------|----------------------------------------------------------|
| Core question | Which trust, privacy, and cost boundaries should the runtime expose? | Which of those local or optional components can the current host run honestly? |
| Primary artifact | Runtime modes such as `disabled`, `local`, `developer_assisted`, and `api` | A filtered shortlist of CPU-feasible, deferred, or gated tools tied to host capacity |
| Main constraint type | Architectural boundary and deployment policy | Hardware throughput, resource contention, and practical latency |
| Typical outputs | Mode flags, cloud gating rules, modular local vision stages | Tool feasibility notes, sprint reprioritization, cost/license annotations, BYO-GPU deferrals |
| Failure mode if ignored | Hidden cloud dependence or privacy/cost drift | A roadmap that promises features the homelab cannot deliver well |
| Best use | Early architecture definition and deployment policy | Final roadmap shaping before implementation and service rollout |

## Analysis

The two concepts solve adjacent but different problems. [[Free-First Vision Pipeline Modes for Spatial Planning Apps]] is a policy page: it prevents the app from accidentally smuggling paid APIs, developer tooling, or unsafe defaults into production. That is necessary because a room-planning product handles live user images and needs a clear trust boundary. But policy alone does not answer the next question a serious builder immediately hits: "Given my actual homelab, which local stack should I commit to first?"

That is where [[CPU-Bound AI Stack Planning for Homelab Spatial Apps]] becomes necessary. The newer checkpoint does not overturn the earlier policy; it operationalizes it. Once `local` is declared the preferred mode, the planner still has to decide whether "local" means a lightweight CPU extraction lane or an unrealistic dream of ComfyUI, Stable Diffusion, and ControlNet on hardware that lacks an NVIDIA GPU. The roadmap checkpoint adds exactly that missing realism by turning host facts into feature sequencing.

The contrast is easiest to see in how each page treats optionality. The policy page says cloud inference can exist, but only through explicit configuration. The hardware-feasibility page says some local stacks should also be treated as optional, even though they are nominally self-hosted, because self-hosting alone does not guarantee a good product experience. A CPU-only machine may satisfy privacy goals while still failing usability goals if a feature takes a minute per image. So the newer concept tightens the older one: it replaces "can be self-hosted" with "can be self-hosted well enough on this machine."

Together, the two pages form a better decision stack than either alone. Policy prevents hidden boundary mistakes. Hardware realism prevents hidden performance fantasies. When combined, they produce a roadmap that is both principled and honest: local-first extraction where CPU latencies are acceptable, developer-assisted tooling for analysis and comparison, and GPU-heavy or cloud-backed stages deferred until there is an explicit infrastructure or budget decision.

## Key Insights

1. **Policy is necessary but not sufficient** — [[Free-First Vision Pipeline Modes for Spatial Planning Apps]] sets safe runtime boundaries, but the newer checkpoint shows that local mode still needs host-specific feasibility filtering.
2. **Self-hosted can still be the wrong default** — [[CPU-Bound AI Stack Planning for Homelab Spatial Apps]] shows that GPU-hungry local stacks may violate user-experience expectations even when they satisfy privacy goals.
3. **Roadmaps improve when constraints are pushed upstream** — the best time to annotate cost, licenses, and hardware viability is before a sprint plan turns aspirational tooling into committed architecture.

## Open Questions

- What minimum hardware profile should let a spatial-planning app graduate from CPU-first extraction to practical local generation or heavier multimodal models?
- Which local tasks should always remain asynchronous, even on stronger hardware, to preserve a good interactive planning experience?
- If the homelab later adds a discrete GPU, which deferred features should move first: image restyling, ControlNet-guided structure extraction, or richer local multimodal interpretation?

## Sources

- [[Copilot Session Checkpoint: Clarifying Vision Options]]
- [[Copilot Session Checkpoint: Spatial Studio Production Roadmap]]
