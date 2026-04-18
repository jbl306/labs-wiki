---
title: "Homelab Server Deployment Architecture for NBA ML Platform"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "9f90b86f2aab32a86e7ca650c6477398444e04958726c5b3ca2ccd9f465e7581"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-retrained-models-deploying-improvements-59ba9a6c.md
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-data-source-expansion-exploration-b12f747f.md
quality_score: 100
concepts:
  - homelab-server-deployment-nba-ml-platform
related:
  - "[[Docker]]"
  - "[[Copilot Session Checkpoint: Data Source Expansion Exploration]]"
tier: hot
tags: [homelab, docker, deployment, scheduling, mlops]
---

# Homelab Server Deployment Architecture for NBA ML Platform

## Overview

The NBA ML prediction platform is deployed on a homelab server using Docker containers to encapsulate all components. This architecture supports local development, deployment, and scheduled execution of data pipelines and model training in an isolated environment.

## How It Works

The homelab deployment architecture consists of multiple Docker containers orchestrated via Docker Compose with environment variables managed through an `.env` file. Key components include:

- **nba-ml-db:** A TimescaleDB instance for time-series optimized storage of basketball data.
- **nba-ml-mlflow:** MLflow tracking server to manage model experiments and registry.
- **nba-ml-api:** FastAPI service handling data ingestion, model training, and prediction APIs.
- **nba-ml-dashboard:** Streamlit-based dashboard for visualization and monitoring.
- **nba-ml-scheduler:** Ofelia cron scheduler running scheduled jobs such as daily data ingestion and model retraining.

The deployment process involves:

1. Building Docker images with updated code.
2. Running database migrations using Alembic to update schema with new tables and columns.
3. Starting containers with `docker compose --env-file .env -f compose/compose.nba-ml.yml up -d`.
4. Scheduling cron jobs for pipeline execution at 3 AM ET (08:00 UTC) with staggered timings for different pipeline stages.

The architecture supports:

- Local development without SSH by running all services on the homelab server.
- Isolation of dependencies and environment consistency via containers.
- Scalability by adding or updating containers independently.
- Robust scheduling and monitoring of pipelines.

This setup enables efficient iterative development and deployment cycles for the NBA ML platform.

## Key Properties

- **Containerization:** All components run in Docker containers ensuring environment consistency and isolation.
- **Orchestration:** Docker Compose manages multi-container orchestration with environment variables loaded from a centralized `.env` file.
- **Scheduling:** Ofelia cron scheduler runs pipeline jobs with precise timing using a 6-field cron format including seconds.
- **Database:** TimescaleDB provides time-series optimized storage for large volumes of basketball game and player data.
- **Deployment Commands:** Deployment requires running `docker compose` commands from the homelab directory with proper environment variable loading.

## Limitations

Running all services on a single homelab server may limit scalability and fault tolerance compared to cloud deployments. Resource constraints could cause out-of-memory errors during model training or data ingestion. The setup requires careful environment management, such as ensuring the `.env` file is loaded correctly to prevent database crashes. Cron jobs must be carefully scheduled to avoid overlapping resource usage. Native library dependencies (e.g., LightGBM's libgomp.so.1) may cause failures if not properly containerized.

## Example

Docker Compose snippet for scheduling pipeline jobs:

```yaml
services:
  nba-ml-scheduler:
    image: nba-ml-scheduler:latest
    command: ofelia daemon
    volumes:
      - ./ofelia_jobs:/etc/ofelia/jobs
    environment:
      - ENV_VAR=value

# ofelia_jobs/pipeline.job
schedule: '0 0 8 * * *'
command: python main.py pipeline
```

This schedules the main pipeline to run daily at 08:00 UTC (3 AM ET).

## Relationship to Other Concepts

- **[[Docker]]** — Docker is the container platform used to package and run the NBA ML platform services.
- **Scheduled Pipeline Execution** — Ofelia cron jobs in the homelab deployment schedule data ingestion and model retraining pipelines.

## Practical Applications

This architecture is suitable for small to medium scale ML projects requiring reproducible environments and controlled scheduling without cloud dependencies. It enables rapid iteration and testing on local hardware with full-stack orchestration.

## Sources

- [[Copilot Session Checkpoint: Data Source Expansion Exploration]] — primary source for this concept
- [[Copilot Session Checkpoint: Retrained Models, Deploying Improvements]] — additional source
