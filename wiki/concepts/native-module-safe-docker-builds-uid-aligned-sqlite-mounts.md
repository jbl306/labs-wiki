---
title: "Native-Module-Safe Docker Builds and UID-Aligned SQLite Mounts"
type: concept
created: 2026-04-27
last_verified: 2026-04-27
source_hash: f05f51c65d6378e15448fa0d095133e89e8748f012e2613260b283a03ff2836c
sources:
  - raw/2026-04-27-copilot-session-homelab-migration-and-tunnel-fix-78392c21.md
related:
  - "[[Docker Container Resource Auditing and Optimization]]"
  - "[[Homelab Infrastructure Patterns for AI Memory Migration]]"
  - "[[Single-User Local SQLite Migration for Self-Hosted Web Apps]]"
tier: hot
tags: [docker, sqlite, nodejs, better-sqlite3, permissions, homelab]
quality_score: 62
---

# Native-Module-Safe Docker Builds and UID-Aligned SQLite Mounts

## Overview

Native-module-safe Docker builds with UID-aligned SQLite mounts are a deployment pattern for Node-based self-hosted apps that use compiled native dependencies and bind-mounted local databases. The pattern combines two safeguards: keep host build artifacts out of the image so container-native binaries are not silently replaced, and run the container with filesystem ownership that matches the mounted data directory so SQLite can actually open and write its database.

This matters because the failure modes are deceptively indirect. A build may appear successful, the container may start, and only then do runtime crashes reveal ABI mismatch errors or `SQLITE_CANTOPEN` permission faults. The checkpoint preserves both bugs in one place, making the pattern especially valuable for homelab services that use `better-sqlite3`, `sharp`, `sqlite3`, or any other module that compiles against the image's Node runtime.

## How It Works

The first half of the pattern addresses native module integrity. When a Node app depends on a package like `better-sqlite3`, the installed binary is compiled against a specific Node ABI and system environment. In local development, that binary may be built against the host's OS, libc, CPU target, and Node version. In a container build, the binary is built again for the image's own runtime. Problems arise when the image build succeeds correctly, but the final image later copies host-side `node_modules` into the container, overwriting the container-built artifact with one compiled for a different ABI. The result is the classic runtime crash: the module exists, but its binary does not match the Node version actually executing in the container.

That is exactly why `.dockerignore` is not just a build-speed optimization in this pattern; it is part of the correctness boundary. Excluding `node_modules`, `.nuxt`, `.output`, and similar host artifacts ensures the Docker context contains source code and manifests rather than development leftovers. In the checkpoint, this solved a `NODE_MODULE_VERSION 115` vs `127` mismatch for `better-sqlite3`. The important lesson is that the build context itself can be a source of runtime corruption. A multi-stage Dockerfile is not enough if the wrong files are still allowed into the context.

The second half of the pattern addresses file ownership for SQLite. SQLite is just a file, which makes it operationally simple, but that simplicity means the application's runtime UID must have correct access to the bind-mounted directory. In many homelabs, persistent volumes are owned by `PUID:PGID` values defined once in the infrastructure repo. If a new container runs as a different default user—such as UID `1001` while the host data directory is owned by `1000:1000`—the application can start, resolve its path, and still fail the moment it tries to create or open the database. The error often surfaces as `SQLITE_CANTOPEN`, which sounds like a path bug but is frequently just a permissions mismatch.

The fix is conceptually simple but operationally important: explicitly run the container as the same UID and GID scheme the rest of the homelab uses. In this checkpoint that meant setting `user: "${PUID}:${PGID}"` in `compose.web.yml`. This aligned the application's effective filesystem identity with the ownership of `/opt/homelab/data/debrid-downloader-web/`, letting SQLite open and create files consistently. The deeper principle is that local-database apps inherit all the reality of POSIX ownership. Once storage moves into a bind mount, container identity is part of database design.

There is also a sequencing insight here. The native-module bug and the permissions bug happened one after the other, and both only appeared after deployment. That makes them easy to misclassify as one "flaky deploy" problem. In reality they live at different layers: one is build artifact contamination, the other is runtime filesystem identity. Treating them as separate classes of failure is what makes the pattern reusable. If the container crashes before loading the app, inspect ABI and build context. If the app starts but the database cannot open, inspect volume ownership and runtime UID/GID.

The pattern also benefits from health-oriented validation. Because these bugs can hide behind a successful image build or a green `docker compose config`, the checkpoint validated at the service boundary: Caddy returned HTTP 200, `/api/settings` returned `{}`, the container reported healthy, and SQLite files appeared in the mounted data directory. This is important because build correctness, container liveness, and application correctness are not the same thing. The pattern expects verification at the point where the user-facing app actually exercises the native module and the mounted database.

Another useful intuition is that local SQLite plus native Node modules move complexity *from infrastructure services into packaging discipline*. You may delete a whole Postgres or Supabase dependency, but you inherit greater sensitivity to build context purity and volume permissions. That is still often a good trade in a homelab, because the resulting system is simpler overall. But it is only simple if the build and mount invariants are explicit and repeatable.

Finally, this pattern complements—not replaces—broader deployment conventions such as those in **[[Homelab Infrastructure Patterns for AI Memory Migration]]**. Compose file organization, environment management, and deployment scripts still matter. This concept just isolates the two hardening steps that become essential when a Node app with native dependencies starts carrying its own SQLite file into production.

## Key Properties

- **Build-context purity:** `.dockerignore` becomes a correctness tool that protects container-built native binaries from host-side overwrite.
- **ABI awareness:** Native modules are coupled to the runtime they were built for, so image success does not guarantee runtime compatibility.
- **Filesystem-identity alignment:** SQLite bind mounts require the container's runtime UID/GID to match the ownership model used on the host.
- **Runtime-bound validation:** Successful deploys are confirmed by application behavior and database creation, not just by image build or compose parsing.

## Limitations

This pattern does not solve every SQLite deployment problem; it will not help with lock contention, corruption from unsafe host operations, or schema bugs inside the app. It also assumes control over Compose configuration and volume ownership, which may be harder in managed environments. For teams with heterogeneous hosts or complex CI image pipelines, the ABI story can become more subtle than a single `.dockerignore` file.

## Examples

```dockerignore
node_modules
.nuxt
.output
dist
```

```yaml
services:
  app:
    user: "${PUID}:${PGID}"
    volumes:
      - ${HOMELAB_BASE}/data/debrid-downloader-web:/data
```

The first snippet protects the image from host binary contamination. The second ensures the process that opens `/data/debrid-downloader.sqlite` has the same ownership expectations as the host directory.

## Practical Applications

Use this pattern for self-hosted Node services that bundle native modules and persist state to local disk: dashboard backends, download managers, media tools, internal control panels, and lightweight APIs built around SQLite. It is especially useful in homelabs where images are built on one machine, deployed via Compose, and expected to write to long-lived bind-mounted directories owned by shared `PUID:PGID` conventions.

## Related Concepts

- **[[Single-User Local SQLite Migration for Self-Hosted Web Apps]]**: Covers the application-level simplification that often introduces SQLite into the deployment in the first place.
- **[[Docker Container Resource Auditing and Optimization]]**: Addresses adjacent operational concerns once the service is up and running under Compose.
- **[[Homelab Infrastructure Patterns for AI Memory Migration]]**: Places this packaging pattern inside the larger repo and deployment conventions of the homelab.

## Sources

- [[Copilot Session Checkpoint: Homelab migration and tunnel fix]] — primary checkpoint for the pattern
