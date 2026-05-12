---
title: "Free-First Vision Pipeline Modes for Spatial Planning Apps"
type: concept
created: 2026-05-12
last_verified: 2026-05-12
source_hash: "47cdb90273c4de212de47aaf8fde339926e688cd13758b8166d01787137e4145"
sources:
  - raw/2026-05-12-copilot-session-clarifying-vision-options-3cbd5600.md
related:
  - "[[Developer-Assisted Vision Workflows for Spatial Planning Apps]]"
  - "[[Vision Support in LLM Knowledge Ingestion Using GPT-4.1]]"
  - "[[Source-Aware Model Routing in Wiki Ingestion Pipelines]]"
tier: hot
tags: [vision, self-hosting, spatial-design-studio, multimodal, homelab, computer-vision]
---

# Free-First Vision Pipeline Modes for Spatial Planning Apps

## Overview

Free-first vision pipeline modes are a deployment pattern for spatial-planning applications that need image understanding without assuming a paid, always-on multimodal API. The core idea is to make the production contract explicit in configuration: keep the app in `disabled` or `local` mode by default, allow a developer-assisted path for prototyping, and require deliberate opt-in before any cloud provider handles user images.

In this checkpoint, the concept matters because the product goal is concrete: take reference photos and gradually turn them into scene structure, dimensions, masks, and perhaps rough 3D proxies inside [[Spatial Design Studio]]. The durable insight is that the right abstraction is not "pick one best model," but "define safe operating modes with different trust, cost, and privacy boundaries."

## How It Works

The pattern begins by refusing to collapse several very different workloads into one box labeled "vision." A spatial-planning app needs at least four operational states: **`disabled`**, where no image interpretation happens at all; **`local`**, where self-hosted models and classical CV run inside the app's own infrastructure; **`developer_assisted`**, where humans may use external tools during design or debugging; and **`api`**, where paid cloud providers are allowed to process end-user data. The checkpoint makes this explicit through configuration examples such as `SPATIAL_VISION_MODE=disabled|local|developer_assisted|api`, `SPATIAL_VISION_ALLOW_CLOUD=false`, and `SPATIAL_VISION_DEVICE=cpu|cuda`.

That mode split matters because the first production question is not "How smart is the model?" but "Who is allowed to see the image, under what budget, and on whose hardware?" In a homelab deployment, local inference has a very different operational profile from API inference. Local inference costs compute time and GPU/CPU memory, but it preserves privacy and avoids per-request billing. API inference may be stronger or easier, but it introduces credentials, unpredictable spend, latency variance, and a harder compliance story for personal photos or home interiors. By encoding these as modes instead of ad hoc decisions, the system becomes reviewable and testable.

Inside the `local` mode, the checkpoint recommends a staged stack rather than a single giant VLM. The first stage is **image cleanup and normalization** with OpenCV, Pillow, or scikit-image. That stage handles the boring but necessary work: resizing, color normalization, metadata stripping, edge cleanup, and simple geometric preprocessing. The next stage is **depth estimation**, where models such as Depth Anything V2 Small or DPT/MiDaS produce relative depth maps that can support rough scene reasoning. These models do not automatically solve room layout, but they provide the geometric prior needed for later object placement or scale estimation.

After depth comes **semantic and instance structure extraction**. The checkpoint separates this into complementary jobs. Mask2Former or MMSegmentation-style models provide broad semantic segmentation, which is useful when the app needs coarse labels such as wall, floor, window, table, or sofa. Grounding DINO provides open-set detection, which is valuable when the target category is not fixed ahead of time or when the user names a product class interactively. SAM 2 then sharpens that structure by turning boxes or points into cleaner masks. The important design lesson is that no single component has to do everything: open-set detection finds candidates, segmentation provides scene context, and mask refinement improves boundaries.

Only after those lower-level stages does the pattern recommend optional **multimodal interpretation layers** such as Qwen2.5-VL, LLaVA, or BLIP-2. These models can help guess material types, generate object descriptions, or assist with ambiguous scene semantics, but the checkpoint intentionally treats them as optional. That is a subtle but important architectural choice. If the first shipping version depends on a large VLM for every request, local deployment becomes much harder. If the first version depends on classical CV plus a few targeted perception models, the app can still produce useful structure even on modest hardware.

