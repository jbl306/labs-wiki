---
title: "Book-Then-Retry Booking Flow Optimization"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "bb401f462b2e63524f82f4333d7d7a4473910a60cefc4b4025c3ece7601e0153"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-optimizing-snipe-book-then-retry-flow-a86837aa.md
quality_score: 100
concepts:
  - book-then-retry-booking-flow-optimization
related:
  - "[[Durable Copilot Session Checkpoint Promotion]]"
  - "[[Copilot Session Checkpoint: Optimizing Snipe Book-Then-Retry Flow]]"
tier: hot
tags: [booking, automation, retry-strategy, optimization]
---

# Book-Then-Retry Booking Flow Optimization

## Overview

Book-Then-Retry is a booking flow strategy designed to optimize the process of reserving limited resources, such as golf tee times, by immediately booking available options before retrying for any missing ones. This approach improves efficiency and success rates compared to retry-before-book methods that may prematurely exit on partial results.

## How It Works

The Book-Then-Retry strategy operates in two distinct passes:

1. **Pass 1 - Immediate Booking:** The system performs a search for available tee times across multiple courses. It immediately books any available tee times found for each course, respecting per-course booking limits. This ensures that any available slots are secured without delay.

2. **Pass 2 - Retry for Missing Courses:** After the initial booking, the system checks if any courses remain unbooked. If so, it waits for a configured delay (e.g., 2 seconds) to allow for new tee times to be released or become available. It then performs a second search and attempts to book tee times only for those courses that were not booked in the first pass.

This approach contrasts with the previous retry-before-book method, where the system would retry searching multiple times before booking, which could cause premature exit if any course returned results, even if other courses had none.

The implementation involves refactoring the core booking function `_search_and_book` to return a dictionary mapping course IDs to the number of bookings made, and to accept this dictionary as input to accumulate bookings across passes. The retry loop is replaced by explicit two-pass logic in the `snipe_tee_time` function.

**Key algorithmic steps:**
- Search tee times for all configured courses.
- Filter and book available tee times per course up to a maximum booking cap.
- Accumulate booking counts per course.
- If any course remains unbooked, wait for a delay and repeat search and booking only for those courses.

This method ensures that courses with available tee times are booked immediately, while still allowing a retry for courses that may release times slightly later. It reduces missed bookings caused by early loop exit and improves overall booking success.

**Trade-offs and edge cases:**
- The delay between passes must be tuned to balance responsiveness and likelihood of new tee times appearing.
- The approach assumes that the search endpoint returns all courses’ tee times in one call, enabling efficient filtering.
- If tee times are released asynchronously or unpredictably, multiple retries might be needed, but the design limits retries to one for efficiency.
- The booking priority is maintained by ordering courses in the configuration, ensuring higher priority courses are booked first.

This strategy is particularly effective in scenarios where multiple similar resources are released simultaneously but may appear at slightly different times.

## Key Properties

- **Two-Pass Booking:** First pass books all immediately available tee times; second pass retries only for missing courses.
- **Per-Course Booking Limits:** Each course has a maximum booking count (e.g., 1), enforced during booking.
- **Retry Delay:** Configurable delay (e.g., 2 seconds) between passes to allow new tee times to appear.
- **Booking Priority:** Courses are booked in priority order defined by COURSE_IDS.

## Limitations

This approach assumes a single search endpoint returns tee times for all courses, which may not generalize to systems with separate endpoints. The single retry pass may not suffice if tee times are released with longer delays or irregular intervals. Also, the method depends on accurate course ID filtering and booking caps; misconfiguration can cause missed bookings or overbooking. Immediate booking may fail if the API or system has rate limits or concurrency constraints.

## Example

Pseudocode for the two-pass book-then-retry flow:

```python
booked_by_course = {}

# Pass 1: Search and book immediately
booked_by_course = _search_and_book(course_ids=all_courses, booked_by_course=booked_by_course)

# Check for unbooked courses
unbooked_courses = [cid for cid in all_courses if booked_by_course.get(cid, 0) < MAX_BOOKINGS]

if unbooked_courses:
    sleep(SNIPE_DELAY_SECONDS)
    # Pass 2: Retry booking only for unbooked courses
    booked_by_course = _search_and_book(course_ids=unbooked_courses, booked_by_course=booked_by_course)

return booked_by_course
```

## Relationship to Other Concepts

- **[[Durable Copilot Session Checkpoint Promotion]]** — This concept is an example of a durable checkpoint promoted for reliable workflow optimization.

## Practical Applications

This booking flow optimization is applicable to any automated reservation system where multiple resources are released asynchronously but need to be booked quickly and reliably. Examples include sports facility bookings, ticket sniping bots, or limited product release bots. The strategy reduces missed opportunities caused by premature retry loop exits and improves resource utilization efficiency.

## Sources

- [[Copilot Session Checkpoint: Optimizing Snipe Book-Then-Retry Flow]] — primary source for this concept
