---
title: "Validation-Run Policy for Audit-Log Suppression"
type: concept
created: 2026-04-20
last_verified: 2026-04-20
source_hash: "e5b02c64f03eff41baf89ddea2376fb47d6f03914f6c1c7d77afb1833f4012b2"
sources:
  - raw/2026-04-20-copilot-session-url-followup-pass-b53bba3e.md
quality_score: 100
concepts:
  - validation-run-policy-audit-log-suppression
related:
  - "[[Content-Root Selection for Article Extraction]]"
  - "[[Image Ranking and Extraction for Article Content]]"
  - "[[Copilot Session Checkpoint: URL Followup Pass]]"
tier: hot
tags: [validation, audit-log, wiki-ingestion, workflow]
---

# Validation-Run Policy for Audit-Log Suppression

## Overview

The validation-run policy is a mechanism for suppressing audit-log noise and notifications during targeted refresh-only validation reruns. It enables manual and batch validation flows that update raw snapshots and wiki pages without triggering failure notifications, supporting clean review cycles in durable wiki pipelines.

## How It Works

The validation-run policy was introduced to address the need for silent, targeted validation reruns in wiki ingestion workflows. When running a refresh-only validation (e.g., after code patches or selector updates), normal audit-log entries and notifications (such as `ntfy` alerts) can create unnecessary noise and confusion. The policy ensures that these are suppressed during validation runs, allowing for clean manual and batch review cycles.

The policy is implemented via a `--validation-run` CLI flag in `scripts/auto_ingest.py`. When this flag is set, the following behaviors are triggered:
- **Audit-Log Suppression:** Normal audit-log entries and notifications are suppressed. This includes failure notifications that would otherwise be sent during batch validation exceptions.
- **Raw Snapshot and Wiki Page Updates:** Validation runs still update raw snapshots and wiki pages, ensuring that content changes are captured.
- **Force Requirement:** Validation runs require the `--force` flag to ensure that updates are applied even if the content has not changed.
- **Single-File and Batch Path Support:** The policy propagates validation mode into both single-file and batch processing flows. In batch mode, `process_all_pending(..., validation_run=True, force=True)` ensures that validation semantics are applied across multiple files.

The implementation involved several patches:
- Suppression of failure `ntfy` in batch validation mode.
- Removal of single-file parser restriction, allowing batch validation.
- Propagation of validation mode through relevant functions.

Edge cases include situations where validation-run semantics may not be desirable in batch mode, or where documentation does not match actual CLI behavior. The policy is designed to be extensible, with documentation updates required to clarify intended usage.

Trade-offs involve balancing the need for silent validation with the risk of missing important failure notifications. The policy is primarily intended for targeted/manual review reruns, but now supports batch mode as well.

## Key Properties

- **Audit-Log and Notification Suppression:** Suppresses audit-log entries and notifications during validation runs to reduce noise.
- **Supports Both Single-File and Batch Validation:** Validation mode can be applied to individual files or batches, propagating semantics as needed.
- **Force Requirement:** Requires --force to ensure updates are applied during validation runs.

## Limitations

If used inappropriately, validation-run suppression can hide important failures. Documentation and CLI semantics must be kept in sync to avoid confusion. Batch validation may not always be desirable from a product perspective.

## Example

```bash
python scripts/auto_ingest.py --validation-run --force raw/2026-04-08-lightgbm-light-gradient-boosting-machine-geeksforgeeks.md
# Suppresses audit-log noise, updates raw snapshot

python scripts/auto_ingest.py --validation-run --force
# Batch validation mode, propagates suppression across all pending files
```

## Visual

No explicit diagram, but the workflow is described in the session history and README/docs updates.

## Relationship to Other Concepts

- **[[Content-Root Selection for Article Extraction]]** — Validation-run is often used to test new extraction logic after selector or scoring changes.
- **[[Image Ranking and Extraction for Article Content]]** — Validation-run is used to review image extraction improvements in batch or targeted mode.

## Practical Applications

Supports clean manual and batch validation cycles in durable wiki ingestion pipelines, enabling targeted review of extraction logic changes without audit-log noise. Useful for QA, code review, and content fidelity assurance.

## Sources

- [[Copilot Session Checkpoint: URL Followup Pass]] — primary source for this concept
