# Homelab Graph Integration + UI Plan

> **Goal:** Deploy the labs-wiki knowledge graph (`graphify-integration.md`) as a first-class homelab service with a browser UI, so the graph is queryable/viewable from any device on the network without running a local Python stack or opening Obsidian.
>
> **Depends on:** [claude-obsidian-and-live-memory-integration.md](claude-obsidian-and-live-memory-integration.md) (live memory loop, done ✅), [graphify-integration.md](graphify-integration.md) (graph backend spec).
>
> **Status:** Plan. Implementation starts after graphify Phase 1 (graph.json build pipeline) is wired into `auto_ingest.py`.

---

## Why Move It to the Homelab

Today the graph — if it existed — would live as files on the laptop (`labs-wiki/wiki/graph/*`). That has four problems:

1. **Not always-on.** Shut the laptop → graph is gone until next boot.
2. **No shared view.** Phone, tablet, other devices can't reach it.
3. **Compute asymmetry.** Leiden clustering and graph layout are happier on the Beelink (32 GB RAM, always plugged in) than a laptop running ML workloads.
4. **No UI.** vis.js HTML exports are static — no live re-query, no MCP integration from the browser.

Putting the graph service on the homelab fixes all four and plugs neatly into the existing Caddy + Docker Compose + homepage stack.

## Non-Goals

- Replacing Obsidian. Obsidian's local graph view stays — this is the **network-reachable** alternative plus programmatic access.
- Replacing labs-wiki itself. The wiki (markdown files + auto-ingest) remains canonical. The graph is derived.
- Supporting remote **write/ingest** from the internet. Public surface is read-only (viewer + query). The `/internal/rebuild` and `/graph/rebuild` endpoints stay LAN/loopback-only.

## Access Model — LAN + Public

Mirrors the existing homelab pattern ([`homelab/docs/08-cloudflare-tunnel.md`](../../homelab/docs/08-cloudflare-tunnel.md)): same Caddy hostname reachable two ways.

| Path | Entry | TLS | Auth | Allowed |
|------|-------|-----|------|---------|
| LAN | AdGuard DNS rewrite `graph.jbl-lab.com → 192.168.1.238` → Caddy :80 | none (HTTP on LAN) | none | full UI + read API |
| Public | Cloudflare edge → Tunnel → `cloudflared` → Caddy :80 | Cloudflare-terminated | **Cloudflare Access** (email OTP / Google SSO, 24 h session) | full UI + read API |
| Admin (`/graph/rebuild`, `/internal/*`) | loopback / Docker network only | n/a | `X-Admin-Token` | watcher + manual curl |

Same posture as Grafana, Riven, Seerr, memory-ui — **no new auth infra introduced**. Cloudflare Access is configured once in Zero Trust → Applications, scoped to `graph.jbl-lab.com` and `graph-api.jbl-lab.com`.

---

## Architecture

```
┌───────────────────────────────────────────────────────────────────────┐
│  Homelab — Beelink GTi13 (Ubuntu 24.04, Docker Compose)                │
└───────────────────────────────────────────────────────────────────────┘

  ┌────────────────────┐     ┌────────────────────┐
  │  labs-wiki repo    │     │  mempalace palace  │
  │  (NFS? bind mount) │     │  ~/.mempalace/     │
  └──────────┬─────────┘     └─────────┬──────────┘
             │ read-only                │ read-only
             │                          │
  ┌──────────▼──────────────────────────▼──────────┐
  │        wiki-graph-api  (NEW container)          │
  │  FastAPI + NetworkX + Leiden + Sentence-BERT   │
  │                                                 │
  │  Endpoints:                                     │
  │   GET  /graph/stats                             │
  │   GET  /graph/nodes/{id}                        │
  │   GET  /graph/neighbors/{id}?depth=N            │
  │   POST /graph/query        (natural language)   │
  │   GET  /graph/communities                       │
  │   GET  /graph/god-nodes                         │
  │   GET  /graph/surprises                         │
  │   GET  /graph/export/json                       │
  │   GET  /graph/export/graphml                    │
  │   GET  /graph/rebuild      (admin, auth-gated)  │
  │                                                 │
  │  MCP endpoint (SSE): /mcp                       │
  └─────────────┬──────────────────────┬───────────┘
                │                      │
    ┌───────────▼─────────┐   ┌────────▼────────┐
    │ wiki-graph-ui       │   │  Cache volume   │
    │ (NEW container)     │   │  graph.json     │
    │ SvelteKit + Cosmos  │   │  extraction/    │
    │ GPU-accelerated     │   │  communities/   │
    │ graph visualization │   └─────────────────┘
    └───────────┬─────────┘
                │
  ┌─────────────▼──────────────────────────────────┐
  │            Caddy (existing proxy, :80)          │
  │  graph.${DOMAIN}       → wiki-graph-ui:3000    │
  │  graph-api.${DOMAIN}   → wiki-graph-api:8000   │
  └─────────────┬──────────────────────────────────┘
                │
        ┌───────┴────────────────┐
        ▼                        ▼
   LAN clients             cloudflared → Cloudflare edge
   (AdGuard DNS            (Access-gated public hostnames,
    rewrite, HTTP)          TLS-terminated at the edge)
```

