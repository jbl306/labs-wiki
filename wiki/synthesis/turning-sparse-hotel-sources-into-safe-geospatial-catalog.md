---
title: Turning Sparse Hotel Sources into a Safe Geospatial Catalog
type: synthesis
created: '2026-05-30'
last_verified: '2026-05-30'
source_hash: 14f942419bb014ea5d63af066edc6f5ef33eee105d208d166706c910d457dcc5
sources:
- raw/2026-05-30-copilot-session-researching-the-edit-hotel-auto-population-72a00d67.md
- raw/2026-05-30-copilot-session-implementing-hotel-auto-population-pipeline-3ef0ada5.md
concepts:
- third-party-map-ingestion-location-rich-travel-catalogs
- resumable-geocoding-city-centroid-fallback-travel-catalogs
- provenance-aware-hotel-catalog-diffing-mixed-source-refresh
related:
- '[[The Edit by Chase Travel]]'
- '[[Chase Sapphire Benefits v2]]'
- '[[Hotel Auto-Population Pipeline]]'
- '[[Choosing a Source of Truth for The Edit Hotel Catalog]]'
- '[[Automated Catalog Refresh Pipeline]]'
tier: hot
tags:
- hotel-catalog
- synthesis
- geocoding
- chase-travel
- provenance
- automation
evidence_scope: within-source
evidence_source_count: 2
evidence_origin_family_count: 1
---

# Turning Sparse Hotel Sources into a Safe Geospatial Catalog

## Question

How do you turn a broad but incomplete travel-data source into a production-safe geospatial catalog for [[Chase Sapphire Benefits v2]] without private-session scraping?

## Summary

The earlier research checkpoint solved the acquisition question only partially: a third-party source could expose enough of [[The Edit by Chase Travel]] to bootstrap the catalog, but not enough trustworthy coordinates to use it directly. The implementation checkpoint answers the missing half by adding [[Resumable Geocoding with City-Centroid Fallback for Travel Catalogs]] and [[Provenance-Aware Hotel Catalog Diffing for Mixed-Source Refresh]], which together convert sparse source coverage into admissible app data without letting weaker evidence overwrite curated truth.

## Comparison

| Dimension | [[Third-Party Map Ingestion for Location-Rich Travel Catalogs]] | [[Resumable Geocoding with City-Centroid Fallback for Travel Catalogs]] | [[Provenance-Aware Hotel Catalog Diffing for Mixed-Source Refresh]] |
|-----------|---------------|---------------|---------------|
| Primary job | Acquire broad place candidates from public community sources | Recover usable coordinates when the source lacks geometry | Decide which enriched candidates may add, update, or flag existing records |
| Best input shape | Map/KML/KMZ export with names and ideally coordinates | Normalized hotel rows with `name`, `city`, and `country` | Existing catalog plus enriched candidates carrying `sourceType` |
| Core risk | Source is broad but not authoritative | Public geocoder misses exact properties or rate-limits long runs | Lower-authority bulk rows overwrite curated or official rows |
| Main control | Corroborate against additional sources | Cache, rate-limit, and retry with city-centroid fallback | Curated preserve set plus review-oriented `flag-remove` behavior |
| Output guarantee | Candidate coverage | Spatial coverage, sometimes with reduced precision | Safe mutation policy and durable provenance |
| Failure mode | Incomplete or drifting upstream feed | Stacked centroid coordinates or unresolved rows | Stale curated rows or noisy review queues |

## Analysis

The important shift across the two checkpoints is that source selection and safe application are different problems. The research pass established that a fully public official source for The Edit was unlikely to be complete, while third-party maps could at least expose much more of the inventory. That solved the question of where candidate rows might come from, but not the question of how those rows could meet the app's stricter contract.

The implementation pass shows why the gap matters. The chosen KML export was broad enough on names and locality to produce 1,553 placemarks and 1,363 normalized hotels, but it carried no geometry. In a spreadsheet-oriented system that might be fine. In [[Chase Sapphire Benefits v2]], it is not, because the app needs `latitude` and `longitude` for map display and nearest-hotel ranking. That requirement turns coordinate recovery from a convenience into the central engineering problem.

