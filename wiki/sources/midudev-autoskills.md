---
title: midudev/autoskills
type: source
created: '2026-04-21'
last_verified: '2026-04-22'
source_hash: 5bbf4cdf139d7fcc5f04a806962c94847bca27b85f6ab111d39d84f8b4fecdbe
sources:
- raw/2026-04-10-httpsgithubcommidudevautoskills.md
source_url: https://github.com/midudev/autoskills
tags:
- github
- typescript
tier: warm
knowledge_state: ingested
ingest_method: manual-reprocess-github-2026-04-22
quality_score: 80
concepts:
- automated-ai-skill-stack-installation
- automated-skill-path-generation-containerized-agent-systems
- agent-skill-routing-architecture
---

# midudev/autoskills

## What it is

`autoskills` is a single-command (`npx autoskills`) tool from midudev that scans a project, infers the tech stack from manifests like `package.json`, Gradle files, `deno.json`, `pyproject.toml`, etc., and installs the matching AI agent skills from `skills.sh`. If Claude Code is the target, it also writes a `CLAUDE.md` summary of the installed skills. It's effectively `create-react-app` for an agent's skill library.

## Why it matters

Useful as a reference implementation for the kind of stack-aware skill installer we'd want for new project bootstraps. We don't run `autoskills` ourselves — our skill stack is curated manually under `external-powers/` and `.github/skills/` — but the detection ruleset (Next.js, Nuxt, Spring Boot, Tauri, Cloudflare Agents, Vercel AI SDK, Drizzle, Better Auth, etc.) is a good catalog of what other agent stacks consider important to specialise on.

## Key concepts

- **Stack auto-detection** — Reads project manifests across many ecosystems (JS/TS, Go, Bun, Deno, Dart, Spring Boot, .NET, Python, Ruby on Rails) to infer technologies. See [[automated-ai-skill-stack-installation]].
- **Skill installation via skills.sh** — Pulls matching skills from the `skills.sh` registry into `.claude/skills/` (or equivalent for other agents). See [[automated-skill-path-generation-containerized-agent-systems]].
- **Multi-agent target support** — Detects Claude Code, OpenCode, Kiro, and others; emits the right per-agent format. See [[agent-skill-routing-architecture]].
- **Generated CLAUDE.md summary** — Optional summary written from the markdown files in `.claude/skills`.
- **Multi-select TUI** — Interactive picker with already-installed skills pre-unchecked.
- **Dry-run support** — `--dry-run` shows what would be installed without writing.

## How it works

- Run `npx autoskills` in project root.
- Detection routines walk the workspace (`package.json`, Gradle settings, `deno.jsonc`, `pyproject.toml`, etc.) and produce a list of detected technologies.
- For each detected tech, the corresponding skill (curated in `SKILLS_MAP`) is fetched from `skills.sh` and installed into the per-agent skills directory.
- If `claude-code` is auto-detected (or forced with `-a claude-code`), a `CLAUDE.md` summary is generated.
- Recent additions: Python ecosystem detection, Laravel multi-signal detection, Electron, .NET / ASP.NET Core, React Hook Form, Three.js, Zod.

## Setup

```bash
npx autoskills              # interactive
npx autoskills --dry-run    # preview only
npx autoskills -y           # accept defaults
npx autoskills -a claude-code   # force agent target
```

## Integration notes

Not a fit for direct adoption — our skill stack is hand-curated and tracked via git in `external-powers/` and `.github/skills/`, not pulled from `skills.sh`. The `SKILLS_MAP` in this repo is, however, a useful "what does the rest of the ecosystem think matters per stack" reference when curating our own skill library or building a `context-doc-factory` entry.

## Caveats / Gotchas

- License is **CC BY-NC 4.0** — non-commercial. Worth noting before reusing the detection code in any commercial workspace tool.
- Requires Node.js >= 22.
- v0.2.7 changed the build to compile TypeScript to `dist/` and ships a shipped `dist/main.js`; older versions ran `.ts` directly via tsx.
- v0.2.6 stopped auto-generating CLAUDE.md by default in some flows; check `--help` for current behavior.

## Repo metadata

| Field | Value |
|---|---|
| Stars | 3,566 |
| Primary language | TypeScript |
| Topics | (none) |
| License | CC BY-NC 4.0 |

## Source

- Raw dump: `raw/2026-04-10-httpsgithubcommidudevautoskills.md`
- Upstream: https://github.com/midudev/autoskills
