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
ingest_method: manual-deepen-github-2026-04-22
quality_score: 56
concepts:
- html-over-the-wire-with-htmx
- htmx-attribute-api
---

# bigskysoftware/htmx

## What it is

htmx is a small (~14 kB min+gzipped), dependency-free JavaScript library that gives plain HTML access to AJAX, CSS Transitions, WebSockets, and Server-Sent Events through HTML attributes. Instead of returning JSON to a SPA, the server returns HTML fragments and htmx swaps them into the page on user-triggered events. It is the spiritual successor to intercooler.js and a practical implementation of the HATEOAS / hypermedia-as-the-engine-of-application-state idea.

## Why it matters

For our internal tools (debrid-downloader desktop UI, nba-fantasy-draft-tool web UI, future labs-wiki dashboards) htmx is a much lower-overhead alternative to spinning up Vue/Nuxt when the backend is already FastAPI returning rendered templates. The bundle size and zero-build-step ergonomics fit small-footprint tooling well, and it composes naturally with FastAPI + Jinja or Nuxt server routes.

## Architecture / Technical model

**HTML-over-the-wire** — Server returns HTML fragments; the client never parses JSON.

> See [[html-over-the-wire-with-htmx]] for the full treatment.

**Attribute-driven behavior** — Declarative `hx-*` attributes replace imperative JavaScript: `hx-get`, `hx-post`, `hx-put`, `hx-delete`, `hx-patch`, `hx-trigger`, `hx-target`, `hx-swap`, `hx-include`, `hx-vals`, `hx-headers`, `hx-boost`, `hx-push-url`, `hx-select`, `hx-indicator`, etc.

> See [[htmx-attribute-api]] for attribute inventory and composition rules.

**Event system** — Any DOM event can trigger a request: `click`, `submit`, `change`, `mouseenter`, `keyup`, custom events. Event modifiers: `once`, `changed`, `delay:<time>`, `throttle:<time>`, `from:<selector>`, `target:<selector>`, `consume`, `queue:<strategy>`.

**Swap model** — Seven core strategies: `innerHTML` (default), `outerHTML`, `beforebegin`, `afterbegin`, `beforeend`, `afterend`, `delete`, `none`. Additional strategies via extensions: `morph` (morphdom integration), `multi-swap` (swap multiple targets in one response).

**OOB (out-of-band) swaps** — Response can include `hx-swap-oob="true"` on elements to update targets not specified in the original request. Enables multi-target updates in one round trip.

**Request lifecycle** — DOM scan → event trigger → request build (gather `hx-vals`, `hx-include`) → AJAX call → response parse → swap → settle (CSS class transitions) → DOM rescan for new `hx-*` attributes.

**Extensions API** — Events: `htmx:configRequest`, `htmx:beforeSwap`, `htmx:afterSwap`, `htmx:load`, etc. 20+ lifecycle hooks. Extensions shipped: `sse` (Server-Sent Events), `ws` (WebSockets), `preload`, `ajax-header`, `response-targets`, `head-support`, `class-tools`, `path-deps`.

**Zero dependencies** — No jQuery, no framework. 14 kB min.gz'd (v2.0.10). Built with TypeScript; tests with mocha + chai + sinon + @web/test-runner (Playwright).

**HATEOAS compliance** — Extends REST's hypermedia-as-the-engine-of-application-state to all HTML elements, not just `<a>` and `<form>`.

## How it works

1. **DOM scan on load** — htmx scans for `hx-*` attributes when the page loads and after every swap. New elements brought in via AJAX inherit htmx behavior automatically.

2. **Event binding** — For each element with `hx-get|post|put|delete|patch`, htmx binds the event specified in `hx-trigger` (defaults: `click` for buttons, `submit` for forms, `change` for inputs).

3. **Request construction** — On trigger, htmx gathers: (a) element values (if form/input), (b) `hx-vals` (extra JSON params), (c) `hx-include` (additional element values by selector), (d) `hx-headers` (custom headers).