[[Resumable Geocoding with City-Centroid Fallback for Travel Catalogs]] is the answer to the enrichment side of that problem. It accepts that public geocoders are slow and imperfect, then designs around those facts with cache persistence, bounded throughput, and an honest precision ladder. The key insight is that a city centroid is not perfect truth, but it can be useful truth when the alternative is excluding the hotel from the product entirely.

[[Provenance-Aware Hotel Catalog Diffing for Mixed-Source Refresh]] answers the control-plane side. Once coordinates exist, the system still must decide what authority those rows have. The checkpoint's `sourceType` design keeps third-party bootstrap data from masquerading as curated or portal-derived truth. That preserves room for a future authenticated export workflow without forcing the current bootstrap path to become destructive.

Taken together, the three concepts describe a staged conversion pipeline: broad public acquisition, bounded spatial enrichment, then source-aware admission into the canonical catalog. The result is not perfect canonical truth, but it is an operationally safe bridge from scarce public evidence to a much more useful product surface.

## Key Insights


1. **Broad candidate coverage is only the first half of the problem; geospatial products need coordinate recovery before a source is actually usable.** — supported by [[Third-Party Map Ingestion for Location-Rich Travel Catalogs]], [[Resumable Geocoding with City-Centroid Fallback for Travel Catalogs]]
2. **Imperfect coordinates can still be productively useful if the system records their lower confidence and keeps the workflow resumable.** — supported by [[Resumable Geocoding with City-Centroid Fallback for Travel Catalogs]], [[Hotel Auto-Population Pipeline]]
3. **Mixed-source catalogs stay stable only when provenance constrains overwrite and removal authority.** — supported by [[Provenance-Aware Hotel Catalog Diffing for Mixed-Source Refresh]], [[Authenticated Export for Private Travel Catalogs]]

## Evidence Map

| Insight | Supporting pages | Raw provenance | Confidence / limits |
|---|---|---|---|
| **Broad candidate coverage is only the first half of the problem; geospatial products need coordinate recovery before a source is actually usable.** | [[Third-Party Map Ingestion for Location-Rich Travel Catalogs]], [[Resumable Geocoding with City-Centroid Fallback for Travel Catalogs]] | `raw/2026-05-30-copilot-session-implementing-hotel-auto-population-pipeline-3ef0ada5.md`, `raw/2026-05-30-copilot-session-researching-the-edit-hotel-auto-population-72a00d67.md` | Legacy mapping reconstructed from existing wikilinks and declared provenance; verify semantics. |
| **Imperfect coordinates can still be productively useful if the system records their lower confidence and keeps the workflow resumable.** | [[Resumable Geocoding with City-Centroid Fallback for Travel Catalogs]], [[Hotel Auto-Population Pipeline]] | `raw/2026-05-30-copilot-session-implementing-hotel-auto-population-pipeline-3ef0ada5.md` | Legacy mapping reconstructed from existing wikilinks and declared provenance; verify semantics. |
| **Mixed-source catalogs stay stable only when provenance constrains overwrite and removal authority.** | [[Provenance-Aware Hotel Catalog Diffing for Mixed-Source Refresh]], [[Authenticated Export for Private Travel Catalogs]] | `raw/2026-05-30-copilot-session-implementing-hotel-auto-population-pipeline-3ef0ada5.md`, `raw/2026-05-30-copilot-session-researching-the-edit-hotel-auto-population-72a00d67.md` | Legacy mapping reconstructed from existing wikilinks and declared provenance; verify semantics. |

## Open Questions

- How many hotels will remain on `city-centroid` precision after the first full run, and should the UI surface that distinction?
- When an authenticated Chase Travel export becomes available, should it automatically supersede matching `third_party` rows or require a review pass first?
- What threshold of repeated `flag-remove` observations should promote a hotel from review state into archival or deactivation?

## Sources

- [[Copilot Session Checkpoint: Researching The Edit hotel auto-population]]
- [[Copilot Session Checkpoint: Implementing hotel auto-population pipeline]]
