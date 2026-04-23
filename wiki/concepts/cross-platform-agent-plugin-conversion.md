---
title: Cross-Platform Agent Plugin Conversion
type: concept
created: '2026-04-23'
last_verified: '2026-04-23'
source_hash: 47dca59f5e85d3b968b39b0119e3e03fe82d3bc935cfa91eaa1b03d60cf1aeeb
sources:
  - raw/2026-04-23-httpsgithubcomeveryinccompound-engineering-plugin.md
quality_score: 82
related:
  - "[[Compound Engineering Workflow]]"
  - "[[Custom Agents in VS Code]]"
  - "[[Source Adapter Plugin Specification]]"
tier: hot
tags:
  - agent-platforms
  - claude-code
  - conversion
  - plugin
  - portability
  - typescript
---

# Cross-Platform Agent Plugin Conversion

## Overview

Cross-Platform Agent Plugin Conversion is the practice of treating one agent-plugin format as source-of-truth, loading it into a normalized internal model, and then emitting compatible artifacts for several different host runtimes. In `EveryInc/compound-engineering-plugin`, the canonical source format is the Claude-compatible plugin structure, while the outputs target Codex, OpenCode, Pi, Gemini CLI, Kiro, and other agent environments. The concept matters because it turns workflow authoring into a "write once, distribute many" problem rather than a repeated hand-porting exercise.

## How It Works

The conversion pipeline begins with a canonical schema. In this repository, that schema is the Claude plugin model defined in `src/types/claude.ts`. It describes a plugin as manifest metadata plus collections of agents, commands, skills, hooks, and optional MCP server definitions. Crucially, the content itself is not stored only in JSON; agents and commands live as Markdown with frontmatter, and skills are represented by `SKILL.md` files in per-skill directories. That makes the authoring format ergonomic for humans while still preserving enough structure for deterministic parsing.

`src/parsers/claude.ts` is the loader that turns that file tree into data. It resolves the plugin root by finding `.claude-plugin/plugin.json`, reads the manifest, then walks the configured `agents/`, `commands/`, and `skills/` directories. For each agent or command file, it parses frontmatter, extracts fields such as `name`, `description`, `model`, or `allowed-tools`, and stores the Markdown body separately. For skills, it reads `SKILL.md`, records the containing directory, and honors the optional `ce_platforms` field so a skill can be included only on certain targets. Hook definitions can come from a default `hooks/hooks.json`, from manifest-declared hook paths, or directly from inline manifest data, and the parser merges them into one in-memory object. Optional `.mcp.json` definitions are also unwrapped into a standard `mcpServers` map.

That normalized representation is what makes the rest of the pipeline possible. Once the plugin is expressed as typed objects, converters can focus on semantic translation instead of filesystem trivia. The repo has dedicated converter modules for `claude-to-codex`, `claude-to-copilot`, `claude-to-droid`, `claude-to-gemini`, `claude-to-kiro`, `claude-to-opencode`, and `claude-to-pi`. Each converter answers questions like: What is the target's command shape? How are tools named? Where do prompts live? Which features do not exist natively? What must be dropped, adapted, or rewritten?

The target writer layer sits below the converter layer. `src/targets/index.ts` registers implemented handlers for `opencode`, `codex`, `pi`, `gemini`, and `kiro`. The contract is explicit: each target has a `convert` function that accepts the normalized Claude plugin and returns a bundle, and a `write` function that materializes that bundle in the host's expected directory structure. That separation matters because conversion and installation are not always the same concern. A bundle might be representable in memory even if the write target has tricky path rules, merge semantics, or cleanup requirements.

Path discipline is one of the hard parts of cross-platform conversion, and the repository treats it as a first-class design problem. `AGENTS.md` says OpenCode output must remain at `opencode.json` and `.opencode/{agents,skills,plugins}`, with `opencode.json` being deep-merged rather than replaced wholesale. The README says Codex installs keep generated skills under `~/.codex/skills/compound-engineering/` and avoid dumping new files into `~/.agents`. `src/utils/opencode-config.ts` resolves OpenCode's global root through `OPENCODE_CONFIG_DIR` when present, falling back to `~/.config/opencode`, so install and cleanup agree on the same location. These are not cosmetic details: cross-platform portability fails quickly when the generated files land in the wrong place or overwrite user-owned config.

