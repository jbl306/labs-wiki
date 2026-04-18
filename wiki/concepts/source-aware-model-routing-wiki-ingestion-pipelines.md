---
title: "Source-Aware Model Routing in Wiki Ingestion Pipelines"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "c65fce884e028922d59862433952d95e905dc7bcd8639c99bbaa0493de3d3fbb"
sources:
  - raw/2026-04-18-copilot-session-session-wiki-promotion-405414ae.md
quality_score: 100
concepts:
  - source-aware-model-routing-wiki-ingestion-pipelines
related:
  - "[[Durable Copilot Session Checkpoint Promotion]]"
  - "[[Karpathy Compile-Once Wiki Principle]]"
  - "[[Copilot Session Checkpoint: Session Wiki Promotion]]"
tier: hot
tags: [model-routing, wiki-ingestion, efficiency, priority-queueing, copilot, github-models]
---

# Source-Aware Model Routing in Wiki Ingestion Pipelines

## Overview

Source-aware model routing is a technique for dynamically assigning incoming raw knowledge sources to specialized model lanes during wiki ingestion. By classifying sources (e.g., Copilot session checkpoints, MemPalace exports, standard text, images), the system optimizes compile-time efficiency and ensures appropriate model selection and resource allocation.

## How It Works

The ingestion pipeline begins with a route classifier, implemented in scripts such as `auto_ingest.py` and `watch_raw.py`. This classifier examines each incoming raw file, infers its source class (e.g., copilot-session-checkpoint, mempalace-export, image-bearing), and assigns it to a model lane ('light', 'default', 'vision').

Each lane is configured with specific model environment variables (e.g., `GITHUB_MODELS_MODEL_LIGHT`, `GITHUB_MODELS_MODEL_VISION`), character limits (`max_source_chars`), and processing priorities. For example, Copilot session checkpoints are routed to the 'light' lane with a priority of 30 and a character cap of 18,000, while vision sources are routed to the 'vision' lane with a higher cap. The classifier logs the chosen route and ensures that interactive sources are processed ahead of backlog.

The pipeline maintains an inflight set to suppress duplicate concurrent processing, ensuring that repeated inotify events do not trigger redundant compilation. Pending work is sorted by route priority, so urgent or interactive sources are ingested before session backlog or low-priority exports.

Model selection is flexible: if dedicated environment variables are not set, the system falls back to a default model (e.g., `gpt-4.1`). This allows for future upgrades or specialization as new models become available. The routing logic is observable, with logs and metrics tracking route assignment, processing order, and compile events.

This approach supports efficient compile-time ingestion, minimizes unnecessary model calls, and aligns with the principle that only the compile step should invoke external models. It also enables robust handling of diverse source types, ensuring that each is processed with the appropriate resources and constraints.

## Key Properties

- **Dynamic Source Classification:** Incoming raw files are classified by source type and assigned to specialized model lanes, optimizing resource usage and processing order.
- **Priority Queueing:** Pending work is sorted by route priority, ensuring that interactive or urgent sources are processed before backlog.
- **Inflight Suppression:** An in-memory inflight set prevents duplicate concurrent processing, improving robustness and efficiency.
- **Flexible Model Selection:** Model lanes are configurable via environment variables, with fallback to default models if not specified.

## Limitations

The effectiveness of routing depends on accurate source classification; misclassified sources may be processed inefficiently or with inappropriate models. If environment variables are misconfigured or missing, the system may fall back to less optimal models. The approach assumes that source types are well-defined and that lane-specific caps and priorities are appropriate for all use cases.

## Example

Example routing logic:

```python
route = classify_ingest_route(raw_file)
if route.lane == 'light':
    model = os.environ.get('GITHUB_MODELS_MODEL_LIGHT', 'gpt-4.1')
    max_chars = 18000
elif route.lane == 'vision':
    model = os.environ.get('GITHUB_MODELS_MODEL_VISION', 'gpt-4.1')
    max_chars = 24000
else:
    model = os.environ.get('GITHUB_MODELS_MODEL_DEFAULT', 'gpt-4.1')
    max_chars = 20000
```

Pending files are sorted by `route.priority` before processing.

## Visual

No diagrams or charts are present in the source.

## Relationship to Other Concepts

- **[[Durable Copilot Session Checkpoint Promotion]]** — Source-aware routing is central to efficient promotion and compilation of session checkpoints.
- **[[Karpathy Compile-Once Wiki Principle]]** — Routing ensures compile-once ingestion aligns with model boundaries and resource constraints.

## Practical Applications

Source-aware routing is applicable in any wiki or knowledge management system that ingests diverse sources and needs to optimize compile-time efficiency. It is especially valuable in environments with strict model boundaries (e.g., Copilot Pro+ / GitHub Models-only), supporting robust, scalable, and efficient knowledge compilation.

## Sources

- [[Copilot Session Checkpoint: Session Wiki Promotion]] — primary source for this concept
