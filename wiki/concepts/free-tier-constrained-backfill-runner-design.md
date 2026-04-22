---
title: "Free-Tier-Constrained Backfill Runner Design"
type: concept
created: 2026-04-21
last_verified: 2026-04-21
source_hash: "6d1d5390738d68e0aaef5baf1126bb8caaff561e8e8b9d0084a6fcafd3d0555f"
sources:
  - raw/2026-04-21-copilot-session-free-tier-backfill-runner-a2d20186.md
quality_score: 79
concepts:
  - free-tier-constrained-backfill-runner-design
related:
  - "[[Backfill Script for Copilot Session Checkpoint Curation]]"
  - "[[Durable Copilot Session Checkpoint Promotion]]"
  - "[[Copilot Session Checkpoint: Free Tier Backfill Runner]]"
tier: hot
tags: [backfill, rate-limit, api-quota, wiki-ingestion, automation, security]
---

# Free-Tier-Constrained Backfill Runner Design

## Overview

The Free-Tier-Constrained Backfill Runner is a specialized script and workflow for ingesting and backfilling wiki URL content while strictly adhering to GitHub Models free-tier API rate limits. It is designed for conservative, durable operation, with dry-run-first validation, candidate ranking, and batch execution that automatically pauses on rate-limit signals. This approach minimizes risk of service interruption and maximizes value from limited API quotas.

## How It Works

The runner is implemented as a standalone script (`tmp_free_tier_url_backfill.py`) that reuses core ingestion logic from the project's main `auto_ingest.py` pipeline. It is designed to operate in a dedicated worktree, ensuring isolation from mainline development and facilitating safe experimentation and validation.

**Candidate Selection and Ranking:**
- The runner scans for wiki raw files of type `url` with `status: ingested` but lacking a persisted fetched-content block. It excludes candidates without a corresponding non-archive source page, ensuring only actionable items are processed.
- Candidates are ranked using a composite score based on the tier of the source page (e.g., 'hot', 'established'), the number of associated concepts, related links, and tags. This ranking allows for prioritization of 'high-value' items (e.g., those with score >= 50) in early phases, deferring lower-value items to later, less resource-critical runs.

**Dry-Run-First and Validation:**
- By default, the runner performs a dry-run, generating a preview and JSON report of what would be backfilled, without making changes. This enables safe review and adjustment of candidate selection, scoring thresholds, and execution parameters.
- The script supports CLI flags for execution mode, validation-only runs, minimum/maximum score cutoffs, and a limit on consecutive rate-limit-triggered stops (`--stop-after-rate-limits`).

**Batch Execution and Rate-Limit Handling:**
- When executed, the runner invokes `auto_ingest.py` as a subprocess for each candidate, passing the GitHub Models token via the `GITHUB_MODELS_TOKEN` environment variable (not on the command line, to avoid accidental leakage in logs or reports).
- The runner tracks rate-limit signals (e.g., API responses indicating quota exhaustion) and halts further processing after a configurable number of consecutive rate-limit events. This prevents overrun and ensures compliance with free-tier constraints.
- Small batch sizes (1–3 items) are used in conservative phases, with larger batches deferred to overnight or scheduled runs with explicit throttling.

**Security and Reporting:**
- A security bug was identified and fixed: the initial runner stored the full command line (including the sensitive token) in its JSON report. The fix involved moving the token to an environment variable and sanitizing report outputs.
- Each run generates a detailed report, including candidate selection, execution results, rate-limit events, and score distributions, supporting auditability and iterative tuning.

**Phase Support and Integration:**
- The runner supports explicit phase boundaries via `--min-score` and `--max-score`, enabling separation of high-value and full backfill phases as defined in the operational strategy document.
- Integration with session planning, SQL todo tracking, and MemPalace documentation ensures that the workflow is durable, reproducible, and transparent.

**Homelab Scheduler Integration (Planned):**
- For large-scale or overnight backfills, the runner is intended to be wrapped in a host-cron or Ofelia-based scheduler, with ntfy notifications on rate-limit pauses and completion. This ensures unattended, resilient operation aligned with homelab infrastructure conventions.

## Key Properties

- **Dry-Run-First Execution:** Default mode previews candidate selection and planned actions without making changes, supporting safe validation.
- **Candidate Ranking and Phase Cutoffs:** Candidates are scored and filtered by source page tier and metadata, enabling prioritized high-value and full backfill phases.
- **Rate-Limit-Aware Batch Processing:** Runner halts after configurable consecutive rate-limit signals, preventing quota overruns and ensuring compliance with free-tier limits.
- **Security-Conscious Token Handling:** Sensitive tokens are passed via environment variables and not logged, preventing accidental exposure in reports.
- **Integration with Existing Ingestion Logic:** Reuses core parsing and ingestion routines from `auto_ingest.py`, avoiding code duplication and ensuring consistency.

## Limitations

The runner is constrained by the GitHub Models free-tier API quota, which can halt progress if rate limits are hit frequently. Its conservative batch sizes may result in slow progress for large backfill jobs. The approach assumes that all ingestion logic and error handling in `auto_ingest.py` is robust; failures there may propagate. The runner does not implement its own retry or exponential backoff logic, instead relying on manual or scheduled re-invocation. The security fix for token handling mitigates leakage in reports, but other forms of sensitive data exposure must still be considered.

## Example

Example CLI usage for a high-value dry-run preview:

```bash
python scripts/tmp_free_tier_url_backfill.py --min-score 50 --dry-run
```

To execute a conservative batch, halting after one rate-limit event:

```bash
GITHUB_MODELS_TOKEN=... python scripts/tmp_free_tier_url_backfill.py --min-score 50 --execute --stop-after-rate-limits 1
```

The runner will process eligible candidates, update fetched-content blocks, and stop if a rate-limit is detected, logging results in a JSON report.

## Relationship to Other Concepts

- **[[Backfill Script for Copilot Session Checkpoint Curation]]** — The free-tier runner is a specialized adaptation of the general backfill script pattern, emphasizing quota-aware operation.
- **[[Durable Copilot Session Checkpoint Promotion]]** — The runner's output feeds into durable, promoted checkpoints for persistent wiki ingestion.

## Practical Applications

This pattern is directly applicable to any large-scale data ingestion or backfill operation where API quotas or rate limits are a hard constraint. It is especially relevant for teams using free-tier or limited-access APIs for knowledge base population, ensuring high-value content is prioritized and ingestion is resilient to quota exhaustion. The dry-run-first and security-conscious design is also a template for safe, auditable automation in regulated or sensitive environments.

## Sources

- [[Copilot Session Checkpoint: Free Tier Backfill Runner]] — primary source for this concept
