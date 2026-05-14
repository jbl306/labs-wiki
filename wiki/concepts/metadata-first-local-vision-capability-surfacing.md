---
title: "Metadata-First Local Vision Capability Surfacing"
type: concept
created: 2026-05-14
last_verified: 2026-05-14
source_hash: "c2c1e0f4ec58dfd8c603b1ce0e4231d656ce300cab8d51853141f3abaa454768"
sources:
  - raw/2026-05-14-copilot-session-implementing-s9-features-fe18e8fa.md
related:
  - "[[CPU-Bound AI Stack Planning for Homelab Spatial Apps]]"
  - "[[Free-First Vision Pipeline Modes for Spatial Planning Apps]]"
  - "[[Review-First Candidate Acceptance for Reference Jobs]]"
  - "[[Spatial Design Studio]]"
tier: hot
tags: [spatial-design-studio, local-vision, metadata, model-capabilities, homelab, ai-integration]
---

# Metadata-First Local Vision Capability Surfacing

## Overview

Metadata-first local vision capability surfacing is the implementation pattern where an application ships the contract, configuration, model registry, and user-facing capability disclosures for local AI before it claims to run a fully autonomous heavyweight inference stack. In this S9 checkpoint for [[Spatial Design Studio]], the concept matters because the team had already done the policy and hardware-feasibility thinking; the remaining problem was how to expose a credible local-vision path without lying about what the product could actually execute today.

The durable insight is that there is a middle state between "no AI integration" and "fully operational multimodel runtime." A serious homelab product can wire model profiles, capability flags, warnings, and worker metadata first, then let future execution stages plug into that contract instead of forcing every sprint to either overpromise or defer everything entirely.

## How It Works

The pattern starts by separating **capability declaration** from **state-mutating inference**. Earlier planning pages for [[Spatial Design Studio]] had already decided that local-first vision was the right boundary and that the available homelab hardware favored CPU-feasible models plus explicit deferrals. But a plan is still only a plan until the repo exposes stable places for configuration, model identity, UI messaging, and runtime metadata. Metadata-first wiring answers that gap by making those surfaces real even before every model path is implemented end to end.

In the checkpoint, the first concrete mechanism is a **seeded model-profile registry**. Instead of letting model availability live only in a README or an engineer's memory, the app adds database seed data in `apps/api/spatial_api/db.py` for named local profiles such as **Qwen2-VL-2B Q4**, **Depth-Anything-v2-small**, **SAM2-tiny**, and **HorizonNet**. Each profile acts like a durable contract entry: it tells the rest of the stack that a capability exists conceptually, what class of model it belongs to, and whether it should be presented as active, optional, or deferred. This matters because downstream code can reason about known profiles without inventing ad hoc strings or silently coupling UI behavior to whichever model an engineer happens to mention in a comment.

The second mechanism is **runtime metadata emission without silent mutation**. The checkpoint adds `localVision` metadata in `apps/api/spatial_api/ai_runner.py`, but the source is explicit that this does **not** mutate scene state. That distinction is the heart of the concept. A weaker implementation would hide uncertainty by making a best effort guess, writing results directly into the scene model, and only later discovering that the runtime was too slow, too incomplete, or too fragile. Metadata-first wiring does the opposite: it allows the worker or API surface to say, in effect, "here is what local vision is configured to know about," without pretending that a seeded model card is equivalent to a trustworthy production inference result.

The third mechanism is **configuration and deployment normalization**. The checkpoint expands `.env.example`, `apps/api/spatial_api/config.py`, and `compose/compose.spatial-design-studio.yml` with `SPATIAL_VISION_*` variables plus `SPATIAL_OLLAMA_BASE_URL`. This turns local vision from an implementation rumor into an operationally visible contract. Operators can see which knobs exist, what services or URLs local inference would depend on, and which deployments are allowed to enable or block certain modes. The production guard against `SPATIAL_VISION_ALLOW_CLOUD=true` is especially important. It proves that metadata-first wiring is not a slippery slope toward accidental cloud drift; the configuration layer still encodes the privacy and cost boundary established in earlier planning.

Another important part of the pattern is **truthful user-facing capability surfacing**. The source notes `apps/web/app/lib/ai-model-capabilities.ts` and `AiJobsPanel.tsx` changes that show capability badges and license warnings. This is not cosmetic garnish. In AI-heavy products, user interfaces often become the place where teams accidentally overstate readiness. A badge that says a model exists, a warning that says a profile is deferred, or a label that marks a capability as local-only keeps the UI aligned with operational truth. It also helps future engineers because the frontend is now reading from a shared capability vocabulary instead of inventing one-off prose whenever a model is added or postponed.

