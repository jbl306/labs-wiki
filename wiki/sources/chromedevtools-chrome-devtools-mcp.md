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
ingest_method: manual-reprocess-github-2026-04-22
quality_score: 80
concepts:
- model-context-protocol-mcp-server-for-chrome-devtools
- chrome-devtools-mcp-cli-interface
---

# ChromeDevTools/chrome-devtools-mcp

## What it is

`chrome-devtools-mcp` is an official Chrome DevTools project that lets a coding agent (Gemini, Claude, Cursor, Copilot, etc.) drive and inspect a live Chrome browser. It runs as a Model Context Protocol server, exposing the full DevTools surface — performance traces, network requests, console messages, screenshots — to the agent for automation, debugging, and performance analysis. A standalone CLI is also provided for use without MCP.

## Why it matters

For any project here that touches the web (debrid-downloader-web, parkcityyt scraping, the booking bots, future labs-wiki frontend work), this gives a coding agent first-class access to the same tooling a human would use in DevTools, without writing custom Puppeteer glue. It pairs naturally with the `stealth-browser` skill in `.github/skills/` for protected-site work, where you want both bot evasion *and* DevTools introspection.

## Key concepts

- **MCP server for browser control** — Standardised tool surface so any MCP-compatible agent can inspect/automate Chrome. See [[model-context-protocol-mcp-server-for-chrome-devtools]].
- **Performance insights** — Records DevTools traces and extracts actionable performance findings (uses the same Chrome DevTools frontend code).
- **Network + console inspection** — Source-mapped stack traces, network requests, browser console messages.
- **Puppeteer-backed automation** — Reliable wait-for-result behavior for clicks, navigation, and form interaction.
- **Slim mode** — `--slim` reduces the tool surface for basic browser tasks, lowering token cost. See [[chrome-devtools-mcp-cli-interface]].
- **CrUX integration** — Optional real-user performance data via the Chrome User Experience Report (disable with `--no-performance-crux`).

## How it works

- Agent connects to the MCP server (`npx -y chrome-devtools-mcp@latest`).
- Server launches/attaches to a Chrome instance using Puppeteer.
- Agent invokes MCP tools to navigate, screenshot, profile, or inspect; results are returned as structured data and source-mapped traces.
- Server periodically checks npm for updates (disable with `CHROME_DEVTOOLS_MCP_NO_UPDATE_CHECKS`).
- Telemetry is on by default; disable with `--no-usage-statistics` or env vars `CHROME_DEVTOOLS_MCP_NO_USAGE_STATISTICS` / `CI`.

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

- Exposes full browser content — including sensitive cookies/sessions — to whichever agent is connected. Avoid sharing instances that hold credentials you don't want the model to see.
- Officially supports only Google Chrome and Chrome for Testing; other Chromium-based browsers are unsupported.
- Telemetry on by default; the README is explicit that opting out of Chrome metrics does *not* opt you out here.
- Requires Node.js v20.19+ (latest LTS) and current-stable Chrome.

## Repo metadata

| Field | Value |
|---|---|
| Stars | 36,605 |
| Primary language | TypeScript |
| Topics | browser, chrome, chrome-devtools, debugging, devtools, mcp, mcp-server, puppeteer |
| License | (see upstream — Apache-2.0 per Chrome DevTools convention) |

## Source

- Raw dump: `raw/2026-04-13-httpsgithubcomchromedevtoolschrome-devtools-mcp.md`
- Upstream: https://github.com/ChromeDevTools/chrome-devtools-mcp