4. **AJAX call** — Fires request with `HX-Request: true` header (server can detect htmx). `HX-Trigger`, `HX-Trigger-Name`, `HX-Target`, `HX-Current-URL` headers pass client state.

5. **Response handling** — Server returns HTML fragment. htmx inspects `HX-*` response headers for retargeting (`HX-Retarget`), reswap (`HX-Reswap`), client-side redirect (`HX-Redirect`), trigger events (`HX-Trigger`).

6. **Swap** — htmx replaces/inserts content into `hx-target` (default: triggering element itself) using `hx-swap` strategy. Swap is wrapped in CSS class transitions (`htmx-swapping`, `htmx-settling`).

7. **Settle** — After 20ms, htmx applies `htmx-added` class to new elements and removes `htmx-swapping` from old. CSS transitions bridge the states.

8. **DOM rescan** — htmx rescans the updated subtree for new `hx-*` attributes, enabling infinite scroll, lazy load, nested forms, etc.

**Bundle size**: v2.0.10 is 14,304 bytes min.gz'd. Unminified: ~3,500 LoC.

**Test coverage**: 1,000+ tests across `/test/attributes`, `/test/core`, `/test/ext`. Run locally via `npx serve` → `http://0.0.0.0:3000/test/`.

**Build**: `./scripts/dist.sh` → uglify-js minification → `dist/htmx.min.js`. TypeScript definitions generated via `tsc --declaration --emitDeclarationOnly`.

## API / interface surface

### Core attributes

| Attribute | Purpose | Example |
|---|---|---|
| `hx-get` | Issue GET to URL | `<button hx-get="/items">Load</button>` |
| `hx-post` | Issue POST to URL | `<form hx-post="/save">...</form>` |
| `hx-put` | Issue PUT to URL | `<button hx-put="/item/1">Update</button>` |
| `hx-delete` | Issue DELETE to URL | `<button hx-delete="/item/1">Remove</button>` |
| `hx-patch` | Issue PATCH to URL | `<button hx-patch="/item/1">Patch</button>` |
| `hx-trigger` | Event to trigger request | `hx-trigger="mouseenter"` |
| `hx-target` | CSS selector for swap target | `hx-target="#results"` |
| `hx-swap` | Swap strategy | `hx-swap="outerHTML"` (or `innerHTML`, `beforebegin`, `afterbegin`, `beforeend`, `afterend`, `delete`, `none`) |
| `hx-include` | Additional elements to include in request | `hx-include="[name='filter']"` |
| `hx-vals` | Extra JSON values | `hx-vals='{"page":2}'` |
| `hx-headers` | Custom headers | `hx-headers='{"X-API-Key":"..."}'` |
| `hx-indicator` | Element to show during request | `hx-indicator=".spinner"` |
| `hx-push-url` | Push URL to history | `hx-push-url="true"` |
| `hx-select` | CSS selector to extract from response | `hx-select="#content"` |
| `hx-boost` | Progressive enhancement for `<a>` / `<form>` | `<body hx-boost="true">` |

### Event modifiers (in `hx-trigger`)

- `once` — trigger only once, then unbind
- `changed` — trigger only if value changed
- `delay:<time>` — debounce (e.g. `delay:500ms`)
- `throttle:<time>` — rate limit
- `from:<selector>` — listen on ancestor
- `target:<selector>` — listen on descendant
- `consume` — prevent event propagation
- `queue:<strategy>` — `first`, `last`, `all`, `none`

### Server response headers

- `HX-Trigger` — trigger client-side events after swap
- `HX-Retarget` — override `hx-target` on this response
- `HX-Reswap` — override `hx-swap` on this response
- `HX-Redirect` — client-side redirect
- `HX-Refresh` — force page refresh
- `HX-Push-Url` — override push-url behavior
- `HX-Replace-Url` — replace URL without push

## Setup