The checkpoint's handling of **deferred models** shows why this approach works better than a binary shipped/not-shipped mindset. `stable-diffusion-controlnet` is seeded as disabled and surfaced only as deferred metadata. That means the product can acknowledge the architectural slot for generation-heavy guidance without claiming that the current CPU-bound homelab can run it well. In effect, the model profile becomes a placeholder with integrity: it records the intended seam, the current status, and the fact that future enablement depends on hardware or product decisions that have not happened yet.

This pattern also improves future integration work because it creates a stable handoff between planning and execution. Once profiles, config keys, compose wiring, runtime metadata, and UI capability rendering exist, later sessions can focus on narrower questions: Should a given model run synchronously or via background jobs? Which outputs are trustworthy enough to promote into reviewed artifacts? How should failed local inference be reported? The system no longer has to redesign its vocabulary each time. The architecture has a defined slot for new capability logic.

The trade-off is that metadata-first wiring deliberately refuses to masquerade as finished product intelligence. Users may see capability labels before they can trigger every advanced path, and engineers still need to implement the hard parts of extraction quality, latency control, and promotion into durable scene state. But that restraint is exactly what makes the pattern durable. It preserves truthful interfaces, keeps privacy and hardware boundaries explicit, and prevents roadmap intent from being lost between planning documents and code.

## Key Properties

- **Declared capability registry:** named model profiles become durable app data instead of informal notes.
- **No silent scene mutation:** runtime metadata can surface readiness or provenance without pretending inference is complete.
- **Config-first deployment contract:** env keys, compose wiring, and guards make vision mode decisions operationally visible.
- **Truthful UI exposure:** badges and warnings explain what is active, local-only, licensed, or deferred.
- **Deferred-path integrity:** heavyweight models can be represented honestly as disabled or BYO-GPU candidates rather than being omitted or overpromised.

## Limitations

This pattern does not solve model quality, latency, or human-trust problems by itself. A seeded profile can still point at a model that is too slow for the current machine or too weak for production use. Capability badges may also confuse users if the product exposes too many future-facing options before enough of them are actionable. Finally, metadata-first wiring requires discipline: teams must resist the temptation to treat the presence of a config flag or model card as proof that an end-to-end feature is ready.

## Examples

A simplified version of the pattern looks like this:

```python
MODEL_PROFILES = {
    "qwen2-vl-2b-q4": {"mode": "local", "status": "available", "surface": "metadata"},
    "depth-anything-v2-small": {"mode": "local", "status": "available", "surface": "metadata"},
    "stable-diffusion-controlnet": {"mode": "deferred", "status": "disabled", "surface": "ui-only"},
}

def local_vision_capabilities():
    return {
        "profiles": MODEL_PROFILES,
        "cloud_allowed": False,
        "scene_mutation": False,
    }
```

In the S9 checkpoint, that logic is distributed across DB seed data, config, compose wiring, API metadata, and UI labels rather than existing as a single dictionary. The principle is the same: expose the contract truthfully before promising more than the runtime can support.

## Practical Applications

Metadata-first capability surfacing is useful whenever a self-hosted or safety-sensitive product is adopting AI under real operational constraints. Homelab apps, private document systems, local media-analysis tools, and industrial review workflows can all benefit from it. It is especially valuable when the team already knows the eventual model family but needs to keep product, deployment, and UI surfaces honest while the heavier inference path is still being staged.

## Related Concepts

- **[[CPU-Bound AI Stack Planning for Homelab Spatial Apps]]** — decides which local models are realistic on the current hardware; metadata-first wiring turns that plan into app-level contracts.
- **[[Free-First Vision Pipeline Modes for Spatial Planning Apps]]** — defines the trust and privacy boundary that metadata-first wiring must preserve in config and deployment.
- **[[Review-First Candidate Acceptance for Reference Jobs]]** — shows the complementary rule for when model-derived evidence is finally allowed to mutate durable application state.

## Sources

- [[Copilot Session Checkpoint: Implementing S9 Features]] — records the seeded model profiles, `localVision` metadata, env/compose/docs wiring, UI capability surfacing, and explicit deferral of heavyweight generation paths.
