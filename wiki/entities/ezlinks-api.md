---
title: "EZLinks API"
type: entity
created: 2026-04-18
last_verified: 2026-04-22
source_hash: "bb401f462b2e63524f82f4333d7d7a4473910a60cefc4b4025c3ece7601e0153"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-optimizing-snipe-book-then-retry-flow-a86837aa.md
quality_score: 62
concepts:
  - ezlinks-api
related:
  - "[[Book-Then-Retry Booking Flow Optimization]]"
  - "[[Copilot Session Checkpoint: Optimizing Snipe Book-Then-Retry Flow]]"
  - "[[Galloping-Bot]]"
  - "[[Durable Copilot Session Checkpoint]]"
tier: hot
tags: [api, booking, golf]
---

# EZLinks API

## Overview

EZLinks API is the backend service used by Galloping-Bot to search and book golf tee times. It provides a single search endpoint that returns available tee times for multiple courses in one response, enabling efficient filtering and booking by course ID and time window. The API supports player card access types and enforces booking limits.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Tool |
| Created | Unknown |
| Creator | Unknown |
| URL | N/A |
| Status | Active |

## Relevance

EZLinks API is the critical external system that Galloping-Bot interacts with to perform tee time searches and bookings. Its design influences the bot's booking flow and retry strategies.

## Associated Concepts

- **[[Book-Then-Retry Booking Flow Optimization]]** — The API's single search endpoint enables the two-pass booking strategy.

## Related Entities

- **[[Galloping-Bot]]** — co-mentioned in source (Tool)
- **[[Durable Copilot Session Checkpoint]]** — co-mentioned in source (Concept)

## Sources

- [[Copilot Session Checkpoint: Optimizing Snipe Book-Then-Retry Flow]] — where this entity was mentioned
