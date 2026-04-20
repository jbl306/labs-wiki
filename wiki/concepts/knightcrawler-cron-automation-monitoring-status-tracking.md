---
title: "Knightcrawler Cron Automation Monitoring and Status Tracking"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "9087cb7649f7304dd2917525af12c2fd1f436fd5b0eb12bcf0b6c9787bb8f3f4"
sources:
  - raw/2026-04-18-copilot-session-knightcrawler-done-routing-traced-7bbbddcd.md
quality_score: 100
concepts:
  - knightcrawler-cron-automation-monitoring-status-tracking
related:
  - "[[Durable Copilot Session Checkpoint Promotion]]"
  - "[[Copilot Session Checkpoint: Knightcrawler done, routing traced]]"
tier: hot
tags: [monitoring, automation, cron, homelab, status-tracking, dashboard]
---

# Knightcrawler Cron Automation Monitoring and Status Tracking

## Overview

A robust, database-backed monitoring and status tracking system for Knightcrawler's cron-driven automation, enabling precise visibility into job outcomes, error classification, and operational health. This system replaces brittle log scraping with structured status persistence and exposes real-time metrics for dashboard integration.

## How It Works

The Knightcrawler cron automation monitoring system is designed to provide reliable, granular insight into the health and results of scheduled jobs that drive content ingestion and mapping for the Knightcrawler/Stremio addon. The core mechanism involves instrumenting the main cron scripts (`kc-populate-files.sh` and `kc-scrape-recent.sh`) to report their execution status, outcome classification, and key metrics into a dedicated Postgres table (`automation_job_status`).

A shared shell helper (`kc-status.sh`) is sourced by both cron scripts. This helper ensures the `automation_job_status` table exists (creating it lazily if needed) and provides functions to upsert status records keyed by job name. Each job invocation records timestamps for start, finish, and last success, as well as counters for rows inserted, pass/fail counts, and detailed outcome breakdowns (e.g., imported, no_streams, no_episodes, errors).

For example, `kc-populate-files.sh` writes its run status and inserted row counts at the end of each execution, while `kc-scrape-recent.sh` classifies each processed title and tallies how many were actually imported versus skipped due to missing streams or episodes. This explicit classification addresses a prior bug where all zero-exit helper calls were counted as imports, even when nothing was actually added.

The monitoring system is tightly integrated with the Homepage dashboard via a custom FastAPI exporter (`homepage-db-stats/app.py`). This exporter exposes a `/metrics/knightcrawler-automation` endpoint that summarizes job freshness, current-year coverage, and last known status for each automation job. The dashboard card is configured to display these metrics, providing at-a-glance operational health and surfacing actionable signals (e.g., stale jobs, missing titles, recent errors).

By persisting job status in the database (rather than relying on ephemeral logs or host mounts), the system is resilient to container restarts, network boundaries, and deployment changes. It also enables historical analysis, alerting, and future extensibility (e.g., tracking additional job types or integrating with external monitoring systems).

## Key Properties

- **Database-Backed Status Tracking:** All automation job outcomes are persisted in the Knightcrawler Postgres database, ensuring durability and cross-container visibility.
- **Granular Outcome Classification:** Jobs explicitly classify outcomes (imported, no_streams, no_episodes, errors), avoiding misleading success reporting.
- **Dashboard Integration:** Metrics are exposed via a FastAPI exporter endpoint and surfaced in the Homepage dashboard for real-time monitoring.
- **Resilience to Deployment Boundaries:** Status tracking does not depend on host log scraping or mounts, making it robust to Docker network and container changes.

## Limitations

The system depends on the correct operation of the `kc-status.sh` helper and the availability of the Postgres database. If the database is unavailable, status updates may fail silently. Additionally, the approach assumes that all relevant scripts are instrumented to report status; untracked scripts or manual interventions may not be reflected. The classification logic must be maintained as job logic evolves to avoid drift between actual outcomes and reported metrics.

## Example

Suppose `kc-scrape-recent.sh` runs and processes 100 titles. Of these, 60 are imported, 30 are skipped due to 'no streams', and 10 due to 'no episodes'. The script writes: 

```sql
INSERT INTO automation_job_status (job_name, last_status, imported_count, no_streams_count, no_episodes_count, error_count, last_started_at, last_finished_at, last_success_at)
VALUES ('kc-scrape-recent', 'OK', 60, 30, 10, 0, now(), now(), now())
ON CONFLICT (job_name) DO UPDATE ...;
```
The Homepage dashboard then displays: 'Scrape Status: OK 2m ago, Imported: 60, No Streams: 30, No Episodes: 10'.

## Visual

No diagrams or images are included in the source; all information is text-based.

## Relationship to Other Concepts

- **[[Durable Copilot Session Checkpoint Promotion]]** — This monitoring system is a concrete implementation promoted via durable Copilot checkpoints.

## Practical Applications

This approach is valuable for any homelab or production environment where cron-driven automations must be monitored reliably, especially in containerized or distributed setups. It enables operators to quickly detect and diagnose failures, track job freshness, and ensure that critical content ingestion or processing tasks are running as expected. The pattern is generalizable to other automation domains, such as data pipelines, backup jobs, or periodic ETL processes.

## Sources

- [[Copilot Session Checkpoint: Knightcrawler done, routing traced]] — primary source for this concept
