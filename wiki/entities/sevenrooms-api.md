---
title: SevenRooms API
type: entity
created: 2026-06-04
last_verified: 2026-06-04
source_hash: "bc4ff46ec79a09c0988ecab531657aa46ffc64d566bc7f8883456e723cbdb79d"
sources:
  - raw/2026-06-04-doordash-going-out-sevenrooms-api-research.md
concepts: [public-reservation-widget-availability-endpoints, partner-gated-reservation-apis]
related:
  - "[[DoorDash Going Out]]"
  - "[[Public Reservation Widget Availability Endpoints]]"
  - "[[Partner-Gated Reservation APIs]]"
tier: hot
tags: [sevenrooms, api, reservations, hospitality, partner-integration]
---

# SevenRooms API

## Overview

The SevenRooms API is the credentialed integration surface behind SevenRooms' reservation, guest, and venue-management workflows. In the ingested source, its public documentation landing page is visible, but the substantive docs are access-controlled and routed through a partnerships flow, which makes it materially different from the publicly callable widget traffic that restaurant sites use for anonymous availability search.

This distinction matters because it defines the real trust boundary in the SevenRooms ecosystem. Public widget endpoints can expose enough information to discover availability patterns, but the operational APIs that move reservations, export data, and manage customer records remain gated behind partner credentials and approval.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Partner API Platform |
| Created | Unknown |
| Creator | SevenRooms |
| URL | https://api-docs.sevenrooms.com/ |
| Status | Active |

## Access Model

The source notes that the API documentation is no longer openly readable. New integrators are directed to a partnerships form, while previously provisioned users are pointed to `api-integration-support@sevenrooms.com`. Secondary connector documentation adds concrete integration requirements: a Venue Group ID, Client ID, Client Secret, Base URL, and explicit permissions.

## Operational Surface

The same secondary documentation references official operations for venues, reservation requests, reservations export, events, clients, charges, and feedback. That indicates the API is not limited to a narrow booking mutation; it is a broader hospitality data layer that supports reporting, guest CRM, operational workflows, and partner platform integrations such as [[DoorDash Going Out]].

## Public vs. Private Boundary

The source is especially valuable because it separates two layers that are easy to conflate. Community code repeatedly references a public SevenRooms widget availability endpoint used by embedded restaurant widgets. That endpoint is useful for read-only discovery, but it is not equivalent to the official SevenRooms API described in partner docs. The private API layer carries more operational power, stronger authentication requirements, and higher sensitivity because it likely governs booking creation, reservation exports, client records, and other privileged actions.
