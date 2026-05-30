---
title: Hotel Auto-Population Pipeline
type: entity
created: 2026-05-30
last_verified: 2026-05-30
source_hash: "2ace2c413350f715b3e61d68960b7a40483b50a7724a286c5a171aebba0da3b1"
sources:
  - raw/2026-05-30-copilot-session-implementing-hotel-auto-population-pipeline-3ef0ada5.md
concepts:
  - resumable-geocoding-city-centroid-fallback-travel-catalogs
  - provenance-aware-hotel-catalog-diffing-mixed-source-refresh
related:
  - "[[The Edit by Chase Travel]]"
  - "[[Chase Sapphire Benefits v2]]"
  - "[[Automated Catalog Refresh Pipeline]]"
  - "[[Resumable Geocoding with City-Centroid Fallback for Travel Catalogs]]"
  - "[[Provenance-Aware Hotel Catalog Diffing for Mixed-Source Refresh]]"
tier: hot
tags: [hotel-catalog, geocoding, kml, chase-travel, provenance, automation]
---

# Hotel Auto-Population Pipeline

## Overview

The Hotel Auto-Population Pipeline is a deterministic ingest workflow added to [[Chase Sapphire Benefits v2]] for turning a community-maintained export of [[The Edit by Chase Travel]] into the app's geospatial hotel catalog. Its job is to acquire a broad upstream list, normalize names and locations, recover coordinates through bounded geocoding, cross-check public Chase references, and write a CSV that the existing import and seed path can apply.

What makes the pipeline important is the way it closes the gap between a semantically rich but operationally awkward source and the app's strict runtime schema. The checkpoint is explicit that the chosen KML source carries hotel names and locality metadata but no coordinates, while the downstream `ChaseEditHotel` model requires `latitude` and `longitude` for map rendering and nearest-hotel ranking. The pipeline therefore acts as an enrichment and control plane, not just a file converter.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool |
| Created | 2026-05-30 |
| Creator | Copilot CLI |
| URL | N/A |
| Status | Active |

## Architecture

The implementation is split across `src/lib/hotels-refresh/` plus the `scripts/refresh-hotels.ts` orchestrator:

- `types.ts` defines contracts for raw placemarks, normalized source hotels, geocode cache entries, resolved hotels, validation results, diffs, and refresh reports.
- `kml.ts` parses placemarks from the export, filters metadata rows, and fingerprints the input with `sha256`.
- `normalize.ts` converts raw placemark strings into stable hotel keys by title-casing names, canonicalizing countries, and splitting `Location: CITY, COUNTRY`.
- `geocode.ts` handles provider selection, cache load/save, rate-limited batch geocoding, and the city-centroid fallback path.
- `corroborate.ts` fetches public Chase pages, extracts featured hotel names, and records corroboration signals.
- `validate.ts` enforces minimum-count thresholds before a write is trusted.
- `diff.ts` compares normalized resolved rows against the current CSV while preserving curated records and only flagging removable third-party entries.
- `apply.ts` serializes the final sorted CSV used by `scripts/import-hotels.ts` and `prisma/seed.ts`.

## Operational Model

The pipeline follows an acquire -> parse -> normalize -> geocode -> corroborate -> validate -> diff -> apply loop. In the captured run, 1,553 upstream placemarks collapsed to 1,363 deduplicated hotels across 91 countries. Because the source lacked geometry, coordinate recovery became the pacing step: Nominatim was used with a 1100 ms delay and a cache flushed every 25 records so the long-running job could survive interruptions or rate limits.

The most consequential implementation choice is the fallback hierarchy for weak geocoding inputs. Direct queries like `Name, City, Country` work for well-known chain properties but miss many boutique hotels. Rather than treating those misses as hard failures, the pipeline retries with `City, Country`, accepts a lower-precision centroid when needed, and marks that reduced accuracy explicitly. This lets the app reach broad spatial coverage in v1 while remaining honest about confidence.

## Safety and Provenance

The pipeline does not treat every upstream change as equally trustworthy. It introduces source-aware behavior through `sourceType`: rows marked `manual`, `user_chase_travel_export`, or `official_public_example` are curated and win conflicts, while the KML-derived rows remain `third_party`. When the source shrinks or changes names, only third-party rows are candidates for `flag-remove`; curated entries are preserved and unresolved rows are held out of the write path entirely.

This makes the workflow a specialized extension of [[Automated Catalog Refresh Pipeline]]. The earlier benefits refresher proved out deterministic extraction plus validation gates for issuer copy. The hotel variant adds two new responsibilities the benefits pipeline did not need: coordinate recovery and provenance-sensitive merge policy across mixed-confidence sources.

## Impact

The checkpoint records that the app could move from a 3-row hand-maintained hotel list toward a roughly 1,363-row geographically usable catalog without storing Chase credentials or depending on opaque LLM extraction. It also records supporting work outside the pipeline core, including a `sourceType` column added to the CSV flow, faster batch lookups in seed/import code, and a hotels UI updated to show counts, country coverage, freshness, and a nearest-60 presentation limit.

## Sources

- [[Copilot Session Checkpoint: Implementing hotel auto-population pipeline]] — documents the module layout, normalization and geocoding strategy, provenance rules, and operational status of the first bulk run.
