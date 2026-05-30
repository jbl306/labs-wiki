---
title: "Validation-Gated Catalog Diffing and Auto-Apply"
type: concept
created: 2026-05-30
last_verified: 2026-05-30
source_hash: "08204272a2f0b096de2243fbc27aeabf42cdfe2dff0c35c2009703567cca6d13"
sources:
  - raw/2026-05-30-copilot-session-implementing-automated-catalog-refresh-pipeline-a5fa5230.md
related:
  - "[[Deterministic Public-Web Catalog Refresh for Benefits Apps]]"
  - "[[Phased Progress Tracking With Validation Gates]]"
  - "[[Pipeline Resilience in Machine Learning Systems]]"
tier: hot
tags: [catalog-refresh, guardrails, validation, automation, provenance, change-management]
---

# Validation-Gated Catalog Diffing and Auto-Apply

## Overview

Validation-gated catalog diffing and auto-apply is the control layer that decides whether freshly extracted public facts are safe enough to write back into a canonical catalog. In this checkpoint it is the difference between "we can parse the page" and "we can let automation touch production-facing data" for [[Chase Sapphire Benefits v2]].

## How It Works

The first principle of the pattern is that extraction success is not the same thing as mutation safety. A parser can find headings, amounts, and dates while still being wrong about meaning, enum values, or source integrity. The checkpoint makes this concrete with the travel-credit cadence mismatch: dry-run produced a plausible but incorrect proposed change from `anniversary_year` to `anniversary`. Nothing was broken at the HTML level; the error came from a mismatch between extracted wording and the catalog's accepted enum. A validation-gated system treats that kind of output as a reviewable diff, not an instruction to rewrite truth.

The mechanism begins with structural validation. Before trusting any extracted facts, the pipeline computes a fingerprint of the source HTML and compares it against hard expectations. In the checkpoint, the default thresholds require at least 5 benefit-item blocks and 8 `<h3>` headings. There is also a `looksBlocked()` style anti-bot or failure check that aborts if the fetch appears to have returned a blocked page, login wall, or unexpected interstitial. These rules are not fancy, but they are powerful because they filter out entire classes of false confidence. If the page layout no longer resembles the known source, the safe action is to stop.

The next layer is semantic validation of extraction coverage. Every credit-oriented rule must match, and every matched rule must produce a parseable amount within configured sanity bounds. This step is crucial because it converts "the parser found something" into "the parser found the minimum complete set of things we consider essential." A deterministic pipeline can be extremely precise if it is willing to fail closed. Missing one important benefit or parsing an amount outside its expected range is treated as evidence that assumptions have drifted, not as a small imperfection to ignore.

Only after the source passes both structural and semantic gates does the system compute a diff against the catalog. The catalog is not rewritten wholesale. Instead, each proposed mutation is classified field by field. Expiry-date fills and cadence changes may be considered safe enough to apply automatically, while amount changes are subject to a magnitude test. The checkpoint records `DEFAULT_DIFF_OPTIONS maxDeltaPct 40`, which means the system computes a relative change score such as

$$
\Delta\% = \frac{|new - old|}{old} \times 100
$$

and auto-applies only when the result is within the configured tolerance. Larger deltas become `hold` actions rather than write operations. This matters because product-copy changes can be real, but they can also signal parsing mistakes, changed source semantics, or a benefit-program redesign that deserves human review.

Another important part of the pattern is separating **dry-run** from **apply**. The orchestrator script writes snapshots and `.refresh-report.json` even when nothing is changed in the catalog. That report becomes an evidence artifact: it tells the operator what matched, what failed, what would change, and why. The apply path is therefore not the only useful outcome. A good validation-gated system produces durable review materials before it produces durable mutations. In the checkpoint, that is exactly how the spurious cadence issue surfaced—through a safe dry-run that exposed the mismatch without corrupting the catalog.

The change-application layer also preserves provenance. The catalog JSON acts as a canonical artifact, the report stores the proposed-change reasoning, and a normal git diff becomes the audit trail. Because the workflow is deterministic, this audit trail is unusually high value. A reviewer can rerun the same fixture or fetch, inspect the same rule definitions, and verify whether the classification logic was correct. That makes approval or rollback legible in a way that many automated sync jobs are not.

Operationally, the pattern behaves like a decision function around extracted evidence. It asks a sequence of binary questions: does the page still look like the expected source, did every required rule match, do the parsed values fit allowed ranges, and is each resulting delta small enough to trust automatically? Only when all relevant answers are yes does the write path open. This gives the system a graceful failure mode. It can stop, report, and wait for a human without pretending partial success is good enough.

The broader intuition is that auto-apply should be the smallest possible subset of the automation problem. The expensive and ambiguous part of the workflow is discovering truth from the web. Once that truth is only partially trusted, the safest design is to shrink the set of changes the machine is allowed to commit on its own. Validation gates, diff classes, and hold thresholds operationalize that discipline.

## Key Properties

- **Fail-closed behavior:** suspicious structure, missing coverage, or oversized deltas stop automation instead of being silently tolerated.
- **Field-level classification:** amount, cadence, and expiry updates are evaluated differently rather than treated as one undifferentiated "catalog changed" event.
- **Dry-run first:** snapshots and reports are first-class outputs, not optional debugging leftovers.
- **Threshold-backed safety:** minimum page-shape counts and `maxDeltaPct` convert fuzzy trust into explicit policy.
- **Audit-friendly mutations:** git diff and report artifacts preserve exactly what the system wanted to change.

## Limitations

Thresholds can overfit the current page shape and may need maintenance after legitimate upstream redesigns. A conservative `maxDeltaPct` prevents catastrophic errors but can also delay real large changes that deserve quick adoption. Enum mismatches and catalog-schema drift can still create noisy diffs even when structure is intact. Finally, auto-apply policies are only as safe as the rule definitions beneath them; if a rule systematically extracts the wrong field, the control layer may faithfully classify a bad fact.

## Examples

```python
def classify_change(old_value, new_value, max_delta_pct=40):
    if old_value is None:
        return "hold"
    delta_pct = abs(new_value - old_value) / old_value * 100
    return "apply" if delta_pct <= max_delta_pct else "hold"
```

In the checkpoint's recorded run, this pattern allowed three low-risk expiry-date fills to remain candidates for automatic application while surfacing a cadence-enum mismatch as a review item rather than silently rewriting the catalog.

## Practical Applications

This concept applies anywhere an internal system must synchronize curated structured data from a semi-stable external source: benefit catalogs, pricing tables, vendor reference data, compliance control libraries, or ML feature registries backed by upstream exports. It is especially valuable when the source is trustworthy enough to automate against, but not trustworthy enough to mutate production state without intermediate policy checks.

## Related Concepts

- **[[Deterministic Public-Web Catalog Refresh for Benefits Apps]]** — Supplies the extracted candidate facts that this control layer evaluates.
- **[[Phased Progress Tracking With Validation Gates]]** — Describes the broader engineering discipline of gating progress and mutation on explicit criteria.
- **[[Pipeline Resilience in Machine Learning Systems]]** — Shares the same philosophy of bounding blast radius with precondition checks and controlled failure modes.

## Sources

- [[Copilot Session Checkpoint: Implementing automated catalog refresh pipeline]] — captures the thresholds, diff policy, dry-run behavior, and the cadence-mismatch incident that motivated the guardrails.
