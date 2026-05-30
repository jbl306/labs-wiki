---
title: "Resumable Geocoding with City-Centroid Fallback for Travel Catalogs"
type: concept
created: 2026-05-30
last_verified: 2026-05-30
source_hash: "2ace2c413350f715b3e61d68960b7a40483b50a7724a286c5a171aebba0da3b1"
sources:
  - raw/2026-05-30-copilot-session-implementing-hotel-auto-population-pipeline-3ef0ada5.md
related:
  - "[[Third-Party Map Ingestion for Location-Rich Travel Catalogs]]"
  - "[[Provenance-Aware Hotel Catalog Diffing for Mixed-Source Refresh]]"
  - "[[Validation-Gated Catalog Diffing and Auto-Apply]]"
  - "[[Turning Sparse Hotel Sources into a Safe Geospatial Catalog]]"
tier: hot
tags: [geocoding, travel-data, hotel-catalog, resumability, kml, geospatial]
---

# Resumable Geocoding with City-Centroid Fallback for Travel Catalogs

## Overview

Resumable geocoding with city-centroid fallback is an enrichment pattern for catalog sources that identify places well enough to name and locate them textually, but not well enough to provide stable coordinates directly. The pattern matters when a downstream product needs usable latitude and longitude on every record, yet the upstream artifact is incomplete, rate-limited to enrich, and too large to reprocess from scratch after every interruption.

In this checkpoint the concept matters because the chosen The Edit hotel source exposed 1,553 placemarks with names and `Location: CITY, COUNTRY` metadata but no geometry. The hotel app could not accept those rows as-is: `ChaseEditHotel` requires coordinates for map rendering and nearest-hotel ranking, so the pipeline had to recover coordinates deterministically while tolerating long runtimes, partial failures, and boutique-name misses.

## How It Works

The pattern begins by treating geocoding as a first-class pipeline stage rather than a one-off helper function. If a travel catalog has a few records, an application can often geocode everything in one run and ignore the operational details. That stops working once the source grows into the thousands and the provider has strict throughput limits. The checkpoint records exactly this situation: Nominatim was operated at roughly one request per second with a 1100 ms delay, and the full run was expected to take 30-50 minutes. At that scale, the core problem is not only "how do I get coordinates?" but also "how do I keep my progress if the process is interrupted, rate-limited, or only partially successful?"

The first mechanism is normalization before lookup. A raw placemark rarely arrives in the shape a geocoder wants. The pipeline parses the KML-like structure, filters metadata entries, extracts the hotel name, and splits the embedded location string into `city` and `country`. It then canonicalizes country names, title-cases names, and forms a stable identity key using `name|city|country`. This matters because geocoders are sensitive to string quality. Two queries that refer to the same property but differ in capitalization, punctuation, or country spelling can produce different results or cache misses. By normalizing first, the system increases both hit rate and cache reuse.

The second mechanism is persistent caching. Each geocode attempt is stored in `catalog/hotels/.geocode-cache.json`, and the checkpoint notes that the cache is flushed every 25 records. That decision is small but architecturally important. A single terminal crash, network hiccup, or provider block should not erase twenty minutes of progress. With periodic flushes, the batch can restart from disk and skip the rows it already resolved. This makes the geocoding stage **resumable**, which changes the operator experience from "fragile bulk job" to "bounded background process." In practice, resumability is what makes slow public geocoders usable for medium-sized catalogs.

The third mechanism is a two-step query strategy. Direct hotel-name lookups are attempted first because they offer the best precision. A query shaped like `Hotel Name, City, Country` can produce property-level coordinates when the hotel is well indexed. But the checkpoint shows the failure mode clearly: branded chain hotels such as Park Hyatt Seoul resolve, while boutique properties such as Cap Juluca and Il Pellicano often do not. If the pipeline stopped there, the long tail of luxury or independently branded properties would remain unresolved and the resulting catalog would be too incomplete to use.

City-centroid fallback is the recovery path. When the precise query misses, the pipeline retries with `City, Country` and accepts a city-level coordinate instead of a property-level one. This does not pretend to be exact. The point is to preserve usable spatial placement when the application's first-order requirement is map coverage and rough proximity ranking rather than turn-by-turn navigation. The checkpoint explicitly frames this as a trade: lower precision is acceptable in v1 because the alternative is dropping many hotels entirely. A centroid is worse than a rooftop coordinate, but much better than a null latitude/longitude pair that blocks the row from entering the app at all.

One way to reason about the trade-off is with a weighted coverage metric:

$$
\text{effective coordinate coverage} = \frac{\text{precise hits} + 0.5 \times \text{centroid hits}}{\text{normalized hotels}}
$$

