---
title: "CPU-Bound AI Stack Planning for Homelab Spatial Apps"
type: concept
created: 2026-05-14
last_verified: 2026-05-14
source_hash: "028eef72e54ad8269b0d7824b0cb19ec07877d03e58c629e8af12a3f492bb762"
sources:
  - raw/2026-05-14-copilot-session-spatial-studio-production-roadmap-9170f546.md
related:
  - "[[Free-First Vision Pipeline Modes for Spatial Planning Apps]]"
  - "[[Developer-Assisted Vision Workflows for Spatial Planning Apps]]"
  - "[[Homelab Service Inventory And Dashboard Synchronization]]"
tier: hot
tags: [homelab, spatial-design-studio, ai-planning, cpu-inference, self-hosting, roadmap]
---

# CPU-Bound AI Stack Planning for Homelab Spatial Apps

## Overview

CPU-bound AI stack planning is the discipline of choosing vision, multimodal, observability, and workflow components based on the hardware that actually exists rather than on the strongest demos available online. In this checkpoint, the concept matters because [[Spatial Design Studio]] was being pushed toward a production-grade roadmap inside a personal [[Homelab]], not onto an elastic cloud platform with a spare GPU budget.

The durable insight is that "self-hosted" is still too vague. A CPU-only homelab with an Intel iGPU already occupied by media transcoding has very different safe defaults from a workstation with a discrete NVIDIA card. Good planning therefore starts by converting hardware facts into product and roadmap constraints before model selection hardens into architecture.

## How It Works

The method begins with an inventory pass, not a model pass. Before choosing tools, the planner identifies the serving machine, memory ceiling, storage, accelerator type, and any competing workloads already using those resources. In the checkpoint, those facts are concrete: a Beelink GTi13 Ultra, Intel Core i9-13900HK, 32 GB DDR5, 1 TB NVMe, Ubuntu Server 24.04, and Intel Iris Xe graphics already doing Jellyfin transcoding. The absence of a discrete NVIDIA GPU is not just a procurement detail; it is the primary filter that decides whether image-generation-heavy plans are realistic or merely aspirational.

Once the hardware is known, the next step is to classify candidate AI components by **operational fit**, not by benchmark prestige. The checkpoint implicitly uses at least four buckets. First are **CPU-feasible building blocks**, such as Depth Anything V2 small/base, SAM2 small/base for batch work, HorizonNet, RoomFormer, and small Ollama-served language or multimodal models like Llama 3.2 3B, Qwen 2.5 3B Q4, or Qwen2-VL-2B Q4. These are imperfect but usable inside the current machine profile. Second are **CPU-possible but user-experience-poor tools**, where the model might technically run but only at latencies that break the product. Third are **GPU-dependent tools**, such as ComfyUI plus Stable Diffusion and ControlNet, whose value depends on throughput and iteration speed that the checkpoint's host cannot honestly offer. Fourth are **cloud fallbacks**, like Workers AI, which may solve capability gaps but cross cost and privacy boundaries and therefore must remain deliberate exceptions.

This classification is only useful if it is grounded in approximate runtime expectations. The checkpoint captures exactly that kind of operational calibration. Depth inference in roughly 1-3 seconds per image is acceptable for asynchronous enrichment or a preview flow. SAM2 in roughly 5-15 seconds on CPU can still work in batch or background job mode. Qwen2-VL queries in the 10-30 second range may be fine for low-frequency interpretation or operator review. But Stable Diffusion 1.5 at roughly 30-90 seconds per 512x512 image, before ControlNet overhead, crosses the line from "slow" to "misleading roadmap dependency." The core mechanism, then, is not just to say "CPU good, GPU better." It is to convert expected latency into a product truth about whether a feature belongs in the first shipping path, a deferred path, or an optional bring-your-own-GPU mode.

Another part of the process is **contention analysis**. Homelab planners often overestimate accelerators because they count the device only once, as if the machine were dedicated to the new feature. The checkpoint does not make that mistake. It notes that Intel Iris Xe could potentially accelerate some workloads through OpenVINO, but the same iGPU is already serving Jellyfin transcoding. That turns a nominal acceleration opportunity into a risk of degraded media service, degraded AI latency, or both. CPU-bound planning therefore treats shared accelerators conservatively. A feature is not deployment-safe merely because some hardware path exists; it must coexist with the rest of the machine's obligations.

Cost and licensing are folded into the same planning loop rather than treated as an afterthought. The checkpoint's preferred stack keeps observability, analytics, QA, backups, and most inference components in the $0 self-hosted lane: Grafana, Loki, Tempo, Prometheus, Promtail, GlitchTip, Umami or self-hosted PostHog, Uptime Kuma, MinIO, pgBackRest, restic, Trivy, Semgrep community, gitleaks, Renovate, Storybook, Lost Pixel, Playwright, Ollama, and local models. But the important mechanism is not a shopping list; it is the decision rule that a "free" component still fails planning if it carries restrictive licensing, hidden hosted usage, or hardware demands the system cannot satisfy. That is why Stable Diffusion license constraints and research-model license uncertainty are preserved right next to cost notes instead of being deferred to legal cleanup later.

