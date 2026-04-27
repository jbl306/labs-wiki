---
title: "Single-User Local SQLite Migration for Self-Hosted Web Apps"
type: concept
created: 2026-04-27
last_verified: 2026-04-27
source_hash: f05f51c65d6378e15448fa0d095133e89e8748f012e2613260b283a03ff2836c
sources:
  - raw/2026-04-27-copilot-session-homelab-migration-and-tunnel-fix-78392c21.md
related:
  - "[[Homelab Infrastructure Patterns for AI Memory Migration]]"
  - "[[Native-Module-Safe Docker Builds and UID-Aligned SQLite Mounts]]"
  - "[[Homelab Service Inventory And Dashboard Synchronization]]"
tier: hot
tags: [sqlite, self-hosting, migration, nuxt, supabase, single-user]
---

# Single-User Local SQLite Migration for Self-Hosted Web Apps

## Overview

Single-user local SQLite migration is a pattern for taking a web app that assumed hosted authentication and remote persistence, then reshaping it into a self-hosted service optimized for one trusted operator. The key move is not merely swapping one database for another; it is collapsing the application's trust model, state model, and deployment assumptions so the software behaves naturally inside a homelab instead of pretending to be a SaaS product.

This matters because many personal or household tools inherit unnecessary complexity from cloud-first starters such as Supabase auth modules, multi-tenant session flows, and environment layouts built for platforms like Vercel. In a homelab, that complexity adds operational burden without adding meaningful value. A local SQLite migration removes those layers while still preserving durable state, encryption for sensitive settings, and stable API boundaries.

## How It Works

The pattern starts by identifying which parts of the app are genuinely product logic and which parts are just artifacts of its original hosting model. In this checkpoint, the hosted assumptions were easy to spot: `@nuxtjs/supabase`, Supabase-backed tables for settings and download history, auth pages, route guards, and a Vercel-oriented deployment shape. None of those were fundamental to the user's actual goal, which was a private downloader running in a trusted homelab. The migration therefore treated Supabase not as a feature to re-host, but as an implementation detail to remove.

The first major step is to define a local persistence core with a simpler operational contract. SQLite is attractive here because it gives ACID storage, file-based durability, and no separate service dependency. But the more important design choice is *where* the rewrite boundary sits. Instead of forcing the whole codebase to learn a new persistence API, the session introduced a dedicated `local-store.ts` for schema creation and CRUD while preserving helper names in the old `supabase.ts` wrapper. That meant functions like `getUserSetting`, `getUserSettings`, `setUserSetting`, and `getAllSettingsForUI` could keep their call sites, even though the implementation underneath now used a local encrypted database. This is a migration pattern worth preserving: keep the call surface stable, move the storage semantics underneath it.

The second step is collapsing authentication into the true trust model of the deployment. In a public SaaS, authentication exists to separate users from one another and to protect provider-managed state. In a private homelab app used by one operator, those requirements usually disappear. The checkpoint therefore replaced the app's previous auth flow with a fixed local identity: `id: 'local-user'` and `email: 'local@homelab'`. This is not a hack; it is an explicit statement that the deployment boundary now provides the trust perimeter. The complexity budget once spent on login pages, password resets, and route guards is instead spent on deployment reliability and local-state correctness.

A third step is carefully separating *state confidentiality* from *identity complexity*. Removing hosted auth does not mean removing all security concerns. The session kept AES-256-GCM encryption for sensitive settings, but repurposed it as local-at-rest protection instead of SaaS-backed secret storage. This is a subtle but important design move. It lets the migration stay honest about what needs protection while refusing to keep a whole remote identity subsystem alive just to justify a few encrypted fields. In other words, the app becomes single-user, not careless.

The fourth step is adapting request flows and UI assumptions to the new model. Because the auth layer is gone, pages no longer need middleware gating, logout UI, or "current user" chrome. API wrappers become simpler because there is no session token choreography to preserve. Download routes stop reading and writing remote tables and instead call local helper functions. The migration is successful when the user still sees coherent product behavior—settings persist, downloads appear, searches work—but can no longer tell that the old app was built around a remote backend.

