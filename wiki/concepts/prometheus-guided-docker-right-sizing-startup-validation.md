---
title: "Prometheus-Guided Docker Right-Sizing with Startup Validation"
type: concept
created: 2026-04-24
last_verified: 2026-04-24
source_hash: "96f3fb59664d099a456f5080ba4d80ba8e177a8b0561c0bd77500383240cb3ee"
sources:
  - raw/2026-04-24-copilot-session-homelab-memory-optimization-beddybyes-ingest-9a440dbe.md
related:
  - "[[Docker Container Resource Auditing and Optimization]]"
  - "[[Comprehensive Grafana Monitoring for Docker Homelab Services]]"
  - "[[Out-of-Memory (OOM) Failure Diagnosis and Remediation in ML Containers]]"
tier: hot
tags: [docker, prometheus, cadvisor, homelab, resource-management, memory-optimization]
---

# Prometheus-Guided Docker Right-Sizing with Startup Validation

## Overview

Prometheus-guided Docker right-sizing is a resource-tuning method that uses time-windowed operational telemetry, rather than static guesses, to set container CPU and memory limits. The distinctive feature is the second half of the loop: after deploying new caps, the operator immediately validates startup behavior and backs off any limit that leaves a service running too close to saturation. In the checkpoint behind this page, that approach surfaced hidden host memory pressure, reclaimed wasted headroom, and still caught under-sized Immich services before they caused instability.

## How It Works

The method starts from the idea that a single `docker stats` snapshot is not enough to size a fleet. A host can look calm in the present while still being unhealthy over longer windows. In this session, the live snapshot showed 31 GB of RAM with roughly 16 GB used and a CPU profile that looked completely safe. The 7-day Prometheus view, however, told the real story: swap was averaging 7.92 GB, `MemAvailable` had fallen as low as 0.55 GB, and there had already been an OOM event. That is the core diagnostic insight: right-sizing should be driven by historical stress signals, not by the current minute's comfort.

Prometheus and cAdvisor make that possible by separating host-level and container-level evidence. Host metrics reveal whether the machine is actually memory-bound, CPU-bound, or just over-provisioned on paper. Container metrics show where the pressure is or is not coming from. In the checkpoint, CPU was effectively ruled out early because the 7-day average was only 9.5% and the p95 was 28.6% across 20 cores. Memory, by contrast, showed a classic mismatch between configured limits and real demand: the fleet's container working set averaged around 7.5 GB but could flare to 17.5 GB, and some services carried far more reserved memory than their observed behavior justified.

Once the operator has that evidence, the next step is ranking containers into three buckets: obviously over-allocated, obviously under-allocated, and uncertain. The checkpoint's actionable set came from services whose limits were either missing or disconnected from real usage. `flaresolverr` stood out because it had no cap at all. Media and utility services such as Jellyfin, Riven, and OpenCode had generous limits that did not match their observed pressure. The practical sizing target is not the average; it is a buffer above meaningful steady-state and restart-time behavior. A useful heuristic for that decision loop is:

$$
u = \frac{\text{working\_set}}{\text{memory\_limit}}
$$

and then

$$
\text{target\_limit} = \max(1.1 \times \text{startup\_peak},\ 1.25 \times \text{steady\_state\_p95})
$$

The checkpoint does not state those formulas explicitly, but it follows that operational logic: choose caps that cut waste while preserving meaningful headroom.

The deployment phase matters just as much as the analysis phase. The operator did not merely edit Compose files and walk away. First, the system's stale swap debt was cleared with `swapoff -a && swapon -a`, which reset the baseline and made later observations easier to interpret. Then multiple services were recreated under lower limits. This is where many "optimization" efforts fail: they assume historical averages are sufficient. In reality, some services have sharp initialization spikes, cache-warm phases, or transient model loads that never show up in simple means. As soon as the revised Immich services started, both `immich-server` and `immich-machine-learning` landed around 89-90% utilization. That was the signal to reverse part of the cut and restore both to 768 MB.

