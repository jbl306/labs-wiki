---
name: wiki-setup
description: Initialize or validate the labs-wiki directory structure. Safe to re-run — idempotent.
allowed-tools:
  - read
  - write
  - bash
  - glob
---

# /wiki-setup

Initialize or validate the labs-wiki wiki structure. This skill is **idempotent** — safe to run at any time without data loss.

## What It Does

1. **Validates directory structure** — checks that all required directories exist:
   - `raw/`, `raw/assets/`
   - `wiki/sources/`, `wiki/concepts/`, `wiki/entities/`, `wiki/synthesis/`
   - `agents/`, `templates/`, `scripts/`, `docs/`
   - `.github/skills/`, `.github/hooks/`

2. **Creates missing directories** — any missing directory is created with a `.gitkeep`

3. **Seeds wiki files** — creates `wiki/index.md` and `wiki/log.md` if they don't exist:
   ```markdown
   # Wiki Index
   
   > Auto-generated catalog of all wiki pages. Do not edit manually.
   > Rebuilt by `/wiki-ingest`, `/wiki-update`, and `/wiki-orchestrate`.
   
   *No pages yet. Run `/wiki-ingest` to process sources from `raw/`.*
   ```

4. **Validates tool configs** — checks that these files exist and are non-empty:
   - `AGENTS.md`
   - `.github/copilot-instructions.md`
   - `opencode.json`

5. **Creates symlink** — `.opencode/skills/` → `.github/skills/` (if OpenCode is in use)

6. **Reports status** — prints a summary of what was created, what was validated, and any issues found

## When to Use

- First time setting up the wiki
- After cloning the repo on a new machine
- After any structural change to verify integrity
- When troubleshooting "file not found" errors

## Rules

- **Never delete existing files** — only create missing ones
- **Never overwrite existing content** — if `wiki/index.md` exists, leave it alone
- **Always report what was done** — list every action taken
