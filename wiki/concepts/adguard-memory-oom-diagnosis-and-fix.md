---
title: "AdGuard Memory Out-Of-Memory (OOM) Diagnosis and Fix"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "5d62c5ec9d154108bd891ed92b71cf061018b412b20cfcfc2b686c64b646c9e9"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-nba-ml-agents-and-homelab-fixes-646cf99a.md
quality_score: 100
concepts:
  - adguard-memory-oom-diagnosis-and-fix
related:
  - "[[Container Resource Tuning And Performance Remediation]]"
  - "[[Homelab Service Inventory And Dashboard Synchronization]]"
  - "[[Copilot Session Checkpoint: NBA-ML Agents and Homelab Fixes]]"
tier: hot
tags: [adguard, oom, container-memory, docker, homelab]
---

# AdGuard Memory Out-Of-Memory (OOM) Diagnosis and Fix

## Overview

Diagnosis and remediation of an out-of-memory (OOM) crash in the AdGuard container running on a homelab server. The issue was caused by filter update spikes exceeding the container's memory limit, leading to process termination by the kernel.

## How It Works

AdGuard runs as a Docker container with a memory limit set in the `compose.infra.yml` configuration file. During a filter update, the number of filtering rules increased from 330,000 to 421,000, resulting in a 9.7MB filter file. This spike caused the container to exceed its 256MB memory limit, triggering an OOM kill by the Linux kernel.

The diagnosis involved:

- Checking container status and logs for errors.
- Inspecting system dmesg logs to confirm OOM kill events.
- Reviewing memory usage and swap status on the host machine.

The fix involved increasing the memory limit for the AdGuard container from 256MB to 512MB in the Docker Compose infrastructure YAML file. After redeployment, the container ran stably with the increased memory allocation, and DNS resolution was verified to be functional.

This approach balances resource allocation with system stability, ensuring AdGuard can handle large filter updates without crashing.

## Key Properties

- **Memory Limit:** Initial limit 256MB, increased to 512MB to accommodate filter update spikes.
- **Filter Size:** Filter rules increased from 330K to 421K, with a 9.7MB file size.
- **System Resources:** Host has 31GB RAM, 10GB used, swap nearly full at 7.9/8.0GB.
- **Container Restart Policy:** Configured as 'restart: unless-stopped' to maintain uptime.

## Limitations

Memory increase is a reactive fix; underlying filter growth may continue, requiring monitoring. Swap near full indicates potential host memory pressure, which could affect other services. The fix does not address root causes of filter size growth or optimize filter processing efficiency.

## Example

To fix the OOM issue, edit `compose/compose.infra.yml`:

```yaml
services:
  adguard:
    mem_limit: 512M  # increased from 256M
```

Then redeploy:

```bash
docker compose up -d adguard
```

Verify container memory limit and DNS functionality after restart.

## Relationship to Other Concepts

- **[[Container Resource Tuning And Performance Remediation]]** — Memory tuning is a key remediation strategy for container stability.
- **[[Homelab Service Inventory And Dashboard Synchronization]]** — Monitoring container health is part of homelab service management.

## Practical Applications

Ensures reliable operation of DNS filtering services in homelab or production environments by preventing memory-related crashes during filter updates. Applicable to containerized network services with dynamic resource demands.

## Sources

- [[Copilot Session Checkpoint: NBA-ML Agents and Homelab Fixes]] — primary source for this concept