The approach then maps these constraints into roadmap structure. Instead of promising a broad "AI-powered spatial workflow," the planner decomposes the backlog into what can ship now and what should be deferred. CPU-feasible extraction stages become candidates for the core product path. GPU-heavy generation stages become optional, explicitly postponed, or moved behind a "BYO-GPU" or paid-cloud gate. Observability or storage services already present in homelab are marked as reuse targets rather than greenfield deployment tasks. In the checkpoint, this shows up as a requirement to update the roadmap itself: add a homelab capacity section, annotate cost and GPU feasibility in the toolchain table, and rewrite the SDS-132 local AI provider row so it reflects CPU-only realism.

This planning style also changes the meaning of "best model." In a cloud-first product, the strongest available multimodal or image-generation model may really be the best answer if the budget tolerates it. In a CPU-bound homelab, the best model is the one whose latency, memory use, operational complexity, and license all fit the actual environment while still giving the product a credible user experience. That usually favors smaller specialized models, asynchronous execution, reviewable intermediate artifacts, and explicit mode flags over monolithic high-capability stacks.

Finally, CPU-bound AI stack planning works because it is honest about sequence. It does not reject ambitious capabilities forever; it puts them in the correct order. First prove the product can do useful local extraction, review, and planning on the hardware you own. Then document what additional hardware, hosted inference, or licensing approval would be needed to unlock more advanced generation or multimodal interpretation. That sequencing keeps the roadmap trustworthy. It prevents the team from building a product story on top of compute assumptions the infrastructure cannot currently honor.

## Key Properties

- **Hardware-first filtering:** CPU, RAM, storage, and accelerator availability are evaluated before tool selection hardens into architecture.
- **Latency-aware feasibility:** Candidate tools are sorted by whether their expected runtimes still produce a believable product experience.
- **Shared-resource realism:** Accelerators already serving workloads like Jellyfin are treated as contested resources, not free capacity.
- **Roadmap translation:** Hardware and license constraints are pushed back into sprint plans, table annotations, and feature sequencing.
- **Cost-plus-license discipline:** A component must fit budget, license, and hardware simultaneously to qualify as a default choice.

## Limitations

CPU-bound planning can become too conservative if it is used to permanently rule out valuable capabilities instead of sequencing them. Runtime estimates are also context-sensitive: model quantization, batch size, image resolution, and implementation quality can move actual latencies meaningfully. Another limitation is that planning around a single host profile may underfit future changes; adding a discrete GPU or offloading a competing service can reopen options quickly. Finally, this concept helps choose a realistic stack, but it does not itself solve extraction quality, room-scale ambiguity, or evaluation of model correctness on difficult interior scenes.

## Examples

```python
def classify_component(needs_nvidia_gpu, cpu_latency_s, shares_busy_igpu, license_ok):
    if not license_ok:
        return "reject"
    if needs_nvidia_gpu:
        return "defer-or-byo-gpu"
    if shares_busy_igpu:
        return "cpu-only-or-background"
    if cpu_latency_s <= 15:
        return "ship-local"
    return "optional-or-async"
```

Applied to the checkpoint's stack, Depth Anything V2 lands in `ship-local`, SAM2 small/base in `optional-or-async` or background local processing, Qwen2-VL-2B in low-frequency local interpretation, and Stable Diffusion plus ControlNet in `defer-or-byo-gpu`. The point is not mathematical precision; it is to make hardware truth visible early enough that the roadmap stays honest.

## Practical Applications

This concept is useful for any self-hosted product that wants AI features without quietly adopting cloud assumptions. Room planners, media-analysis pipelines, knowledge systems with optional local inference, and homelab automation tools all benefit from it. It is especially valuable when a project has already accumulated an exciting tool shortlist and needs a disciplined way to separate "possible in a demo" from "credible in production on this machine."

## Related Concepts

- **[[Free-First Vision Pipeline Modes for Spatial Planning Apps]]**: Defines runtime trust modes; CPU-bound planning narrows which local mode components are actually viable on current hardware.
- **[[Developer-Assisted Vision Workflows for Spatial Planning Apps]]**: Explains how stronger external tooling can remain in the engineering lane when local production hardware is modest.
- **[[Homelab Service Inventory And Dashboard Synchronization]]**: Reinforces the same discipline of checking what the environment already runs before adding new infrastructure promises.

## Sources

- [[Copilot Session Checkpoint: Spatial Studio Production Roadmap]] — provides the concrete host profile, latency estimates, cost notes, and roadmap adjustments that define the concept.