### Rebuild trigger flow

```
labs-wiki/wiki/*.md changes
   │  (via mempalace-watcher already deployed)
   ▼
mempalace-watcher sees event → triggers wiki-graph-api /internal/rebuild
   │  (new webhook; watcher extended)
   ▼
wiki-graph-api:
   1. Incremental extract (SHA-cache skips unchanged pages)
   2. Rebuild NetworkX graph from extracted edges
   3. Re-run Leiden on affected communities only
   4. Publish new graph.json + invalidate UI cache
   │
   ▼
wiki-graph-ui gets SSE "graph-updated" event → reloads
```

## Components

### 1. `wiki-graph-api` container

- **Base image:** `python:3.12-slim`.
- **Stack:** FastAPI, NetworkX, `leidenalg` (via `igraph-python`), `sentence-transformers` (already on box via mempalace). Optional `cdlib` for richer community algorithms.
- **Storage:** graph state in a Docker named volume `wiki_graph_data`. Extraction cache keyed by `sha256(page_content)` (matches graphify-integration.md spec).
- **Bind mounts:**
  - `~/projects/labs-wiki/wiki` → `/app/wiki:ro`
  - `~/.mempalace` → `/app/mempalace:ro` (optional — lets the API enrich graph nodes with drawer counts/excerpts)
- **MCP surface:** exposes the same tools (`wiki_graph_neighbors`, `wiki_graph_shortest_path`, `wiki_graph_communities`, `wiki_graph_god_nodes`, `wiki_graph_surprises`) over SSE so Copilot CLI, VS Code, and OpenCode can all connect to one canonical graph.

### 2. `wiki-graph-ui` container

- **Stack candidates (ranked):**
  1. **SvelteKit + @cosmograph/cosmograph** — WebGL-based, handles 1M+ nodes, best perf/UX combo. **Recommended.**
  2. SvelteKit + vis-network — easier to author, caps out ~5k nodes with good UX.
  3. React + react-force-graph — more complex, heavier bundle.
- **Features (MVP):**
  - Full-graph view with community colors.
  - Click-node → side panel with frontmatter, excerpt, neighbors, [[wikilinks]] (links back to Obsidian URL scheme when opened from the laptop).
  - Search bar (fuzzy over node titles and frontmatter tags).
  - Filters: type (concept/entity/source/synthesis), tier (hot/established/core), community, stale-only.
  - "Surprises" toggle → highlight cross-community edges.
  - "Path" mode → click A then B, shortest path is drawn.
- **Features (Phase 2):**
  - Live-updates via SSE (`graph-updated` event) without full reload.
  - Saved views (URL-encoded filter state) for bookmarking specific investigations.
  - Natural-language query box: POSTs to `/graph/query` and renders the result subgraph.

### 3. `compose/compose.wiki-graph.yml`

Follows the Caddy-label pattern used by every other homelab stack (see [`compose.wiki.yml`](../../homelab/compose/compose.wiki.yml), [`compose.monitoring.yml`](../../homelab/compose/compose.monitoring.yml)). Caddy auto-discovers routes from container labels — no manual Caddyfile edits.

