---
applyTo: "wiki/**/*.md"
---
# Wiki Page Standards

You are editing a wiki page in the labs-wiki knowledge system.

## Frontmatter Requirements

Every wiki page MUST have this YAML frontmatter:

```yaml
---
title: "Title Case Name"
type: source | concept | entity | synthesis
created: YYYY-MM-DD
last_verified: YYYY-MM-DD
source_hash: "sha256-hex"
sources:
  - raw/source-file.md
quality_score: 0-100
concepts: [extracted-concepts]
related:
  - "[[Related Page]]"
tier: hot | established | core | workflow
tags: [topic, subtopic]
---
```

**Required:** `title`, `type`, `created`, `sources` — others are auto-populated by skills.

## Directory Rules

| Type | Must live in |
|------|-------------|
| `source` | `wiki/sources/` |
| `concept` | `wiki/concepts/` |
| `entity` | `wiki/entities/` |
| `synthesis` | `wiki/synthesis/` |

## Conventions

- Filenames: `kebab-case.md`
- Titles: Title Case in frontmatter
- Cross-references: `[[Page Title]]` wikilinks (Obsidian-compatible)
- Every fact must trace to an entry in `sources:` (provenance chain)
- After editing, update `last_verified` to today's date
- Never delete existing content — append or revise with attribution
- Do not edit `wiki/index.md` or `wiki/log.md` manually — they are auto-generated
