# Tool Setup

> How to configure VS Code Copilot, Copilot CLI, and OpenCode for labs-wiki.

## VS Code + GitHub Copilot

### Prerequisites

- [VS Code](https://code.visualstudio.com/)
- [GitHub Copilot extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot)
- [GitHub Copilot Chat extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat)

### How It Works

VS Code Copilot reads two config files:

| File | Purpose | Always Loaded? |
|------|---------|---------------|
| `.github/copilot-instructions.md` | Compact wiki conventions | ✅ Yes |
| `AGENTS.md` | Full schema (referenced by instructions) | When opened or cited |

### Skills in VS Code

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
3. Check directory structure
4. Verify key files exist
5. Report status

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Skills not showing in VS Code | Ensure `.github/skills/wiki-*/SKILL.md` files exist |
| OpenCode can't find skills | Run `./setup.sh` to create symlink |
| `/wiki-lint` reports errors | Run `python3 scripts/lint_wiki.py` for details |
| Index out of date | Run `python3 scripts/compile_index.py` |
| AGENTS.md not being read | Ensure you're in the repo root directory |
