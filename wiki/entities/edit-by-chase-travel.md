---
title: The Edit by Chase Travel
type: entity
created: 2026-05-30
last_verified: 2026-05-30
source_hash: "436e060abf51c78f92d168896c46be67e679d4ba7f4e87e5f482189f4173389f"
sources:
  - raw/2026-05-30-copilot-session-researching-the-edit-hotel-auto-population-72a00d67.md
concepts: [authenticated-export-private-travel-catalogs, third-party-map-ingestion-location-rich-travel-catalogs]
related:
  - "[[Chase Sapphire Benefits v2]]"
  - "[[Automated Catalog Refresh Pipeline]]"
  - "[[Authenticated Export for Private Travel Catalogs]]"
  - "[[Third-Party Map Ingestion for Location-Rich Travel Catalogs]]"
tier: hot
tags: [chase-travel, hotel-program, travel-catalog, luxury-hotels, location-data, benefits-tracker]
---

# The Edit by Chase Travel

## Overview

The Edit by Chase Travel is Chase Travel's premium hotel collection, surfaced in the checkpoint as the target catalog for an automated hotel-ingestion workflow inside [[Chase Sapphire Benefits v2]]. Its practical importance comes from the combination of scale and product fit: the 2026 collection was described as having roughly 1,371 properties, while the consuming app currently tracks only 3 manually entered hotels.

The checkpoint makes clear that The Edit is easy to recognize as a travel program but hard to ingest directly from an open canonical source. Public Chase Travel marketing pages still exist, yet the full filterable inventory appears to sit behind an authenticated portal flow. That makes The Edit a good example of a semi-public data domain: widely marketed, operationally relevant, but not fully exposed in a clean public feed.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Travel Program |
| Created | Unknown |
| Creator | Chase Travel |
| URL | https://www.chase.com/travel/the-edit |
| Status | Active |

## Program Scope

The checkpoint records an estimated 2026 footprint of about 1,371 properties worldwide. It also identifies three named sub-collections within the program: **Hotel + Resort**, **All-In**, and **Boutique**. Those distinctions matter for ingestion because a future catalog should ideally preserve enough source fidelity to support filtering, comparison, or later enrichment by collection type.

## Data Surface and Update Constraints

The most important operational fact is that the public web does not appear to expose the full authoritative inventory. Direct Chase URLs either returned `404` or redirected into an authenticated Chase Travel experience, and the checkpoint explicitly describes "See All Stays" inside the portal as the source of truth for the complete hotel list. In other words, the official list exists, but the durable ingestion question is how to access it without teaching the app to store credentials or automate a private browsing session.

That constraint creates room for secondary evidence sources. The checkpoint notes several third-party maintained maps and lists, including a Google MyMaps world map hosted from the US Credit Card Guide ecosystem. Those sources matter less as branding artifacts than as structured location data: if they include names plus coordinates, they can drastically reduce enrichment work for the downstream app.

## Relevance to Workspace

For [[Chase Sapphire Benefits v2]], The Edit is not just another content collection. The app's hotel schema requires coordinates, supports map exploration, and ranks nearby properties with distance calculations, so the program's usable representation is a normalized, geospatially complete catalog rather than a simple list of hotel names. That makes source choice a first-order architectural decision, not a scraping implementation detail.

The checkpoint also connects The Edit work to the already-shipped [[Automated Catalog Refresh Pipeline]]. The earlier benefits pipeline established a deterministic fetch-validate-diff-apply pattern for public issuer data; this entity highlights the adjacent case where the real problem is choosing a trustworthy evidence source before the refresh machinery can be reused.

## Sources

- [[Copilot Session Checkpoint: Researching The Edit hotel auto-population]] — captures the size estimate, source-access constraints, candidate third-party lists, and the app-side data-model requirements.
