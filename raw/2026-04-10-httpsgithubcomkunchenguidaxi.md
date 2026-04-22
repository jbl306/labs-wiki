---
title: https://github.com/kunchenguid/axi
type: url
captured: 2026-04-10 12:46:15.099835+00:00
source: android-share
url: https://github.com/kunchenguid/axi
content_hash: sha256:7bdf60ec60c55a435a654e5f668ec402c5f9482ec20d8f6730ccff27dd5cec41
tags: []
status: ingested
last_refreshed: '2026-04-22T02:44:17+00:00'
---

https://github.com/kunchenguid/axi

<!-- fetched-content:start -->
## Fetched Metadata
- fetched_at: 2026-04-22T02:44:17+00:00
- source_url: https://github.com/kunchenguid/axi
- resolved_url: https://github.com/kunchenguid/axi
- content_type: application/vnd.github+json
- image_urls: []

## Fetched Content
Repository: kunchenguid/axi
Description: Design principles for agent ergonomics. Higher accuracy with lower token cost than both MCP and regular CLI.
Stars: 763
Language: TypeScript

## README

<h1 align="center">AXI: Agent eXperience Interface</h1>

<p align="center">
  <a href="https://axi.md"><img alt="Website" src="https://img.shields.io/badge/axi.md-Website-blue?style=flat-square" /></a>
  <a href="https://x.com/kunchenguid"><img alt="X" src="https://img.shields.io/badge/X-@kunchenguid-black?style=flat-square" /></a>
  <a href="https://discord.gg/Wsy2NpnZDu"><img alt="Discord" src="https://img.shields.io/discord/1439901831038763092?style=flat-square&label=discord" /></a>
</p>

<h3 align="center">10 design principles for building agent-ergonomic apps.</h3>

<p align="center">
  <img src="docs/axi-splash.png" alt="AXI — Let's build apps agents love." width="800">
</p>

AI agents interact with external services through two dominant paradigms today: **CLIs** which were originally built for humans, and structured tool protocols like **MCP**. Both impose significant overhead.

AXI is a **new paradigm** — agent-native CLI tools built from **10 design principles** that treat token budget as a first-class constraint.

## Results

### Browser Benchmark

Evaluated across 490 runs (14 tasks × 7 conditions × 5 repeats) using Claude Sonnet 4.6:

| Condition                      | Success  | Avg Cost   | Avg Duration | Avg Turns |
| ------------------------------ | -------- | ---------- | ------------ | --------- |
| **chrome-devtools-axi**        | **100%** | **$0.074** | **21.5s**    | **4.5**   |
| dev-browser                    | 99%      | $0.078     | 28.6s        | 4.9       |
| agent-browser                  | 99%      | $0.088     | 24.6s        | 4.8       |
| chrome-devtools-mcp-compressed | 100%     | $0.091     | 29.7s        | 7.6       |
| chrome-devtools-mcp-search     | 99%      | $0.096     | 29.4s        | 7.5       |
| chrome-devtools-mcp            | 99%      | $0.101     | 26.0s        | 6.2       |
| chrome-devtools-mcp-code       | 100%     | $0.120     | 36.2s        | 6.4       |

### GitHub Benchmark

Evaluated across 425 runs (17 tasks × 5 conditions × 5 repeats) using Claude Sonnet 4.6:

| Condition               | Success  | Avg Cost   | Avg Duration | Avg Turns |
| ----------------------- | -------- | ---------- | ------------ | --------- |
| **gh-axi**              | **100%** | **$0.050** | **15.7s**    | **3**     |
| gh (CLI)                | 86%      | $0.054     | 17.4s        | 3         |
| GitHub MCP              | 87%      | $0.148     | 34.2s        | 6         |
| GitHub MCP + ToolSearch | 82%      | $0.147     | 41.1s        | 8         |
| MCP + Code Mode         | 84%      | $0.101     | 43.4s        | 7         |

## Quick Start

Reference AXI implementations:

