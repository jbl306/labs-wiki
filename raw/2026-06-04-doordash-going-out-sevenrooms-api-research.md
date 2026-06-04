---
title: "DoorDash Going Out and SevenRooms API Reverse Engineering Discovery"
type: note
captured: 2026-06-04T00:35:00Z
source: autoresearch
rounds: 3
sources:
  - url: https://www.businesswire.com/news/home/20250930891127/en/DoorDash-Launches-Going-Out-Adding-Reservations-and-In-Store-Rewards-to-the-App
    title: "DoorDash Launches Going Out, Adding Reservations and In-Store Rewards to the App"
    quality: primary
  - url: https://sevenrooms.com/platform/doordash-reservations/
    title: "DoorDash Reservations - SevenRooms"
    quality: primary
  - url: https://api-docs.sevenrooms.com/
    title: "SevenRooms API Documentation"
    quality: primary
  - url: https://www.restaurantdive.com/news/doordash-going-out-in-store-rewards-reservations/761445/
    title: "DoorDash launches dine-in rewards, reservations"
    quality: secondary
  - url: https://www.restaurantdive.com/news/DoorDash-acquires-sevenrooms-1-billion/747226/
    title: "DoorDash to buy SevenRooms for $1.2B"
    quality: secondary
  - url: https://docs.kleene.ai/docs/sevenrooms
    title: "SevenRooms - Kleene Docs"
    quality: secondary
  - url: https://raw.githubusercontent.com/mvanhorn/printing-press-library/b2ce7c20e84e179638e243bb1426d88fa9e5177e/library/commerce/doordash/README.md
    title: "Doordash CLI README"
    quality: community
  - url: https://raw.githubusercontent.com/mvanhorn/printing-press-library/b2ce7c20e84e179638e243bb1426d88fa9e5177e/library/commerce/doordash/spec.yaml
    title: "DoorDash GraphQL Operation Spec"
    quality: community
confidence: medium
tags: [doordash, sevenrooms, reservations, api-discovery, reverse-engineering]
status: ingested
---

# DoorDash Going Out and SevenRooms API Reverse Engineering Discovery

## Summary

Public sources support a medium-confidence conclusion: SevenRooms availability discovery is partly reverse-engineerable through public reservation widget traffic, while official SevenRooms booking/data APIs and DoorDash's new Going Out reservation marketplace are gated behind partner/account access. DoorDash's existing consumer web APIs are known to use GraphQL for food-ordering flows, but the public community specs found during this run do not yet expose Going Out/reservation operations.

## Key Findings

- DoorDash announced Going Out as an app feature that combines reservations, in-store rewards, and exclusive DashPass offers. The announcement says in-app reservations debut in Miami and New York and expand through the SevenRooms partnership. (BusinessWire DoorDash announcement)
- DoorDash says restaurants using SevenRooms can offer reservations directly through the DoorDash app with zero cover fees, enriched guest profiles, Voice AI, event management, and a 360-degree guest view across delivery, pickup, walk-ins, and reservations. (BusinessWire DoorDash announcement; SevenRooms DoorDash Reservations page)
- SevenRooms' public DoorDash Reservations page says availability can be showcased directly in the DoorDash app, exclusive tables/offers can be adjusted, bookings flow into SevenRooms, and DoorDash/SevenRooms guest data can be integrated into one SevenRooms platform view. (SevenRooms DoorDash Reservations page)
- Official SevenRooms API documentation exists but is no longer publicly readable without individually provisioned documentation access. New API users are directed to a partnerships form; previously provisioned users are directed to api-integration-support@sevenrooms.com. (SevenRooms API Documentation landing page)
- Secondary connector documentation confirms the official SevenRooms API requires a Venue Group ID, Client ID, Client Secret, Base URL, and permissions. It references official operations for venues, reservation requests, reservations export, events, clients, charges, and feedback. (Kleene SevenRooms docs)
- Public GitHub code references repeatedly show a public SevenRooms widget availability endpoint: `https://www.sevenrooms.com/api-yoa/availability/widget/range` with parameters such as `venue`, `time_slot`, `party_size`, `halo_size_interval`, `start_date`, `num_days`, and `channel=SEVENROOMS_WIDGET`. These examples are community code and should be treated as unstable/unsupported. (GitHub public code search results from jasonpraful/sevenrooms, francisbulus/eek, xunhuang/yumyum-v2)
- A public DoorDash community spec says DoorDash web traffic uses GraphQL endpoints under `https://www.doordash.com/graphql/<operation>?operation=<operation>`, cookie auth plus CSRF, and operations such as `autocompleteFacetFeed`, `storepageFeed`, `itemPage`, `listCarts`, `checkout`, and `createOrderFromCart`. It explicitly describes the spec as sniffed/browser-captured and not official. (mvanhorn/printing-press-library DoorDash README and spec.yaml)
- That DoorDash community spec appears focused on delivery/cart/order flows. No Going Out or reservations operation was found in the inspected public DoorDash spec. (mvanhorn/printing-press-library DoorDash README and spec.yaml)
- GitHub code search briefly hit a rate limit during this run, so broad GitHub searching was stopped and the remaining work used already-identified raw/official pages. (session observation)

