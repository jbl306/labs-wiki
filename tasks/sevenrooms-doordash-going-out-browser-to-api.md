# SevenRooms / DoorDash Going Out Browser-to-API Discovery

## Goal

Use Browserbase's `browser-to-api` workflow to produce a best-effort API artifact for the SevenRooms / DoorDash Going Out reservation surface, focused on:

1. Public, read-only SevenRooms widget availability discovery.
2. A non-mutating booking-flow boundary map for DoorDash Going Out / SevenRooms partner APIs.

## Safety scope

- Allowed: low-frequency public availability discovery requests and offline OpenAPI/spec generation from captured traffic.
- Allowed: document inferred booking-flow steps and gated partner/private boundaries.
- Not allowed: create, cancel, or modify live reservations; bypass auth or bot defenses; extract credentials, cookies, or private account data.

## Plan

1. Load/review the upstream `browser-to-api` skill and local labs-wiki context.
2. Get the browser-to-api scripts and create a `browser-trace`-compatible run directory.
3. Capture or synthesize trace data only from real, low-frequency public network responses.
4. Run `discover.mjs` to emit OpenAPI, HTML report, markdown report, confidence, samples, and client files.
5. Add a reviewed booking-flow overlay that marks booking mutations as gated/undiscovered unless directly observed.
6. Verify generated JSON/YAML and summarize outputs.

## Results

Completed.

Artifacts were written under `.o11y/sevenrooms-doordash-going-out/api-spec/`:

- `openapi.yaml` / `openapi.json` — Browserbase `browser-to-api` generated spec with 3 live-observed operations.
- `report.md` / `index.html` — generated coverage reports.
- `client.mjs` — generated zero-dependency client; syntax-checked with `node --check`.
- `booking-flow.md` — safety-scoped discovery + booking-flow boundary map.
- `booking-flow-overlay.openapi.yaml` — overlay for live-observed discovery plus static-observed booking-flow clues.
- `static-js-endpoints.md` / `.json` — 19 endpoint strings extracted from public SevenRooms widget JavaScript.

Verification:

- `discover.mjs` completed with 5 paired requests, 5 response bodies attached, 3 normalized endpoints, and 3 spec paths.
- `openapi.json`, `confidence.json`, and `static-js-endpoints.json` parsed successfully.
- `client.mjs` passed `node --check`.
- No live booking hold, payment, reservation creation, cancellation, auth bypass, or credentialed DoorDash/SevenRooms call was attempted.
