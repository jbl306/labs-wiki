---
title: ChromeDevTools/chrome-devtools-mcp
type: source
created: '2026-04-21'
last_verified: '2026-04-22'
source_hash: 1d475978a97022195cd7c9a199d6b07df2932945141fa124a6d0a8fd51d93fdb
sources:
- raw/2026-04-13-httpsgithubcomchromedevtoolschrome-devtools-mcp.md
source_url: https://github.com/ChromeDevTools/chrome-devtools-mcp
tags:
- browser
- chrome
- chrome-devtools
- debugging
- devtools
- github
- mcp
- mcp-server
tier: warm
knowledge_state: ingested
ingest_method: manual-deepen-github-2026-04-22
quality_score: 59
concepts:
- model-context-protocol-mcp-server-for-chrome-devtools
- chrome-devtools-mcp-cli-interface
- mcp-tool-categories
---

# ChromeDevTools/chrome-devtools-mcp

## What it is

`chrome-devtools-mcp` is an official Chrome DevTools project that lets a coding agent (Gemini, Claude, Cursor, Copilot, etc.) drive and inspect a live Chrome browser. It runs as a Model Context Protocol server, exposing the full DevTools surface — performance traces, network requests, console messages, screenshots — to the agent for automation, debugging, and performance analysis. A standalone CLI is also provided for use without MCP.

## Why it matters

For any project here that touches the web (debrid-downloader-web, parkcityyt scraping, the booking bots, future labs-wiki frontend work), this gives a coding agent first-class access to the same tooling a human would use in DevTools, without writing custom Puppeteer glue. It pairs naturally with the `stealth-browser` skill in `.github/skills/` for protected-site work, where you want both bot evasion *and* DevTools introspection.

## Architecture / Technical model

- **MCP server wrapper** — Exposes Chrome DevTools Protocol (CDP) + Puppeteer to any MCP-compatible LLM agent (Claude, Gemini, Copilot, Cursor). Each tool call translates to CDP commands or Puppeteer actions with automatic wait-for-complete logic.
> See [[model-context-protocol-mcp-server-for-chrome-devtools]] for the full treatment.

- **34 MCP tools** — Grouped into 7 categories: Input automation (9), Navigation automation (6), Emulation (2), Performance (3), Network (2), Debugging (6), Extensions (5), Memory (1).
> See [[mcp-tool-categories]] for category design rationale.

- **Performance trace analysis** — `performance_start_trace` / `performance_stop_trace` / `performance_analyze_insight` use the same Chrome DevTools frontend code (shipped in the `chrome-devtools-frontend` npm package) to generate actionable performance recommendations. Optionally fetches real-user data via Google CrUX API (disable with `--no-performance-crux`).

- **Source-mapped stack traces** — Console messages (`get_console_message`, `list_console_messages`) return full stack traces mapped to original source files when sourcemaps are available, unlike raw CDP which exposes only transpiled line numbers.

- **Slim mode** — `--slim` drops the Performance/Memory/Extensions categories and reduces tool count to ~15 for basic navigation+debugging workflows (faster MCP handshake, lower LLM token cost).
> See [[chrome-devtools-mcp-cli-interface]] for CLI configuration.

- **Lighthouse audit integration** — `lighthouse_audit` tool runs a full Lighthouse audit (performance, accessibility, best-practices, SEO) and returns structured JSON results + HTML report.

