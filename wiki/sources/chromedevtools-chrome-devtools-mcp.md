---
title: ChromeDevTools/chrome-devtools-mcp
type: source
created: '2026-04-21'
last_verified: '2026-04-21'
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
ingest_method: self-synthesis-no-llm
quality_score: 50
---

# ChromeDevTools/chrome-devtools-mcp

## Summary

Chrome DevTools for coding agents

## Repository Info

- **Source URL**: https://github.com/ChromeDevTools/chrome-devtools-mcp
- **Stars**: 36605
- **Primary language**: TypeScript
- **Topics**: browser, chrome, chrome-devtools, debugging, devtools, mcp, mcp-server, puppeteer

## README Excerpt

# Chrome DevTools for Agents

[![npm chrome-devtools-mcp package](https://img.shields.io/npm/v/chrome-devtools-mcp.svg)](https://npmjs.org/package/chrome-devtools-mcp)

Chrome DevTools for Agents (`chrome-devtools-mcp`) lets your coding agent (such as Gemini, Claude, Cursor or Copilot)
control and inspect a live Chrome browser. It acts as a Model-Context-Protocol
(MCP) server, giving your AI coding assistant access to the full power of
Chrome DevTools for reliable automation, in-depth debugging, and performance analysis.
A [CLI](docs/cli.md) is also provided for use without MCP.

## Activity Snapshot

### Recent Releases

### chrome-devtools-mcp-v0.22.0 (2026-04-21)
### Recent Commits

- 2026-04-21 a1612be Nicholas Roscino: test: refactor tests to reduce duplication (#1926)
- 2026-04-21 42be7c3 Alex Rudenko: docs: clarify resource limitations around the number of tabs (#1927)
- 2026-04-21 b53752d Wolfgang Beyer: chore: move resolveCdpElementId (#1923)
- 2026-04-21 f0da776 browser-automation-bot: chore(main): release chrome-devtools-mcp 0.22.0 (#1884)
- 2026-04-21 76ab9fa Alex Rudenko: docs: clarify tools included into CLI (#1925)
- 2026-04-21 3ff21cf Nicholas Roscino: feat: support Chrome extensions debugging (#1922)
- 2026-04-21 86ffd58 Nicholas Roscino: test: add test for console log from content script (#1920)
- 2026-04-20 57648b7 Alex Rudenko: chore(deps): update lh (#1913)
- 2026-04-20 9211c6b Nikolay Vitkov: chore(memory): expose a tool for getting the inital data. (#1909)
- 2026-04-20 ec895f1 Nicholas Roscino: refactor: use puppeteer Extension API (#1911)
- 2026-04-20 562c308 dependabot[bot]: chore(deps-dev): bump the dev-dependencies group with 2 updates (#1907)
- 2026-04-20 3a24d71 Mukunda Rao Katta: test: save WebP responses with the right extension (#1901)
- 2026-04-20 e3a5f6b Cocoon-Break: fix(cli): correct WebP MIME type check in handleResponse ('webp' → 'image/webp') (#1899)
- 2026-04-20 0f29acf Alex Rudenko: chore: fix viewport eval (#1888)
- 2026-04-20 da33cb5 Nikolay Vitkov: feat: auto handle dialogs during script evaluation  (#1839)
- 2026-04-20 0ed086e Nikolay Vitkov: chore: remove code around Audits setup (#1893)
- 2026-04-17 0a6aaa5 yulunz: chore: generate a json file for flag usage metrics (#1881)
- 2026-04-17 0331f6a Nikolay Vitkov: chore: implement memory snapshot information (#1874)
- 2026-04-17 ea57e86 Asish Kumar: fix: ignore unmapped PerformanceIssue events (#1852)
- 2026-04-17 2f458c1 Nikolay Vitkov: fix(network): trailing data in Network redirect chain (#1880)
### Open Issues (top 10)

- #1912 Unable to read the Google Sheet Web Page (by maxsxu)
- #1921 Browser hangs / crashes when MCP connects to Chrome with many tabs (by jabagawee)
- #1775 Feature: Add evaluate_script_file tool to evaluate JavaScript files from the local filesystem (by achideal)
### Recently Merged PRs (top 10)

- #1926 test: refactor tests to reduce duplication (merged 2026-04-21)
- #1927 docs: clarify resource limitations around the number of tabs (merged 2026-04-21)
- #1923 chore: move resolveCdpElementId (merged 2026-04-21)
- #1884 chore(main): release chrome-devtools-mcp 0.22.0 (merged 2026-04-21)
- #1925 docs: clarify tools included into CLI (merged 2026-04-21)
- #1922 feat: support Chrome extensions debugging (merged 2026-04-21)
- #1920 test: add test for console log from content script (merged 2026-04-21)
- #1913 chore(deps): update lh (merged 2026-04-20)
- #1909 chore(memory): expose a tool for getting the inital data. (merged 2026-04-20)
- #1022 feat: add pageId routing for parallel multi-agent workflows (merged 2026-02-26)

## Crawled Files

Source dump in `raw/2026-04-13-httpsgithubcomchromedevtoolschrome-devtools-mcp.md` includes:

- `.gitignore`
- `LICENSE`
- `package-lock.json`
- `package.json`
- `docs/cli.md`
- `docs/debugging-android.md`
- `docs/design-principles.md`
- `docs/slim-tool-reference.md`
- `docs/tool-reference.md`
- `docs/troubleshooting.md`
- `.mcp.json`
- `.release-please-manifest.json`
- `CHANGELOG.md`
