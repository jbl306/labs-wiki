---
title: "Copilot Session Checkpoint: Scheduler DNS Agents Cleanup"
type: source
created: 2026-04-20
last_verified: 2026-04-20
source_hash: "8d4ffe804f00fc1786f05b552df93998c7e6bf7f3b353158464961c4edb4f8a3"
sources:
  - raw/2026-04-20-copilot-session-scheduler-dns-agents-cleanup-2222559c.md
quality_score: 100
concepts:
  - stale-training-status-detection-remediation-ml-pipelines
  - split-dns-routing-cloudflare-tunnel-overrides-homelab-services
  - agent-skill-surface-optimization-multi-tool-ai-project-compatibility
related:
  - "[[Stale Training Status Detection and Remediation in ML Pipelines]]"
  - "[[Split-DNS Routing and Cloudflare Tunnel Overrides for Homelab Services]]"
  - "[[Agent and Skill Surface Optimization for Multi-Tool AI Project Compatibility]]"
  - "[[NBA ML Engine]]"
  - "[[Homelab]]"
  - "[[Ofelia Scheduler]]"
  - "[[AdGuard]]"
tier: hot
tags: [mempalace, checkpoint, agents, dashboard, nba-ml-engine, ml-pipeline, scheduler, homelab, fileback, dns, durable-knowledge, debugging, surface-optimization, ai-agent, copilot-session]
checkpoint_class: durable-debugging
retention_mode: retain
knowledge_state: validated
---

# Copilot Session Checkpoint: Scheduler DNS Agents Cleanup

## Summary

This durable Copilot session checkpoint documents a systematic debugging and optimization workflow across the NBA ML Engine and homelab infrastructure. The session tackled a false training state bug, DNS routing issues for Immich, Ofelia scheduler job timing, and extensive agent/skill surface optimization for compatibility with VS Code, GitHub Copilot, Copilot CLI, and OpenCode. Branch cleanup was initiated but not completed at compaction.

## Key Points

- Diagnosed and fixed stale NBA ML training status bug caused by dead pipeline runs.
- Resolved LAN/public DNS routing for Immich by updating AdGuard rewrites and Cloudflare tunnel documentation.
- Moved Ofelia scheduler props-refresh job to 4 PM EDT and optimized agent/skill surfaces for multi-tool compatibility.
- Executed code review, fixed skill/symlink drift, and merged feature branches; branch cleanup inventory gathered but not executed.

## Concepts Extracted

- **[[Stale Training Status Detection and Remediation in ML Pipelines]]** — Stale training status detection is a mechanism for identifying and correcting false 'running' states in machine learning pipelines, especially when jobs are killed or crash unexpectedly. This is crucial for maintaining accurate UI and API reporting, preventing misleading pipeline states, and ensuring robust retrain scheduling.
- **[[Split-DNS Routing and Cloudflare Tunnel Overrides for Homelab Services]]** — Split-DNS routing is a strategy for differentiating DNS answers between LAN and public access, enabling secure HTTPS routing for homelab services. Cloudflare tunnel overrides are used to ensure TLS-sensitive services resolve to public IPs even on LAN, preventing certificate errors and routing failures.
- **[[Agent and Skill Surface Optimization for Multi-Tool AI Project Compatibility]]** — Agent and skill surface optimization is the process of structuring and exposing project-specific skills and agents for seamless integration with AI tools like VS Code, GitHub Copilot, Copilot CLI, and OpenCode. This enables consistent, discoverable workflows and robust compatibility across development environments.

## Entities Mentioned

- **[[NBA ML Engine]]** — NBA ML Engine is a machine learning platform focused on NBA data modeling, prediction, and pipeline orchestration. It includes training, calibration, backtesting, and dashboard workflows, and is integrated with agent/skill surfaces for VS Code, GitHub Copilot, Copilot CLI, and OpenCode.
- **[[Homelab]]** — Homelab is the infrastructure stack supporting NBA ML Engine and other services, including DNS routing, Cloudflare tunnel integration, and Ofelia scheduler orchestration. It manages LAN/public access, service deployment, and configuration.
- **[[Ofelia Scheduler]]** — Ofelia Scheduler is a cron-based job orchestration tool used in the homelab stack to schedule and execute recurring tasks, such as NBA ML Engine pipeline refreshes and data ingest jobs. It supports 6-field cron syntax and integrates with Docker containers.
- **[[AdGuard]]** — AdGuard is a DNS and network filtering tool used in the homelab stack to manage LAN DNS answers, including split-DNS routing and exact-host overrides for Cloudflare tunnel integration. It maintains the source-of-truth for DNS rewrites.

## Notable Quotes

> "The fix was to normalize status in src/training/status.py: add PID tracking, add stale/dead-run detection, mark dead/stale runs as failed/non-running, persist corrected status." — Session technical details
> "Decision: .github/skills/ is the canonical project skill layer. .opencode/skills/ mirrors the same skill set for OpenCode." — Agent/skill surface optimization

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-20-copilot-session-scheduler-dns-agents-cleanup-2222559c.md` |
| Type | note |
| Author | Unknown |
| Date | 2026-04-20T00:21:48.353093Z |
| URL | N/A |
