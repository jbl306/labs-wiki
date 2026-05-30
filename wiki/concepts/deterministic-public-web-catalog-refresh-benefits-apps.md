---
title: "Deterministic Public-Web Catalog Refresh for Benefits Apps"
type: concept
created: 2026-05-30
last_verified: 2026-05-30
source_hash: "08204272a2f0b096de2243fbc27aeabf42cdfe2dff0c35c2009703567cca6d13"
sources:
  - raw/2026-05-30-copilot-session-implementing-automated-catalog-refresh-pipeline-a5fa5230.md
related:
  - "[[Deterministic Reference Artifact Pipeline]]"
  - "[[Validation-Gated Catalog Diffing and Auto-Apply]]"
  - "[[Phased Progress Tracking With Validation Gates]]"
tier: hot
tags: [catalog-refresh, deterministic-extraction, privacy-preserving, web-scraping, automation, benefits-tracker]
---

# Deterministic Public-Web Catalog Refresh for Benefits Apps

## Overview

Deterministic public-web catalog refresh is a pattern for updating an application's structured product catalog from stable, publicly accessible web pages without using an LLM, browser automation, or private account data. In this checkpoint it matters because [[Chase Sapphire Benefits v2]] needs fresher benefit definitions, but its trust model forbids solutions that would depend on user credentials, opaque extraction, or issuer-side private APIs.

## How It Works

The concept starts from a policy decision before it becomes an implementation detail: only **public benefit definitions** are eligible for automation. That boundary shapes the entire workflow. Rather than attempting account-aware scraping, logging into Chase, or correlating reward usage history, the system treats the issuer's public benefits page as a narrow source of truth for catalog metadata such as amount, cadence wording, and expiration dates. This dramatically reduces privacy risk because no personally identifying information, tokens, or cardholder state ever need to enter the pipeline. In other words, the automation target is product-definition content, not user data.

Once that boundary is established, the next step is to find a page shape that is stable enough to parse reproducibly. The checkpoint shows this being done through direct HTML discovery against a real fixture of the Chase Sapphire Reserve page. The durable observation is that the page is server-rendered HTML around 255 KB, not a JavaScript-heavy shell, and that useful benefit content appears in repeated component blocks such as `cmp-sapphirebenefits__textitem`. That matters because a deterministic parser becomes realistic only when the source has structure that survives across requests. Instead of asking a model to infer meaning from arbitrary presentation, the workflow can segment the document along known delimiters like `<h3>` headings and repeatedly obtain the same sections.

After structure discovery comes rule encoding. Here the implementation does not attempt a generic "benefit extractor." It creates a catalog-specific rules file, `catalog/benefits/extraction-rules.json`, that maps each known benefit slug to precise text patterns and parsing behavior. Some rules extract straightforward annual credits, while others must interpret phrasing nuances. A particularly revealing example is StubHub: the page may advertise a `$300` aggregate yearly value, but the catalog models it as `$150` per half-year period, so the extractor must deliberately match the per-period text rather than the headline. This is where determinism becomes more than "just regex." The rules encode domain semantics that reconcile marketing copy with the application's canonical data model.

The extraction stage then converts each benefit section into structured candidate facts. Section text is normalized, tags are stripped where appropriate, and fields such as amount, cadence, and `benefitEndDate` are parsed using explicit routines. The checkpoint calls out support for several date formats, including `M/D/YY`, `M/D/YYYY`, and `"Month D, YYYY"`. These small details are critical. A deterministic system succeeds not by being broadly intelligent, but by being locally exact across a finite set of expected forms. The algorithm works because the page surface is narrow and the catalog targets are known in advance.

An important part of the mechanism is repeatability. The same fixture can be rerun through the parser, the same segmentation boundaries can be inspected, and the same rule set can be version-controlled next to the catalog. If the output changes, the operator has a small set of possible causes: the upstream page changed, the rule file changed, or the parsing code changed. That is operationally superior to a model-based extractor whose behavior might drift without any code or prompt modifications. In practice, determinism turns extraction bugs into debuggable software defects instead of prompt-tuning mysteries.