```bash
# Via CDN (production)
# <script src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.10/dist/htmx.min.js"
#         integrity="sha384-H5SrcfygHmAuTDZphMHqBJLc3FhssKjG7w/CeCpFReSfwBWDTKpkzPP8c+cLsK+V"
#         crossorigin="anonymous"></script>

# Via npm — note the package is htmx.org, not htmx
npm install htmx.org --save

# Local development
npm install
npx serve
# Visit http://0.0.0.0:3000/test/ for test suite

# Build dist
./scripts/dist.sh && npm run types-generate && npm run web-types-generate
```

Example usage:

```html
<script src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.10/dist/htmx.min.js"
        crossorigin="anonymous"></script>

<button hx-post="/clicked" hx-swap="outerHTML">
  Click Me
</button>

<div hx-get="/search" hx-trigger="input changed delay:500ms" hx-target="#results">
  <input name="q" placeholder="Search...">
</div>
<div id="results"></div>
```

## Integration notes

Pairs cleanly with our FastAPI + Jinja stack. Strong fit for the debrid-downloader web UI's real-time bits where we currently use raw WebSocket plumbing. Less appropriate for the Nuxt-based debrid-downloader-web (already SPA-shaped). For the nba-fantasy-draft-tool's Textual + web hybrid, htmx could remove the Vue dependency entirely.

**With FastAPI + Jinja**:
- Return `HTMLResponse` from routes, not `JSONResponse`
- Use `Jinja2Templates` to render partials
- Set `HX-Trigger` response header to fire client-side events
- Leverage `hx-boost` on `<body>` for progressive enhancement

**WebSocket alternative via `sse` extension**:
- `<div hx-ext="sse" sse-connect="/stream" sse-swap="message"></div>`
- FastAPI SSE endpoint: `return EventSourceResponse(event_generator())`

**Common patterns**:
- Infinite scroll: `hx-get="/next" hx-trigger="revealed" hx-swap="afterend"`
- Active search: `hx-get="/search" hx-trigger="input changed delay:500ms"`
- Inline editing: `hx-get="/edit/1" hx-swap="outerHTML"` → return form → `hx-put="/update/1"`

## Caveats / Gotchas

- The npm package is `htmx.org`, not `htmx` — the latter is a stale/broken package.
- License is BSD 0-Clause (BSD-Zero) — extremely permissive.
- Encourages a server-rendering style; teams used to JSON APIs need to adjust their backend templating story.
- v2.0 breaking changes from v1: removed `hx-sse` / `hx-ws` core attributes (now extensions), changed default swap from `innerHTML` to `outerHTML` for `hx-boost`, renamed some events.
- `hx-swap="outerHTML"` on elements with `style` attribute can leave `htmx-swapping` class behind (fixed in v2.0.7).
- Nested OOB swaps with `off` attribute still execute (issue #3743).
- WebSocket/SSE extension event handling with `hx-on` had issues in 1.9.10, improved in v2.
- Missing TypeScript types in recent releases (issue #3757) — use `dist/htmx.esm.d.ts`.

## Repo metadata

| Field | Value |
|---|---|
| Stars | 47,867 |
| Primary language | JavaScript (92.1%), HTML (7.1%), CSS (0.4%), TypeScript (0.2%) |
| Topics | hateoas, html, htmx, hyperscript, javascript, rest |
| License | BSD-0 (Zero-Clause BSD) |
| Latest release | v2.0.10 (2026-04-20) |
| Contributors | 200+ |
| Test framework | mocha + chai + sinon + @web/test-runner (Playwright) |
| Bundle | 14 kB min.gz'd |

## Related concepts

- [[html-over-the-wire-with-htmx]] — the hypermedia architecture htmx enables
- [[htmx-attribute-api]] — full attribute inventory and composition rules

## Source

- Raw dump: `raw/2026-04-07-test-github-repo.md`
- Upstream: https://github.com/bigskysoftware/htmx
- Docs: https://htmx.org/docs
- Examples: https://htmx.org/examples
