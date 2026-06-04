---
title: "DoorDash Going Out and SevenRooms API Reverse Engineering Discovery"
type: source
created: '2026-06-04'
last_verified: '2026-06-04'
source_hash: bc4ff46ec79a09c0988ecab531657aa46ffc64d566bc7f8883456e723cbdb79d
sources:
  - raw/2026-06-04-doordash-going-out-sevenrooms-api-research.md
tags: [doordash, sevenrooms, reservations, api-discovery, reverse-engineering, graphql]
tier: hot
knowledge_state: ingested
ingest_method: copilot-cli-gpt-5.4
quality_score: 75
---

# DoorDash Going Out and SevenRooms API Reverse Engineering Discovery

## Summary

This research note maps the public and private interface layers around [[DoorDash Going Out]] and the [[SevenRooms API]]. Its core conclusion is that SevenRooms exposes a partially observable public availability layer through embedded widgets, while booking, guest-profile, and operational workflows remain inside credentialed partner APIs that also appear to power DoorDash's reservation integration.

## Key Points

- DoorDash positioned [[DoorDash Going Out]] as a dine-in expansion that combines reservations, in-store rewards, and exclusive DashPass offers, with initial launch markets in Miami and New York.
- DoorDash's SevenRooms partnership lets participating restaurants surface availability in the DoorDash app with zero cover fees, while bookings flow back into SevenRooms alongside enriched guest profile data and event-management workflows.
- The most concrete publicly observable SevenRooms interface is the widget availability endpoint discussed by community code: `https://www.sevenrooms.com/api-yoa/availability/widget/range`.
- Community examples indicate that the widget layer accepts parameters such as `venue`, `time_slot`, `party_size`, `halo_size_interval`, `start_date`, `num_days`, and `channel=SEVENROOMS_WIDGET`, and returns slot-oriented availability metadata.
- SevenRooms' official API documentation is no longer openly readable; new users are directed to a partnerships form, while already provisioned users are routed to support for access.
- Secondary connector documentation describes the official [[SevenRooms API]] as a credentialed surface requiring a Venue Group ID, Client ID, Client Secret, Base URL, and permissions for operations such as venues, reservation requests, reservations export, events, clients, charges, and feedback.
- Public community DoorDash traffic research shows a GraphQL-heavy consumer web surface for ordering flows, but this source did not find public Going Out or reservation operations in the inspected community specs.
- The strongest reverse-engineering conclusion is read-only discovery: public widget traffic can reveal venue identifiers and availability structure, while booking mutations and guest-data access should be treated as partner-gated.
- The likely DoorDash reservation integration boundary resembles a mobile or [[Backend-For-Frontend (BFF) Pattern in Modern Dashboard Architecture]] surface layered on top of SevenRooms' private partner interfaces, but the exact operation names and schemas were not available in public documentation.

## Key Concepts

- [[Public Reservation Widget Availability Endpoints]]
- [[Partner-Gated Reservation APIs]]
- [[Backend-For-Frontend (BFF) Pattern in Modern Dashboard Architecture]]

## Related Entities

- **[[DoorDash Going Out]]** — DoorDash's dine-in reservations and rewards feature that appears to use SevenRooms as a fulfillment and guest-data partner.
- **[[SevenRooms API]]** — The gated reservation and guest-management API family behind the partnership and back-office workflows.
