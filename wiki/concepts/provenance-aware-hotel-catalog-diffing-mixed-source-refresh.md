---
title: "Provenance-Aware Hotel Catalog Diffing for Mixed-Source Refresh"
type: concept
created: 2026-05-30
last_verified: 2026-05-30
source_hash: "2ace2c413350f715b3e61d68960b7a40483b50a7724a286c5a171aebba0da3b1"
sources:
  - raw/2026-05-30-copilot-session-implementing-hotel-auto-population-pipeline-3ef0ada5.md
related:
  - "[[Validation-Gated Catalog Diffing and Auto-Apply]]"
  - "[[Authenticated Export for Private Travel Catalogs]]"
  - "[[Resumable Geocoding with City-Centroid Fallback for Travel Catalogs]]"
  - "[[Turning Sparse Hotel Sources into a Safe Geospatial Catalog]]"
tier: hot
tags: [provenance, catalog-refresh, hotel-catalog, diffing, source-type, automation]
---

# Provenance-Aware Hotel Catalog Diffing for Mixed-Source Refresh

## Overview

Provenance-aware hotel catalog diffing is a refresh pattern where the system decides how aggressively to add, update, preserve, or flag records based not only on field values, but also on where each record came from. It matters when a travel catalog combines manual curation, operator exports, official public examples, and broad third-party imports, because those sources do not deserve equal write authority.

In this checkpoint the concept matters because the new hotel pipeline feeds [[Chase Sapphire Benefits v2]] from a third-party KML export, while the app already contains curated rows and a schema that anticipates multiple source classes. The implementation therefore cannot behave like a blind "replace the CSV with the newest dump" job. It has to preserve trusted rows, admit bulk third-party additions, and distinguish "missing upstream today" from "safe to delete."

## How It Works

The first step is making provenance explicit in the schema. The checkpoint records that the hotel CSV, parser, and seed/import flow were extended with a `sourceType` column. That means each hotel row carries more than name and coordinates; it also carries a statement about how the record entered the system. In the recorded design, the important values are `manual`, `user_chase_travel_export`, `official_public_example`, and `third_party`. Once provenance becomes data, diff policy can branch on it deterministically instead of relying on undocumented operator intuition.

The next step is stable identity. The pipeline uses `keyOf(name, city, country)` with a lowercased `name|city|country` composite as the canonical comparison key. This is a practical choice for travel catalogs because hotel programs often lack stable public IDs across sources, while names and locality remain the best common denominator. The key is not perfect; hotels can rename, rebrand, or shift locality labels. But it is strong enough to let the system answer the core refresh question: "does this upstream candidate refer to an existing record we already know?"

Once identity is stable, provenance controls collision handling. This is the heart of the concept. The checkpoint defines a curated preserve set of `{manual, user_chase_travel_export, official_public_example}`. When a new third-party candidate collides on key with one of those curated records, the curated row wins. The pipeline may still learn from the third-party row, perhaps by adding corroboration notes or identifying a likely match, but it does not let a lower-authority source overwrite a higher-authority one automatically. This rule is what turns provenance from metadata into policy.

The design is especially interesting because it does **not** elevate corroboration into false authority. The checkpoint explicitly says that corroboration against public Chase pages adds a note, not a source change. In other words, a `third_party` row remains `third_party` even if some part of it appears on an official page. That is an important discipline. Provenance should describe the data path that produced the record, not the operator's confidence in it after auxiliary checks. Mixing those ideas would make it much harder to reason about why a row was allowed to overwrite another row later.

The removal side of diffing uses the same principle. When the third-party source shrinks, the pipeline does not auto-delete missing rows wholesale. Instead, only rows whose current provenance is `third_party` are eligible for `flag-remove`. Curated rows are never flagged just because the bulk source stopped mentioning them. This matters because absence means different things for different source classes. If a manual row disappears from a community map, that says almost nothing. If a `third_party` row disappears from the very source that created it, that is meaningful enough to surface for review.

Validation thresholds add another layer of safety. The checkpoint notes defaults such as `minSourceHotels=800`, `minCountries=30`, and `minResolved=1`. These are not provenance rules in themselves, but they protect provenance policy from acting on obviously broken inputs. A mixed-source catalog needs both ideas at once: source-aware conflict resolution and whole-run sanity checks. Without thresholds, a malformed upstream dump could still produce a provenance-legible but operationally disastrous diff.