The concept also depends on choosing the right abstraction level for evidence. The system does not try to build a generic DOM knowledge graph or store all raw fragments as product truth. It extracts directly into the catalog's own identifiers and fields. That keeps the pipeline aligned with the consuming application. A candidate benefit is meaningful because it maps to an existing catalog slug, not because the parser found some vaguely relevant sentence. The checkpoint's exact mappings—travel credit, Edit by Chase Travel, Select Hotels, dining, StubHub, Peloton, Lyft, and annual fee—show a design centered on operational usefulness rather than theoretical completeness.

Another reason this approach works is that the upstream content changes relatively slowly. Benefit programs do not mutate dozens of times per day, and the canonical page copy tends to follow branded content-management conventions. In that environment, a carefully authored parser can stay cheap, fast, and robust for long stretches. The extraction logic effectively trades breadth for reliability: it is worse at handling arbitrary websites, but better at handling one important website with high precision and strong auditability.

The mathematical intuition behind the pattern is simple: trust increases when the transformation from HTML to catalog fields is small, inspectable, and bounded. If we describe rule coverage as

$$
\text{coverage} = \frac{\text{matched credit rules}}{\text{total credit rules}},
$$

then deterministic refresh aims to keep coverage at `1.0` for the known catalog surface. Anything less is not "partially correct enough"; it is a signal that the source page, rule set, or assumptions have drifted and should trigger review. That mindset distinguishes a production-grade deterministic refresher from a best-effort scraper.

## Key Properties

- **Public-source boundary:** Only issuer-published benefit definitions are ingested; no private or credentialed data path is introduced.
- **Stable-structure parsing:** The workflow depends on repeatable HTML cues such as `<h3>` boundaries and known component classes rather than probabilistic extraction.
- **Catalog-specific rules:** Each benefit slug gets explicit patterns, making the parser precise about domain semantics like cadence and per-period versus aggregate value.
- **Replayability:** Fixtures, rules, and code can be rerun locally to reproduce both successes and failures.
- **Low operational cost:** No headless browser, model endpoint, or dynamic site interaction is required.

## Limitations

The approach is only as durable as the issuer page's structural stability. A redesign that removes the expected headings or changes component-class patterns can collapse extraction coverage immediately. It also struggles with semantic mismatches between marketing language and the app's internal model, as shown by the cadence-value mismatch and the StubHub aggregate-versus-period nuance. Finally, deterministic refresh does not generalize automatically to other issuers or products; each new source usually requires its own rule file and structural discovery pass.

## Examples

```python
def extract_public_catalog(html, rules):
    sections = segment_sections(html, split_on="h3")
    extracted = {}
    for rule in rules:
        section = find_matching_section(sections, rule["match"])
        extracted[rule["slug"]] = {
            "amount_cents": parse_amount(section, rule),
            "cadence": parse_cadence(section, rule),
            "benefit_end_date": parse_expiry(section),
        }
    return extracted
```

In the checkpoint's concrete implementation, this pattern correctly captured public facts such as a `$300` travel credit, a `$250` per-booking Edit by Chase Travel credit, a `$250` Select Hotel credit expiring on `12/31/26`, and informational expiry dates for Peloton and Lyft.

## Practical Applications

This concept fits privacy-sensitive internal tools that maintain structured catalogs from small sets of public reference pages: card-benefit trackers, loyalty-program reference apps, subscription-plan databases, or internal compliance inventories. It is especially appropriate when the consuming system already has a strong domain schema and needs a refresh mechanism that is inspectable, cheap to operate, and easy to disable when the source drifts.

## Related Concepts

- **[[Deterministic Reference Artifact Pipeline]]** — Shares the same no-LLM, evidence-first philosophy, but applies it to image processing rather than web content.
- **[[Validation-Gated Catalog Diffing and Auto-Apply]]** — Describes the downstream safety layer that decides whether extracted facts can mutate the catalog.
- **[[Phased Progress Tracking With Validation Gates]]** — Provides the broader workflow discipline that keeps this kind of automation implementation staged and reviewable.

## Sources

- [[Copilot Session Checkpoint: Implementing automated catalog refresh pipeline]] — records the HTML discovery findings, rule design, and domain-specific parsing details.