```yaml
networks:
  proxy:
    external: true

services:
  wiki-graph-api:
    build:
      context: ${REPO_ROOT:-/home/jbl/projects}/labs-wiki
      dockerfile: Dockerfile.graph-api
    container_name: wiki-graph-api
    restart: unless-stopped
    environment:
      - WIKI_PATH=/app/wiki
      - CACHE_DIR=/data/cache
      - MEMPALACE_PATH=/app/mempalace
      - ADMIN_TOKEN=${WIKI_GRAPH_ADMIN_TOKEN}
      - TZ=${TZ}
    volumes:
      - ${REPO_ROOT:-/home/jbl/projects}/labs-wiki/wiki:/app/wiki:ro
      - ${HOME}/.mempalace:/app/mempalace:ro
      - wiki_graph_data:/data
    networks:
      - proxy
    labels:
      caddy: http://graph-api.${DOMAIN}
      caddy.reverse_proxy: "{{upstreams 8000}}"
      # block admin endpoints at the edge; rebuild must come via Docker network only
      caddy.@admin.path: "/internal/* /graph/rebuild"
      caddy.respond: "@admin 403"
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: "1.0"

  wiki-graph-ui:
    build:
      context: ${REPO_ROOT:-/home/jbl/projects}/labs-wiki
      dockerfile: Dockerfile.graph-ui
    container_name: wiki-graph-ui
    restart: unless-stopped
    environment:
      - PUBLIC_API_URL=https://graph-api.${DOMAIN}
      - TZ=${TZ}
    networks:
      - proxy
    depends_on:
      - wiki-graph-api
    labels:
      caddy: http://graph.${DOMAIN}
      caddy.reverse_proxy: "{{upstreams 3000}}"
      caddy.encode: gzip
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: "0.5"

volumes:
  wiki_graph_data:
```

Register the stack in `compose/docker-compose.yml` include list and in `scripts/ops/deploy.sh` `STACKS=(...)` array.

### 4. DNS + tunnel wiring

**LAN (AdGuard):** add two entries to `config/adguard/dns-rewrites.json`, then run `scripts/ops/sync-dns-rewrites.sh`:

```json
{ "domain": "graph.jbl-lab.com",     "answer": "192.168.1.238" },
{ "domain": "graph-api.jbl-lab.com", "answer": "192.168.1.238" }
```

**Public (Cloudflare Tunnel):** in Zero Trust → Networks → Tunnels → `jbl-lab` → Public Hostnames, add two routes:

| Subdomain | Domain | Service |
|-----------|--------|---------|
| `graph` | `jbl-lab.com` | `http://caddy:80` |
| `graph-api` | `jbl-lab.com` | `http://caddy:80` |

**Cloudflare Access (required for public paths):** Zero Trust → Access → Applications → Add Application (Self-hosted):

- Application: `wiki-graph`
- Domains: `graph.jbl-lab.com`, `graph-api.jbl-lab.com`
- Session: 24 h
- Policy: `Allow` where Emails in `{your @email}` **or** Identity Provider = Google + domain match
- Bypass path on `graph-api`: none (API also gated — MCP clients use service tokens, see Phase G3)

The UI container needs to tolerate Cloudflare's `CF_Authorization` cookie on public, absent on LAN — SvelteKit's default session handling doesn't care. For API calls from the SPA, send `credentials: 'include'` so the cookie rides along.

### 5. homepage integration

Add a **new row** `Knowledge Graph` to [`homelab/config/homepage/services.yaml`](../../homelab/config/homepage/services.yaml) (same file that defines the Media, System Health, and Container Activity rows). Uses the `{{HOMEPAGE_VAR_DOMAIN}}` template already wired through `compose.infra.yml`, so the same homepage row works for both LAN and public access (AdGuard / Cloudflare resolve the hostname appropriately).

```yaml
- Knowledge Graph:
    - Graph UI:
        icon: mdi-graph-outline
        href: https://graph.{{HOMEPAGE_VAR_DOMAIN}}
        description: Interactive labs-wiki knowledge graph
        server: homelab
        container: wiki-graph-ui
        siteMonitor: http://wiki-graph-ui:3000
        widget:
          type: customapi
          url: http://wiki-graph-api:8000/graph/stats
          refreshInterval: 60000
          mappings:
            - field: node_count
              label: Nodes
            - field: edge_count
              label: Edges
            - field: communities
              label: Clusters
            - field: last_rebuild
              label: Updated
    - Graph API:
        icon: mdi-api
        href: https://graph-api.{{HOMEPAGE_VAR_DOMAIN}}/docs
        description: FastAPI + MCP endpoint
        server: homelab
        container: wiki-graph-api
        siteMonitor: http://wiki-graph-api:8000/health
    - Wiki Sidecar:
        icon: mdi-notebook-edit-outline
        href: https://wiki.{{HOMEPAGE_VAR_DOMAIN}}
        description: labs-wiki auto-ingest API (source of truth)
        server: homelab
        container: wiki-ingest-api
        siteMonitor: http://wiki-ingest-api:8000/health
```

