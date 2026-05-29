---
title: Chase Sapphire Benefits v2
type: entity
created: 2026-05-29
last_verified: 2026-05-29
source_hash: "5f3a4872a42695aaa980acb96649f300ff224cbd0c4834bd58a2c691a0351c9a"
sources:
  - raw/2026-05-29-copilot-session-implementing-csr-benefits-ui-ux-uplift-72d037fa.md
concepts:
  - phased-ux-uplift-manual-first-nextjs-benefits-apps
  - redirect-safe-client-feedback-nextjs-server-actions
related:
  - "[[Durable Copilot Session Checkpoint]]"
  - "[[Copilot CLI]]"
  - "[[Tailwind CSS 4]]"
tier: hot
tags: [benefits-tracker, nextjs, prisma, sqlite, manual-first, privacy-preserving]
---

# Chase Sapphire Benefits v2

## Overview

Chase Sapphire Benefits v2 is a private, manual-first web application for tracking and using cardholder benefits connected to the Chase Sapphire ecosystem. In the checkpoint source it appears as a Next.js 16 App Router application with TypeScript, Prisma 6, SQLite, and [[Tailwind CSS 4]], with dedicated dashboard, benefits, places, and quick-add flows.

What makes the project notable is the combination of product ambition and strict privacy boundaries. The source is explicit that the app must not store Chase credentials, must not use Plaid, must not scrape issuer systems, and should rely on key-less map tiles. The resulting architecture favors local state, manually entered events, and carefully chosen client islands over cloud-dependent automation.

## Key Facts

| Field | Value |
|-------|-------|
| Type | Application |
| Created | Unknown |
| Creator | Unknown |
| URL | N/A |
| Status | Active |

## Product Scope

The product surface described in the checkpoint includes a home dashboard, a benefits explorer, a places view, and a quick-add workflow for recording benefit usage. The UX refresh was benchmarked against sites such as AwardHelper, AwardFares, seats.aero, point.me, CreditFlow, and MaxMyPoint, but the goal was not feature cloning. The goal was to reach a similar level of polish and navigability while staying aligned with a private operator workflow.

## Architecture Snapshot

The app combines server-rendered pages with narrowly scoped client components. Server code prepares serializable summaries and search indexes; client islands then handle filter/sort density controls, toast-driven action feedback, command-palette navigation, and the Leaflet-based map surface. This keeps the overall system close to the data model while still making the UI feel responsive.

The checkpoint also records two operational details that matter for anyone touching the app later. First, Prisma resolves `file:./dev.sqlite` relative to the `prisma/` directory, which means the real seeded development database sits at `prisma/dev.sqlite`. Second, redirecting server actions behave differently from revalidate-only actions, so interactive feedback wrappers must be applied selectively.

## Current Uplift Status

At the time captured by the source, phases 0 through 4 of the UI/UX uplift were complete: the design system, app shell, dashboard visualization, benefits explorer, and places map all existed and had been typechecked or built successfully. Phase 5 was actively in progress and left the quick-add page broken mid-edit because `benefitOptions` had not yet been defined. That makes the checkpoint especially useful as a handoff artifact: it captures both what is already durable and what exact line of work remained open.

## Related Concepts

- **[[Phased UX Uplift for Manual-First Next.js Benefits Apps]]** — Describes the page-by-page modernization strategy used for the app.
- **[[Redirect-Safe Client Feedback for Next.js Server Actions]]** — Captures the action-wrapper rule that shaped the quick-add and dashboard interactions.

## Sources

- [[Copilot Session Checkpoint: Implementing CSR benefits UI/UX uplift]] — Primary checkpoint documenting the app's architecture and the in-progress uplift.