Another challenge is tool-surface mismatch. Hosts rarely expose the exact same tool vocabulary. `src/utils/codex-agents.ts` addresses that explicitly by maintaining a managed AGENTS.md block that maps Claude-centric tool names such as `Read`, `Edit`, `Task`, or `WebFetch` onto Codex equivalents like shell reads, `apply_patch`, sequential main-thread execution, or `curl`. This is a concrete example of semantic adaptation: the target runtime may not have the same primitives, so the converter has to preserve behavior by translating intent rather than merely copying syntax.

Detection and installation orchestration are also part of the concept. `src/utils/detect-tools.ts` looks for host-specific markers such as `~/.codex`, `~/.copilot`, `~/.pi`, `~/.factory`, `~/.gemini`, `~/.kiro`, and workspace-level paths like `.github/skills` or `.opencode`. This allows the installer or setup flow to infer which targets are relevant on a machine instead of asking users to memorize every integration path manually.

The final important layer is cleanup. Cross-platform converters frequently suffer from stale-artifact drift: a new install writes the new files, but old renamed files still exist and shadow them in the host runtime. This repository addresses that with `src/utils/legacy-cleanup.ts` and `src/data/plugin-legacy-artifacts.ts`, which enumerate old skill, agent, and prompt names and move them into a `compound-engineering/legacy-backup/` directory during cleanup. That means portability here includes lifecycle management, not just initial installation.

In aggregate, the pattern is straightforward but powerful:

```text
Claude-compatible plugin tree
  -> parse into typed objects
  -> filter/reshape for target capabilities
  -> write to stable target-specific paths
  -> clean stale artifacts so old installs do not shadow new ones
```

The concept generalizes beyond this repo. Any team authoring agent workflows for multiple runtimes can use the same strategy: pick one expressive source format, define a typed intermediate model, write explicit converters, and own the artifact lifecycle end to end.

## Key Properties

- **Canonical source format**: One plugin model acts as the single source-of-truth.
- **Typed intermediate representation**: Parsing separates authoring concerns from target-writing concerns.
- **Explicit per-target converters**: Each host runtime gets its own conversion logic instead of a generic lossy exporter.
- **Stable artifact paths**: Writers preserve target-specific install semantics and merge behavior.
- **Lifecycle-aware cleanup**: Portability includes migration and stale-artifact cleanup, not just initial conversion.

## Limitations

Cross-platform conversion is constrained by the least expressive target. Features that exist in the source format may need to be approximated or omitted on certain hosts, especially around tool permissions, subagent dispatch, or hook semantics. The approach also incurs maintenance cost: every host format drift requires converter and writer updates, plus new tests. Finally, the more behavior relies on textual prompt conventions instead of formal schemas, the more fragile semantic translation becomes.

## Examples

In this repo, a plugin author can keep editing the Claude-style source and then install it elsewhere:

```bash
# Convert/install to a converter-backed target
bunx @every-env/compound-plugin install compound-engineering --to opencode

# Codex hybrid flow
codex plugin marketplace add EveryInc/compound-engineering-plugin
bunx @every-env/compound-plugin install compound-engineering --to codex
```

Conceptually, the flow is:

1. Parse `.claude-plugin/plugin.json`.
2. Load Markdown agents, commands, and skills.
3. Filter skills by target platform when `ce_platforms` is present.
4. Convert the normalized model to the host bundle.
5. Write to target-specific locations.
6. Run cleanup so stale renamed artifacts do not shadow the new install.

## Practical Applications

This pattern is useful whenever the same agent workflow needs to travel across multiple development environments without fragmenting into divergent copies. It is especially valuable for organizations that mix Claude Code, Copilot, Codex, and niche agent CLIs but still want one maintained workflow catalog. In a knowledge system like `labs-wiki`, it is also a good reference for building source-of-truth schemas that compile cleanly into several downstream surfaces.

## Related Concepts

- **[[Compound Engineering Workflow]]**: The workflow is what the conversion system is transporting across runtimes.
- **[[Custom Agents in VS Code]]**: Both concepts treat agent behavior as a configurable product surface rather than a one-off prompt.
- **[[Source Adapter Plugin Specification]]**: Another example of formalizing a pluggable contract so one core system can be extended safely.

## Sources

- [[EveryInc/compound-engineering-plugin]] — primary source for the parser, converter, writer, and install model
