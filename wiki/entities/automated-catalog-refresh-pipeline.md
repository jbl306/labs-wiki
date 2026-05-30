---
title: Automated Catalog Refresh Pipeline
type: entity
created: 2026-05-30
last_verified: 2026-05-30
source_hash: "08204272a2f0b096de2243fbc27aeabf42cdfe2dff0c35c2009703567cca6d13"
sources:
  - raw/2026-05-30-copilot-session-implementing-automated-catalog-refresh-pipeline-a5fa5230.md
concepts:
  - deterministic-public-web-catalog-refresh-benefits-apps
  - validation-gated-catalog-diffing-auto-apply
related:
  - "[[Chase Sapphire Benefits v2]]"
  - "[[Copilot CLI]]"
  - "[[Durable Copilot Session Checkpoint]]"
tier: hot
tags: [catalog-refresh, automation, deterministic-extraction, benefits-tracker, nextjs, privacy-preserving]
---

# Automated Catalog Refresh Pipeline

## Overview

The Automated Catalog Refresh Pipeline is a deterministic update workflow added to [[Chase Sapphire Benefits v2]] to keep the public benefit catalog aligned with issuer-published definitions. Instead of using an LLM or browser automation, it fetches a public Chase Sapphire Reserve benefits page, segments the server-rendered HTML into benefit sections, extracts structured facts with explicit rules, validates the page shape, diffs against the catalog, and auto-applies only changes that pass narrow safety criteria.

What makes the pipeline important is not just that it refreshes data, but that it does so without weakening the product's trust model. The checkpoint is explicit that the application remains manual-first and privacy-preserving: only public benefit metadata is touched, large or suspicious diffs are held for review, and the catalog JSON plus refresh report provide an audit trail for every proposed mutation.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool |
| Created | 2026-05-30 |
| Creator | Copilot CLI |
| URL | N/A |
| Status | Active |

## Architecture

The pipeline is intentionally decomposed into small modules so each phase can be reasoned about independently:

- `src/lib/catalog-refresh/types.ts` defines the shared contract for extraction rules, fingerprints, validation results, proposed changes, and refresh reports.
- `src/lib/catalog-refresh/html.ts` handles normalization primitives such as `stripTags`, `segmentSections`, `sha256`, and structural fingerprinting with `node-html-parser`.
- `src/lib/catalog-refresh/extract.ts` loads rule definitions, parses expiry dates, and emits benefit-level facts from the segmented page.
- `src/lib/catalog-refresh/validate.ts` enforces structural gates such as minimum benefit-item and heading counts before any diff is trusted.
- `src/lib/catalog-refresh/diff.ts` compares extracted facts against `catalog/benefits/chase-sapphire-reserve.json` and classifies changes as safe apply or hold.
- `src/lib/catalog-refresh/apply.ts` performs pure application of accepted changes and writes the updated catalog.
- `scripts/refresh-catalog.ts` acts as the CLI orchestrator, exposing dry-run and apply modes along with optional snapshot seeding, max-delta overrides, and webhook notification.

## Validation and Safety Model

The checkpoint records several explicit guardrails that define the pipeline's operating contract. First, the fetched page must still look like the expected issuer layout: at least 5 benefit items and 8 `<h3>` headings must be present, and anti-bot or blocked-page heuristics must stay false. Second, every credit-oriented extraction rule must match and produce a parseable amount within its configured sanity bounds. Third, the diff engine limits automatic amount updates to modest drift; larger changes are held instead of silently rewriting the catalog.

This separation is valuable because it prevents a structurally valid fetch from becoming a logically unsafe write. The reported cadence mismatch in the checkpoint shows why: the HTML was parseable, but a value-level enum mismatch still produced a bad proposed change. By capturing that discrepancy in dry-run rather than mutating the catalog, the pipeline demonstrates that validation is not a formality; it is the mechanism that turns deterministic extraction into safe automation.

## Operational Workflow

1. Fetch the live page or read a saved fixture.
2. Normalize HTML and segment benefit sections on `<h3>` boundaries.
3. Apply explicit extraction rules to capture amount, cadence, and expiry fields by catalog slug.
4. Validate the page fingerprint and rule coverage.
5. Diff extracted facts against the current catalog, classifying changes as `apply` or `hold`.
6. Write a report and snapshot in dry-run mode, or update the catalog JSON in apply mode.
7. Seed downstream runtime data with the refreshed catalog if the apply step is accepted.

## Impact

The pipeline turns benefit-catalog maintenance from a manual review exercise into a bounded automation loop with deterministic failure modes. It gives the project a way to consume public issuer updates faster while still preserving provenance, reviewability, and the app's manual-first privacy stance.

## Sources

- [[Copilot Session Checkpoint: Implementing automated catalog refresh pipeline]] — documents the module layout, thresholds, discovery findings, and pending fixes.