A fifth step is aligning external integrations with the self-hosted reality. In this source, torrent acquisition became multi-source and operator-controlled rather than implicitly centralized around one public upstream. `NUXT_TORRENTIO_SOURCES` / `TORRENTIO_SOURCES` now describe a prioritized list of providers, with **[[KnightCrawler]]** promoted above public Torrentio. That is conceptually part of the same migration: once the app is local-first, it should also prefer local infrastructure first. The persistence layer, auth model, and upstream dependency order all become expressions of the same deployment philosophy.

The main intuition behind this pattern is that homelab migrations work best when they remove whole categories of assumptions instead of emulating them locally. Rebuilding Supabase with a local Postgres, auth provider, and token lifecycle might preserve surface similarity, but it keeps the operational shape of a cloud app. Migrating to single-user SQLite changes the center of gravity: data lives beside the app, the operator is implicit, deployment is simpler, and failures are more legible. For a privately run service, those are usually the right trade-offs.

The trade-off, of course, is that this pattern deliberately narrows scope. It gives up multi-user collaboration, remote identity delegation, and some future portability back to a hosted platform. But that is usually acceptable when the real goal is dependable personal infrastructure rather than a general-purpose product. The checkpoint shows that the right question is not "How do we preserve every old abstraction?" but "Which abstractions still earn their keep after the hosting model changes?"

## Key Properties

- **Stable helper surface:** Existing storage-oriented helper names can remain in place while the backend shifts from remote tables to a local SQLite file.
- **Trust-boundary collapse:** Authentication is simplified into a fixed local identity because the homelab itself becomes the security perimeter.
- **Local encrypted state:** Sensitive settings can remain encrypted at rest even after multi-user auth and remote secret storage are removed.
- **Operator-first integrations:** Upstream services can be reprioritized to prefer local infrastructure, such as routing search through **[[KnightCrawler]]** before public providers.

## Limitations

This pattern is a poor fit for applications that genuinely need multiple human users, delegated access, or audit-quality identity boundaries. SQLite can also become awkward if the app evolves toward high write concurrency or independent worker fleets. Finally, preserving old helper names during migration reduces blast radius, but it can also hide architectural change long enough that future contributors miss how different the deployment model really is.

## Examples

```ts
// Keep the old helper surface stable while swapping the backend.
export async function setUserSetting(key: string, value: string) {
  const encrypted = encryptForLocalStore(value)
  localStore.upsertUserSetting("local-user", key, encrypted)
}

export function getCurrentUser() {
  return { id: "local-user", email: "local@homelab" }
}
```

In practice, the UI can delete auth pages and route guards, while API routes keep calling the same helper names. The user experiences continuity; the operator gets a far simpler service to deploy and recover.

## Practical Applications

This pattern is ideal for private dashboards, download managers, household tools, internal control panels, and other apps that are used by one trusted operator or a small trusted household. It is especially valuable when the original codebase was scaffolded around Supabase, Firebase, Clerk, or other hosted defaults that would be expensive to preserve but easy to remove. Inside a homelab, it pairs naturally with Dockerized deployment, bind-mounted data directories, and reverse-proxy exposure through a broader infrastructure repo.

## Related Concepts

- **[[Homelab Infrastructure Patterns for AI Memory Migration]]**: Covers the broader repo, compose, and deployment structure that usually surrounds this app-level migration pattern.
- **[[Native-Module-Safe Docker Builds and UID-Aligned SQLite Mounts]]**: Complements this concept by covering the deployment-hardening work needed once local SQLite is introduced.
- **[[Homelab Service Inventory And Dashboard Synchronization]]**: Describes how the newly migrated service gets reflected in operational UI such as Homepage.

## Sources

- [[Copilot Session Checkpoint: Homelab migration and tunnel fix]] — primary checkpoint for the pattern
