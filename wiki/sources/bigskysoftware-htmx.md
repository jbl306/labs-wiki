---
title: bigskysoftware/htmx
type: source
created: '2026-04-21'
last_verified: '2026-04-22'
source_hash: ca2cfb1d28fe1ee978e9b0876ad605f92affa272f2fbdf6db5f16eb8559d3c25
sources:
- raw/2026-04-07-test-github-repo.md
source_url: https://github.com/bigskysoftware/htmx
tags:
- github
- hateoas
- html
- htmx
- hyperscript
- javascript
- rest
tier: warm
knowledge_state: ingested
ingest_method: manual-reprocess-github-2026-04-22
quality_score: 80
concepts:
- html-over-the-wire-with-htmx
- htmx-attribute-api
---

# bigskysoftware/htmx

## What it is

htmx is a small (~14 kB min+gzipped), dependency-free JavaScript library that gives plain HTML access to AJAX, CSS Transitions, WebSockets, and Server-Sent Events through HTML attributes. Instead of returning JSON to a SPA, the server returns HTML fragments and htmx swaps them into the page on user-triggered events. It is the spiritual successor to intercooler.js and a practical implementation of the HATEOAS / hypermedia-as-the-engine-of-application-state idea.

## Why it matters

For our internal tools (debrid-downloader desktop UI, nba-fantasy-draft-tool web UI, future labs-wiki dashboards) htmx is a much lower-overhead alternative to spinning up Vue/Nuxt when the backend is already FastAPI returning rendered templates. The bundle size and zero-build-step ergonomics fit small-footprint tooling well, and it composes naturally with FastAPI + Jinja or Nuxt server routes.

## Key concepts

- **HTML-over-the-wire** — Server returns HTML fragments; the client never parses JSON. See [[html-over-the-wire-with-htmx]].
- **`hx-*` attributes** — Behavior is declarative: `hx-get`, `hx-post`, `hx-trigger`, `hx-target`, `hx-swap` etc. attached directly to elements. See [[htmx-attribute-api]].
- **Generalised hypertext** — Any element can issue any HTTP verb, on any event, replacing any part of the DOM. Removes the "only `<a>` and `<form>`" / "only GET and POST" / "only full-page replace" constraints of vanilla HTML.
- **Extensions** — First-party extensions for SSE, WebSockets, preloading, response targeting, etc.
- **No build step** — Drop in via CDN `<script>` tag; no bundler required.

## How it works

- htmx scans the DOM for `hx-*` attributes on page load and after every swap.
- A configured event (default: the natural one for the element) triggers an AJAX call to the configured URL with the configured verb.
- The response — expected to be HTML — is swapped into the configured target using the configured strategy (`innerHTML`, `outerHTML`, `beforebegin`, etc.).
- Extensions and `hyperscript` (a sister project) layer on richer client-side behavior when needed.
- Tests use mocha + chai + sinon; bundle is built with TypeScript (recent v2.10 prep added `--skipLibCheck` to the build).

## Setup

```html
<script src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.10/dist/htmx.min.js"
        crossorigin="anonymous"></script>

<button hx-post="/clicked" hx-swap="outerHTML">
  Click Me
</button>
```

```bash
# Or via npm — note the package is htmx.org, not htmx
npm install htmx.org --save
```

## Integration notes

Pairs cleanly with our FastAPI + Jinja stack. Strong fit for the debrid-downloader web UI's real-time bits where we currently use raw WebSocket plumbing. Less appropriate for the Nuxt-based debrid-downloader-web (already SPA-shaped). For the nba-fantasy-draft-tool's Textual + web hybrid, htmx could remove the Vue dependency entirely.

## Caveats / Gotchas

- The npm package is `htmx.org`, not `htmx` — the latter is a stale/broken package.
- License is BSD 2-Clause Zero (BSD0).
- Encourages a server-rendering style; teams used to JSON APIs need to adjust their backend templating story.

## Repo metadata

| Field | Value |
|---|---|
| Stars | 47,867 |
| Primary language | JavaScript |
| Topics | hateoas, html, htmx, hyperscript, javascript, rest |
| License | BSD-Zero (see repo) |

## Source

- Raw dump: `raw/2026-04-07-test-github-repo.md`
- Upstream: https://github.com/bigskysoftware/htmx
