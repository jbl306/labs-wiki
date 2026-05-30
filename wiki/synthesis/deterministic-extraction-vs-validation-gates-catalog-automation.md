---
title: "Deterministic Extraction vs Validation Gates in Catalog Automation"
type: synthesis
created: '2026-05-30'
last_verified: '2026-05-30'
source_hash: "synthesis-generated"
sources:
  - raw/2026-05-30-copilot-session-implementing-automated-catalog-refresh-pipeline-a5fa5230.md
concepts:
  - deterministic-public-web-catalog-refresh-benefits-apps
  - validation-gated-catalog-diffing-auto-apply
related:
  - "[[Automated Catalog Refresh Pipeline]]"
  - "[[Chase Sapphire Benefits v2]]"
  - "[[Copilot Session Checkpoint: Implementing automated catalog refresh pipeline]]"
tier: hot
tags: [catalog-refresh, synthesis, deterministic-extraction, guardrails, automation]
---

# Deterministic Extraction vs Validation Gates in Catalog Automation

## Question

How should a privacy-preserving internal app divide the job of learning from a public source page from the job of deciding whether those learned facts are safe to apply automatically?

## Summary

The checkpoint suggests that these should be treated as two distinct layers, not one blended scraper. [[Deterministic Public-Web Catalog Refresh for Benefits Apps]] is responsible for turning stable public HTML into structured candidate facts, while [[Validation-Gated Catalog Diffing and Auto-Apply]] is responsible for deciding whether those facts are trustworthy enough to mutate the canonical catalog. The result is a safer automation model: extraction can be ambitious about reading the page, while application remains conservative about changing state.

## Comparison

| Dimension | [[Deterministic Public-Web Catalog Refresh for Benefits Apps]] | [[Validation-Gated Catalog Diffing and Auto-Apply]] |
|-----------|---------------|---------------|
| Primary responsibility | Read issuer HTML and map it into catalog-shaped facts | Decide whether extracted facts are safe to write into the catalog |
| Main input | Public server-rendered page content and rule definitions | Extracted facts, structural fingerprint, and current catalog state |
| Core correctness test | Did the parser find the right benefit sections and values? | Did the source pass thresholds, and are the resulting diffs small and sane enough to trust? |
| Typical failure mode | Upstream page redesign, wording drift, or rule mismatch | False-positive changes, enum drift, or oversized deltas that should be held |
| Output | Candidate amount, cadence, and expiry fields by benefit slug | `apply` or `hold` classifications plus a refresh report and catalog diff |
| Human role | Author and maintain rules when page structure changes | Review held changes and adjust policy thresholds or schema mappings |

## Analysis

The two concepts solve different trust problems. Extraction answers, "Can we reliably interpret this page at all?" Validation answers, "Even if we interpreted it, should the machine commit the result?" Those are related but not identical questions. A deterministic parser can be locally correct and still produce unsafe writes if its output does not align with the catalog schema. The cadence mismatch captured in the checkpoint is the clearest evidence: reading the page was not the problem, but blindly trusting the resulting value would have been.

This separation also creates better failure modes. If extraction and mutation are fused, any parsing success tends to create pressure to write immediately, because there is no explicit stage boundary where skepticism can be applied. By isolating validation and diff policy, the workflow stays useful even when it refuses to mutate anything. A dry-run that exposes three good expiry fills and one bad cadence proposal is not a failed run; it is a successful review artifact that narrows the next fix to one enum mapping.

There is also an architectural benefit. Extraction logic should optimize for page comprehension: DOM segmentation, regex coverage, date parsing, and source-specific semantics. Validation logic should optimize for blast-radius control: minimum structure counts, blocked-page detection, sanity bounds, and delta thresholds. Combining those concerns in one module usually makes both harder to reason about. The checkpoint's decomposition into `extract.ts`, `validate.ts`, `diff.ts`, and `apply.ts` is valuable precisely because each file answers a different trust question.

For privacy-preserving internal tools, this layered model is especially attractive. The product can gain operational leverage from automation without granting the automation blanket authority. Public web data becomes a suggestion engine backed by deterministic evidence, not an unreviewable sync oracle. That is a strong fit for apps like [[Chase Sapphire Benefits v2]], where correctness and trust matter more than maximum automation volume.

## Key Insights

1. **Deterministic parsing and safe mutation are separate engineering problems, even when they live in one script stack.** — supported by [[Deterministic Public-Web Catalog Refresh for Benefits Apps]], [[Validation-Gated Catalog Diffing and Auto-Apply]]
2. **Dry-run artifacts are a product feature, not just a debugging aid, because they let automation surface useful partial truth without forcing a write.** — supported by [[Validation-Gated Catalog Diffing and Auto-Apply]], [[Copilot Session Checkpoint: Implementing automated catalog refresh pipeline]]
3. **A privacy-preserving app can automate public catalog maintenance effectively when rule-based extraction is paired with explicit hold policies instead of blind synchronization.** — supported by [[Deterministic Public-Web Catalog Refresh for Benefits Apps]], [[Automated Catalog Refresh Pipeline]]

## Open Questions

- How frequently should fixture-based regression runs be scheduled so upstream issuer drift is caught before a live refresh attempt fails?
- Should future versions add schema-aware enum validation earlier in extraction so value mismatches are rejected before diff generation?
- At what point would a second issuer or card program justify abstracting the rules engine beyond a single-source implementation?

## Sources

- [[Copilot Session Checkpoint: Implementing automated catalog refresh pipeline]]