- [`gh-axi`](https://github.com/kunchenguid/gh-axi) — GitHub operations
- [`chrome-devtools-axi`](https://github.com/kunchenguid/chrome-devtools-axi) — Browser automation

```sh
npm install -g gh-axi
npm install -g chrome-devtools-axi
```

Add to your `CLAUDE.md` or `AGENTS.md`:

```
Use `gh-axi` for GitHub and `chrome-devtools-axi` for browser automation.
```

## The 10 Principles

These principles define what makes a CLI tool "an AXI":

| #   | Principle                          | Summary                                                                     |
| --- | ---------------------------------- | --------------------------------------------------------------------------- |
| 1   | **Token-efficient output**         | Use [TOON](https://toonformat.dev/) format for ~40% token savings over JSON |
| 2   | **Minimal default schemas**        | 3–4 fields per list item, not 10                                            |
| 3   | **Content truncation**             | Truncate large text with size hints and `--full` escape hatch               |
| 4   | **Pre-computed aggregates**        | Include aggregated counts and statuses that eliminate round trips           |
| 5   | **Definitive empty states**        | Explicit "0 results" rather than ambiguous empty output                     |
| 6   | **Structured errors & exit codes** | Idempotent mutations, structured errors, no interactive prompts             |
| 7   | **Ambient context**                | Self-install into session hooks so agents see state before invoking         |
| 8   | **Content first**                  | Running with no arguments shows live data, not help text                    |
| 9   | **Contextual disclosure**          | Include next-step suggestions after each output                             |
| 10  | **Consistent way to get help**     | Concise per-subcommand reference when agents need it                        |

## Build Your Own AXI

Install the AXI skill to get the design guidelines and scaffolding for building an AXI-compliant CLI:

```sh
npx skills add kunchenguid/axi
```

This installs the [AXI skill](.agents/skills/axi/SKILL.md) — a detailed guide with examples for each principle that your coding agent can reference while building.

## Development

### Browser Benchmark

The browser benchmark harness lives in `bench-browser/`. It compares browser automation tools across 16 browsing tasks.

```sh
cd bench-browser
npm install

# Run a single condition × task
npm run bench -- run --condition chrome-devtools-axi --task read_static_page

# Run the full matrix
npm run bench -- matrix --repeat 5

# Generate summary report
npm run bench -- report

# Render the social video
npm run render:social
```

The HyperFrames composition for the social asset lives in `bench-browser/social/`. Edit `social/index.html` for the animation and render `docs/social/rendered/race.mp4` with `npm run render:social`.

Published results (490 runs): [`bench-browser/published-results/report.md`](bench-browser/published-results/report.md)

### GitHub Benchmark

The GitHub benchmark harness lives in `bench-github/`. It runs agent tasks across different interface conditions and grades results with an LLM judge.

```sh
cd bench-github
npm install

# Run a single condition × task
npm run bench -- run --condition axi --task merged_pr_ci_audit --repeat 5 --agent claude

# Run the full matrix
npm run bench -- matrix --repeat 5 --agent claude

# Generate summary report
npm run bench -- report
```

Published results (425 runs): [`bench-github/published-results/STUDY.md`](bench-github/published-results/STUDY.md)

## Links

- [Website](https://axi.md)
- [AXI Skill definition](.agents/skills/axi/SKILL.md)
- [Browser benchmark study](bench-browser/published-results/STUDY.md)
- [GitHub benchmark study](bench-github/published-results/STUDY.md)

Languages: TypeScript 93.8%, HTML 5.8%, JavaScript 0.4%

## Recent Releases

### axi-sdk-js-v0.1.4 (2026-04-03)

## [0.1.4](https://github.com/kunchenguid/axi/compare/axi-sdk-js-v0.1.3...axi-sdk-js-v0.1.4) (2026-04-03)


### Features

* **cli:** add explicit argv support ([#25](https://github.com/kunchenguid/axi/issues/25)) ([7b1202b](https://github.com/kunchenguid/axi/commit/7b1202b1be9a4c1349e16630dc1b99aede827f54))

### axi-sdk-js-v0.1.3 (2026-04-02)

## [0.1.3](https://github.com/kunchenguid/axi/compare/axi-sdk-js-v0.1.2...axi-sdk-js-v0.1.3) (2026-04-02)


### Features

* **cli:** add version flag support ([#23](https://github.com/kunchenguid/axi/issues/23)) ([e05e312](https://github.com/kunchenguid/axi/commit/e05e312c5341175c1babe1a0c067a60a773f75f9))

### axi-sdk-js-v0.1.2 (2026-04-02)

## [0.1.2](https://github.com/kunchenguid/axi/compare/axi-sdk-js-v0.1.1...axi-sdk-js-v0.1.2) (2026-04-02)


### Features

* better encapsulation of args handling in sdk ([#21](https://github.com/kunchenguid/axi/issues/21)) ([c7414b5](https://github.com/kunchenguid/axi/commit/c7414b50f20b1dd6c28b0f10007f3f8fd761e116))

### axi-sdk-js-v0.1.1 (2026-04-02)

## [0.1.1](https://github.com/kunchenguid/axi/compare/axi-sdk-js-v0.1.0...axi-sdk-js-v0.1.1) (2026-04-02)


### Features

* axi-sdk-js ([#18](https://github.com/kunchenguid/axi/issues/18)) ([309ef60](https://github.com/kunchenguid/axi/commit/309ef60c25cc0843764245cd2fc65f5a1f918d00))

### v0.1.3 (2026-03-23)

## [0.1.3](https://github.com/kunchenguid/axi/compare/v0.1.2...v0.1.3) (2026-03-23)


### Features

* initial commit ([ee125cd](https://github.com/kunchenguid/axi/commit/ee125cdf3c35bffcee5a12ae3af2ce7212336876))


### Bug Fixes

* **package:** correct repository URL ([f4f60c7](https://github.com/kunchenguid/axi/commit/f4f60c71077dbdd7ea04ecc4f617a624b21a245b))
* **README:** update search description ([bc79a50](https://github.com/kunchenguid/axi/commit/bc79a504ea6d85f71cc5c738d47af047184941e4))

## Recent Commits

- 2026-04-17 5feecbc Kun Chen: feat(bench-browser): add HyperFrames social video workflow (#30)
- 2026-04-08 5839015 kunchenguid: feat(docs): add social video rendering and update race colors
- 2026-04-07 8be89a2 kunchenguid: fix: fixed mcp-code condition
- 2026-04-07 3f86192 kunchenguid: fix(bench): improve social video rendering and tests
- 2026-04-04 65e6c8a Kun Chen: feat: refresh browser benchmark (#27)
- 2026-04-03 d343bcb github-actions[bot]: chore(main): release axi-sdk-js 0.1.4 (#26)
- 2026-04-03 7b1202b Kun Chen: feat(cli): add explicit argv support (#25)
- 2026-04-02 7d73d07 github-actions[bot]: chore(main): release axi-sdk-js 0.1.3 (#24)
- 2026-04-02 e05e312 Kun Chen: feat(cli): add version flag support (#23)
- 2026-04-02 cc2333f github-actions[bot]: chore(main): release axi-sdk-js 0.1.2 (#22)
- 2026-04-02 c7414b5 Kun Chen: feat: better encapsulation of args handling in sdk (#21)
- 2026-04-02 c2ce65f Kun Chen: fix: formatter ignore (#20)
- 2026-04-02 01c5be8 github-actions[bot]: chore(main): release axi-sdk-js 0.1.1 (#19)
- 2026-04-02 309ef60 Kun Chen: feat: axi-sdk-js (#18)
- 2026-04-01 e5df9a8 Kun Chen: fix(skill): update Claude Code and Codex sections in SKILL.md (#17)
- 2026-03-30 62bdc8b kunchenguid: chore(readme): update discord invite link
- 2026-03-29 29cb5f1 kunchenguid: fix: update skill on contextual disclosure best practice
- 2026-03-29 d44a674 kunchenguid: docs: document best practice for home view
- 2026-03-29 db3a0be Truong Khanh Nguyen: Fix a few issues when trying the project (#15)
- 2026-03-29 f56110e kunchenguid: feat(render): add social race video rendering script and assets

## Open Issues (top 10)

- #32 Thoughts on JSON output? (by themightychris)
- #31 Feedback wanted: building a Google Workspace AXI CLI (by themightychris)

## Recently Merged PRs (top 10)

- #30 feat(bench-browser): add HyperFrames social video workflow (merged 2026-04-17)
- #27 feat: refresh browser benchmark (merged 2026-04-04)
- #26 chore(main): release axi-sdk-js 0.1.4 (merged 2026-04-03)
- #25 feat(cli): add explicit argv support (merged 2026-04-03)
- #24 chore(main): release axi-sdk-js 0.1.3 (merged 2026-04-02)
- #23 feat(cli): add version flag support (merged 2026-04-02)
- #22 chore(main): release axi-sdk-js 0.1.2 (merged 2026-04-02)
- #21 feat: better encapsulation of args handling in sdk (merged 2026-04-02)
- #20 fix: formatter ignore (merged 2026-04-02)
- #19 chore(main): release axi-sdk-js 0.1.1 (merged 2026-04-02)


## File: .gitignore

```
# Dependencies
node_modules/

# Build output
dist/

# Benchmark results (generated, often large)
bench/results/*
bench/ITERATIONS.md
!bench/results/.gitkeep
bench-github/results/
bench-browser/results/

# Published benchmark results (tracked)
!bench/published-results/

# Blog draft (not version-controlled)
docs/blog.md
docs/social/rendered/

# Desloppify
.desloppify/

# OS
.DS_Store

.gnhf/runs/

```


## File: bench-browser/package-lock.json

```
{
  "name": "axi-bench-browser",
  "version": "0.1.0",
  "lockfileVersion": 3,
  "requires": true,
  "packages": {
    "": {
      "name": "axi-bench-browser",
      "version": "0.1.0",
      "dependencies": {
        "@modelcontextprotocol/sdk": "^1.12.0",
        "yaml": "^2.7.0"
      },
      "devDependencies": {
        "@types/node": "^22.0.0",
        "tsx": "^4.19.0",
        "typescript": "^5.7.0",
        "vitest": "^3.0.0"
      },
      "engines": {
        "node": ">=20"
      }
    },
    "node_modules/@esbuild/aix-ppc64": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/aix-ppc64/-/aix-ppc64-0.27.4.tgz",
      "integrity": "sha512-cQPwL2mp2nSmHHJlCyoXgHGhbEPMrEEU5xhkcy3Hs/O7nGZqEpZ2sUtLaL9MORLtDfRvVl2/3PAuEkYZH0Ty8Q==",
      "cpu": [
        "ppc64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "aix"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/android-arm": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/android-arm/-/android-arm-0.27.4.tgz",
      "integrity": "sha512-X9bUgvxiC8CHAGKYufLIHGXPJWnr0OCdR0anD2e21vdvgCI8lIfqFbnoeOz7lBjdrAGUhqLZLcQo6MLhTO2DKQ==",
      "cpu": [
        "arm"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "android"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/android-arm64": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/android-arm64/-/android-arm64-0.27.4.tgz",
      "integrity": "sha512-gdLscB7v75wRfu7QSm/zg6Rx29VLdy9eTr2t44sfTW7CxwAtQghZ4ZnqHk3/ogz7xao0QAgrkradbBzcqFPasw==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "android"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/android-x64": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/android-x64/-/android-x64-0.27.4.tgz",
      "integrity": "sha512-PzPFnBNVF292sfpfhiyiXCGSn9HZg5BcAz+ivBuSsl6Rk4ga1oEXAamhOXRFyMcjwr2DVtm40G65N3GLeH1Lvw==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "android"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/darwin-arm64": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/darwin-arm64/-/darwin-arm64-0.27.4.tgz",
      "integrity": "sha512-b7xaGIwdJlht8ZFCvMkpDN6uiSmnxxK56N2GDTMYPr2/gzvfdQN8rTfBsvVKmIVY/X7EM+/hJKEIbbHs9oA4tQ==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "darwin"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/darwin-x64": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/darwin-x64/-/darwin-x64-0.27.4.tgz",
      "integrity": "sha512-sR+OiKLwd15nmCdqpXMnuJ9W2kpy0KigzqScqHI3Hqwr7IXxBp3Yva+yJwoqh7rE8V77tdoheRYataNKL4QrPw==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "darwin"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/freebsd-arm64": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/freebsd-arm64/-/freebsd-arm64-0.27.4.tgz",
      "integrity": "sha512-jnfpKe+p79tCnm4GVav68A7tUFeKQwQyLgESwEAUzyxk/TJr4QdGog9sqWNcUbr/bZt/O/HXouspuQDd9JxFSw==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "freebsd"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/freebsd-x64": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/freebsd-x64/-/freebsd-x64-0.27.4.tgz",
      "integrity": "sha512-2kb4ceA/CpfUrIcTUl1wrP/9ad9Atrp5J94Lq69w7UwOMolPIGrfLSvAKJp0RTvkPPyn6CIWrNy13kyLikZRZQ==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "freebsd"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/linux-arm": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-arm/-/linux-arm-0.27.4.tgz",
      "integrity": "sha512-aBYgcIxX/wd5n2ys0yESGeYMGF+pv6g0DhZr3G1ZG4jMfruU9Tl1i2Z+Wnj9/KjGz1lTLCcorqE2viePZqj4Eg==",
      "cpu": [
        "arm"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/linux-arm64": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-arm64/-/linux-arm64-0.27.4.tgz",
      "integrity": "sha512-7nQOttdzVGth1iz57kxg9uCz57dxQLHWxopL6mYuYthohPKEK0vU0C3O21CcBK6KDlkYVcnDXY099HcCDXd9dA==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/linux-ia32": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-ia32/-/linux-ia32-0.27.4.tgz",
      "integrity": "sha512-oPtixtAIzgvzYcKBQM/qZ3R+9TEUd1aNJQu0HhGyqtx6oS7qTpvjheIWBbes4+qu1bNlo2V4cbkISr8q6gRBFA==",
      "cpu": [
        "ia32"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/linux-loong64": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-loong64/-/linux-loong64-0.27.4.tgz",
      "integrity": "sha512-8mL/vh8qeCoRcFH2nM8wm5uJP+ZcVYGGayMavi8GmRJjuI3g1v6Z7Ni0JJKAJW+m0EtUuARb6Lmp4hMjzCBWzA==",
      "cpu": [
        "loong64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/linux-mips64el": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-mips64el/-/linux-mips64el-0.27.4.tgz",
      "integrity": "sha512-1RdrWFFiiLIW7LQq9Q2NES+HiD4NyT8Itj9AUeCl0IVCA459WnPhREKgwrpaIfTOe+/2rdntisegiPWn/r/aAw==",
      "cpu": [
        "mips64el"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/linux-ppc64": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-ppc64/-/linux-ppc64-0.27.4.tgz",
      "integrity": "sha512-tLCwNG47l3sd9lpfyx9LAGEGItCUeRCWeAx6x2Jmbav65nAwoPXfewtAdtbtit/pJFLUWOhpv0FpS6GQAmPrHA==",
      "cpu": [
        "ppc64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/linux-riscv64": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-riscv64/-/linux-riscv64-0.27.4.tgz",
      "integrity": "sha512-BnASypppbUWyqjd1KIpU4AUBiIhVr6YlHx/cnPgqEkNoVOhHg+YiSVxM1RLfiy4t9cAulbRGTNCKOcqHrEQLIw==",
      "cpu": [
        "riscv64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/linux-s390x": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-s390x/-/linux-s390x-0.27.4.tgz",
      "integrity": "sha512-+eUqgb/Z7vxVLezG8bVB9SfBie89gMueS+I0xYh2tJdw3vqA/0ImZJ2ROeWwVJN59ihBeZ7Tu92dF/5dy5FttA==",
      "cpu": [
        "s390x"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/linux-x64": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-x64/-/linux-x64-0.27.4.tgz",
      "integrity": "sha512-S5qOXrKV8BQEzJPVxAwnryi2+Iq5pB40gTEIT69BQONqR7JH1EPIcQ/Uiv9mCnn05jff9umq/5nqzxlqTOg9NA==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/netbsd-arm64": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/netbsd-arm64/-/netbsd-arm64-0.27.4.tgz",
      "integrity": "sha512-xHT8X4sb0GS8qTqiwzHqpY00C95DPAq7nAwX35Ie/s+LO9830hrMd3oX0ZMKLvy7vsonee73x0lmcdOVXFzd6Q==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "netbsd"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/netbsd-x64": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/netbsd-x64/-/netbsd-x64-0.27.4.tgz",
      "integrity": "sha512-RugOvOdXfdyi5Tyv40kgQnI0byv66BFgAqjdgtAKqHoZTbTF2QqfQrFwa7cHEORJf6X2ht+l9ABLMP0dnKYsgg==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "netbsd"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/openbsd-arm64": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/openbsd-arm64/-/openbsd-arm64-0.27.4.tgz",
      "integrity": "sha512-2MyL3IAaTX+1/qP0O1SwskwcwCoOI4kV2IBX1xYnDDqthmq5ArrW94qSIKCAuRraMgPOmG0RDTA74mzYNQA9ow==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "openbsd"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/openbsd-x64": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/openbsd-x64/-/openbsd-x64-0.27.4.tgz",
      "integrity": "sha512-u8fg/jQ5aQDfsnIV6+KwLOf1CmJnfu1ShpwqdwC0uA7ZPwFws55Ngc12vBdeUdnuWoQYx/SOQLGDcdlfXhYmXQ==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "openbsd"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/openharmony-arm64": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/openharmony-arm64/-/openharmony-arm64-0.27.4.tgz",
      "integrity": "sha512-JkTZrl6VbyO8lDQO3yv26nNr2RM2yZzNrNHEsj9bm6dOwwu9OYN28CjzZkH57bh4w0I2F7IodpQvUAEd1mbWXg==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "openharmony"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/sunos-x64": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/sunos-x64/-/sunos-x64-0.27.4.tgz",
      "integrity": "sha512-/gOzgaewZJfeJTlsWhvUEmUG4tWEY2Spp5M20INYRg2ZKl9QPO3QEEgPeRtLjEWSW8FilRNacPOg8R1uaYkA6g==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "sunos"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/win32-arm64": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/win32-arm64/-/win32-arm64-0.27.4.tgz",
      "integrity": "sha512-Z9SExBg2y32smoDQdf1HRwHRt6vAHLXcxD2uGgO/v2jK7Y718Ix4ndsbNMU/+1Qiem9OiOdaqitioZwxivhXYg==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "win32"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/win32-ia32": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/win32-ia32/-/win32-ia32-0.27.4.tgz",
      "integrity": "sha512-DAyGLS0Jz5G5iixEbMHi5KdiApqHBWMGzTtMiJ72ZOLhbu/bzxgAe8Ue8CTS3n3HbIUHQz/L51yMdGMeoxXNJw==",
      "cpu": [
        "ia32"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "win32"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/win32-x64": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/win32-x64/-/win32-x64-0.27.4.tgz",
      "integrity": "sha512-+knoa0BDoeXgkNvvV1vvbZX4+hizelrkwmGJBdT17t8FNPwG2lKemmuMZlmaNQ3ws3DKKCxpb4zRZEIp3UxFCg==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "win32"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@hono/node-server": {
      "version": "1.19.11",
      "resolved": "https://registry.npmjs.org/@hono/node-server/-/node-server-1.19.11.tgz",
      "integrity": "sha512-dr8/3zEaB+p0D2n/IUrlPF1HZm586qgJNXK1a9fhg/PzdtkK7Ksd5l312tJX2yBuALqDYBlG20QEbayqPyxn+g==",
      "license": "MIT",
      "engines": {
        "node": ">=18.14.1"
      },
      "peerDependencies": {
        "hono": "^4"
      }
    },
    "node_modules/@jridgewell/sourcemap-codec": {
      "version": "1.5.5",
      "resolved": "https://registry.npmjs.org/@jridgewell/sourcemap-codec/-/sourcemap-codec-1.5.5.tgz",
      "integrity": "sha512-cYQ9310grqxueWbl+WuIUIaiUaDcj7WOq5fVhEljNVgRfOUhY9fy2zTvfoqWsnebh8Sl70VScFbICvJnLKB0Og==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/@modelcontextprotocol/sdk": {
      "version": "1.28.0",
      "resolved": "https://registry.npmjs.org/@modelcontextprotocol/sdk/-/sdk-1.28.0.tgz",
      "integrity": "sha512-gmloF+i+flI8ouQK7MWW4mOwuMh4RePBuPFAEPC6+pdqyWOUMDOixb6qZ69owLJpz6XmyllCouc4t8YWO+E2Nw==",
      "license": "MIT",
      "dependencies": {
        "@hono/node-server": "^1.19.9",
        "ajv": "^8.17.1",
        "ajv-formats": "^3.0.1",
        "content-type": "^1.0.5",
        "cors": "^2.8.5",
        "cross-spawn": "^7.0.5",
        "eventsource": "^3.0.2",
        "eventsource-parser": "^3.0.0",
        "express": "^5.2.1",
        "express-rate-limit": "^8.2.1",
        "hono": "^4.11.4",
        "jose": "^6.1.3",
        "json-schema-typed": "^8.0.2",
        "pkce-challenge": "^5.0.0",
        "raw-body": "^3.0.0",
        "zod": "^3.25 || ^4.0",
        "zod-to-json-schema": "^3.25.1"
      },
      "engines": {
        "node": ">=18"
      },
      "peerDependencies": {
        "@cfworker/json-schema": "^4.1.1",
        "zod": "^3.25 || ^4.0"
      },
      "peerDependenciesMeta": {
        "@cfworker/json-schema": {
          "optional": true
        },
        "zod": {
          "optional": false
        }
      }
    },
    "node_modules/@rollup/rollup-android-arm-eabi": {
      "version": "4.60.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-android-arm-eabi/-/rollup-android-arm-eabi-4.60.0.tgz",
      "integrity": "sha512-WOhNW9K8bR3kf4zLxbfg6Pxu2ybOUbB2AjMDHSQx86LIF4rH4Ft7vmMwNt0loO0eonglSNy4cpD3MKXXKQu0/A==",
      "cpu": [
        "arm"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "android"
      ]
    },
    "node_modules/@rollup/rollup-android-arm64": {
      "version": "4.60.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-android-arm64/-/rollup-android-arm64-4.60.0.tgz",
      "integrity": "sha512-u6JHLll5QKRvjciE78bQXDmqRqNs5M/3GVqZeMwvmjaNODJih/WIrJlFVEihvV0MiYFmd+ZyPr9wxOVbPAG2Iw==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "licens
```


## File: bench-browser/package.json

```
{
  "name": "axi-bench-browser",
  "version": "0.1.0",
  "type": "module",
  "description": "Benchmark harness comparing browser automation tools for agent tasks",
  "scripts": {
    "build": "tsc",
    "test": "vitest run",
    "bench": "tsx src/cli.ts",
    "render:social": "cd social && npx hyperframes render --output=../../docs/social/rendered/race.mp4"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.12.0",
    "yaml": "^2.7.0"
  },
  "devDependencies": {
    "@types/node": "^22.0.0",
    "tsx": "^4.19.0",
    "typescript": "^5.7.0",
    "vitest": "^3.0.0"
  },
  "engines": {
    "node": ">=20"
  }
}

```


## File: bench-github/package-lock.json

```
{
  "name": "axi-bench",
  "version": "0.1.0",
  "lockfileVersion": 3,
  "requires": true,
  "packages": {
    "": {
      "name": "axi-bench",
      "version": "0.1.0",
      "dependencies": {
        "yaml": "^2.7.0"
      },
      "devDependencies": {
        "@types/node": "^22.0.0",
        "tsx": "^4.19.0",
        "typescript": "^5.7.0",
        "vitest": "^3.0.0"
      },
      "engines": {
        "node": ">=20"
      }
    },
    "node_modules/@esbuild/aix-ppc64": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/aix-ppc64/-/aix-ppc64-0.27.4.tgz",
      "integrity": "sha512-cQPwL2mp2nSmHHJlCyoXgHGhbEPMrEEU5xhkcy3Hs/O7nGZqEpZ2sUtLaL9MORLtDfRvVl2/3PAuEkYZH0Ty8Q==",
      "cpu": [
        "ppc64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "aix"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/android-arm": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/android-arm/-/android-arm-0.27.4.tgz",
      "integrity": "sha512-X9bUgvxiC8CHAGKYufLIHGXPJWnr0OCdR0anD2e21vdvgCI8lIfqFbnoeOz7lBjdrAGUhqLZLcQo6MLhTO2DKQ==",
      "cpu": [
        "arm"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "android"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/android-arm64": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/android-arm64/-/android-arm64-0.27.4.tgz",
      "integrity": "sha512-gdLscB7v75wRfu7QSm/zg6Rx29VLdy9eTr2t44sfTW7CxwAtQghZ4ZnqHk3/ogz7xao0QAgrkradbBzcqFPasw==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "android"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/android-x64": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/android-x64/-/android-x64-0.27.4.tgz",
      "integrity": "sha512-PzPFnBNVF292sfpfhiyiXCGSn9HZg5BcAz+ivBuSsl6Rk4ga1oEXAamhOXRFyMcjwr2DVtm40G65N3GLeH1Lvw==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "android"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/darwin-arm64": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/darwin-arm64/-/darwin-arm64-0.27.4.tgz",
      "integrity": "sha512-b7xaGIwdJlht8ZFCvMkpDN6uiSmnxxK56N2GDTMYPr2/gzvfdQN8rTfBsvVKmIVY/X7EM+/hJKEIbbHs9oA4tQ==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "darwin"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/darwin-x64": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/darwin-x64/-/darwin-x64-0.27.4.tgz",
      "integrity": "sha512-sR+OiKLwd15nmCdqpXMnuJ9W2kpy0KigzqScqHI3Hqwr7IXxBp3Yva+yJwoqh7rE8V77tdoheRYataNKL4QrPw==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "darwin"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/freebsd-arm64": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/freebsd-arm64/-/freebsd-arm64-0.27.4.tgz",
      "integrity": "sha512-jnfpKe+p79tCnm4GVav68A7tUFeKQwQyLgESwEAUzyxk/TJr4QdGog9sqWNcUbr/bZt/O/HXouspuQDd9JxFSw==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "freebsd"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/freebsd-x64": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/freebsd-x64/-/freebsd-x64-0.27.4.tgz",
      "integrity": "sha512-2kb4ceA/CpfUrIcTUl1wrP/9ad9Atrp5J94Lq69w7UwOMolPIGrfLSvAKJp0RTvkPPyn6CIWrNy13kyLikZRZQ==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "freebsd"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/linux-arm": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-arm/-/linux-arm-0.27.4.tgz",
      "integrity": "sha512-aBYgcIxX/wd5n2ys0yESGeYMGF+pv6g0DhZr3G1ZG4jMfruU9Tl1i2Z+Wnj9/KjGz1lTLCcorqE2viePZqj4Eg==",
      "cpu": [
        "arm"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/linux-arm64": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-arm64/-/linux-arm64-0.27.4.tgz",
      "integrity": "sha512-7nQOttdzVGth1iz57kxg9uCz57dxQLHWxopL6mYuYthohPKEK0vU0C3O21CcBK6KDlkYVcnDXY099HcCDXd9dA==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/linux-ia32": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-ia32/-/linux-ia32-0.27.4.tgz",
      "integrity": "sha512-oPtixtAIzgvzYcKBQM/qZ3R+9TEUd1aNJQu0HhGyqtx6oS7qTpvjheIWBbes4+qu1bNlo2V4cbkISr8q6gRBFA==",
      "cpu": [
        "ia32"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/linux-loong64": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-loong64/-/linux-loong64-0.27.4.tgz",
      "integrity": "sha512-8mL/vh8qeCoRcFH2nM8wm5uJP+ZcVYGGayMavi8GmRJjuI3g1v6Z7Ni0JJKAJW+m0EtUuARb6Lmp4hMjzCBWzA==",
      "cpu": [
        "loong64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/linux-mips64el": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-mips64el/-/linux-mips64el-0.27.4.tgz",
      "integrity": "sha512-1RdrWFFiiLIW7LQq9Q2NES+HiD4NyT8Itj9AUeCl0IVCA459WnPhREKgwrpaIfTOe+/2rdntisegiPWn/r/aAw==",
      "cpu": [
        "mips64el"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/linux-ppc64": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-ppc64/-/linux-ppc64-0.27.4.tgz",
      "integrity": "sha512-tLCwNG47l3sd9lpfyx9LAGEGItCUeRCWeAx6x2Jmbav65nAwoPXfewtAdtbtit/pJFLUWOhpv0FpS6GQAmPrHA==",
      "cpu": [
        "ppc64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/linux-riscv64": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-riscv64/-/linux-riscv64-0.27.4.tgz",
      "integrity": "sha512-BnASypppbUWyqjd1KIpU4AUBiIhVr6YlHx/cnPgqEkNoVOhHg+YiSVxM1RLfiy4t9cAulbRGTNCKOcqHrEQLIw==",
      "cpu": [
        "riscv64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/linux-s390x": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-s390x/-/linux-s390x-0.27.4.tgz",
      "integrity": "sha512-+eUqgb/Z7vxVLezG8bVB9SfBie89gMueS+I0xYh2tJdw3vqA/0ImZJ2ROeWwVJN59ihBeZ7Tu92dF/5dy5FttA==",
      "cpu": [
        "s390x"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/linux-x64": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-x64/-/linux-x64-0.27.4.tgz",
      "integrity": "sha512-S5qOXrKV8BQEzJPVxAwnryi2+Iq5pB40gTEIT69BQONqR7JH1EPIcQ/Uiv9mCnn05jff9umq/5nqzxlqTOg9NA==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/netbsd-arm64": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/netbsd-arm64/-/netbsd-arm64-0.27.4.tgz",
      "integrity": "sha512-xHT8X4sb0GS8qTqiwzHqpY00C95DPAq7nAwX35Ie/s+LO9830hrMd3oX0ZMKLvy7vsonee73x0lmcdOVXFzd6Q==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "netbsd"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/netbsd-x64": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/netbsd-x64/-/netbsd-x64-0.27.4.tgz",
      "integrity": "sha512-RugOvOdXfdyi5Tyv40kgQnI0byv66BFgAqjdgtAKqHoZTbTF2QqfQrFwa7cHEORJf6X2ht+l9ABLMP0dnKYsgg==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "netbsd"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/openbsd-arm64": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/openbsd-arm64/-/openbsd-arm64-0.27.4.tgz",
      "integrity": "sha512-2MyL3IAaTX+1/qP0O1SwskwcwCoOI4kV2IBX1xYnDDqthmq5ArrW94qSIKCAuRraMgPOmG0RDTA74mzYNQA9ow==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "openbsd"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/openbsd-x64": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/openbsd-x64/-/openbsd-x64-0.27.4.tgz",
      "integrity": "sha512-u8fg/jQ5aQDfsnIV6+KwLOf1CmJnfu1ShpwqdwC0uA7ZPwFws55Ngc12vBdeUdnuWoQYx/SOQLGDcdlfXhYmXQ==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "openbsd"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/openharmony-arm64": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/openharmony-arm64/-/openharmony-arm64-0.27.4.tgz",
      "integrity": "sha512-JkTZrl6VbyO8lDQO3yv26nNr2RM2yZzNrNHEsj9bm6dOwwu9OYN28CjzZkH57bh4w0I2F7IodpQvUAEd1mbWXg==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "openharmony"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/sunos-x64": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/sunos-x64/-/sunos-x64-0.27.4.tgz",
      "integrity": "sha512-/gOzgaewZJfeJTlsWhvUEmUG4tWEY2Spp5M20INYRg2ZKl9QPO3QEEgPeRtLjEWSW8FilRNacPOg8R1uaYkA6g==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "sunos"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/win32-arm64": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/win32-arm64/-/win32-arm64-0.27.4.tgz",
      "integrity": "sha512-Z9SExBg2y32smoDQdf1HRwHRt6vAHLXcxD2uGgO/v2jK7Y718Ix4ndsbNMU/+1Qiem9OiOdaqitioZwxivhXYg==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "win32"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/win32-ia32": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/win32-ia32/-/win32-ia32-0.27.4.tgz",
      "integrity": "sha512-DAyGLS0Jz5G5iixEbMHi5KdiApqHBWMGzTtMiJ72ZOLhbu/bzxgAe8Ue8CTS3n3HbIUHQz/L51yMdGMeoxXNJw==",
      "cpu": [
        "ia32"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "win32"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/win32-x64": {
      "version": "0.27.4",
      "resolved": "https://registry.npmjs.org/@esbuild/win32-x64/-/win32-x64-0.27.4.tgz",
      "integrity": "sha512-+knoa0BDoeXgkNvvV1vvbZX4+hizelrkwmGJBdT17t8FNPwG2lKemmuMZlmaNQ3ws3DKKCxpb4zRZEIp3UxFCg==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "win32"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@jridgewell/sourcemap-codec": {
      "version": "1.5.5",
      "resolved": "https://registry.npmjs.org/@jridgewell/sourcemap-codec/-/sourcemap-codec-1.5.5.tgz",
      "integrity": "sha512-cYQ9310grqxueWbl+WuIUIaiUaDcj7WOq5fVhEljNVgRfOUhY9fy2zTvfoqWsnebh8Sl70VScFbICvJnLKB0Og==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/@rollup/rollup-android-arm-eabi": {
      "version": "4.59.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-android-arm-eabi/-/rollup-android-arm-eabi-4.59.0.tgz",
      "integrity": "sha512-upnNBkA6ZH2VKGcBj9Fyl9IGNPULcjXRlg0LLeaioQWueH30p6IXtJEbKAgvyv+mJaMxSm1l6xwDXYjpEMiLMg==",
      "cpu": [
        "arm"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "android"
      ]
    },
    "node_modules/@rollup/rollup-android-arm64": {
      "version": "4.59.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-android-arm64/-/rollup-android-arm64-4.59.0.tgz",
      "integrity": "sha512-hZ+Zxj3SySm4A/DylsDKZAeVg0mvi++0PYVceVyX7hemkw7OreKdCvW2oQ3T1FMZvCaQXqOTHb8qmBShoqk69Q==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "android"
      ]
    },
    "node_modules/@rollup/rollup-darwin-arm64": {
      "version": "4.59.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-darwin-arm64/-/rollup-darwin-arm64-4.59.0.tgz",
      "integrity": "sha512-W2Psnbh1J8ZJw0xKAd8zdNgF9HRLkdWwwdWqubSVk0pUuQkoHnv7rx4GiF9rT4t5DIZGAsConRE3AxCdJ4m8rg==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "darwin"
      ]
    },
    "node_modules/@rollup/rollup-darwin-x64": {
      "version": "4.59.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-darwin-x64/-/rollup-darwin-x64-4.59.0.tgz",
      "integrity": "sha512-ZW2KkwlS4lwTv7ZVsYDiARfFCnSGhzYPdiOU4IM2fDbL+QGlyAbjgSFuqNRbSthybLbIJ915UtZBtmuLrQAT/w==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "darwin"
      ]
    },
    "node_modules/@rollup/rollup-freebsd-arm64": {
      "version": "4.59.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-freebsd-arm64/-/rollup-freebsd-arm64-4.59.0.tgz",
      "integrity": "sha512-EsKaJ5ytAu9jI3lonzn3BgG8iRBjV4LxZexygcQbpiU0wU0ATxhNVEpXKfUa0pS05gTcSDMKpn3Sx+QB9RlTTA==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "freebsd"
      ]
    },
    "node_modules/@rollup/rollup-freebsd-x64": {
      "version": "4.59.0",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-freebsd-x64/-/rollup-freebsd-x64-4.59.0.tgz",
      "integrity": "sha512-d3DuZi2KzTMjImrxoHIAODUZYoUUMsuUiY4SRRcJy6NJoZ6iIqWnJu9IScV9jXysyGMVu
```


## File: bench-github/package.json

```
{
  "name": "axi-bench",
  "version": "0.1.0",
  "type": "module",
  "description": "Benchmark harness comparing cli, axi, and GitHub MCP for agent tasks",
  "scripts": {
    "build": "tsc",
    "test": "vitest run",
    "bench": "tsx src/cli.ts"
  },
  "dependencies": {
    "yaml": "^2.7.0"
  },
  "devDependencies": {
    "@types/node": "^22.0.0",
    "tsx": "^4.19.0",
    "typescript": "^5.7.0",
    "vitest": "^3.0.0"
  },
  "engines": {
    "node": ">=20"
  }
}

```


## File: LICENSE

```
MIT License

Copyright (c) 2026 Kun Chen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

```


## File: package-lock.json

```
{
  "name": "axi-repo-tools",
  "lockfileVersion": 3,
  "requires": true,
  "packages": {
    "": {
      "name": "axi-repo-tools",
      "devDependencies": {
        "@eslint/js": "^10.0.1",
        "eslint": "^10.1.0",
        "eslint-config-prettier": "^10.1.8",
        "globals": "^17.4.0",
        "prettier": "^3.6.2",
        "typescript-eslint": "^8.46.2"
      }
    },
    "node_modules/@eslint-community/eslint-utils": {
      "version": "4.9.1",
      "resolved": "https://registry.npmjs.org/@eslint-community/eslint-utils/-/eslint-utils-4.9.1.tgz",
      "integrity": "sha512-phrYmNiYppR7znFEdqgfWHXR6NCkZEK7hwWDHZUjit/2/U0r6XvkDl0SYnoM51Hq7FhCGdLDT6zxCCOY1hexsQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "eslint-visitor-keys": "^3.4.3"
      },
      "engines": {
        "node": "^12.22.0 || ^14.17.0 || >=16.0.0"
      },
      "funding": {
        "url": "https://opencollective.com/eslint"
      },
      "peerDependencies": {
        "eslint": "^6.0.0 || ^7.0.0 || >=8.0.0"
      }
    },
    "node_modules/@eslint-community/eslint-utils/node_modules/eslint-visitor-keys": {
      "version": "3.4.3",
      "resolved": "https://registry.npmjs.org/eslint-visitor-keys/-/eslint-visitor-keys-3.4.3.tgz",
      "integrity": "sha512-wpc+LXeiyiisxPlEkUzU6svyS1frIO3Mgxj1fdy7Pm8Ygzguax2N3Fa/D/ag1WqbOprdI+uY6wMUl8/a2G+iag==",
      "dev": true,
      "license": "Apache-2.0",
      "engines": {
        "node": "^12.22.0 || ^14.17.0 || >=16.0.0"
      },
      "funding": {
        "url": "https://opencollective.com/eslint"
      }
    },
    "node_modules/@eslint-community/regexpp": {
      "version": "4.12.2",
      "resolved": "https://registry.npmjs.org/@eslint-community/regexpp/-/regexpp-4.12.2.tgz",
      "integrity": "sha512-EriSTlt5OC9/7SXkRSCAhfSxxoSUgBm33OH+IkwbdpgoqsSsUg7y3uh+IICI/Qg4BBWr3U2i39RpmycbxMq4ew==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": "^12.0.0 || ^14.0.0 || >=16.0.0"
      }
    },
    "node_modules/@eslint/config-array": {
      "version": "0.23.3",
      "resolved": "https://registry.npmjs.org/@eslint/config-array/-/config-array-0.23.3.tgz",
      "integrity": "sha512-j+eEWmB6YYLwcNOdlwQ6L2OsptI/LO6lNBuLIqe5R7RetD658HLoF+Mn7LzYmAWWNNzdC6cqP+L6r8ujeYXWLw==",
      "dev": true,
      "license": "Apache-2.0",
      "dependencies": {
        "@eslint/object-schema": "^3.0.3",
        "debug": "^4.3.1",
        "minimatch": "^10.2.4"
      },
      "engines": {
        "node": "^20.19.0 || ^22.13.0 || >=24"
      }
    },
    "node_modules/@eslint/config-helpers": {
      "version": "0.5.3",
      "resolved": "https://registry.npmjs.org/@eslint/config-helpers/-/config-helpers-0.5.3.tgz",
      "integrity": "sha512-lzGN0onllOZCGroKJmRwY6QcEHxbjBw1gwB8SgRSqK8YbbtEXMvKynsXc3553ckIEBxsbMBU7oOZXKIPGZNeZw==",
      "dev": true,
      "license": "Apache-2.0",
      "dependencies": {
        "@eslint/core": "^1.1.1"
      },
      "engines": {
        "node": "^20.19.0 || ^22.13.0 || >=24"
      }
    },
    "node_modules/@eslint/core": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/@eslint/core/-/core-1.1.1.tgz",
      "integrity": "sha512-QUPblTtE51/7/Zhfv8BDwO0qkkzQL7P/aWWbqcf4xWLEYn1oKjdO0gglQBB4GAsu7u6wjijbCmzsUTy6mnk6oQ==",
      "dev": true,
      "license": "Apache-2.0",
      "dependencies": {
        "@types/json-schema": "^7.0.15"
      },
      "engines": {
        "node": "^20.19.0 || ^22.13.0 || >=24"
      }
    },
    "node_modules/@eslint/js": {
      "version": "10.0.1",
      "resolved": "https://registry.npmjs.org/@eslint/js/-/js-10.0.1.tgz",
      "integrity": "sha512-zeR9k5pd4gxjZ0abRoIaxdc7I3nDktoXZk2qOv9gCNWx3mVwEn32VRhyLaRsDiJjTs0xq/T8mfPtyuXu7GWBcA==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": "^20.19.0 || ^22.13.0 || >=24"
      },
      "funding": {
        "url": "https://eslint.org/donate"
      },
      "peerDependencies": {
        "eslint": "^10.0.0"
      },
      "peerDependenciesMeta": {
        "eslint": {
          "optional": true
        }
      }
    },
    "node_modules/@eslint/object-schema": {
      "version": "3.0.3",
      "resolved": "https://registry.npmjs.org/@eslint/object-schema/-/object-schema-3.0.3.tgz",
      "integrity": "sha512-iM869Pugn9Nsxbh/YHRqYiqd23AmIbxJOcpUMOuWCVNdoQJ5ZtwL6h3t0bcZzJUlC3Dq9jCFCESBZnX0GTv7iQ==",
      "dev": true,
      "license": "Apache-2.0",
      "engines": {
        "node": "^20.19.0 || ^22.13.0 || >=24"
      }
    },
    "node_modules/@eslint/plugin-kit": {
      "version": "0.6.1",
      "resolved": "https://registry.npmjs.org/@eslint/plugin-kit/-/plugin-kit-0.6.1.tgz",
      "integrity": "sha512-iH1B076HoAshH1mLpHMgwdGeTs0CYwL0SPMkGuSebZrwBp16v415e9NZXg2jtrqPVQjf6IANe2Vtlr5KswtcZQ==",
      "dev": true,
      "license": "Apache-2.0",
      "dependencies": {
        "@eslint/core": "^1.1.1",
        "levn": "^0.4.1"
      },
      "engines": {
        "node": "^20.19.0 || ^22.13.0 || >=24"
      }
    },
    "node_modules/@humanfs/core": {
      "version": "0.19.1",
      "resolved": "https://registry.npmjs.org/@humanfs/core/-/core-0.19.1.tgz",
      "integrity": "sha512-5DyQ4+1JEUzejeK1JGICcideyfUbGixgS9jNgex5nqkW+cY7WZhxBigmieN5Qnw9ZosSNVC9KQKyb+GUaGyKUA==",
      "dev": true,
      "license": "Apache-2.0",
      "engines": {
        "node": ">=18.18.0"
      }
    },
    "node_modules/@humanfs/node": {
      "version": "0.16.7",
      "resolved": "https://registry.npmjs.org/@humanfs/node/-/node-0.16.7.tgz",
      "integrity": "sha512-/zUx+yOsIrG4Y43Eh2peDeKCxlRt/gET6aHfaKpuq267qXdYDFViVHfMaLyygZOnl0kGWxFIgsBy8QFuTLUXEQ==",
      "dev": true,
      "license": "Apache-2.0",
      "dependencies": {
        "@humanfs/core": "^0.19.1",
        "@humanwhocodes/retry": "^0.4.0"
      },
      "engines": {
        "node": ">=18.18.0"
      }
    },
    "node_modules/@humanwhocodes/module-importer": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/@humanwhocodes/module-importer/-/module-importer-1.0.1.tgz",
      "integrity": "sha512-bxveV4V8v5Yb4ncFTT3rPSgZBOpCkjfK0y4oVVVJwIuDVBRMDXrPyXRL988i5ap9m9bnyEEjWfm5WkBmtffLfA==",
      "dev": true,
      "license": "Apache-2.0",
      "engines": {
        "node": ">=12.22"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/nzakas"
      }
    },
    "node_modules/@humanwhocodes/retry": {
      "version": "0.4.3",
      "resolved": "https://registry.npmjs.org/@humanwhocodes/retry/-/retry-0.4.3.tgz",
      "integrity": "sha512-bV0Tgo9K4hfPCek+aMAn81RppFKv2ySDQeMoSZuvTASywNTnVJCArCZE2FWqpvIatKu7VMRLWlR1EazvVhDyhQ==",
      "dev": true,
      "license": "Apache-2.0",
      "engines": {
        "node": ">=18.18"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/nzakas"
      }
    },
    "node_modules/@types/esrecurse": {
      "version": "4.3.1",
      "resolved": "https://registry.npmjs.org/@types/esrecurse/-/esrecurse-4.3.1.tgz",
      "integrity": "sha512-xJBAbDifo5hpffDBuHl0Y8ywswbiAp/Wi7Y/GtAgSlZyIABppyurxVueOPE8LUQOxdlgi6Zqce7uoEpqNTeiUw==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/@types/estree": {
      "version": "1.0.8",
      "resolved": "https://registry.npmjs.org/@types/estree/-/estree-1.0.8.tgz",
      "integrity": "sha512-dWHzHa2WqEXI/O1E9OjrocMTKJl2mSrEolh1Iomrv6U+JuNwaHXsXx9bLu5gG7BUWFIN0skIQJQ/L1rIex4X6w==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/@types/json-schema": {
      "version": "7.0.15",
      "resolved": "https://registry.npmjs.org/@types/json-schema/-/json-schema-7.0.15.tgz",
      "integrity": "sha512-5+fP8P8MFNC+AyZCDxrB2pkZFPGzqQWUzpSeuuVLvm8VMcorNYavBqoFcxK8bQz4Qsbn4oUEEem4wDLfcysGHA==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/@typescript-eslint/eslint-plugin": {
      "version": "8.58.0",
      "resolved": "https://registry.npmjs.org/@typescript-eslint/eslint-plugin/-/eslint-plugin-8.58.0.tgz",
      "integrity": "sha512-RLkVSiNuUP1C2ROIWfqX+YcUfLaSnxGE/8M+Y57lopVwg9VTYYfhuz15Yf1IzCKgZj6/rIbYTmJCUSqr76r0Wg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@eslint-community/regexpp": "^4.12.2",
        "@typescript-eslint/scope-manager": "8.58.0",
        "@typescript-eslint/type-utils": "8.58.0",
        "@typescript-eslint/utils": "8.58.0",
        "@typescript-eslint/visitor-keys": "8.58.0",
        "ignore": "^7.0.5",
        "natural-compare": "^1.4.0",
        "ts-api-utils": "^2.5.0"
      },
      "engines": {
        "node": "^18.18.0 || ^20.9.0 || >=21.1.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/typescript-eslint"
      },
      "peerDependencies": {
        "@typescript-eslint/parser": "^8.58.0",
        "eslint": "^8.57.0 || ^9.0.0 || ^10.0.0",
        "typescript": ">=4.8.4 <6.1.0"
      }
    },
    "node_modules/@typescript-eslint/eslint-plugin/node_modules/ignore": {
      "version": "7.0.5",
      "resolved": "https://registry.npmjs.org/ignore/-/ignore-7.0.5.tgz",
      "integrity": "sha512-Hs59xBNfUIunMFgWAbGX5cq6893IbWg4KnrjbYwX3tx0ztorVgTDA6B2sxf8ejHJ4wz8BqGUMYlnzNBer5NvGg==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">= 4"
      }
    },
    "node_modules/@typescript-eslint/parser": {
      "version": "8.58.0",
      "resolved": "https://registry.npmjs.org/@typescript-eslint/parser/-/parser-8.58.0.tgz",
      "integrity": "sha512-rLoGZIf9afaRBYsPUMtvkDWykwXwUPL60HebR4JgTI8mxfFe2cQTu3AGitANp4b9B2QlVru6WzjgB2IzJKiCSA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@typescript-eslint/scope-manager": "8.58.0",
        "@typescript-eslint/types": "8.58.0",
        "@typescript-eslint/typescript-estree": "8.58.0",
        "@typescript-eslint/visitor-keys": "8.58.0",
        "debug": "^4.4.3"
      },
      "engines": {
        "node": "^18.18.0 || ^20.9.0 || >=21.1.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/typescript-eslint"
      },
      "peerDependencies": {
        "eslint": "^8.57.0 || ^9.0.0 || ^10.0.0",
        "typescript": ">=4.8.4 <6.1.0"
      }
    },
    "node_modules/@typescript-eslint/project-service": {
      "version": "8.58.0",
      "resolved": "https://registry.npmjs.org/@typescript-eslint/project-service/-/project-service-8.58.0.tgz",
      "integrity": "sha512-8Q/wBPWLQP1j16NxoPNIKpDZFMaxl7yWIoqXWYeWO+Bbd2mjgvoF0dxP2jKZg5+x49rgKdf7Ck473M8PC3V9lg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@typescript-eslint/tsconfig-utils": "^8.58.0",
        "@typescript-eslint/types": "^8.58.0",
        "debug": "^4.4.3"
      },
      "engines": {
        "node": "^18.18.0 || ^20.9.0 || >=21.1.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/typescript-eslint"
      },
      "peerDependencies": {
        "typescript": ">=4.8.4 <6.1.0"
      }
    },
    "node_modules/@typescript-eslint/scope-manager": {
      "version": "8.58.0",
      "resolved": "https://registry.npmjs.org/@typescript-eslint/scope-manager/-/scope-manager-8.58.0.tgz",
      "integrity": "sha512-W1Lur1oF50FxSnNdGp3Vs6P+yBRSmZiw4IIjEeYxd8UQJwhUF0gDgDD/W/Tgmh73mxgEU3qX0Bzdl/NGuSPEpQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@typescript-eslint/types": "8.58.0",
        "@typescript-eslint/visitor-keys": "8.58.0"
      },
      "engines": {
        "node": "^18.18.0 || ^20.9.0 || >=21.1.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/typescript-eslint"
      }
    },
    "node_modules/@typescript-eslint/tsconfig-utils": {
      "version": "8.58.0",
      "resolved": "https://registry.npmjs.org/@typescript-eslint/tsconfig-utils/-/tsconfig-utils-8.58.0.tgz",
      "integrity": "sha512-doNSZEVJsWEu4htiVC+PR6NpM+pa+a4ClH9INRWOWCUzMst/VA9c4gXq92F8GUD1rwhNvRLkgjfYtFXegXQF7A==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": "^18.18.0 || ^20.9.0 || >=21.1.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/typescript-eslint"
      },
      "peerDependencies": {
        "typescript": ">=4.8.4 <6.1.0"
      }
    },
    "node_modules/@typescript-eslint/type-utils": {
      "version": "8.58.0",
      "resolved": "https://registry.npmjs.org/@typescript-eslint/type-utils/-/type-utils-8.58.0.tgz",
      "integrity": "sha512-aGsCQImkDIqMyx1u4PrVlbi/krmDsQUs4zAcCV6M7yPcPev+RqVlndsJy9kJ8TLihW9TZ0kbDAzctpLn5o+lOg==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@typescript-eslint/types": "8.58.0",
        "@typescript-eslint/typescript-estree": "8.58.0",
        "@typescript-eslint/utils": "8.58.0",
        "debug": "^4.4.3",
        "ts-api-utils": "^2.5.0"
      },
      "engines": {
        "node": "^18.18.0 || ^20.9.0 || >=21.1.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/typescript-eslint"
      },
      "peerDependencies": {
        "eslint": "^8.57.0 || ^9.0.0 || ^10.0.0",
        "typescript": ">=4.8.4 <6.1.0"
      }
    },
    "node_modules/@typescript-eslint/types": {
      "version": "8.58.0",
      "resolved": "https://registry.npmjs.org/@typescript-eslint/types/-/types-8.58.0.tgz",
      "integrity": "sha512-O9CjxypDT89fbHxRfETNoAnHj/i6IpRK0CvbVN3qibxlLdo5p5hcLmUuCCrHMpxiWSwKyI8mCP7qRNYuOJ0Uww==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": "^18.18.0 || ^20.9.0 || >=21.1.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/typescript-eslint"
      }
    },
    "node_modules/@typescript-eslint/typescript-estree": {
      "version": "8.58.0",
      "resolved": "https://registry.npmjs.org/@typescript-eslint/typescript-estree/-/typescript-estree-8.58.0.tgz",
      "integrity": "sha512-7vv5UWbHqew/dvs+D3e1RvLv1v2eeZ9txRHPnEEBUgSNLx5ghdzjHa0sgLWYVKssH+lYmV0JaWdoubo0ncGYLA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@typescript-eslint/project-service": "8.58.0",
        "@typescript-eslint/tsconfig-utils": "8.58.0",
        "@typescript-eslint/types": "8.58.0",
        "@typescript-eslint/visitor-keys": "8.58.0",
        "debug": "^4.4.3",
        "minimatch": "^10.2.2",
        "semver": "^7.7.3",
        "tinyglobby": "^0.2.15",
        "ts-api-utils": "^2.5.0"
      },
      "engines": {
        "node": "^18.18.0 || ^20.9.0 || >=21.1.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/typescript-eslint"
      },
      "peerDependencies": {
        "typescript": ">=4.8.4 <6.1.0"
      }
    },
    "node_modules/@typescript-eslint/utils": {
      "version": "8.58.0",
      "resolved": "https://registry.npmjs.org/@typescript-eslint/utils/-/utils-8.58.0.tgz",
      "integrity": "sha512-RfeSqcFeHMHlAWzt4TBjWOAtoW9lnsAGiP3GbaX9uVgTYYrMbVnGONEfUCiSss+xMHFl+eHZiipmA8WkQ7FuNA==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@eslint-community/eslint-utils": "^4.9.1",
        "@typescript-eslint/scope-manager": "8.58.0",
        "@typescript-eslint/types": "8.58.0",
        "@typescript-eslint/typescript-estree": "8.58.0"
      },
      "engines": {
        "node": "^18.18.0 || ^20.9.0 || >=21.1.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/typescript-eslint"
      },
      "peerDependencies": {
        "eslint": "^8.57.0 || ^9.0.0 || ^10.0.0",
        "typescript": ">=4.8.4 <6.1.0"
      }
    },
    "node_modules/@typescript-eslint/visitor-keys": {
      "version": "8.58.0",
      "resolved": "https://registry.npmjs.org/@typescript-eslint/visitor-keys/-/visitor-keys-8.58.0.tg
```


## File: package.json

```
{
  "name": "axi-repo-tools",
  "private": true,
  "type": "module",
  "scripts": {
    "lint": "eslint packages/axi-sdk-js/src packages/axi-sdk-js/test eslint.config.mjs",
    "format": "prettier --write \"packages/axi-sdk-js/**/*.{ts,js,mjs,cjs,json,md}\" \".github/workflows/axi-sdk-js-*.yml\" \"release-please-config.json\" \".release-please-manifest.json\"",
    "format:check": "prettier --check \"packages/axi-sdk-js/**/*.{ts,js,mjs,cjs,json,md}\" \".github/workflows/axi-sdk-js-*.yml\" \"release-please-config.json\" \".release-please-manifest.json\""
  },
  "devDependencies": {
    "@eslint/js": "^10.0.1",
    "eslint": "^10.1.0",
    "eslint-config-prettier": "^10.1.8",
    "globals": "^17.4.0",
    "prettier": "^3.6.2",
    "typescript-eslint": "^8.46.2"
  }
}

```


## File: packages/axi-sdk-js/LICENSE

```
MIT License

Copyright (c) 2026 kunchenguid

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

```


## File: packages/axi-sdk-js/package-lock.json

```
{
  "name": "axi-sdk-js",
  "version": "0.1.4",
  "lockfileVersion": 3,
  "requires": true,
  "packages": {
    "": {
      "name": "axi-sdk-js",
      "version": "0.1.4",
      "dependencies": {
        "@toon-format/toon": "^2.1.0"
      },
      "devDependencies": {
        "@types/node": "^22.0.0",
        "typescript": "^5.7.0",
        "vitest": "^3.0.0"
      },
      "engines": {
        "node": ">=20"
      }
    },
    "node_modules/@esbuild/aix-ppc64": {
      "version": "0.27.5",
      "resolved": "https://registry.npmjs.org/@esbuild/aix-ppc64/-/aix-ppc64-0.27.5.tgz",
      "integrity": "sha512-nGsF/4C7uzUj+Nj/4J+Zt0bYQ6bz33Phz8Lb2N80Mti1HjGclTJdXZ+9APC4kLvONbjxN1zfvYNd8FEcbBK/MQ==",
      "cpu": [
        "ppc64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "aix"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/android-arm": {
      "version": "0.27.5",
      "resolved": "https://registry.npmjs.org/@esbuild/android-arm/-/android-arm-0.27.5.tgz",
      "integrity": "sha512-Cv781jd0Rfj/paoNrul1/r4G0HLvuFKYh7C9uHZ2Pl8YXstzvCyyeWENTFR9qFnRzNMCjXmsulZuvosDg10Mog==",
      "cpu": [
        "arm"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "android"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/android-arm64": {
      "version": "0.27.5",
      "resolved": "https://registry.npmjs.org/@esbuild/android-arm64/-/android-arm64-0.27.5.tgz",
      "integrity": "sha512-Oeghq+XFgh1pUGd1YKs4DDoxzxkoUkvko+T/IVKwlghKLvvjbGFB3ek8VEDBmNvqhwuL0CQS3cExdzpmUyIrgA==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "android"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/android-x64": {
      "version": "0.27.5",
      "resolved": "https://registry.npmjs.org/@esbuild/android-x64/-/android-x64-0.27.5.tgz",
      "integrity": "sha512-nQD7lspbzerlmtNOxYMFAGmhxgzn8Z7m9jgFkh6kpkjsAhZee1w8tJW3ZlW+N9iRePz0oPUDrYrXidCPSImD0Q==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "android"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/darwin-arm64": {
      "version": "0.27.5",
      "resolved": "https://registry.npmjs.org/@esbuild/darwin-arm64/-/darwin-arm64-0.27.5.tgz",
      "integrity": "sha512-I+Ya/MgC6rr8oRWGRDF3BXDfP8K1BVUggHqN6VI2lUZLdDi1IM1v2cy0e3lCPbP+pVcK3Tv8cgUhHse1kaNZZw==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "darwin"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/darwin-x64": {
      "version": "0.27.5",
      "resolved": "https://registry.npmjs.org/@esbuild/darwin-x64/-/darwin-x64-0.27.5.tgz",
      "integrity": "sha512-MCjQUtC8wWJn/pIPM7vQaO69BFgwPD1jriEdqwTCKzWjGgkMbcg+M5HzrOhPhuYe1AJjXlHmD142KQf+jnYj8A==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "darwin"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/freebsd-arm64": {
      "version": "0.27.5",
      "resolved": "https://registry.npmjs.org/@esbuild/freebsd-arm64/-/freebsd-arm64-0.27.5.tgz",
      "integrity": "sha512-X6xVS+goSH0UelYXnuf4GHLwpOdc8rgK/zai+dKzBMnncw7BTQIwquOodE7EKvY2UVUetSqyAfyZC1D+oqLQtg==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "freebsd"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/freebsd-x64": {
      "version": "0.27.5",
      "resolved": "https://registry.npmjs.org/@esbuild/freebsd-x64/-/freebsd-x64-0.27.5.tgz",
      "integrity": "sha512-233X1FGo3a8x1ekLB6XT69LfZ83vqz+9z3TSEQCTYfMNY880A97nr81KbPcAMl9rmOFp11wO0dP+eB18KU/Ucg==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "freebsd"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/linux-arm": {
      "version": "0.27.5",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-arm/-/linux-arm-0.27.5.tgz",
      "integrity": "sha512-0wkVrYHG4sdCCN/bcwQ7yYMXACkaHc3UFeaEOwSVW6e5RycMageYAFv+JS2bKLwHyeKVUvtoVH+5/RHq0fgeFw==",
      "cpu": [
        "arm"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/linux-arm64": {
      "version": "0.27.5",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-arm64/-/linux-arm64-0.27.5.tgz",
      "integrity": "sha512-euKkilsNOv7x/M1NKsx5znyprbpsRFIzTV6lWziqJch7yWYayfLtZzDxDTl+LSQDJYAjd9TVb/Kt5UKIrj2e4A==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/linux-ia32": {
      "version": "0.27.5",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-ia32/-/linux-ia32-0.27.5.tgz",
      "integrity": "sha512-hVRQX4+P3MS36NxOy24v/Cdsimy/5HYePw+tmPqnNN1fxV0bPrFWR6TMqwXPwoTM2VzbkA+4lbHWUKDd5ZDA/w==",
      "cpu": [
        "ia32"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/linux-loong64": {
      "version": "0.27.5",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-loong64/-/linux-loong64-0.27.5.tgz",
      "integrity": "sha512-mKqqRuOPALI8nDzhOBmIS0INvZOOFGGg5n1osGIXAx8oersceEbKd4t1ACNTHM3sJBXGFAlEgqM+svzjPot+ZQ==",
      "cpu": [
        "loong64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/linux-mips64el": {
      "version": "0.27.5",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-mips64el/-/linux-mips64el-0.27.5.tgz",
      "integrity": "sha512-EE/QXH9IyaAj1qeuIV5+/GZkBTipgGO782Ff7Um3vPS9cvLhJJeATy4Ggxikz2inZ46KByamMn6GqtqyVjhenA==",
      "cpu": [
        "mips64el"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/linux-ppc64": {
      "version": "0.27.5",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-ppc64/-/linux-ppc64-0.27.5.tgz",
      "integrity": "sha512-0V2iF1RGxBf1b7/BjurA5jfkl7PtySjom1r6xOK2q9KWw/XCpAdtB6KNMO+9xx69yYfSCRR9FE0TyKfHA2eQMw==",
      "cpu": [
        "ppc64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/linux-riscv64": {
      "version": "0.27.5",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-riscv64/-/linux-riscv64-0.27.5.tgz",
      "integrity": "sha512-rYxThBx6G9HN6tFNuvB/vykeLi4VDsm5hE5pVwzqbAjZEARQrWu3noZSfbEnPZ/CRXP3271GyFk/49up2W190g==",
      "cpu": [
        "riscv64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/linux-s390x": {
      "version": "0.27.5",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-s390x/-/linux-s390x-0.27.5.tgz",
      "integrity": "sha512-uEP2q/4qgd8goEUc4QIdU/1P2NmEtZ/zX5u3OpLlCGhJIuBIv0s0wr7TB2nBrd3/A5XIdEkkS5ZLF0ULuvaaYQ==",
      "cpu": [
        "s390x"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/linux-x64": {
      "version": "0.27.5",
      "resolved": "https://registry.npmjs.org/@esbuild/linux-x64/-/linux-x64-0.27.5.tgz",
      "integrity": "sha512-+Gq47Wqq6PLOOZuBzVSII2//9yyHNKZLuwfzCemqexqOQCSz0zy0O26kIzyp9EMNMK+nZ0tFHBZrCeVUuMs/ew==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "linux"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/netbsd-arm64": {
      "version": "0.27.5",
      "resolved": "https://registry.npmjs.org/@esbuild/netbsd-arm64/-/netbsd-arm64-0.27.5.tgz",
      "integrity": "sha512-3F/5EG8VHfN/I+W5cO1/SV2H9Q/5r7vcHabMnBqhHK2lTWOh3F8vixNzo8lqxrlmBtZVFpW8pmITHnq54+Tq4g==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "netbsd"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/netbsd-x64": {
      "version": "0.27.5",
      "resolved": "https://registry.npmjs.org/@esbuild/netbsd-x64/-/netbsd-x64-0.27.5.tgz",
      "integrity": "sha512-28t+Sj3CPN8vkMOlZotOmDgilQwVvxWZl7b8rxpn73Tt/gCnvrHxQUMng4uu3itdFvrtba/1nHejvxqz8xgEMA==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "netbsd"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/openbsd-arm64": {
      "version": "0.27.5",
      "resolved": "https://registry.npmjs.org/@esbuild/openbsd-arm64/-/openbsd-arm64-0.27.5.tgz",
      "integrity": "sha512-Doz/hKtiuVAi9hMsBMpwBANhIZc8l238U2Onko3t2xUp8xtM0ZKdDYHMnm/qPFVthY8KtxkXaocwmMh6VolzMA==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "openbsd"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/openbsd-x64": {
      "version": "0.27.5",
      "resolved": "https://registry.npmjs.org/@esbuild/openbsd-x64/-/openbsd-x64-0.27.5.tgz",
      "integrity": "sha512-WfGVaa1oz5A7+ZFPkERIbIhKT4olvGl1tyzTRaB5yoZRLqC0KwaO95FeZtOdQj/oKkjW57KcVF944m62/0GYtA==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "openbsd"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/openharmony-arm64": {
      "version": "0.27.5",
      "resolved": "https://registry.npmjs.org/@esbuild/openharmony-arm64/-/openharmony-arm64-0.27.5.tgz",
      "integrity": "sha512-Xh+VRuh6OMh3uJ0JkCjI57l+DVe7VRGBYymen8rFPnTVgATBwA6nmToxM2OwTlSvrnWpPKkrQUj93+K9huYC6A==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "openharmony"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/sunos-x64": {
      "version": "0.27.5",
      "resolved": "https://registry.npmjs.org/@esbuild/sunos-x64/-/sunos-x64-0.27.5.tgz",
      "integrity": "sha512-aC1gpJkkaUADHuAdQfuVTnqVUTLqqUNhAvEwHwVWcnVVZvNlDPGA0UveZsfXJJ9T6k9Po4eHi3c02gbdwO3g6w==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "sunos"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/win32-arm64": {
      "version": "0.27.5",
      "resolved": "https://registry.npmjs.org/@esbuild/win32-arm64/-/win32-arm64-0.27.5.tgz",
      "integrity": "sha512-0UNx2aavV0fk6UpZcwXFLztA2r/k9jTUa7OW7SAea1VYUhkug99MW1uZeXEnPn5+cHOd0n8myQay6TlFnBR07w==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "win32"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/win32-ia32": {
      "version": "0.27.5",
      "resolved": "https://registry.npmjs.org/@esbuild/win32-ia32/-/win32-ia32-0.27.5.tgz",
      "integrity": "sha512-5nlJ3AeJWCTSzR7AEqVjT/faWyqKU86kCi1lLmxVqmNR+j4HrYdns+eTGjS/vmrzCIe8inGQckUadvS0+JkKdQ==",
      "cpu": [
        "ia32"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "win32"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@esbuild/win32-x64": {
      "version": "0.27.5",
      "resolved": "https://registry.npmjs.org/@esbuild/win32-x64/-/win32-x64-0.27.5.tgz",
      "integrity": "sha512-PWypQR+d4FLfkhBIV+/kHsUELAnMpx1bRvvsn3p+/sAERbnCzFrtDRG2Xw5n+2zPxBK2+iaP+vetsRl4Ti7WgA==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "win32"
      ],
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@jridgewell/sourcemap-codec": {
      "version": "1.5.5",
      "resolved": "https://registry.npmjs.org/@jridgewell/sourcemap-codec/-/sourcemap-codec-1.5.5.tgz",
      "integrity": "sha512-cYQ9310grqxueWbl+WuIUIaiUaDcj7WOq5fVhEljNVgRfOUhY9fy2zTvfoqWsnebh8Sl70VScFbICvJnLKB0Og==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/@rollup/rollup-android-arm-eabi": {
      "version": "4.60.1",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-android-arm-eabi/-/rollup-android-arm-eabi-4.60.1.tgz",
      "integrity": "sha512-d6FinEBLdIiK+1uACUttJKfgZREXrF0Qc2SmLII7W2AD8FfiZ9Wjd+rD/iRuf5s5dWrr1GgwXCvPqOuDquOowA==",
      "cpu": [
        "arm"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "android"
      ]
    },
    "node_modules/@rollup/rollup-android-arm64": {
      "version": "4.60.1",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-android-arm64/-/rollup-android-arm64-4.60.1.tgz",
      "integrity": "sha512-YjG/EwIDvvYI1YvYbHvDz/BYHtkY4ygUIXHnTdLhG+hKIQFBiosfWiACWortsKPKU/+dUwQQCKQM3qrDe8c9BA==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "android"
      ]
    },
    "node_modules/@rollup/rollup-darwin-arm64": {
      "version": "4.60.1",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-darwin-arm64/-/rollup-darwin-arm64-4.60.1.tgz",
      "integrity": "sha512-mjCpF7GmkRtSJwon+Rq1N8+pI+8l7w5g9Z3vWj4T7abguC4Czwi3Yu/pFaLvA3TTeMVjnu3ctigusqWUfjZzvw==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "darwin"
      ]
    },
    "node_modules/@rollup/rollup-darwin-x64": {
      "version": "4.60.1",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-darwin-x64/-/rollup-darwin-x64-4.60.1.tgz",
      "integrity": "sha512-haZ7hJ1JT4e9hqkoT9R/19XW2QKqjfJVv+i5AGg57S+nLk9lQnJ1F/eZloRO3o9Scy9CM3wQ9l+dkXtcBgN5Ew==",
      "cpu": [
        "x64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "darwin"
      ]
    },
    "node_modules/@rollup/rollup-freebsd-arm64": {
      "version": "4.60.1",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-freebsd-arm64/-/rollup-freebsd-arm64-4.60.1.tgz",
      "integrity": "sha512-czw90wpQq3ZsAVBlinZjAYTKduOjTywlG7fEeWKUA7oCmpA8xdTkxZZlwNJKWqILlq0wehoZcJYfBvOyhPTQ6w==",
      "cpu": [
        "arm64"
      ],
      "dev": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "freebsd"
      ]
    },
    "node_modules/@rollup/rollup-freebsd-x64": {
      "version": "4.60.1",
      "resolved": "https://registry.npmjs.org/@rollup/rollup-freebsd-x64/-/rollup-freebsd-x64-4.60.1.tgz",
      "integrity": "sha512-KVB2rqsxTHuBtfOeySEyzEOB7ltlB/ux38iu2rBQzkjbwRVlkhAGIEDiiYnO2kFOkJp+Z7pUXKyrRRFu
```


## File: packages/axi-sdk-js/package.json

```
{
  "name": "axi-sdk-js",
  "version": "0.1.4",
  "description": "Shared Node.js primitives for building AXI CLIs",
  "type": "module",
  "repository": {
    "type": "git",
    "url": "https://github.com/kunchenguid/axi.git",
    "directory": "packages/axi-sdk-js"
  },
  "keywords": [
    "axi",
    "agent",
    "cli",
    "sdk",
    "toon",
    "node"
  ],
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/index.js"
    }
  },
  "files": [
    "dist",
    "LICENSE",
    "README.md"
  ],
  "publishConfig": {
    "access": "public"
  },
  "scripts": {
    "build": "tsc -p tsconfig.json",
    "test": "vitest run",
    "prepublishOnly": "npm run build"
  },
  "dependencies": {
    "@toon-format/toon": "^2.1.0"
  },
  "devDependencies": {
    "@types/node": "^22.0.0",
    "typescript": "^5.7.0",
    "vitest": "^3.0.0"
  },
  "license": "MIT",
  "engines": {
    "node": ">=20"
  }
}

```


## File: packages/axi-sdk-js/README.md

```
<h1 align="center">axi-sdk-js</h1>

<p align="center">
  <a href="https://www.npmjs.com/package/axi-sdk-js"><img alt="npm" src="https://img.shields.io/npm/v/axi-sdk-js?style=flat-square" /></a>
  <a href="https://github.com/kunchenguid/axi/actions/workflows/axi-sdk-js-ci.yml"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/kunchenguid/axi/axi-sdk-js-ci.yml?style=flat-square&label=ci" /></a>
  <a href="https://github.com/kunchenguid/axi/actions/workflows/axi-sdk-js-release-please.yml"><img alt="Release" src="https://img.shields.io/github/actions/workflow/status/kunchenguid/axi/axi-sdk-js-release-please.yml?style=flat-square&label=release" /></a>
  <a href="https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-blue?style=flat-square"><img alt="Platform" src="https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-blue?style=flat-square" /></a>
  <a href="https://x.com/kunchenguid"><img alt="X" src="https://img.shields.io/badge/X-@kunchenguid-black?style=flat-square" /></a>
  <a href="https://discord.gg/Wsy2NpnZDu"><img alt="Discord" src="https://img.shields.io/discord/1439901831038763092?style=flat-square&label=discord" /></a>
</p>

<h3 align="center">Ship AXIs without rewriting the boring parts.</h3>

Every Node-based AXI ends up redoing the same work: top-level dispatch, structured errors, TOON output, and hook installation for a few agents.

`axi-sdk-js` pulls those shared runtime pieces into one package. Your AXI can stay focused on business logic, work with plain JavaScript objects, and let the runtime handle official TOON serialization and session hook plumbing.

`runAxiCli()` assumes a command-first CLI shape: `<bin> <command> ...args ...flags`. Bare `--help` is still supported, but flags are not allowed before the top-level command.

If your executable boundary needs to normalize loader-specific arguments before dispatch, pass `argv` explicitly to `runAxiCli()` instead of relying on `process.argv.slice(2)`.

## Quick Start

```sh
$ npm install axi-sdk-js
added 1 package
```

```ts
import { runAxiCli } from "axi-sdk-js";

await runAxiCli({
  description: "Manage GitHub state in the current repository",
  version: "1.2.3",
  argv: process.argv.slice(2),
  topLevelHelp: TOP_LEVEL_HELP,
  resolveContext: ({ command, args }) =>
    command === "issue" || command === "pr"
      ? resolveRepoFromArgs(args)
      : undefined,
  home: async () => ({
    issues: [{ number: 12, title: "Fix auth bug", state: "open" }],
    help: ["Run `gh-axi issue view <number>` for details"],
  }),
  commands: {
    issue: issueCommand,
    pr: prCommand,
  },
});
```

## Reference

`axi-sdk-js` is a library package. In normal use, `runAxiCli()` should be the main entry point.

| API           | Description                                                                                                                                                                                                           |
| ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `runAxiCli()` | Shared runtime for command-first dispatch, bare `--help`/`--version` fast paths, lazy context resolution, home header injection, TOON serialization, standardized errors, and automatic best-effort hook installation |

### Advanced Exports

Most AXI authors should not need these directly.

| API                                      | Description                                                    |
| ---------------------------------------- | -------------------------------------------------------------- |
| `AxiError`                               | Throw structured AXI errors from command handlers              |
| `installSessionStartHooks()`             | Install or repair Claude Code and Codex session hooks directly |
| `shouldInstallHooksForNodeAxiExecPath()` | Check whether an executable path should self-install hooks     |

## Development

```sh
cd packages/axi-sdk-js && npm ci # Install dependencies
npm test # Run tests
npm run build # Build dist output
```

```


## File: .release-please-manifest.json

```
{
  "packages/axi-sdk-js": "0.1.4"
}

```


## File: AGENTS.md

```
# AGENTS.md

This file provides guidance to AI agents when working with code in this repository.

## What This Project Is

AXI (Agent eXperience Interface) defines 10 ergonomic principles for building CLI tools that AI agents use via shell execution. This repo contains:

- **`bench-github/`** — Benchmark harness that compares gh-axi vs gh CLI vs GitHub MCP across 17 agent tasks, graded by an LLM judge.
- **`bench-browser/`** — Benchmark harness that compares browser automation tools (agent-browser, pinchtab, chrome-devtools-mcp) across 16 browsing tasks.
- **`.agents/skills/axi/SKILL.md`** — The AXI skill definition (installable via `npx skills add kunchenguid/axi`).
- **`docs/`** — Static website (axi.md).

The reference AXI implementation (`gh-axi`) lives in a separate repo: [kunchenguid/gh-axi](https://github.com/kunchenguid/gh-axi).

## Development Commands

### Benchmark harness (GitHub)

```sh
cd bench-github
npm install
npm run bench -- run --condition axi --task merged_pr_ci_audit --repeat 5 --agent claude
npm run bench -- matrix --repeat 5 --agent claude
npm run bench -- report
npm test           # Run bench tests (vitest)
```

### Benchmark harness (Browser)

```sh
cd bench-browser
npm install
npm run bench -- run --condition agent-browser --task read_static_page --repeat 5
npm run bench -- matrix --repeat 5    # full run: all conditions × all tasks × 5 repeats
npm run bench -- report
npm test           # Run bench tests (vitest)
```

### Social video rendering

```sh
cd bench-browser
npm run render:social   # Render social/index.html via HyperFrames to docs/social/rendered/race.mp4
```

The source composition is `bench-browser/social/` (a HyperFrames project). Edit `social/index.html` for content/animation; see `social/DESIGN.md` for the visual identity. Use the `/hyperframes` skill when modifying the composition.

Requires Node.js >= 20 and `gh` CLI installed and authenticated.

## Architecture

### Benchmark (GitHub)

`bench-github/src/runner.ts` orchestrates runs: clones a test repo, writes condition-specific AGENTS.md, invokes the agent (codex or claude), parses JSONL usage, and runs the LLM grader. Conditions are defined in `bench-github/config/conditions.yaml`, tasks in `bench-github/config/tasks.yaml`. Results go to `bench-github/results/`, published results in `bench-github/published-results/`.

### Benchmark (Browser)

`bench-browser/src/runner.ts` orchestrates browser benchmark runs: creates a workspace with condition-specific CLAUDE.md, manages browser daemon lifecycle, invokes Claude with `--bare` isolation, parses JSONL usage, and grades results. Conditions are defined in `bench-browser/config/conditions.yaml`, tasks in `bench-browser/config/tasks.yaml`.

## Conventions

- Packages use ES modules (`"type": "module"`) with TypeScript targeting ES2022/Node16.
- Tests are colocated in `test/` directories mirroring `src/` structure and use vitest.

```


## File: CLAUDE.md

```
# AGENTS.md

This file provides guidance to AI agents when working with code in this repository.

## What This Project Is

AXI (Agent eXperience Interface) defines 10 ergonomic principles for building CLI tools that AI agents use via shell execution. This repo contains:

- **`bench-github/`** — Benchmark harness that compares gh-axi vs gh CLI vs GitHub MCP across 17 agent tasks, graded by an LLM judge.
- **`bench-browser/`** — Benchmark harness that compares browser automation tools (agent-browser, pinchtab, chrome-devtools-mcp) across 16 browsing tasks.
- **`.agents/skills/axi/SKILL.md`** — The AXI skill definition (installable via `npx skills add kunchenguid/axi`).
- **`docs/`** — Static website (axi.md).

The reference AXI implementation (`gh-axi`) lives in a separate repo: [kunchenguid/gh-axi](https://github.com/kunchenguid/gh-axi).

## Development Commands

### Benchmark harness (GitHub)

```sh
cd bench-github
npm install
npm run bench -- run --condition axi --task merged_pr_ci_audit --repeat 5 --agent claude
npm run bench -- matrix --repeat 5 --agent claude
npm run bench -- report
npm test           # Run bench tests (vitest)
```

### Benchmark harness (Browser)

```sh
cd bench-browser
npm install
npm run bench -- run --condition agent-browser --task read_static_page --repeat 5
npm run bench -- matrix --repeat 5    # full run: all conditions × all tasks × 5 repeats
npm run bench -- report
npm test           # Run bench tests (vitest)
```

### Social video rendering

```sh
cd bench-browser
npm run render:social   # Render social/index.html via HyperFrames to docs/social/rendered/race.mp4
```

The source composition is `bench-browser/social/` (a HyperFrames project). Edit `social/index.html` for content/animation; see `social/DESIGN.md` for the visual identity. Use the `/hyperframes` skill when modifying the composition.

Requires Node.js >= 20 and `gh` CLI installed and authenticated.

## Architecture

### Benchmark (GitHub)

`bench-github/src/runner.ts` orchestrates runs: clones a test repo, writes condition-specific AGENTS.md, invokes the agent (codex or claude), parses JSONL usage, and runs the LLM grader. Conditions are defined in `bench-github/config/conditions.yaml`, tasks in `bench-github/config/tasks.yaml`. Results go to `bench-github/results/`, published results in `bench-github/published-results/`.

### Benchmark (Browser)

`bench-browser/src/runner.ts` orchestrates browser benchmark runs: creates a workspace with condition-specific CLAUDE.md, manages browser daemon lifecycle, invokes Claude with `--bare` isolation, parses JSONL usage, and grades results. Conditions are defined in `bench-browser/config/conditions.yaml`, tasks in `bench-browser/config/tasks.yaml`.

## Conventions

- Packages use ES modules (`"type": "module"`) with TypeScript targeting ES2022/Node16.
- Tests are colocated in `test/` directories mirroring `src/` structure and use vitest.

```


(… 4450 more files omitted due to size limit)
<!-- fetched-content:end -->
