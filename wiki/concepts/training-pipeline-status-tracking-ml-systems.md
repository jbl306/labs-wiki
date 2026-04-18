---
title: "Training Pipeline Status Tracking in ML Systems"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "5696101c1ddba558560149a708018979e6d8425067b82872f36a6d08784426d9"
sources:
  - raw/2026-04-18-copilot-session-training-status-tracker-and-oom-fix-6c60a486.md
quality_score: 100
concepts:
  - training-pipeline-status-tracking-ml-systems
related:
  - "[[Registry Health Snapshot Tracking and Dashboard Integration]]"
  - "[[Atomic Model Artifact Saving in ML Training Loops]]"
  - "[[Copilot Session Checkpoint: Training Status Tracker and OOM Fix]]"
tier: hot
tags: [ml-ops, pipeline-monitoring, dashboard-integration, atomic-writes]
---

# Training Pipeline Status Tracking in ML Systems

## Overview

Training pipeline status tracking is a mechanism for monitoring and reporting the progress, state, and health of multi-stage machine learning workflows. It enables real-time visibility into which stages are running, completed, or failed, and integrates with dashboards or APIs for operational transparency. This concept is critical for robust ML operations, especially in production environments with long-running or resource-intensive jobs.

## How It Works

The training pipeline status tracker operates by instrumenting key points in the ML workflow codebase, specifically at the start, advancement, completion, and failure of each pipeline stage. In the NBA ML engine described, the tracker is implemented as a Python module (`status.py`) that provides functions such as `start_pipeline()`, `advance_stage()`, `complete_stage()`, and `finish_pipeline()`. These functions update a status object representing the current pipeline state.

To ensure durability and atomicity, the tracker writes the status object as a JSON file to `/tmp/training_status.json`. Atomicity is achieved by writing to a temporary file and then using `os.replace()` to swap it in place, preventing partial writes or corruption if the process is interrupted. This design is resilient to most failures except abrupt process termination (e.g., OOM kills), which can leave the status file in a stale state.

The status tracker is tightly integrated with the training orchestration logic. Hooks are added to the main training functions (`train_pipeline()` and `train_all()`) so that each stage's progress is reflected in the status file. For example, when a stage starts, `advance_stage()` is called; upon completion, `complete_stage()` updates the tracker. If an exception occurs, `finish_pipeline(error=...)` records the error and marks the pipeline as failed.

A public API endpoint (`/training/status`) is exposed via the FastAPI server, reading the status file and enriching it with metadata such as the last training date from the model registry. The endpoint returns pre-formatted fields for dashboard consumption, including `status_label` (e.g., 'Training', 'Idle', 'Failed'), `stage_display` (e.g., '5/12'), `stage_name`, `elapsed_minutes`, and `last_trained`. This allows external systems (like the homepage dashboard) to poll the status and display real-time progress.

The tracker is designed for operational transparency and ease of integration. The homepage dashboard uses a custom API widget to display the pipeline status, refreshing every 30 seconds. The tracker also supports idle and error states, enabling operators to quickly diagnose issues or confirm completion. However, its limitations include stale states if the process is killed before cleanup, and the need for manual intervention to clear or reset the status file in such cases.

Edge cases and trade-offs include handling abrupt failures (OOM kills), ensuring atomic writes, and balancing the granularity of status updates with performance. The tracker is lightweight (90 lines of code) and does not introduce significant overhead, but must be carefully managed in environments with frequent restarts or memory pressure.

## Key Properties

- **Atomic File Writes:** Status updates are written atomically to prevent partial or corrupted files, using temporary files and os.replace().
- **Real-Time Stage Tracking:** Tracks progress across all pipeline stages, including start, advancement, completion, and error states.
- **API Integration:** Exposes a public API endpoint for external dashboard consumption, returning pre-formatted status fields.
- **Resilience to Most Failures:** Handles normal errors gracefully, but can leave stale status if killed abruptly (e.g., OOM).

## Limitations

If the training process is killed abruptly (e.g., OOM), the status file may show a stale 'running: true' state, requiring manual cleanup. The tracker does not persist across container restarts unless explicitly reset. It relies on accurate hooks in the training code; missing or misordered calls can result in incorrect status reporting.

## Example

```python
# Example usage in trainer.py
from status import advance_stage, complete_stage

for i, stat in enumerate(stats):
    advance_stage(stage_name=f'Stat: {stat}', stage_num=i+1)
    train_stat_model(stat)
    complete_stage(stage_name=f'Stat: {stat}', stage_num=i+1)
```

## Visual

No diagrams or charts are included in the source. The dashboard card displays the status as text fields (e.g., 'Training · 1/12 · Minutes Model').

## Relationship to Other Concepts

- **[[Registry Health Snapshot Tracking and Dashboard Integration]]** — Both concepts involve real-time status monitoring and dashboard integration for operational transparency.
- **[[Atomic Model Artifact Saving in ML Training Loops]]** — Both use atomic file operations to ensure durability and consistency during ML pipeline execution.

## Practical Applications

Used in production ML pipelines to provide operators and stakeholders with real-time visibility into training progress, detect failures early, and support automated dashboards. Particularly valuable in environments with long-running jobs, resource constraints, or complex multi-stage workflows.

## Sources

- [[Copilot Session Checkpoint: Training Status Tracker and OOM Fix]] — primary source for this concept
