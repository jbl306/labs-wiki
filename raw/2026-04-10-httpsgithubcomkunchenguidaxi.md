---
title: "https://github.com/kunchenguid/axi"
type: url
captured: 2026-04-10T12:46:15.099835+00:00
source: android-share
url: "https://github.com/kunchenguid/axi"
content_hash: "sha256:6c73a3a0127df3a97cafecfbd3fd0d0cda7a14c9c28c6c19e54cf445acf80f5e"
tags: []
status: ingested
---

https://github.com/kunchenguid/axi

<!-- fetched-content:start -->
## Fetched Metadata
- fetched_at: 2026-04-21T11:05:06+00:00
- source_url: https://github.com/kunchenguid/axi
- resolved_url: https://github.com/kunchenguid/axi
- content_type: application/vnd.github+json
- image_urls: []

## Fetched Content
Repository: kunchenguid/axi
Description: Design principles for agent ergonomics. Higher accuracy with lower token cost than both MCP and regular CLI.
Stars: 761
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
      "resolved": "https://registry.npmjs.org/@typescript-eslint/eslint-plu
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


## File: release-please-config.json

```
{
  "$schema": "https://raw.githubusercontent.com/googleapis/release-please/main/schemas/config.json",
  "bump-minor-pre-major": true,
  "bump-patch-for-minor-pre-major": true,
  "packages": {
    "packages/axi-sdk-js": {
      "release-type": "node",
      "package-name": "axi-sdk-js",
      "component": "axi-sdk-js",
      "include-component-in-tag": true
    }
  }
}

```


## File: .agents/skills/axi/SKILL.md

```
---
name: axi
description: >
  Agent eXperience Interface (AXI) — ergonomic standards for building CLI tools that agents
  use via shell execution. Use when building, modifying, or reviewing any agent-facing CLI.
---

# Agent eXperience Interface (AXI)

AXI defines ergonomic standards for building CLI tools that autonomous agents interact with through shell execution.

## Before you start

Read the [TOON specification](https://toonformat.dev/reference/spec.html) before building any AXI output.

## 1. Token-efficient output

Use [TOON](https://toonformat.dev/) (Token-Oriented Object Notation) as the output format on stdout.
TOON provides ~40% token savings over equivalent JSON while remaining readable by agents.
Convert to TOON at the output boundary — keep internal logic on JSON.

```
tasks[2]{id,title,status,assignee}:
  "1",Fix auth bug,open,alice
  "2",Add pagination,closed,bob
```

## 2. Minimal default schemas

Every field in stdout costs tokens — multiplied by row count in collections.
Default to the smallest schema that lets the agent decide what to do next: typically an identifier, a title, and a status.

- Default list schemas: 3-4 fields, not 10
- Default limits: high enough to cover common cases in one call (if most repos have <100 labels, default to 100, not 30)
- Long-form content (bodies, descriptions) belongs in detail views, not lists
- Offer a `--fields` flag to let agents request additional fields explicitly

## 3. Content truncation

Detail views often contain large text fields. Omitting them forces agents to hunt; including them wastes tokens.
Truncate by default and tell the agent how to get the full version.

```
task:
  number: 42
  title: Fix auth bug
  state: open
  body: First 500 chars of the issue body...
    ... (truncated, 8432 chars total)
help[1]: Run `tasks view 42 --full` to see complete body
```

- Never omit large fields entirely — include a truncated preview
- Show the total size so the agent knows how much it's missing
- Suggest the escape hatch (`--full`) only when content is actually truncated
- Choose a truncation limit that covers most use cases (500-1500 chars)

## 4. Pre-computed aggregates

The most expensive token cost is often not a longer response — it's a follow-up call. If your backend has data that agents commonly need as a next step, compute it and include it.

**Aggregate counts**: include the **total count** in list output, not just the page size. Agents need "how many are there?" and will paginate if the answer isn't definitive.

```
count: 30 of 847 total
tasks[30]{number,title,state}:
  1,Fix auth bug,open
  ...
```

**Derived status fields**: when the next step almost always involves checking related state, include a lightweight summary inline.

```
task:
  number: 42
  title: Deploy pipeline fix
  state: open
  checks: 3/3 passed
  comments: 7
