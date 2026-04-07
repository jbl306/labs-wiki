---
applyTo: "agents/**/*.md"
---
# Agent Persona Definition Standards

Files in `agents/` define AI agent personas used by the wiki system. Each persona is activated by specific skills and has a defined priority hierarchy.

## Required Sections

Every agent persona file must include:

1. **Identity** — Role name and one-line purpose
2. **Priority Hierarchy** — Ordered priorities (e.g., accuracy > completeness > attribution > brevity)
3. **Activation** — Which skills/workflows trigger this persona
4. **Allowed Tools** — Explicit list of tools the persona can use
5. **Operating Rules** — Numbered rules governing behavior

## Current Personas

| Persona | Role | Primary Activation |
|---------|------|-------------------|
| Researcher | Source evaluation, concept extraction | `/wiki-ingest` Phase 1, `/wiki-query` |
| Compiler | Raw → wiki page generation | `/wiki-ingest` Phase 2, `/wiki-update` |
| Curator | Gap analysis, synthesis creation | `/wiki-lint` gap analysis, `/wiki-orchestrate` |
| Auditor | Quality scoring, staleness detection | `/wiki-lint`, `/wiki-update` |

## Conventions

- Priority hierarchies use `>` notation: `accuracy > completeness > attribution > brevity`
- Operating rules are numbered for reference
- Tool lists match the tools available in the agent's activation context
- Cross-reference AGENTS.md for authoritative schema — personas implement that schema
