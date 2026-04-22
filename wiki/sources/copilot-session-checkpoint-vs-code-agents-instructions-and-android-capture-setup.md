---
title: "Copilot Session Checkpoint: VS Code agents, instructions, and Android capture setup"
type: source
created: 2026-04-07
last_verified: 2026-04-21
source_hash: "7d3d52a1d3ee7ec60a8a961500ba692b7abcad812b647e46c6e056aea9857392"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-vs-code-agents-instructions-and-android-capture--a7b54100.md
quality_score: 58
concepts:
  []
related:
  - "[[Labs-Wiki]]"
tier: hot
tags: [copilot-session, checkpoint, fileback, durable-knowledge, labs-wiki, agents, dashboard]
checkpoint_class: durable-architecture
retention_mode: retain
knowledge_state: validated
---

# Copilot Session Checkpoint: VS Code agents, instructions, and Android capture setup

## Summary

The user wants to create a complete VS Code Copilot customization layer (custom agents, scoped instructions, prompt files) for their labs-wiki project — a personal LLM-powered knowledge wiki. The approach uses VS Code best practices with layered context management: slim global instructions (~55 lines), scoped instructions that auto-load by file pattern, custom agents invoked on demand, and prompt files for common tasks. After creating all files, we've been debugging the Android HTTP Shortcuts capture integration, iterating through several configuration issues.

## Key Points

- User asked to create custom agents, skills, and instructions for all wiki management aspects using VS Code best practices and context size management
- Created plan with layered context architecture
- Created 6 scoped instructions in `.github/instructions/`
- Created 7 custom agents in `.github/agents/`
- Created 4 prompt files in `.github/prompts/`
- Fixed all 7 agents: removed invalid tools, updated model to GPT-5.4

## Execution Snapshot

**Files created:**
- `.github/instructions/wiki-pages.instructions.md` — applyTo: wiki/**/*.md
- `.github/instructions/raw-sources.instructions.md` — applyTo: raw/**/*.md
- `.github/instructions/python-scripts.instructions.md` — applyTo: scripts/**/*.py
- `.github/instructions/wiki-templates.instructions.md` — applyTo: templates/**/*.md
- `.github/instructions/api-development.instructions.md` — applyTo: wiki-ingest-api/**
- `.github/instructions/agent-definitions.instructions.md` — applyTo: agents/**/*.md
- `.github/agents/wiki-ingest.agent.md` — Two-phase ingest pipeline
- `.github/agents/wiki-query.agent.md` — Search & synthesize
- `.github/agents/wiki-lint.agent.md` — Quality audit
- `.github/agents/wiki-update.agent.md` — Page revision
- `.github/agents/wiki-curator.agent.md` — Gap analysis
- `.github/agents/wiki-orchestrate.agent.md` — Multi-step coordinator (uses `agents:` property)
- `.github/agents/wiki-capture.agent.md` — Quick capture with handoff to wiki-ingest
- `.github/prompts/ingest-source.prompt.md` — Quick source capture
- `.github/prompts/wiki-status.prompt.md` — Health dashboard
- `.github/prompts/find-gaps.prompt.md` — Coverage analysis
- `.github/prompts/daily-maintenance.prompt.md` — Full maintenance cycle

**Files modified:**
- `.github/copilot-instructions.md` — Slimmed from 208 → 56 lines (lightweight index pointing to agents/instructions/prompts)
- `setup.sh` — Added validation for .github/instructions/, .github/agents/, .github/prompts/ directories + counts
- `docs/tool-setup.md` — Complete rewrite with usage guide for all customization layers
- `docs/capture-sources.md` — Android HTTP Shortcuts section rewritten 3 times debugging issues

**Current state:**
- All VS Code customization files are created and verified via setup.sh
- Active bug: HTTP Shortcuts Android app sending `{request_body}` as literal text instead of resolving the variable

## Technical Details