This startup-validation loop is what makes the method robust. The goal is not minimum possible memory; it is minimum safe memory. If a container comes up already sitting in the red zone, the operator learns that the cap was shaped by the wrong statistic. In other words, right-sizing is not a single optimization pass but a control loop: observe historical pressure, choose a smaller envelope, restart, inspect immediate saturation, and revise. In the checkpoint, this prevented a superficially successful but brittle configuration from being treated as done.

The reason the method works is that it aligns operational decisions with how containerized services actually behave. Many homelab and small-production systems are over-allocated because limits are copied from examples, rounded up "just in case," or never revisited after the first deployment. Those oversized limits do not merely waste headroom; they also hide which services truly matter during a memory crunch. By compressing obviously inflated budgets and watching the services that flirt with saturation, the operator turns the host into a system with clearer priorities. The checkpoint's final state reflects that: waste-heavy services were pulled down, swap was reset, and only the services that proved they needed more memory got it.

## Key Properties

- **History-first diagnosis**: uses multi-day Prometheus and cAdvisor data to detect hidden pressure patterns such as sustained swap use and low `MemAvailable`, not just current usage.
- **Asymmetric resource logic**: can cut memory aggressively while leaving CPU mostly alone when telemetry shows memory pressure is the real bottleneck.
- **Startup-aware validation**: explicitly checks restarted containers for near-saturation behavior, catching cases where average usage understates initialization cost.
- **Iterative safety margin**: favors headroom above p95 and restart spikes rather than sizing directly to means.
- **Compose-native remediation**: the tuning lands in normal Docker Compose resource limits, so the result is durable and deployable.

## Limitations

This technique depends on having reliable telemetry. If Prometheus coverage is incomplete, restart storms polluted the time window, or cAdvisor labels are inconsistent, the resulting caps can be misleading. It also works better for services with reasonably stable behavior than for jobs with rare but legitimate extreme bursts. Startup validation helps, but it cannot predict every future workload change; a once-safe cap can become too small after a software update, new feature, or larger media/model corpus. Finally, reclaimed swap only improves observability if the operator continues measuring after the reset instead of assuming the system is fixed forever.

## Examples

A minimal decision loop looks like this:

```python
services = [
    {"name": "jellyfin", "steady_p95_mb": 620, "startup_peak_mb": 700},
    {"name": "immich-server", "steady_p95_mb": 420, "startup_peak_mb": 690},
]

for svc in services:
    target = max(int(svc["steady_p95_mb"] * 1.25), int(svc["startup_peak_mb"] * 1.10))
    print(svc["name"], "->", target, "MB")

# After redeploy:
# - if utilization > 0.85 immediately after start, raise the cap
# - if utilization remains comfortably low, keep the new value
```

The checkpoint's concrete examples were:

- `flaresolverr`: uncapped -> 512 MB
- `jellyfin`: 2 GB -> 768 MB
- `riven`: 2 GB -> 768 MB
- `opencode`: 2 GB -> 1.5 GB
- `immich-server`: 1 GB -> 512 MB -> 768 MB after restart validation
- `immich-machine-learning`: 1 GB -> 384 MB -> 768 MB after restart validation

## Practical Applications

This concept is useful anywhere a single host runs many mixed-priority containers: homelabs, edge boxes, small inference stacks, and developer platforms. It is especially valuable when operators are facing swap saturation, occasional OOMs, or a growing sprawl of "temporary" generous limits that were never revisited. The method also generalizes well to post-incident cleanup: after an OOM event, it provides a disciplined way to decide which services deserve more memory, which services can be tightened, and which services need follow-up observation instead of guesswork.

## Related Concepts

- **[[Docker Container Resource Auditing and Optimization]]** — the broader pattern of using observed usage to tune Compose limits; this concept narrows it to Prometheus-guided multi-day analysis plus immediate restart validation.
- **[[Comprehensive Grafana Monitoring for Docker Homelab Services]]** — supplies the host and container telemetry that makes right-sizing decisions evidence-based instead of anecdotal.
- **[[Out-of-Memory (OOM) Failure Diagnosis and Remediation in ML Containers]]** — overlaps in failure analysis, but focuses more on recovering from OOMs than on proactive right-sizing loops.

## Sources

- [[Copilot Session Checkpoint: Homelab memory optimization + BeddyByes ingest]] — primary source for the 7-day telemetry, swap reset, and restart-validation examples
