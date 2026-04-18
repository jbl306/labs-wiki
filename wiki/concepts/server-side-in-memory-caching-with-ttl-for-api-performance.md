---
title: "Server-Side In-Memory Caching with TTL for API Performance"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "f073ae4fd7b3295570081cdf37f1d67fc5c9838cf1ce8f2aa7e1d9409b01f107"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-rankings-page-and-performance-optimization-8063e05f.md
quality_score: 100
concepts:
  - server-side-in-memory-caching-with-ttl-for-api-performance
related:
  - "[[Copilot Session Checkpoint: Rankings Page and Performance Optimization]]"
tier: hot
tags: [caching, ttl, api-performance, server-side, in-memory-cache]
---

# Server-Side In-Memory Caching with TTL for API Performance

## Overview

Server-side in-memory caching stores the results of expensive API calls temporarily in memory with a time-to-live (TTL) expiration. This reduces repeated database queries for frequently requested data that changes infrequently, improving API responsiveness and reducing backend load.

## How It Works

The caching mechanism wraps API handler functions with a cache layer that stores the response keyed by request parameters. When a request arrives, the cache is checked first. If a valid cached response exists (not expired), it is returned immediately, bypassing database queries and computation. If not, the handler executes normally, and the result is stored in the cache with a TTL. The TTL ensures data freshness by expiring cached entries after a set duration, forcing periodic recomputation. In this NBA ML Engine, a `cached()` helper function was implemented with TTL-based in-memory cache. Slow endpoints like `/api/rankings` and `/api/backtest` were wrapped with this cache, using TTLs of 5 minutes or 2 minutes depending on data volatility. This approach balances performance with data freshness, preventing stale data from persisting indefinitely. The cache lives in server memory, so it is fast but ephemeral, resetting on server restarts. For distributed or persistent caching, external stores like Redis would be used.

## Key Properties

- **TTL Expiration:** Controls cache freshness by expiring entries after a set time.
- **Memory-Based:** Fast access but limited by server memory and non-persistent.
- **Keyed by Request Parameters:** Ensures cache entries correspond to unique API queries.

## Limitations

Cache invalidation is challenging; data may be stale until TTL expires. Memory usage grows with cache size. Not suitable for highly dynamic data without very short TTLs. Server restarts clear cache.

## Example

The `/api/rankings` endpoint was wrapped with `cached()` with a 5-minute TTL. When a client requests rankings, the first request queries the database and caches the result. Subsequent requests within 5 minutes return cached data instantly, reducing endpoint latency from over 20 seconds to milliseconds.

## Relationship to Other Concepts

- **Backend-For-Frontend (BFF) Pattern in Dashboard Architecture** — Caching is implemented within the BFF layer to optimize API responses.

## Practical Applications

Widely used in web APIs serving dashboards, reports, or any data that changes periodically. Improves user experience by reducing load times and backend resource consumption.

## Sources

- [[Copilot Session Checkpoint: Rankings Page and Performance Optimization]] — primary source for this concept