Restart homepage after edit (`docker compose restart homepage`) — it hot-reloads `services.yaml` but the new row shows up cleanly after a restart.

### 6. mempalace-watcher extension

Extend [`homelab/scripts/mempalace-watcher.py`](../../homelab/scripts/mempalace-watcher.py) with one extra action wired to the labs-wiki-wiki watch:

```python
def trigger_graph_rebuild() -> None:
    try:
        httpx.post(
            "http://wiki-graph-api:8000/internal/rebuild",
            headers={"X-Admin-Token": os.environ["WIKI_GRAPH_ADMIN_TOKEN"]},
            timeout=5.0,
        )
    except httpx.HTTPError as e:
        log.warning("graph rebuild webhook failed: %s", e)
```

Called after every `mine_labs_wiki_full()` — adds ~50ms, skips cleanly if the container is down.

---

## Implementation Phases

### Phase G0 — Prerequisites (not in this plan)

- [ ] `graphify-integration.md` Phase 1 — `scripts/graph_extract.py` + `scripts/graph_build.py` produce a working `wiki/graph/graph.json` locally.

### Phase G1 — API container (P0)

- [ ] `api-scaffold` — `labs-wiki/wiki-graph-api/` FastAPI skeleton with `/graph/stats` and `/graph/nodes/{id}`.
- [ ] `api-dockerfile` — `Dockerfile.graph-api` at labs-wiki root.
- [ ] `api-extract-port` — port `graph_extract.py` + `graph_build.py` logic into the container's startup / rebuild pipeline.
- [ ] `api-cache-volume` — SHA256 per-page extraction cache in `/data/cache`.
- [ ] `api-mcp-endpoint` — `/mcp` SSE endpoint exposing the 5 graph MCP tools.
- [ ] `compose-wiki-graph` — `compose/compose.wiki-graph.yml` with Caddy labels + admin-path block.
- [ ] `compose-register` — add stack to `compose/docker-compose.yml` includes and `scripts/ops/deploy.sh` `STACKS=(...)`.
- [ ] `dns-lan` — add `graph.jbl-lab.com` + `graph-api.jbl-lab.com` to `config/adguard/dns-rewrites.json` and run `sync-dns-rewrites.sh`.
- [ ] `tunnel-public` — add both subdomains as Public Hostnames on the `jbl-lab` Cloudflare Tunnel (Zero Trust UI).
- [ ] `access-policy` — create Cloudflare Access application gating both public hostnames (email OTP + Google SSO, 24 h session).
- [ ] `watcher-webhook` — extend `mempalace-watcher.py` with rebuild trigger (Docker-network-local URL, admin token).

### Phase G2 — UI container (P0)

- [ ] `ui-scaffold` — SvelteKit project under `labs-wiki/wiki-graph-ui/`.
- [ ] `ui-cosmograph` — Cosmograph component, initial full-graph render, community coloring.
- [ ] `ui-node-panel` — click-node side panel with frontmatter + neighbors.
- [ ] `ui-search-filters` — fuzzy search bar + type/tier/community/stale filters.
- [ ] `ui-dockerfile` — `Dockerfile.graph-ui` at labs-wiki root.
- [ ] `ui-credentials-include` — SvelteKit fetch helpers use `credentials: 'include'` so Cloudflare `CF_Authorization` cookie rides along on public path.
- [ ] `homepage-row` — add `Knowledge Graph` row to `config/homepage/services.yaml` (Graph UI + Graph API + Wiki Sidecar entries, stats widget).
- [ ] `rate-limit-public` — Caddy `rate_limit` directive on `graph-api.jbl-lab.com` (60 req/min/IP) via a label on wiki-graph-api.

### Phase G3 — Live updates + advanced queries (P1)

- [ ] `sse-live-updates` — API publishes `graph-updated` SSE; UI hot-reloads.
- [ ] `path-mode` — shortest-path UI interaction.
- [ ] `nl-query` — `/graph/query` endpoint: natural-language → subgraph (uses Copilot Pro+ tokens via an MCP proxy, no separate key).
- [ ] `surprises-view` — highlight cross-community edges with confidence filtering.
- [ ] `saved-views` — URL-encoded filter state.
- [ ] `access-service-tokens` — issue Cloudflare Access service tokens for headless MCP clients, document in `docs/08-cloudflare-tunnel.md`.