## Mechanisms / How It Works

### SevenRooms layers

1. Public widget availability: many restaurant sites embed SevenRooms widgets that call a public availability endpoint. This can expose venue slugs, date/time/party-size search, and available slot metadata.
2. Official SevenRooms APIs: documentation access is gated. Public secondary connector docs indicate these APIs use customer/partner credentials and support operational/reporting data such as reservations, clients, reservation requests, events, charges, and feedback.
3. DoorDash Reservations marketplace: DoorDash and SevenRooms state that DoorDash app bookings flow into SevenRooms with enriched DoorDash guest profile tags. The consumer-facing DoorDash app API surface for this marketplace is not publicly documented in the sources found.

### DoorDash layers

1. Web consumer GraphQL: public community research documents DoorDash web GraphQL operations for food-ordering/search/cart flows.
2. Mobile Going Out/reservations: likely uses DoorDash authenticated mobile or BFF APIs plus SevenRooms backend integration, but endpoint names and schemas were not found in public docs during this run.
3. Booking mutation boundary: creating or modifying reservations would likely require authenticated DoorDash user state and/or SevenRooms partner credentials. It should be treated as high-risk and not automated without explicit authorization and guardrails.

## Practical Extent of Reverse Engineering

- High confidence: identify SevenRooms widget venue slugs and query read-only public availability for a known venue/date/party size with very low-frequency requests.
- Medium confidence: infer the shape of availability responses from community code: availability grouped by date/shift/times, with fields such as `time_iso`, `utc_datetime`, seating/description fields, and `access_persistent_id` for bookable slots.
- Medium confidence: map existing DoorDash web GraphQL conventions for non-reservation surfaces: operation-specific `/graphql/<operation>?operation=<operation>`, POST JSON body, cookies/CSRF for authenticated surfaces.
- Low confidence without live owned-account capture: enumerate DoorDash Going Out/reservation GraphQL or mobile BFF operation names, request variables, auth headers, and response schemas.
- Not supportable from public sources alone: safely create/cancel reservations through DoorDash Going Out, retrieve enriched guest profiles, or access official SevenRooms partner APIs without approved credentials.

## Rate Limit and Safety Notes

- Avoid broad automated GitHub/code searches; a GitHub rate limit was reached during this research.
- Avoid live probing DoorDash or SevenRooms production APIs beyond minimal, human-scale checks.
- Do not attempt auth bypass, anti-bot bypass, TLS-pinning bypass, credential extraction, or automated booking.
- If doing further owned-account discovery, keep it read-only first, capture a single manual session, redact cookies/tokens/PII, and add hard gates before any mutation.

## Open Questions

- What exact DoorDash app/BFF operation powers Going Out reservation search?
- Does DoorDash pass bookings through a DoorDash-owned marketplace service into SevenRooms, or expose SevenRooms availability directly through a DoorDash wrapper?
- Are Going Out reservations available through DoorDash web, mobile only, or both?
- What public/private rate limits apply to SevenRooms widget availability and DoorDash reservation search?

## Sources

- BusinessWire / DoorDash: `https://www.businesswire.com/news/home/20250930891127/en/DoorDash-Launches-Going-Out-Adding-Reservations-and-In-Store-Rewards-to-the-App`
- SevenRooms DoorDash Reservations: `https://sevenrooms.com/platform/doordash-reservations/`
- SevenRooms API docs landing: `https://api-docs.sevenrooms.com/`
- Restaurant Dive Going Out coverage: `https://www.restaurantdive.com/news/doordash-going-out-in-store-rewards-reservations/761445/`
- Restaurant Dive SevenRooms acquisition coverage: `https://www.restaurantdive.com/news/DoorDash-acquires-sevenrooms-1-billion/747226/`
- Kleene SevenRooms connector docs: `https://docs.kleene.ai/docs/sevenrooms`
- Public DoorDash community spec: `https://raw.githubusercontent.com/mvanhorn/printing-press-library/b2ce7c20e84e179638e243bb1426d88fa9e5177e/library/commerce/doordash/README.md`
- Public DoorDash community spec YAML: `https://raw.githubusercontent.com/mvanhorn/printing-press-library/b2ce7c20e84e179638e243bb1426d88fa9e5177e/library/commerce/doordash/spec.yaml`
