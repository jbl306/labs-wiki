---
title: "Copilot Session Checkpoint: Optimizing Snipe Book-Then-Retry Flow"
type: source
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "bb401f462b2e63524f82f4333d7d7a4473910a60cefc4b4025c3ece7601e0153"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-optimizing-snipe-book-then-retry-flow-a86837aa.md
quality_score: 100
concepts:
  - book-then-retry-booking-flow-optimization
related:
  - "[[Book-Then-Retry Booking Flow Optimization]]"
  - "[[Galloping-Bot]]"
  - "[[EZLinks API]]"
  - "[[Durable Copilot Session Checkpoint]]"
tier: hot
tags: [checkpoint, copilot-session, booking, automation, retry-strategy, golf, homelab, durable-knowledge, copilot, fileback]
---

# Copilot Session Checkpoint: Optimizing Snipe Book-Then-Retry Flow

## Summary

This session checkpoint documents the diagnosis and optimization of a golf tee-time sniping bot's booking flow. The user identified a bug causing missed bookings for a specific golf course and redesigned the booking retry logic from a retry-before-book approach to a more efficient book-then-retry two-pass strategy.

## Key Points

- Root cause was a retry loop that exited early when partial course results were found, missing other courses.
- Refactor of the booking flow to a two-pass book-then-retry approach that books available tee times immediately and retries only for missing courses.
- Technical details include API usage, course ID prioritization, environment variable tuning, and Docker image rebuilds.

## Concepts Extracted

- **[[Book-Then-Retry Booking Flow Optimization]]** — Book-Then-Retry is a booking flow strategy designed to optimize the process of reserving limited resources, such as golf tee times, by immediately booking available options before retrying for any missing ones. This approach improves efficiency and success rates compared to retry-before-book methods that may prematurely exit on partial results.

## Entities Mentioned

- **[[Galloping-Bot]]** — Galloping-Bot is a golf tee-time sniping bot designed to automatically search and book tee times for multiple golf courses using the EZLinks API. It supports configuration of multiple course IDs, booking limits per course, and retry logic to maximize booking success. The bot is implemented in Python, runs inside a Docker container, and is orchestrated via cron jobs.
- **[[EZLinks API]]** — EZLinks API is the backend service used by Galloping-Bot to search and book golf tee times. It provides a single search endpoint that returns available tee times for multiple courses in one response, enabling efficient filtering and booking by course ID and time window. The API supports player card access types and enforces booking limits.
- **[[Durable Copilot Session Checkpoint]]** — Durable Copilot Session Checkpoints are saved states of Copilot CLI sessions that capture intermediate work, fixes, and refactors. They serve as durable artifacts for knowledge retention and can be promoted into persistent wiki systems for compile-once ingestion and long-term reference.

## Notable Quotes

> ""The retry loop (`if search_result.tee_times: break`) exited immediately because Galloping Hill had results, never retrying for Ash Brook."" — Durable Session Summary
> ""Redesigned from retry-then-book to book-then-retry strategy: Pass 1: Search → book whatever's available immediately; Pass 2: If any courses unfilled, wait snipe_delay, search again, book remaining."" — Durable Session Summary

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-optimizing-snipe-book-then-retry-flow-a86837aa.md` |
| Type | note |
| Author | Unknown |
| Date | 2026-04-18T03:23:51.483387Z |
| URL | N/A |
