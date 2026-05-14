---
title: "Local Vision Policy vs Planning vs Wiring in Spatial Design Studio"
type: synthesis
created: 2026-05-14
last_verified: 2026-05-14
source_hash: "synthesis-generated"
sources:
  - raw/2026-05-12-copilot-session-clarifying-vision-options-3cbd5600.md
  - raw/2026-05-14-copilot-session-spatial-studio-production-roadmap-9170f546.md
  - raw/2026-05-14-copilot-session-implementing-s9-features-fe18e8fa.md
concepts:
  - free-first-vision-pipeline-modes-spatial-planning-apps
  - cpu-bound-ai-stack-planning-homelab-spatial-apps
  - metadata-first-local-vision-capability-surfacing
related:
  - "[[Free-First Vision Pipeline Modes for Spatial Planning Apps]]"
  - "[[CPU-Bound AI Stack Planning for Homelab Spatial Apps]]"
  - "[[Metadata-First Local Vision Capability Surfacing]]"
  - "[[Spatial Design Studio]]"
tier: hot
tags: [spatial-design-studio, synthesis, local-vision, homelab, planning, implementation]
---

# Local Vision Policy vs Planning vs Wiring in Spatial Design Studio

## Question

How should [[Spatial Design Studio]] move from a sound local-first vision policy to hardware-aware decisions and then to a shipped implementation without pretending the heavy runtime already exists?

## Summary

The three pages answer different layers of the same problem. [[Free-First Vision Pipeline Modes for Spatial Planning Apps]] sets the trust boundary, [[CPU-Bound AI Stack Planning for Homelab Spatial Apps]] filters that boundary through real host capacity, and [[Metadata-First Local Vision Capability Surfacing]] turns the surviving decisions into config, model-profile, runtime-metadata, and UI contracts. Together they show how to ship an honest local-vision trajectory instead of either overpromising or stalling indefinitely.

## Comparison

| Dimension | [[Free-First Vision Pipeline Modes for Spatial Planning Apps]] | [[CPU-Bound AI Stack Planning for Homelab Spatial Apps]] | [[Metadata-First Local Vision Capability Surfacing]] |
|-----------|---------------------------------------------------------------|----------------------------------------------------------|------------------------------------------------------|
| Core question | Which runtime boundaries are acceptable? | Which local options are credible on the current machine? | How do we expose those options in the product before full inference is ready? |
| Primary artifact | Vision modes, cloud gating, trust rules | Feasibility buckets, latency expectations, BYO-GPU deferrals | Model profiles, env vars, compose wiring, `localVision` metadata, UI badges |
| Main risk controlled | Hidden cloud, privacy drift, cost drift | Hardware fantasy and unusable latency | Product overclaiming and undocumented capability seams |
| Typical output | `disabled` / `local` / explicit cloud opt-in | CPU-feasible shortlist and deferred heavy paths | Truthful capability surfaces without silent scene mutation |
| Best stage | Early architecture and deployment policy | Roadmap shaping before implementation | Sprint-level product integration and operator handoff |
| Failure if skipped | Unsafe or ambiguous serving boundary | A roadmap the homelab cannot actually run | A gap between planning docs and what the app exposes |

## Analysis

The most important lesson across the three pages is that "local vision" is not a single decision. Policy, feasibility, and implementation are separate layers, and collapsing them leads to confusion. A team can have excellent instincts about privacy and still build a roadmap around models the host cannot run well. It can also have realistic hardware notes and still fail to encode them into the product, leaving users and future sessions with no shared vocabulary for what is active, deferred, or blocked.

The policy page is the normative layer. It says the product must default to local or disabled behavior, treat developer tools as development aids rather than backend infrastructure, and require explicit approval before cloud inference enters the runtime. That answers the governance question. But it intentionally stops short of saying whether specific local models are wise on the current machine.

The planning page adds the operational filter. It translates hardware facts, shared-resource contention, latency expectations, and licensing notes into a shortlist of what belongs on the first shipping path. This is where the app learns that some nominally self-hosted tools still belong in the deferred lane because a CPU-only homelab cannot run them with believable product responsiveness.

The S9 wiring concept turns those earlier decisions into code and product truth. Instead of waiting for every model path to be complete, the app seeds named profiles, adds config keys, wires compose, emits `localVision` metadata, and surfaces capability badges plus warnings in the UI. That is valuable because it closes the loop between architecture and implementation. The system now has a durable language for readiness, provenance, and deferral. Future model-execution work can plug into known seams rather than re-opening the entire design question.

The combination is stronger than any single page. Policy without planning stays abstract. Planning without wiring stays trapped in notes. Wiring without policy risks accidental drift and wiring without planning risks overpromising. Together they describe an engineering sequence that is unusually reusable for self-hosted AI products: first define what boundaries are allowed, then decide what your hardware can honestly support, then ship those decisions as explicit capability surfaces before graduating them into full inference behavior.

## Key Insights

1. **Boundary discipline should come before model enthusiasm** — [[Free-First Vision Pipeline Modes for Spatial Planning Apps]] keeps privacy and cost rules explicit before implementation details take over.
2. **Hardware realism is a roadmap tool, not just an ops note** — [[CPU-Bound AI Stack Planning for Homelab Spatial Apps]] changes what should ship first, not just what feels fast in a benchmark.
3. **Metadata can be a real product milestone** — [[Metadata-First Local Vision Capability Surfacing]] shows that config, profile, and UI truth are meaningful deliverables even before every heavy model path is active.

## Open Questions

- Which of the seeded local profiles should graduate first from metadata-only surfacing into user-triggerable execution paths?
- What review or artifact boundary should remain in place once local multimodal interpretation moves beyond metadata into scene-affecting suggestions?
- If the homelab later gains stronger GPU capacity, which deferred profiles should become active by default and which should remain opt-in?

## Sources

- [[Copilot Session Checkpoint: Clarifying Vision Options]]
- [[Copilot Session Checkpoint: Spatial Studio Production Roadmap]]
- [[Copilot Session Checkpoint: Implementing S9 Features]]