This is not a universal formula; it is an operational intuition. Property-level matches count fully, while city-centroid fallbacks count partially because they preserve discoverability but weaken local accuracy. The checkpoint's design suggests that improving effective coverage matters more than chasing perfect precision everywhere on day one.

Another crucial part of the mechanism is explicit precision tracking. A well-designed fallback system does not silently flatten precise and approximate coordinates into one undifferentiated `lat/lng` pair. The checkpoint notes a `city-centroid:*` precision marker, which means the pipeline can remember that the coordinate came from a fallback rather than a hotel-name hit. That small annotation unlocks several downstream behaviors: the UI can eventually display confidence, future refreshes can prioritize centroid rows for manual correction, and diff logic can avoid overwriting a verified property coordinate with a lower-confidence fallback.

The concept also relies on separating "unresolved" from "failed permanently." Because the catalog schema requires coordinates, unresolved hotels are held back from CSV output instead of being imported half-complete. This preserves data integrity without pretending the pipeline is all-or-nothing. Some rows may already be good enough to write, while others remain in the queue for a resumed run or a better provider. In other words, resumable geocoding turns missing coordinates into a recoverable state, not a terminal collapse of the whole refresh.

Finally, the pattern works only when it is integrated with the broader validation and diff pipeline. A geocoder can supply coordinates, but it cannot decide whether those coordinates are trustworthy enough to mutate the production catalog. That is why this concept pairs naturally with [[Provenance-Aware Hotel Catalog Diffing for Mixed-Source Refresh]] and [[Validation-Gated Catalog Diffing and Auto-Apply]]. Geocoding recovers spatial data; the control layer decides what to do with it.

## Key Properties

- **Resumable execution:** periodic cache flushes let long-running batches survive interruption, provider throttling, or shell restarts.
- **Precision hierarchy:** the system prefers `Name, City, Country` and only falls back to `City, Country` when needed.
- **Schema-aligned behavior:** unresolved records are held back because downstream consumers require non-null coordinates.
- **Explicit confidence signaling:** fallback-derived coordinates can be labeled so later review or re-geocoding targets the weakest rows first.
- **Provider-aware pacing:** rate limits and user-agent requirements become part of pipeline design, not afterthoughts.

## Limitations

City-centroid fallback can stack many hotels on the same point, which weakens local ranking and can make dense destinations look artificially uniform on a map. Public geocoders may also miss transliterated names, island properties, or resorts whose canonical address differs from their marketing brand. Cache files improve reliability but can preserve stale or wrong answers if the upstream provider changes. And because the pattern accepts bounded imprecision for coverage, it requires downstream consumers that tolerate "close enough" coordinates rather than exact parcel geometry.

## Examples

```python
def resolve_hotel_coords(hotel, cache, geocode):
    key = f"{hotel['name']}|{hotel['city']}|{hotel['country']}"
    if key in cache:
        return cache[key]

    precise = geocode(f"{hotel['name']}, {hotel['city']}, {hotel['country']}")
    if precise:
        cache[key] = {**precise, "precision": "property"}
        return cache[key]

    centroid = geocode(f"{hotel['city']}, {hotel['country']}")
    if centroid:
        cache[key] = {**centroid, "precision": "city-centroid"}
        return cache[key]

    cache[key] = {"precision": "unresolved"}
    return cache[key]
```

In the checkpoint's concrete implementation, this strategy let the hotel refresh job keep progressing even when boutique-name lookups failed. The system accepted city-level placement for the hard cases, persisted that result to cache, and made the bulk geocode run resumable instead of brittle.

## Practical Applications

This concept fits travel catalogs, venue directories, property portfolios, trail and park guides, and any other location-heavy dataset where the source has strong names and locality metadata but weak or missing coordinates. It is especially useful when the consumer is a map or proximity surface, when public geocoders are the only acceptable providers, and when the operator needs a workflow that can run slowly and still converge over multiple passes.

## Related Concepts

- **[[Third-Party Map Ingestion for Location-Rich Travel Catalogs]]** — Describes the broader acquisition pattern; this concept handles the enrichment gap when the map export is not actually coordinate-rich enough.
- **[[Provenance-Aware Hotel Catalog Diffing for Mixed-Source Refresh]]** — Governs how low-confidence fallback coordinates should interact with curated or higher-authority rows.
- **[[Validation-Gated Catalog Diffing and Auto-Apply]]** — Supplies the safety model for deciding whether partially enriched results are safe to write.

## Sources

- [[Copilot Session Checkpoint: Implementing hotel auto-population pipeline]] — captures the cache design, rate-limit assumptions, fallback hierarchy, and the boutique-hotel miss cases that motivated the pattern.