```

Only include derived fields your backend can provide cheaply — a summary ("3/3 passed"), not the full data.

## 5. Definitive empty states

When the answer is "nothing", say so explicitly. Ambiguous empty output causes agents to re-run with different flags to verify.

```
$ tasks list --state closed
tasks: 0 closed tasks found in this repository
```

State the zero with context. Make it clear the command succeeded — the absence of results is the answer.

## 6. Structured errors & exit codes

### Idempotent mutations

Don't error when the desired state already exists. If the agent closes something already closed, acknowledge and move on with exit code 0. Reserve non-zero exit codes for situations where the agent's intent genuinely cannot be satisfied.

```
$ tasks close 42
task: #42 already closed (no-op)    # exit 0
```

### Structured errors on stdout

Errors go to **stdout** in the same structured format as normal output, so the agent can read and act on them. Include what went wrong and an actionable suggestion. Never let raw dependency output (API errors, stack traces) leak through.

```
error: --title is required
help: tasks create --title "..." [--body "..."]
```

- Validate required flags before calling any dependency
- Translate errors — extract actionable meaning, discard noise
- Never leak dependency names — suggestions reference your CLI's commands, not the underlying tool

### No interactive prompts

Every operation must be completable with flags alone. If a required value is missing, fail immediately with a clear error — don't prompt for it. Suppress prompts from wrapped tools.

### Output channels

- **stdout**: all structured output the agent consumes — data, errors, suggestions
- **stderr**: debug logging, progress indicators, diagnostics (agents don't read this)
- **Exit codes**: 0 = success (including no-ops), 1 = error, 2 = usage error

Never mix progress messages into stdout. An agent that reads "Fetching data..." will try to interpret it as data.

## 7. Ambient context via session hooks

Register your tool into the agent's session lifecycle so every conversation starts with relevant state already visible — before the agent takes any action.

**Pattern:**

1. On first invocation, self-install hooks into the agent's configuration (idempotently)
2. At session start, a hook runs your tool and outputs a compact dashboard to stdout
3. The agent receives this as initial context and can act immediately

```
# Agent sees this at session start — no invocation needed:
specs[2]{id,title,status}:
  1,Fix auth bug,open
  2,Add pagination,in-progress

help[2]:
  Run `mytool specs view 1` for details
  Run `mytool specs create --title "..."` to add a spec
```

**Rules:**

- **Default app targets**: by default, support Claude Code and Codex. Do not hard-code a single agent integration when the tool can reasonably support both
- **Self-installing**: register hooks at global/user level on first run — no manual setup required
- **Absolute paths**: hook commands must use the full absolute path of the current executable (via `os.Executable()` or equivalent), not a bare command name. This ensures hooks work regardless of the agent's `$PATH` at runtime
- **Path repair**: on every invocation, check existing hooks and update the executable path if it has changed (e.g., after reinstall or relocation). This turns self-install into self-heal
- **Idempotent**: repeated installs with the same path are silent no-ops
- **Directory-scoped**: show only state relevant to the current working directory
- **Token-budget-aware**: this context loads on _every_ session — ruthlessly minimize it. Include just enough for the agent to orient and act; deep data belongs in explicit invocations
- **Lifecycle capture**: use session-end hooks to capture what happened (transcripts, files touched, specs referenced) so future session-start context gets richer over time

**How to integrate with each app:**

- **Claude Code**: use native hooks in `~/.claude/settings.json` or project `.claude/settings.json`. Prefer `SessionStart` to inject compact context via stdout
- **Codex**: use native hooks in `~/.codex/hooks.json` or `<repo>/.codex/hooks.json`, and ensure `[features].codex_hooks = true` in `config.toml`. Prefer `SessionStart` for ambient context via stdout

## 8. Content first

Running your CLI with no arguments should show the most relevant live content — not a usage manual.
When an agent sees actual state it can act immediately. When it sees help text, it has to make a second call.

```
$ tasks
tasks[3]{id,title,status}:
  1,Fix auth bug,open
  2,Add pagination,open
  3,Update docs,closed
help[2]:
  Run `tasks view <id>` to see full details
  Run `tasks create --title "..."` to add a task
```

## 9. Contextual disclosure

Include **a few next steps** that follow logically from the current output.
The agent discovers your CLI's surface area organically by using it, not by reading a manual upfront.

Rules:

- **Relevant**: after an open item → suggest closing; after an empty list → suggest creating; after a list → suggest viewing
- **Actionable**: every suggestion is a comple
```