The same staged logic applies to 3D ambitions. The source mentions TripoSG as an optional mesh-proxy step, not as a requirement for the first release. That means the free-first pipeline is biased toward **scene understanding before scene generation**. It would rather give the app reliable masks, rough depths, and candidate object regions than promise photorealistic reconstruction too early. For a room-planning workflow, that is usually the right priority: stable measurements and editable object anchors are more valuable than speculative 3D detail.

Another important mechanism is **cloud gating**. The checkpoint does not forbid cloud APIs; it demands that they be explicit. In practice, that means `api` mode should only activate when both the mode and an allow-cloud flag say yes, and when provider credentials are present. This avoids a class of accidental architecture drift where a developer prototypes with a paid service and the app slowly comes to depend on it. The mode system makes that drift visible. If a request works only in `api`, the team knows it has crossed a cost and privacy boundary.

Licensing is part of the same control plane. The source explicitly warns against casually adopting GPL or non-commercial models in a production path. Free-first does not mean "use any open checkpoint you can find." It means prefer self-hosted components whose licenses, hardware requirements, and operational behavior fit the product. That shifts model selection from hype to deployment fitness.

The resulting pipeline is less glamorous than "just call a frontier model," but it is more durable. Each stage can be swapped independently, tested on-device, and disabled when hardware is weak. Most importantly, the application can start with a minimal but honest promise: local extraction first, developer assistance for prototyping, and paid cloud only as a clearly marked exception.

## Key Properties

- **Mode-gated deployment:** Vision behavior is controlled through explicit runtime modes instead of hidden provider assumptions.
- **Local-first backbone:** OpenCV/Pillow/scikit-image, depth models, detectors, and segmenters form the default production stack.
- **Composable perception stages:** Cleanup, depth, detection, segmentation, refinement, and optional VLM interpretation remain separate replaceable layers.
- **Explicit cloud boundary:** Paid APIs are allowed only when configuration and credentials both opt in.
- **License-aware model selection:** "Free" is filtered through license and production suitability, not just download cost.

## Limitations

Local-first pipelines trade simplicity of billing for complexity of systems integration. Model orchestration, hardware sizing, batching, and fallback behavior become the app team's problem. Relative-depth models can help with geometry, but they do not magically recover true room scale or object dimensions. Open-set detection and segmentation also tend to struggle on cluttered interiors, reflective materials, unusual furniture, or low-light photos. Finally, the more optional branches the pipeline gains, the more important it becomes to keep defaults conservative so the product does not drift into a fragile "everything enabled" mode.

## Examples

```python
def choose_vision_path(cfg):
    if cfg.mode == "disabled":
        return "skip"
    if cfg.mode == "local":
        return [
            "opencv_cleanup",
            "depth_anything_v2",
            "grounding_dino",
            "sam2",
            "mask2former",
        ]
    if cfg.mode == "developer_assisted":
        return "human-in-the-loop tooling only"
    if cfg.mode == "api" and cfg.allow_cloud and cfg.provider_key:
        return "paid_provider"
    raise RuntimeError("invalid vision configuration")
```

In the checkpoint's preferred rollout, a user photo first goes through local cleanup and depth estimation, then through detection and mask refinement. The app can expose those intermediate outputs for review before it ever attempts optional captioning or 3D proxy generation.

## Practical Applications

This pattern fits room planners, furniture-layout tools, renovation assistants, and similar products where user photos are useful but privacy, hardware limits, and cost ceilings matter. It is especially appropriate for homelab or self-hosted deployments where operators want predictable behavior and a clear "no-cloud-by-default" stance. It also helps teams stage ambition: ship local extraction first, add human review and optional VLM help later, and reserve paid APIs for cases where the extra capability is worth the boundary crossing.

## Related Concepts

- **[[Developer-Assisted Vision Workflows for Spatial Planning Apps]]** — explains the human-in-the-loop mode that should sit beside, not inside, the production path.
- **[[Vision Support in LLM Knowledge Ingestion Using GPT-4.1]]** — another multimodal pipeline, but one optimized for wiki compilation rather than end-user product requests.
- **[[Source-Aware Model Routing in Wiki Ingestion Pipelines]]** — shows the same design instinct of routing work by modality and operational boundary.

## Sources

- [[Copilot Session Checkpoint: Clarifying Vision Options]] — records the four-mode configuration pattern, the local-model shortlist, and the cloud-gating rule.

