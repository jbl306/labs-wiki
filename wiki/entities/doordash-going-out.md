---
title: DoorDash Going Out
type: entity
created: 2026-06-04
last_verified: 2026-06-04
source_hash: "bc4ff46ec79a09c0988ecab531657aa46ffc64d566bc7f8883456e723cbdb79d"
sources:
  - raw/2026-06-04-doordash-going-out-sevenrooms-api-research.md
concepts: [partner-gated-reservation-apis]
related:
  - "[[SevenRooms API]]"
  - "[[Public Reservation Widget Availability Endpoints]]"
tier: hot
tags: [doordash, reservations, marketplace, rewards, sevenrooms]
---

# DoorDash Going Out

## Overview

DoorDash Going Out is DoorDash's dine-in marketplace feature that adds restaurant reservations, in-store rewards, and DashPass-linked offers to the consumer app. The source material ties its reservation rollout directly to a SevenRooms partnership, making it an example of a consumer marketplace sitting on top of a private hospitality operations stack.

The feature matters because it extends DoorDash beyond delivery logistics into restaurant discovery and on-premise spend. From a systems perspective, it also creates a clean separation between what customers see in the app and what likely happens behind the scenes through authenticated marketplace and partner APIs.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Product Feature |
| Created | 2025-09-30 |
| Creator | DoorDash |
| URL | https://www.businesswire.com/news/home/20250930891127/en/DoorDash-Launches-Going-Out-Adding-Reservations-and-In-Store-Rewards-to-the-App |
| Status | Active |

## Product Scope

The announcement cited in the source describes Going Out as a bundled hospitality surface rather than a narrow booking button. It combines reservation search, in-store rewards, and exclusive DashPass offers, with initial reservation availability in Miami and New York. Restaurants using SevenRooms can surface bookable inventory in the DoorDash app without paying cover fees, while still operating from their existing reservation system.

## Integration Model

DoorDash states that bookings made in the app flow into SevenRooms. The SevenRooms partner page adds that restaurants can manage exclusive tables and offers, enrich guest profiles with DoorDash data, use Voice AI, and maintain a 360-degree guest view across delivery, pickup, walk-ins, and reservations. That implies Going Out is not just a read-only search layer; it is a marketplace workflow that hands off booking and guest context into a deeper restaurant platform.

## Research Implications

For reverse-engineering and interface mapping, Going Out is important mainly because it marks the mutation boundary. Public sources in this ingest did not reveal a public DoorDash reservation API or GraphQL operation for the feature. The evidence instead suggests that any real booking flow requires authenticated DoorDash user state, a private app or BFF layer, and a downstream integration into SevenRooms' gated partner APIs.