## File: .github/workflows/axi-sdk-js-ci.yml

```
name: axi-sdk-js-ci

on:
  push:
    branches: [main]
    paths:
      - packages/axi-sdk-js/**
      - .github/workflows/axi-sdk-js-ci.yml
  pull_request:
    branches: [main]
    paths:
      - packages/axi-sdk-js/**
      - .github/workflows/axi-sdk-js-ci.yml

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v6
        with:
          node-version: 24
          cache: npm
          cache-dependency-path: |
            package-lock.json
            packages/axi-sdk-js/package-lock.json

      - run: npm ci
      - run: npm --prefix packages/axi-sdk-js ci
      - run: npm run format:check
      - run: npm run lint
      - run: npm --prefix packages/axi-sdk-js run build
      - run: npm --prefix packages/axi-sdk-js test

```


## File: .github/workflows/axi-sdk-js-release-please.yml

```
name: axi-sdk-js-release-please

on:
  push:
    branches: [main]
    paths:
      - packages/axi-sdk-js/**
      - release-please-config.json
      - .release-please-manifest.json
      - .github/workflows/axi-sdk-js-release-please.yml

permissions:
  contents: write
  pull-requests: write
  id-token: write

jobs:
  release-please:
    runs-on: ubuntu-latest
    steps:
      - uses: googleapis/release-please-action@v4
        id: release
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          config-file: release-please-config.json
          manifest-file: .release-please-manifest.json

      - uses: actions/checkout@v4
        if: ${{ steps.release.outputs['packages/axi-sdk-js--release_created'] == 'true' }}

      - uses: actions/setup-node@v6
        if: ${{ steps.release.outputs['packages/axi-sdk-js--release_created'] == 'true' }}
        with:
          node-version: 24
          cache: npm
          cache-dependency-path: |
            package-lock.json
            packages/axi-sdk-js/package-lock.json
          registry-url: "https://registry.npmjs.org"

      - run: npm ci
        if: ${{ steps.release.outputs['packages/axi-sdk-js--release_created'] == 'true' }}
      - run: npm --prefix packages/axi-sdk-js ci
        if: ${{ steps.release.outputs['packages/axi-sdk-js--release_created'] == 'true' }}
      - run: npm run format:check
        if: ${{ steps.release.outputs['packages/axi-sdk-js--release_created'] == 'true' }}
      - run: npm run lint
        if: ${{ steps.release.outputs['packages/axi-sdk-js--release_created'] == 'true' }}

      - run: npm --prefix packages/axi-sdk-js run build
        if: ${{ steps.release.outputs['packages/axi-sdk-js--release_created'] == 'true' }}

      - run: npm --prefix packages/axi-sdk-js test
        if: ${{ steps.release.outputs['packages/axi-sdk-js--release_created'] == 'true' }}

      - run: npm publish --access public --provenance
        if: ${{ steps.release.outputs['packages/axi-sdk-js--release_created'] == 'true' }}
        working-directory: packages/axi-sdk-js

```


## File: bench-browser/config/conditions.yaml