### Phase G4 — Observability + polish (P2)

- [ ] `graph-prometheus` — `/metrics` endpoint: rebuild duration, node/edge counts, extraction cache hit rate.
- [ ] `grafana-dashboard` — add graph panel to existing Grafana instance.
- [ ] `graph-report-route` — `/graph/report` serves a formatted `GRAPH_REPORT.md` (god nodes, surprises, suggested questions).
- [ ] `neo4j-export` — `/graph/export/graphml` and Cypher export for external tooling.
- [ ] `backup-integration` — include `wiki_graph_data` volume in `homelab/scripts/backup.sh`.

---

## Security / Safety

- **Cloudflare Access on all public hostnames.** `graph.jbl-lab.com` and `graph-api.jbl-lab.com` both require Access authentication before hitting cloudflared. Unauthenticated requests never reach the homelab.
- **Admin endpoints blocked at Caddy.** `/internal/*` and `/graph/rebuild` are rejected with 403 at the Caddy layer (via the `caddy.@admin.*` label) regardless of entry path. They remain reachable only from inside the `proxy` Docker network (watcher → API service name).
- **Admin-gated rebuild.** `/internal/rebuild` requires `X-Admin-Token` matching `${WIKI_GRAPH_ADMIN_TOKEN}` (generated at setup, stored in `.env`, never committed). Defence-in-depth behind the Caddy rule.
- **Read-only mounts.** The API container reads `labs-wiki/wiki/` and `~/.mempalace` read-only; all writes land in the `wiki_graph_data` volume. No way for the container to corrupt the wiki or palace.
- **Service tokens for programmatic MCP.** For headless clients (Copilot Agent sessions on non-LAN machines), use Cloudflare Access **service tokens** (`CF-Access-Client-Id` / `CF-Access-Client-Secret` headers) rather than bypassing Access. One token per client, rotatable.
- **No PII.** Graph nodes are derived from the wiki, which must already be PII-free per labs-wiki conventions. Add a CI lint to scan graph output for common PII patterns before publishing views.
- **Rate-limit public API.** Add a Caddy `rate_limit` directive on `graph-api.jbl-lab.com` (e.g. 60 req/min per IP) to cap accidental load from a stale browser tab.

## Success Criteria

1. Opening `https://graph.jbl-lab.com` on any LAN device renders the full labs-wiki graph in < 2 seconds (no Access prompt, served over HTTP via AdGuard rewrite).
2. Opening the same URL from a phone on LTE prompts Cloudflare Access login, then renders identically.
3. `mempalace_search` and the graph UI return consistent answers (no divergence between graph view and wiki content).
4. A wiki edit is reflected in the graph UI within 2 minutes end-to-end (watcher debounce + mine + graph rebuild + SSE).
5. Copilot CLI / VS Code / OpenCode can all `wiki_graph_neighbors("RoPE")` and get the same result via the `/mcp` endpoint (LAN direct, remote via service token).
6. Adding a new labs-wiki page with `[[wikilinks]]` automatically produces a graph node and edges with no manual intervention.
7. Zero additional LLM API keys introduced (consistent with the live-memory-loop constraint).
8. `curl https://graph-api.jbl-lab.com/internal/rebuild` from outside the homelab returns 403 without ever reaching the API container.

## Open Questions

1. **Graph rebuild on every wiki edit — too expensive?** Labs-wiki probably has 100-300 pages today. Full Leiden on 300 nodes is sub-second; incremental rebuild scoped to the changed community is overkill for now. Revisit at > 1000 pages.
2. **Cloudflare Access identity provider choice?** Email OTP works zero-config but breaks PWA install flows on iOS. Google SSO is smoother but pins access to a Google identity. Proposal: enable both, let each device pick the smoother path.
3. **Should the graph include drawers from MemPalace?** Labs-wiki pages are LLM-compiled; drawers are raw mined content. Mixing them in one graph may blur provenance. Proposal: keep them separate; drawers show up as *node metadata* on the matching wiki page ("3 related drawers in copilot_sessions"), not as their own nodes. Revisit if drawer graph proves useful independently.
4. **Cosmograph vs vis-network final call?** Start with Cosmograph for future-proofing (WebGL scales well). If bundle size or browser-compat issues hit, fall back to vis-network.
5. **Public API rate limit sizing?** 60 req/min is conservative but the `/graph/query` NL endpoint can stack up on a slow render. Start at 60 and watch Grafana; raise to 300 if legitimate usage trips it.
