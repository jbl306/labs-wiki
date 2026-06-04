---
title: "Public Reservation Widget Availability Endpoints"
type: concept
created: 2026-06-04
last_verified: 2026-06-04
source_hash: "bc4ff46ec79a09c0988ecab531657aa46ffc64d566bc7f8883456e723cbdb79d"
sources:
  - raw/2026-06-04-doordash-going-out-sevenrooms-api-research.md
quality_score: 84
related:
  - "[[Partner-Gated Reservation APIs]]"
  - "[[Backend-For-Frontend (BFF) Pattern in Modern Dashboard Architecture]]"
tier: hot
tags: [reservations, widget, availability, reverse-engineering, sevenrooms]
---

# Public Reservation Widget Availability Endpoints

## Overview

Public reservation widget availability endpoints are read-oriented HTTP surfaces that restaurant booking widgets call before a user is authenticated or committed to a booking. They matter because they expose the minimum operational data needed to render open slots to anonymous browsers while still keeping the actual reservation workflow, customer data, and write operations behind stronger trust boundaries.

## How It Works

The key idea is architectural separation. A restaurant website needs to display whether tables are available for a given party size, date, or time range before a visitor can reasonably decide to book. If the site required partner credentials or a full private API session merely to display candidate slots, the widget would be difficult to embed and fragile to deploy. Public availability endpoints solve that problem by exposing a narrow slice of data: enough to answer "what looks bookable right now?" but not enough to hand over full operational control.

In the SevenRooms case captured by this source, community code repeatedly references a public endpoint at `https://www.sevenrooms.com/api-yoa/availability/widget/range`. The observed parameter set is instructive because it reveals the contract shape of the widget layer. Inputs such as `venue`, `start_date`, `num_days`, and `party_size` define the search envelope. Additional parameters such as `time_slot`, `halo_size_interval`, and `channel=SEVENROOMS_WIDGET` appear to refine how the widget asks for inventory and identify the caller as the public widget channel. Even without official docs, that parameter vocabulary tells you the endpoint is designed for discovery rather than account-level management.

The response pattern also follows the needs of a booking widget instead of a back-office API. The source notes medium-confidence evidence that responses are grouped around date, shift, and time-slot structures, with fields such as `time_iso`, `utc_datetime`, descriptive seating metadata, and `access_persistent_id` values associated with bookable slots. That is exactly the kind of payload a UI can transform into "7:00 PM patio," "7:30 PM standard table," or "join waitlist" options. It is not the shape you would expect for a full reservation ledger, client CRM object, or payment record.

Why does this design work? Because availability is operationally useful but relatively low-sensitivity compared with reservation mutations or guest profiles. A restaurant wants search engines, consumers, and marketplace partners to discover that it has inventory. The widget endpoint therefore acts like a public read facade in front of a much richer reservation system. It is intentionally constrained: it answers an availability query, but it does not by itself prove that a caller can create, modify, or cancel a reservation. That stronger authority is deferred to downstream flows, often involving authenticated applications, partner APIs, or server-side handoff layers.

This separation creates a very particular kind of observability for researchers. Public widget traffic can reveal venue slugs, search dimensions, and broad response schemas with minimal inference. It can support read-only mapping of how a platform exposes availability to the web. But the same visibility does not automatically reveal the booking mutation path. In practice, this means reverse engineering is asymmetric: discovery is often feasible from public browser traffic, while booking workflows remain opaque because they live behind a different interface family entirely.

There are important trade-offs. Public availability endpoints can be scraped, so platforms must balance utility against abuse risk. They may add rate limits, vary field names, or reserve the right to change the contract without notice because the interface is intended for first-party widgets, not third-party clients. That is why the source treats community examples as unstable and unsupported. A field like `access_persistent_id` may be observable today, but relying on it as if it were a documented public contract is risky. The concept is therefore best understood as a pattern: a deliberately narrow public read surface sitting in front of a more privileged booking backend.

## Key Properties

- **Anonymous read access:** The endpoint is designed to answer search-style availability queries without requiring partner credentials.
- **UI-shaped payloads:** Response fields are optimized for rendering time slots and seating options, not for representing full operational entities.
- **Narrow scope:** Inputs usually center on venue identity, party size, date range, and channel markers rather than account or billing state.
- **High observational value:** The surface is often the easiest place to infer venue identifiers, slot structure, and date/party-size constraints.
- **Contract instability:** Because the interface is effectively internal-to-widget plumbing, field names and request semantics may change without public notice.

## Limitations

Public availability endpoints do not provide a reliable foundation for privileged booking automation. They typically omit or abstract away identity, policy, payment, customer history, and write permissions. They may also be rate-limited, selectively exposed, or protected by anti-abuse controls. Most importantly, observing a public availability response does not mean a client has permission to create or alter a reservation.

## Examples

The source's community evidence suggests a query pattern like this:

```text
GET /api-yoa/availability/widget/range
  ?venue=<venue-slug>
  &start_date=2026-06-04
  &num_days=7
  &party_size=2
  &time_slot=DINNER
  &halo_size_interval=15
  &channel=SEVENROOMS_WIDGET
```

In practice, a widget would translate the response into a calendar or list of bookable times, then hand the user into a deeper booking flow for confirmation and guest data entry.

## Practical Applications

This concept is useful when analyzing hospitality platforms, marketplace integrations, and public booking widgets. It explains why a researcher may be able to safely map availability search behavior from public web traffic while still being unable to identify mutation endpoints. It is also relevant for product design: exposing a narrow availability surface can increase discoverability and partner distribution without exposing the full reservation system.

## Related Concepts

- **[[Partner-Gated Reservation APIs]]** — The private interface family that usually handles the actual booking, guest, and reporting workflows behind the public widget layer.
- **[[Backend-For-Frontend (BFF) Pattern in Modern Dashboard Architecture]]** — A useful architectural analogue for understanding how a narrow client-facing surface can sit in front of richer backend capabilities.

## Sources

- [[DoorDash Going Out and SevenRooms API Reverse Engineering Discovery]] — establishes the public SevenRooms widget endpoint, its observed parameters, and the visibility limits of read-only discovery.
