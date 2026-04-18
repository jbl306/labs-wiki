---
title: "Registry Health Snapshot Tracking and Dashboard Integration"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "8e3ec5b24e92a02a9a1b03fb00f1bdd35fbc8dbe8d7723b1a284751ce576ff29"
sources:
  - raw/2026-04-18-copilot-session-sprint-59-shap-coverage-implementation-9a231f70.md
quality_score: 100
concepts:
  - registry-health-snapshot-tracking-and-dashboard-integration
related:
  - "[[Artifact Registry Validation In ML Pipelines]]"
  - "[[Copilot Session Checkpoint: Sprint 59 SHAP Coverage Implementation]]"
tier: hot
tags: [registry-health, dashboard, snapshot, nba-ml-engine]
---

# Registry Health Snapshot Tracking and Dashboard Integration

## Overview

Registry health snapshot tracking introduces a persistent record of model registry status, enabling monitoring and alerting via dashboard UI. Sprint 59 adds a new database table, API endpoint, and React badge component to surface registry health in real time.

## How It Works

Model registries track the status and availability of production artifacts, ensuring that deployed models are discoverable and up-to-date. Sprint 59 introduces a new table, `registry_health_snapshots`, to persist health checks. Each snapshot includes an ID, timestamp (`checked_at`), status, missing artifact count, and detailed JSON describing missing items.

The implementation involves an Alembic migration to create the table, an ORM model in `src/db/models.py`, and logic in `main.py` to write a snapshot row during registry health checks. The CLI command `registry-health` now records the outcome of each run, storing both summary and detailed information.

A new API endpoint (`/api/registry-health`) is added to the dashboard backend (`dashboard-ui/server/src/index.ts`). This endpoint retrieves the latest snapshot, falling back to a live check if the snapshot is older than 30 hours. Error handling ensures that database rollbacks occur on failure, maintaining consistency.

On the frontend, a React badge component displays registry health status, polling the API at a 5-minute interval. The badge provides a visual indicator of missing artifacts or registry issues, supporting rapid response and operational transparency.

Edge cases include stale snapshots, API failures, or database errors. The fallback logic ensures that health checks remain accurate even if snapshots are outdated or missing.

## Key Properties

- **Persistent Health Tracking:** Records registry health over time, enabling historical analysis and alerting.
- **API and UI Integration:** Surfaces registry status via dashboard endpoint and React badge, supporting operational visibility.
- **Fallback Logic:** Ensures live health checks are performed if snapshots are stale, maintaining accuracy.

## Limitations

Snapshot tracking depends on regular health check runs; missed or delayed runs can result in stale status. API and UI components must handle errors gracefully to avoid false negatives. The snapshot does not capture all registry nuances, such as artifact version mismatches or partial failures.

## Example

```python
# ORM model
class RegistryHealthSnapshot(Base):
    __tablename__ = 'registry_health_snapshots'
    id = Column(Integer, primary_key=True)
    checked_at = Column(DateTime(timezone=True))
    status = Column(String(20))
    missing_count = Column(Integer)
    details = Column(JSONB)

# Writing a snapshot
missing = find_missing_production_artifacts(session)
snapshot = RegistryHealthSnapshot(
    checked_at=datetime.utcnow(),
    status='ok' if not missing else 'missing',
    missing_count=len(missing),
    details=serialize_missing(missing)
)
session.add(snapshot)
session.commit()
```

## Visual

No images or UI screenshots included; the badge component and API endpoint are described in text.

## Relationship to Other Concepts

- **[[Artifact Registry Validation In ML Pipelines]]** — Registry health snapshot tracking builds upon artifact validation concepts for production reliability.

## Practical Applications

Registry health tracking is critical for production ML systems, enabling proactive monitoring, alerting, and troubleshooting. It supports operational dashboards, compliance reporting, and automated recovery workflows.

## Sources

- [[Copilot Session Checkpoint: Sprint 59 SHAP Coverage Implementation]] — primary source for this concept