- **Auto-connect mode** — `--autoConnect` attaches to an already-running Chrome instance via remote debugging (Chrome 144+, requires chrome://inspect/#remote-debugging enabled). Alternative: `--browserUrl` / `--wsEndpoint` for explicit connection endpoints.

- **Telemetry + update checks** — Google collects tool invocation success rates, latency, and environment info by default (opt-out: `--no-usage-statistics` or `CHROME_DEVTOOLS_MCP_NO_USAGE_STATISTICS` env var). Update checks poll npm registry (disable with `CHROME_DEVTOOLS_MCP_NO_UPDATE_CHECKS`).

## How it works

1. Agent MCP client starts the server: `npx -y chrome-devtools-mcp@latest` (optionally with `--slim`, `--headless`, `--autoConnect`).
2. Server initializes Puppeteer and launches/attaches to a Chrome instance (lazy: only on first tool invocation requiring a browser).
3. Agent calls MCP tools (e.g., `navigate_page`, `click`, `take_screenshot`, `performance_start_trace`).
4. Server translates each tool call to Puppeteer actions or CDP commands, waits for completion, and returns structured results.
5. For performance tools: server records a DevTools trace, processes it through the Chrome DevTools frontend analysis engine, optionally enriches with CrUX field data, and returns actionable insights.
6. For network tools: maintains a `NetworkCollector` that buffers all requests/responses during the session; tools query this buffer by request ID or return filtered lists.
7. Extension tools (install/reload/trigger/uninstall) use Puppeteer's Extension API to manage unpacked or CRX extensions during the session.
8. Memory tools (`take_memory_snapshot`) capture heap snapshots via CDP and return structured analysis (retained size, detached DOMs, etc.).
9. Server emits telemetry events (success/failure, latency) to Google's collection endpoint unless telemetry is disabled.
10. Update check runs once per session startup unless `CHROME_DEVTOOLS_MCP_NO_UPDATE_CHECKS` is set.

## API / interface surface

### MCP Tools (34 total)

**Input automation (9 tools)**
| Tool | Description |
|------|-------------|
| `click` | Click an element by selector |
| `drag` | Drag an element to a target location |
| `fill` | Fill a form field with text |
| `fill_form` | Fill multiple form fields at once |
| `handle_dialog` | Accept/dismiss browser dialogs (alert/confirm/prompt) |
| `hover` | Hover over an element |
| `press_key` | Send a keyboard event |
| `type_text` | Type text character-by-character |
| `upload_file` | Upload a file to an input |

**Navigation automation (6 tools)**
| Tool | Description |
|------|-------------|
| `close_page` | Close a tab |
| `list_pages` | List all open tabs |
| `navigate_page` | Navigate to a URL |
| `new_page` | Open a new tab |
| `select_page` | Switch active tab |
| `wait_for` | Wait for element/navigation/timeout |

**Emulation (2 tools)**
| Tool | Description |
|------|-------------|
| `emulate` | Set device/viewport/user-agent emulation |
| `resize_page` | Resize viewport |

**Performance (3 tools)**
| Tool | Description |
|------|-------------|
| `performance_analyze_insight` | Analyze a completed trace for actionable insights |
| `performance_start_trace` | Begin recording a DevTools trace |
| `performance_stop_trace` | Stop trace and return trace data |

**Network (2 tools)**
| Tool | Description |
|------|-------------|
| `get_network_request` | Fetch details of a specific network request by ID |
| `list_network_requests` | List all captured network requests (filterable) |

**Debugging (6 tools)**
| Tool | Description |
|------|-------------|
| `evaluate_script` | Evaluate JavaScript in page context |
| `get_console_message` | Fetch a specific console message by ID |
| `lighthouse_audit` | Run a full Lighthouse audit |
| `list_console_messages` | List all console logs with source-mapped stacks |
| `take_screenshot` | Capture a screenshot (full page or selector) |
| `take_snapshot` | Capture DOM snapshot (serialized HTML) |

**Extensions (5 tools)**
| Tool | Description |
|------|-------------|
| `install_extension` | Install a Chrome extension from unpacked dir or CRX |
| `list_extensions` | List installed extensions |
| `reload_extension` | Reload an extension by ID |
| `trigger_extension_action` | Programmatically trigger an extension's action |
| `uninstall_extension` | Remove an extension by ID |

**Memory (1 tool)**
| Tool | Description |
|------|-------------|
| `take_memory_snapshot` | Capture heap snapshot with retained size analysis |

### CLI Interface

```bash
chrome-devtools-mcp [options]
chrome-devtools [options]   # CLI mode (non-MCP)
```

**Key flags:**
- `--autoConnect` / `--auto-connect`: Attach to running Chrome via remote debugging (Chrome 144+)
- `--browserUrl` / `--browser-url`, `-u`: Connect to debuggable Chrome instance (e.g., `http://127.0.0.1:9222`)
- `--wsEndpoint` / `--ws-endpoint`, `-w`: WebSocket endpoint (alternative to `--browserUrl`)
- `--slim`: Enable slim mode (fewer tools)
- `--headless`: Run Chrome in headless mode
- `--no-usage-statistics`: Disable telemetry
- `--no-performance-crux`: Disable CrUX API calls in performance tools
- `--userDataDir`: Custom Chrome profile directory
- `--executablePath`: Custom Chrome/Chromium binary path

## Setup

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    }
  }
}
```

For lightweight headless use:

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest", "--slim", "--headless"]
    }
  }
}
```

## Integration notes

Drop-in MCP server for Copilot CLI / OpenCode by adding to `~/.copilot/mcp-config.json`. Most useful when paired with `stealth-browser` for sites with bot protection — `chrome-devtools-mcp` itself uses Puppeteer and offers no anti-bot stealth. Could replace ad-hoc Selenium/nodriver scripts in the booking bot family for non-protected pages.

## Caveats / Gotchas

- **Exposes full browser content** — Cookies, sessions, localStorage, and all page data are visible to the MCP client. Avoid sharing instances holding credentials you don't want the model to see.
- **Chrome/Chrome for Testing only** — Officially supports only Google Chrome and Chrome for Testing. Other Chromium browsers (Edge, Brave) may work but are unsupported; use at your own risk.
- **Telemetry on by default** — Google collects tool invocation success rates, latency, and environment info. Opt-out requires explicit `--no-usage-statistics` flag or `CHROME_DEVTOOLS_MCP_NO_USAGE_STATISTICS` / `CI` env vars.
- **CrUX API by default** — Performance tools send trace URLs to Google CrUX API for real-user data. Disable with `--no-performance-crux` if you don't want external API calls.
- **Update checks by default** — Server polls npm registry on startup. Set `CHROME_DEVTOOLS_MCP_NO_UPDATE_CHECKS` to disable.
- **Node.js 20.19+ required** — Older Node versions are unsupported. Minimum is v20.19 or newer latest maintenance LTS.
- **Browser instance limits** — Many open tabs (50+) can cause hangs/crashes due to memory pressure; README notes resource limitations.
- **No anti-bot stealth** — Uses standard Puppeteer; detected by Cloudflare, Datadome, PerimeterX, etc. Pair with the `stealth-browser` skill for protected sites.

## Repo metadata

| Field | Value |
|---|---|
| Stars | 36,605 |
| Primary language | TypeScript |
| Topics | browser, chrome, chrome-devtools, debugging, devtools, mcp, mcp-server, puppeteer |
| License | (see upstream — Apache-2.0 per Chrome DevTools convention) |

## Related concepts

- [[model-context-protocol-mcp-server-for-chrome-devtools]]
- [[chrome-devtools-mcp-cli-interface]]
- [[mcp-tool-categories]]

## Source

- Raw dump: `raw/2026-04-13-httpsgithubcomchromedevtoolschrome-devtools-mcp.md`
- Upstream: https://github.com/ChromeDevTools/chrome-devtools-mcp
