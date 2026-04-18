---
title: "Copilot Session Checkpoint: NBA-ML Agents and Homelab Fixes"
type: source
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "5d62c5ec9d154108bd891ed92b71cf061018b412b20cfcfc2b686c64b646c9e9"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-nba-ml-agents-and-homelab-fixes-646cf99a.md
quality_score: 100
concepts:
  - nba-ml-specialized-prediction-agents
  - sprint-workflow-integration-for-ai-agents
  - adguard-memory-oom-diagnosis-and-fix
related:
  - "[[NBA-ML Specialized Prediction Agents]]"
  - "[[Sprint Workflow Integration for AI Agents]]"
  - "[[AdGuard Memory Out-Of-Memory (OOM) Diagnosis and Fix]]"
  - "[[Copilot CLI]]"
  - "[[AdGuard]]"
  - "[[KnightCrawler]]"
tier: hot
tags: [mempalace, checkpoint, copilot-session, automation, labs-wiki, docker, homelab, durable-knowledge, agents, nba-ml, ai-agents, mlops, fileback, nba-ml-engine]
checkpoint_class: durable-debugging
retention_mode: retain
---

# Copilot Session Checkpoint: NBA-ML Agents and Homelab Fixes

## Summary

This session checkpoint documents a multi-repo project involving the development of specialized AI agents for the NBA-ML prediction engine, integration of these agents into sprint workflows, and operational fixes on a homelab server including an AdGuard memory issue and ongoing KnightCrawler troubleshooting. The work includes building four new prediction agents, enhancing sprint process automation, and diagnosing infrastructure problems to improve system reliability and prediction accuracy.

## Key Points

- Built and validated four specialized Copilot CLI agents for the NBA-ML engine to improve prediction hit rates and calibration.
- Integrated agents into the sprint workflow, identifying five gaps in agent routing, data quality gating, backtesting, monitoring, and feedback capture.
- Diagnosed and fixed an out-of-memory (OOM) issue with AdGuard on the homelab server by increasing its memory allocation.
- Began diagnosing a KnightCrawler issue related to missing streaming results for a specific TV episode, with container health verified and database queries in progress.

## Concepts Extracted

- **[[NBA-ML Specialized Prediction Agents]]** — A set of four specialized AI agents developed to enhance the NBA-ML engine's prediction accuracy and operational robustness. These agents focus on model calibration, feature engineering, data quality validation, and backtesting performance to systematically improve the predictive pipeline.
- **[[Sprint Workflow Integration for AI Agents]]** — A structured 10-step sprint execution workflow designed to incorporate multiple AI agents into the software development lifecycle for machine learning projects. This integration aims to automate quality assurance, testing, deployment, and feedback capture phases to improve development efficiency and model reliability.
- **[[AdGuard Memory Out-Of-Memory (OOM) Diagnosis and Fix]]** — Diagnosis and remediation of an out-of-memory (OOM) crash in the AdGuard container running on a homelab server. The issue was caused by filter update spikes exceeding the container's memory limit, leading to process termination by the kernel.

## Entities Mentioned

- **NBA-ML Engine** — A large-scale Python-based machine learning platform for NBA fantasy basketball prediction, featuring multiple model architectures including XGBoost, LightGBM, Random Forest, Ridge regression, LSTM, and stacking ensembles. It uses over 326 features including advanced and contextual statistics to predict 9 categories of fantasy stats with ongoing efforts to improve calibration and hit rates.
- **[[Copilot CLI]]** — A command-line interface tool that supports context-loaded AI agents as personas to assist in software development and operational tasks. It enables running agent playbooks, executing commands, and integrating AI workflows into development pipelines.
- **[[AdGuard]]** — A network-level ad and tracker blocking service running as a Docker container in the homelab environment. It manages large filter lists to block unwanted content and DNS queries, configured with resource limits and restart policies to maintain uptime.
- **[[KnightCrawler]]** — A multi-container infrastructure system managing torrent and streaming metadata, including database services and cron jobs for populating and scraping data. It supports media streaming applications and uses PostgreSQL, Redis, and message queues for data management.

## Notable Quotes

> "Explored: model architecture (XGBoost/LightGBM/RF/Ridge/LSTM/Stacking), 326 features, 9-cat fantasy stats, Sprint 47 audit findings" — Session History
> "Recommended hybrid approach: automate playbook commands via Ofelia/cron, alert on failure via ntfy, invoke agent only for reasoning" — Session History
> "Root cause: memory limit 256MB in compose.infra.yml, but filter update (330K→421K rules, 9.7MB file) exceeded limit" — Session History

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-nba-ml-agents-and-homelab-fixes-646cf99a.md` |
| Type | note |
| Author | Unknown |
| Date | 2026-04-18T03:23:51.483387Z |
| URL | N/A |
