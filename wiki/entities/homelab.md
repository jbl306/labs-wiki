---
title: "Homelab"
type: entity
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "3a38e39284cc0602ec33af8d22ef0dfb3c2a3a21b23b03f06716e3221ca8b49e"
sources:
  - raw/2026-04-20-copilot-session-second-curation-reports-23bcd48f.md
  - raw/2026-04-20-copilot-session-scheduler-dns-agents-cleanup-2222559c.md
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-sprint-11-evaluation-and-report-5b560f0f.md
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-reworking-docs-for-copilot-opencode-4710bc64.md
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-retrained-models-deploying-improvements-59ba9a6c.md
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-building-4-copilot-cli-custom-agents-4d3f83bc.md
quality_score: 100
concepts:
  - homelab
related:
  - "[[Custom Copilot CLI Agents]]"
  - "[[Copilot Session Checkpoint: Building 4 Copilot CLI Custom Agents]]"
  - "[[AutoAgent]]"
  - "[[Copilot CLI]]"
  - "[[MemPalace]]"
tier: hot
tags: [infrastructure, docker-compose, monitoring, automation]
---

# Homelab

## Overview

Homelab is a multi-service infrastructure environment managed with Docker Compose stacks and monitored via Prometheus, Grafana, cAdvisor, and node-exporter. It hosts 13 compose stacks and uses scripts and agents for operations and deployment automation.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Infrastructure |
| Created | Unknown |
| Creator | Unknown |
| URL | N/A |
| Status | Active |

## Relevance

The homelab environment is the target for two custom agents: the homelab-ops agent managing infrastructure operations and the devops-deploy agent handling deployment workflows, demonstrating practical automation of complex infrastructure.

## Associated Concepts

- **[[Custom Copilot CLI Agents]]** — hosts homelab-ops and devops-deploy agents

## Related Entities

- **[[AutoAgent]]** — co-mentioned in source (Framework)
- **[[Copilot CLI]]** — co-mentioned in source (Tool)
- **[[MemPalace]]** — co-mentioned in source (Framework)
- **NBA-ML Engine** — co-mentioned in source (Infrastructure)

## Sources

- [[Copilot Session Checkpoint: Building 4 Copilot CLI Custom Agents]] — where this entity was mentioned
- [[Copilot Session Checkpoint: Retrained Models, Deploying Improvements]] — additional source
- [[Copilot Session Checkpoint: Reworking Docs for Copilot/OpenCode]] — additional source
- [[Copilot Session Checkpoint: Sprint 11 Evaluation and Report]] — additional source
- [[Copilot Session Checkpoint: Scheduler DNS Agents Cleanup]] — additional source
- [[Copilot Session Checkpoint: Second Curation Reports]] — additional source
