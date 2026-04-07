# Tool Setup

> How to configure VS Code Copilot, Copilot CLI, and OpenCode for labs-wiki.

## VS Code + GitHub Copilot

### Prerequisites

- [VS Code](https://code.visualstudio.com/)
- [GitHub Copilot extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot)
- [GitHub Copilot Chat extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat)

### Context Architecture

The wiki uses a layered context system to minimize token usage:

| Layer | Location | When Loaded | Purpose |
|-------|----------|-------------|---------|
| Global | `.github/copilot-instructions.md` | Every prompt | Lightweight index (~55 lines) |
| Scoped | `.github/instructions/*.instructions.md` | When matching files are open | File-pattern-specific rules |
| Agents | `.github/agents/*.agent.md` | Only when `@agent` invoked | Full workflow instructions |
| Skills | `.github/skills/wiki-*/SKILL.md` | Referenced by agents | Detailed operation guides |
| Prompts | `.github/prompts/*.prompt.md` | On-demand from picker | One-click common tasks |
| Schema | `AGENTS.md` | When opened or cited | Authoritative full schema |

**Key point:** Only the global instructions load on every prompt. Everything else loads on demand — this keeps context small and focused.

### Custom Agents

Invoke in VS Code Chat with `@agent-name`. Each agent has specific tools and a focused workflow.

| Agent | Invoke with | What it does |
|-------|-------------|-------------|
| Wiki Capture | `@wiki-capture` | Capture a URL or text into `raw/` for later processing |
| Wiki Ingest | `@wiki-ingest` | Two-phase pipeline: extract concepts → compile wiki pages |
| Wiki Query | `@wiki-query` | Search wiki pages and synthesize an answer with citations |
| Wiki Lint | `@wiki-lint` | Quality audit: broken links, staleness, quality scores |
| Wiki Update | `@wiki-update` | Revise an existing page with new info, preserving provenance |
| Wiki Curator | `@wiki-curator` | Gap analysis, synthesis creation, tier promotion |
| Wiki Orchestrate | `@wiki-orchestrate` | Coordinates other agents for multi-step workflows |

#### Example Usage

```
@wiki-capture https://arxiv.org/abs/2104.09864

@wiki-ingest Process the new RoPE paper source

@wiki-query What does the wiki say about positional encoding?

@wiki-lint Check all pages and fix what you can

@wiki-update Refresh wiki/concepts/positional-encoding.md with latest sources

@wiki-curator Find gaps in our ML coverage

@wiki-orchestrate Run daily maintenance
```

#### Agent Handoffs

Some agents offer handoff buttons after completing their task:

- **Wiki Capture** → offers "Ingest into Wiki" button to process the just-captured source

### Scoped Instructions

These load **automatically** when you open files matching their `applyTo` pattern — no action needed.

| Instruction | Triggers when editing | What it provides |
|-------------|----------------------|-----------------|
| `wiki-pages` | `wiki/**/*.md` | Frontmatter rules, wikilinks, quality standards |
| `raw-sources` | `raw/**/*.md` | Immutability rules, raw source format |
| `python-scripts` | `scripts/**/*.py` | Script conventions, key paths, existing patterns |
| `wiki-templates` | `templates/**/*.md` | Template variable conventions |
| `api-development` | `wiki-ingest-api/**` | FastAPI endpoint patterns, source channels |
| `agent-definitions` | `agents/**/*.md` | Persona structure, priority hierarchy format |

For example, when you open a file in `wiki/concepts/`, the wiki-pages instructions automatically activate — giving Copilot the frontmatter schema, naming rules, and provenance requirements for that context.

### Prompt Files

Prompt files are pre-built tasks you invoke from the chat prompt picker (click the 📎 icon or use the prompt picker dropdown).

| Prompt | What it does |
|--------|-------------|
| `ingest-source` | Quick-capture a URL or text → delegates to `@wiki-capture` |
| `wiki-status` | Dashboard showing pending sources, stale pages, quality issues |
| `find-gaps` | Analyzes coverage: broken wikilinks, missing concepts, synthesis opportunities |
| `daily-maintenance` | Full cycle: ingest pending → lint → auto-fix → stale review → report |

### Skills

Skills are in `.github/skills/wiki-*/SKILL.md`. In Copilot Chat, type the skill name to invoke it:

```
/wiki-ingest raw/2025-07-17-article.md
/wiki-query What is attention?
/wiki-lint
```

### Hooks

`.github/hooks/post-edit.json` defines automation triggers:
- Editing a `wiki/` file auto-triggers lint
- Adding a `raw/` file shows a reminder to run ingest

### Recommended VS Code Settings

Add to your workspace `.vscode/settings.json`:

```json
{
  "files.exclude": {
    "**/.git": true,
    "**/__pycache__": true
  },
  "markdown.validate.enabled": true,
  "editor.wordWrap": "on"
}
```

---

## Common Workflows

### "I found an interesting article"

1. **Capture:** `@wiki-capture https://example.com/article` — saves to `raw/`
2. **Ingest:** Click "Ingest into Wiki" handoff (or `@wiki-ingest`) — creates wiki pages
3. **Verify:** `@wiki-lint` — checks the new pages for quality issues

### "I want a wiki status check"

1. Use the `wiki-status` prompt file — shows pending, stale, quality summary
2. Or: `@wiki-lint` for detailed audit with error/warning breakdown

### "I want to fill knowledge gaps"

1. Use the `find-gaps` prompt file — identifies missing concepts and synthesis opportunities
2. `@wiki-curator` — creates synthesis pages and proposes tier promotions

### "End-of-day maintenance"

1. Use the `daily-maintenance` prompt file — runs the full pipeline automatically
2. Or: `@wiki-orchestrate Run daily maintenance` — same thing via agent

---

## Copilot CLI

### Prerequisites

- [GitHub CLI](https://cli.github.com/) (`gh`)
- [Copilot CLI extension](https://docs.github.com/en/copilot/github-copilot-in-the-cli)

### How It Works

Copilot CLI reads `AGENTS.md` at the repo root. All wiki conventions, workflows, and skill definitions are available automatically.

### Usage

```bash
# Navigate to the repo
cd ~/projects/labs-wiki

# Use Copilot CLI — it reads AGENTS.md automatically
gh copilot

# Skills are available as natural language commands
# "Run wiki-ingest on the new raw source"
# "Lint the wiki and fix issues"
# "Query: what do we know about transformers?"
```

---

## OpenCode

### Prerequisites

- [OpenCode](https://opencode.ai/) installed

### How It Works

OpenCode reads two config files:

| File | Purpose |
|------|---------|
| `AGENTS.md` | Full schema (universal, same as other tools) |
| `opencode.json` | Agent definitions + model assignments |

### Agent Configuration

`opencode.json` defines two agents:

| Agent | Model | Role |
|-------|-------|------|
| `wiki-maintainer` | gpt-5.1-codex | Primary agent — ingest, compile, lint, index |
| `researcher` | sonar-pro | Research subagent — source eval, fact verification |

### Skills

Skills are symlinked from `.github/skills/` to `.opencode/skills/`:

```bash
# setup.sh creates the symlink
./setup.sh

# Verify
ls -la .opencode/skills/
# skills -> ../.github/skills
```

---

## Initial Setup (All Tools)

Run the setup script after cloning:

```bash
git clone https://github.com/jbl306/labs-wiki.git
cd labs-wiki
./setup.sh
```

This will:
1. Create the `.opencode/skills/` symlink
2. Validate Python is available
3. Check directory structure (including agents, instructions, prompts)
4. Verify key files exist
5. Count skills, agents, instructions, and prompts
6. Report status

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Agent not found in VS Code Chat | Ensure `.github/agents/*.agent.md` files exist; restart VS Code |
| "Unknown tool" error on agent | Check `tools:` uses valid identifiers (see below) |
| Scoped instructions not loading | Verify `applyTo:` glob matches the file you're editing |
| Skills not showing in VS Code | Ensure `.github/skills/wiki-*/SKILL.md` files exist |
| OpenCode can't find skills | Run `./setup.sh` to create symlink |
| `/wiki-lint` reports errors | Run `python3 scripts/lint_wiki.py` for details |
| Index out of date | Run `python3 scripts/compile_index.py` |
| AGENTS.md not being read | Ensure you're in the repo root directory |

### Valid Agent Tool Identifiers

These are the only valid values for the `tools:` field in `.agent.md` frontmatter:

| Tool ID | Purpose |
|---------|---------|
| `search` | General search |
| `search/codebase` | Search workspace files |
| `search/usages` | Find symbol usages |
| `web` | General web access |
| `web/fetch` | Fetch a specific URL |
| `agent` | Delegate to sub-agents |
| `vscode/askQuestions` | Prompt user for input |

File editing and terminal commands are **default capabilities** — they don't need to be listed.