- Valid `tools:` frontmatter values: `search`, `search/codebase`, `search/usages`, `web`, `web/fetch`, `agent`, `vscode/askQuestions`
- `editFiles` and `runTerminalCommand` are INTERNAL runtime tool names (appear in hook inputs) — NOT valid for tools: list
- File editing and terminal commands are DEFAULT agent capabilities — always available without listing ### VS Code Custom Agent Format
- File: `.github/agents/*.agent.md`
- Frontmatter: name, description, tools (array), model (array), agents (for orchestrators), handoffs, hooks
- Orchestrator pattern: `tools: ['agent']` + `agents: ['Sub Agent 1', 'Sub Agent 2']`
- Handoff pattern: `handoffs: [{label, agent, prompt, send}]` ### VS Code Scoped Instructions
- File: `.github/instructions/*.instructions.md`
- Frontmatter: `applyTo: "glob-pattern"` — auto-loads when matching files are open
- Searched in locations defined by `chat.instructionsFilesLocations` setting ### HTTP Shortcuts Android App (CRITICAL LESSONS)
- There are NO built-in sharing variables like `sharing_text`
- To receive shared content: create GLOBAL VARIABLES (Static type) → enable "Allow Receiving Value from Share Dialog" in Advanced Settings → set "Use shared value as" to Text or Title/Subject
- Global variable placeholders: single braces `{var_name}` (shown purple in app)
- Local variable placeholders: double braces `{{var_name}}` (shown orange in app)
- `getVariable()` and `setVariable()` work in scripting blocks for both local and global vars
- Shortcut needs "Accept shared text from other apps" in Trigger & Execution Settings
- Raw placeholder substitution in JSON body is DANGEROUS — shared URLs contain chars that break JSON
- Better approach: build JSON in scripting block with `JSON.stringify()`, store in variable, pass through ### CURRENT BUG: `{request_body}` not resolving
- Error: "Expected ':' at line 1 column 15 path $.request_body"
- This means the API received literal `{request_body}` as the POST body
- The variable placeholder is NOT being resolved by HTTP Shortcuts
- Likely cause: the `request_body` variable needs to be inserted via the { } button in the app UI, OR the variable wasn't created as a global variable, OR the variable name doesn't match exactly
- Another possible cause: when request body type is "Custom Text" with content type application/json, HTTP Shortcuts might try to validate/parse it as JSON before variable substitution ### Wiki Ingest API
- POST `/api/ingest` expects: `{type, content, title?, tags?, source?}`
- `type` must be exactly: "url", "text", or "note"
- Returns: `{status: "ok", path: "raw/YYYY-MM-DD-slug.md"}`
- Sends ntfy notification: "📥 New source captured: {title}"
- Auth: Bearer token via `WIKI_API_TOKEN` env var ### Context Size Management
- Global instructions: ~55 lines, loads every prompt
- Scoped instructions: 30-50 lines each, only when matching files open
- Agents: 50-80 lines each, only when @agent invoked
- Skills: referenced by agents, loaded on demand
- Prompts: 20-40 lines, on-demand from picker

## Important Files

- `docs/capture-sources.md`
- Central to current debugging — Android HTTP Shortcuts section
- Rewritten 3 times; currently has scripting-based approach at Step 5 (lines ~173-213)
- NEEDS FIX: the `{request_body}` approach may not work — see next steps

- `.github/copilot-instructions.md`
- Global instructions loaded every prompt — slimmed to 56 lines
- Lightweight index pointing to agents, instructions, prompts, and AGENTS.md

- `.github/agents/` (7 files)
- All use model: `['Claude Sonnet 4', 'GPT-5.4']`
- wiki-orchestrate uses `agents:` property to delegate to other agents
- wiki-capture has handoff to wiki-ingest

- `.github/instructions/` (6 files)
- Each has `applyTo` glob pattern for automatic context loading

- `.github/prompts/` (4 files)
- Each targets a specific agent (wiki-capture, ask, wiki-curator, wiki-orchestrate)

- `docs/tool-setup.md`
- Complete usage guide for all customization layers
- Includes valid tool identifiers reference table

- `setup.sh`
- Updated to validate and count agents, instructions, prompts
- All checks passing

- `wiki-ingest-api/app.py`
- Lines 25-30: IngestRequest model (type, content, title, tags, source)
- Lines 138-139: type validation ("url", "text", "note")
- Lines 95-108: ntfy notification sending

## Next Steps

**Immediate — fix the `{request_body}` not resolving bug:**

**The error "Expected ':' at line 1 column 15 path $.request_body" means the body is being sent literally. Likely fix: HTTP Shortcuts may not resolve variables inside Custom Text body when content type is application/json — it may try to JSON-parse first. Options:**
1. Change body type from "Custom Text (application/json)" to just "Custom Text" (no content type) and set Content-Type header manually (already done in Step 4)
2. Or: skip the `request_body` variable entirely — use the scripting `setBody()` function if it exists in HTTP Shortcuts
3. Or: use form-data parameters instead of raw JSON body, where each field is a separate parameter with variable placeholders

Need to update `docs/capture-sources.md` Android section once the correct approach is confirmed.

## Related Wiki Pages

- [[Labs-Wiki]]

## Notable Quotes

No notable quotes extracted.

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-vs-code-agents-instructions-and-android-capture--a7b54100.md` |
| Type | checkpoint |
| Author | Unknown |
| Date | 2026-04-07 |
| URL | N/A |