This pattern can be described as a write-eligibility function:

$$
\text{auto-write}(r_{new}, r_{old}) =
\begin{cases}
0 & \text{if } source(r_{old}) \in C \land source(r_{new}) \notin C \\
1 & \text{if validated} \land source(r_{new}) = \text{third\_party} \land r_{old} = \varnothing \\
\text{review} & \text{otherwise}
\end{cases}
$$

where \( C = \{\text{manual}, \text{user\_chase\_travel\_export}, \text{official\_public\_example}\} \).

The exact algebra is less important than the discipline it encodes: provenance narrows the set of changes automation is allowed to commit.

Another subtle but crucial part of the concept is how it handles partial enrichment. The schema requires coordinates, so unresolved rows are held instead of imported. That interacts with provenance cleanly. A new `third_party` candidate that lacks coordinates does not become a broken database row, nor does it replace a curated hotel. It simply remains out of the write set until it satisfies the app's contract. This is another example of provenance-aware diffing being more than a field-level compare; it is a gate around what counts as an admissible record.

The final reason this concept matters is that it supports future source evolution. The earlier research checkpoint identified authenticated export as the likely highest-authority path if a clean portal artifact becomes available later. Because the implementation already has provenance-aware diffing, the system can introduce `user_chase_travel_export` rows without rewriting its whole merge model. The current third-party bootstrap and the possible future official-export workflow can coexist, because the diff engine already knows that not all rows speak with the same authority.

## Key Properties

- **Source-class policy:** write behavior depends on `sourceType`, not only on raw field deltas.
- **Curated-row preservation:** `manual`, `user_chase_travel_export`, and `official_public_example` records win conflicts against weaker bulk feeds.
- **Reviewable removals:** disappearing third-party rows are flagged rather than silently deleted, and curated rows are protected from source drift.
- **Identity normalization:** a stable `(name, city, country)` key turns a messy hospitality dataset into a tractable merge problem.
- **Future-ready merge model:** the same catalog can accept better future sources without discarding the current bootstrap path.

## Limitations

Composite keys can break when hotels rebrand, move, or use inconsistent locality names across sources. Provenance tiers also require discipline: if operators mislabel rows, the merge policy can become too conservative or too permissive. Protected curated rows can accumulate stale data if no later workflow promotes fresher higher-authority evidence. And because the system avoids hard deletions, it still needs human review or additional rules to convert repeated `flag-remove` signals into final archival decisions.

## Examples

```python
CURATED = {"manual", "user_chase_travel_export", "official_public_example"}

def merge_candidate(existing, incoming):
    if existing and existing["sourceType"] in CURATED and incoming["sourceType"] not in CURATED:
        return {"action": "preserve-existing"}
    if not incoming.get("latitude") or not incoming.get("longitude"):
        return {"action": "hold-unresolved"}
    if not existing:
        return {"action": "add"}
    return {"action": "update-third-party"}
```

In the checkpoint's concrete implementation, all KML-derived hotels stay `third_party`, corroboration does not upgrade them, curated rows are preserved on collision, and only third-party rows are eligible for removal flags when the source stops mentioning them.

## Practical Applications

This concept applies to any catalog that mixes operator-entered truth with bulk external feeds: property inventories, supplier lists, venue directories, internal CRM references, and marketplace catalogs. It is especially useful when one source is broad but weakly authoritative, another source is narrow but trusted, and the system needs a deterministic way to let them coexist without destructive oscillation.

## Related Concepts

- **[[Validation-Gated Catalog Diffing and Auto-Apply]]** — Provides the generic guardrail model that provenance-aware diffing specializes for mixed-confidence hotel records.
- **[[Authenticated Export for Private Travel Catalogs]]** — Describes the future higher-authority source class that this diffing model is already prepared to admit.
- **[[Resumable Geocoding with City-Centroid Fallback for Travel Catalogs]]** — Supplies the coordinate-enrichment layer whose outputs this diff engine decides whether to admit.

## Sources

- [[Copilot Session Checkpoint: Implementing hotel auto-population pipeline]] — records the `sourceType` design, curated preserve set, keying strategy, validation thresholds, and flag-remove behavior.