```
# Benchmark conditions — each defines how the agent automates a browser

conditions:
  agent-browser:
    name: "Vercel Agent Browser (Rust CLI)"
    tool: agent-browser
    agents_md: |
      # Tools

      You have the `agent-browser` CLI installed for browser automation.
      Use it for all browsing tasks. Do NOT use curl, wget, or WebFetch.

      Run `agent-browser --help` for available commands and usage.
    daemon: auto
    install_command: "agent-browser install"
    command_policy:
      require_any_prefix: ["agent-browser"]
      forbid_any_prefix:
        - "chrome-devtools-axi"
        - "chrome-devtools"
        - "dev-browser"

  chrome-devtools-axi:
    name: "Chrome DevTools AXI (CLI wrapper)"
    tool: chrome-devtools-axi
    agents_md: |
      # Tools

      You have the `chrome-devtools-axi` CLI installed for browser automation.
      Use it for all browsing tasks. Do NOT use curl, wget, or WebFetch.

      Run `chrome-devtools-axi --help` for available commands and usage.
    daemon: explicit
    daemon_start: "chrome-devtools-axi start"
    daemon_stop: "chrome-devtools-axi stop"
    command_policy:
      require_any_prefix: ["chrome-devtools-axi"]
      forbid_any_prefix:
        - "agent-browser"
        - "chrome-devtools"
        - "dev-browser"

  # ── Chrome DevTools MCP variants ────────────────────────────────

  chrome-devtools-mcp:
    name: "Chrome DevTools MCP (no ToolSearch)"
    tool: mcp
    agents_md: |
      # Tools

      You have a Chrome DevTools MCP server with tools for browser automation.
      Use the available MCP tools to interact with web pages.
      Do NOT use curl, wget, or WebFetch.
    daemon: none
    mcp_config:
      mcpServers:
        chrome-devtools:
          command: "npx"
          args: ["-y", "chrome-devtools-mcp@latest", "--headless", "--isolated"]

  chrome-devtools-mcp-search:
    name: "Chrome DevTools MCP (with ToolSearch)"
    tool: mcp
    agents_md: |
      # Tools

      You have a Chrome DevTools MCP server registered with tools for browser
      automation. Use the available MCP tools to interact with web pages.
      Do NOT use curl, wget, or WebFetch.

      The tools follow standard browser automation patterns. Use ToolSearch
      to discover available tools and their parameters.
    daemon: none
    mcp_config:
      mcpServers:
        chrome-devtools:
          command: "npx"
          args: ["-y", "chrome-devtools-mcp@latest", "--headless", "--isolated"]

  chrome-devtools-mcp-code:
    name: "Chrome DevTools (code execution)"
    tool: code
    agents_md: |
      # Tools

      You have strongly-typed TypeScript wrappers for browser automation at
      `./servers/chrome-devtools/`. Each MCP tool is a separate `.ts` module
      with typed input interfaces. Browse the directory to discover tools.

      Write a `.ts` script and run it with `npx tsx`. Example:

          import { navigatePage, takeSnapshot } from "./servers/chrome-devtools/index.js";

          const page = await navigatePage({ url: "https://example.com" });
          const snap = await takeSnapshot({});
          console.log(snap);

      `takeSnapshot` accepts an optional input object, so prefer `takeSnapshot({})`
      when you do not need any options.

      `evaluateScript` expects a `function` string, and also accepts a `script`
      alias for convenience.

      IMPORTANT: Do NOT use `curl`, `wget`, or WebFetch.
      You must use the `./servers/chrome-devtools/` wrappers exclusively.
      Write scripts in the current working directory (not /tmp) so relative
      imports resolve correctly. Browser state persists across scripts.
    daemon: none

  chrome-devtools-mcp-compressed-cli:
    name: "MCP Compressor CLI (chrome-devtools)"
    tool: mcp-compressor-cli
    agents_md: |
      # Tools

      You have a `chrome-devtools` CLI tool for browser automation. Use it via bash.
      Do NOT use curl, wget, WebFetch, or interact with Chrome DevTools Protocol directly.

      Run `chrome-devtools --help` for available subcommands.
      Run `chrome-devtools <subcommand> --help` for parameter details.
    daemon: none
    mcp_compressor:
      level: medium
      server_name: chrome-devtools
      cli_mode: true
      backend_command:
        ["npx", "-y", "chrome-devtools-mcp@latest", "--headless", "--isolated"]
    command_policy:
      require_any_prefix: ["chrome-devtools"]
      forbid_any_prefix:
        - "agent-browser"
        - "chrome-devtools-axi"
        - "dev-browser"

  dev-browser:
    name: "Dev Browser (sandboxed JS CLI)"
    tool: dev-browser
    agents_md: |
      # Tools

      You have the `dev-browser` CLI installed for browser automation.
      Use it for all browsing tasks. Do NOT use curl, wget, or WebFetch.

      For this benchmark run, always execute scripts with:

      - `__AXI_BENCH_DEV_BROWSER_CMD__ run script.js`

      This command already pins a per-run browser name so page state persists
      across scripts within the run.

      Run `dev-browser --help` for the full CLI guide and script API.
    daemon: explicit
    require_healthy_start: true
    daemon_start: "dev-browser status"
    daemon_stop: "dev-browser stop"
    install_command: "dev-browser install"
    command_policy:
      require_any_prefix: ["dev-browser"]
      forbid_any_prefix:
        - "agent-browser"
        - "chrome-devtools-axi"
        - "chrome-devtools"

```


(… 4453 more files omitted due to size limit)
<!-- fetched-content:end -->
