---
applyTo: "templates/**/*.md"
---
# Wiki Template Standards

Templates in `templates/` define the structure for each wiki page type. They are used by the Compiler agent during `/wiki-ingest` Phase 2.

## Placeholder Conventions

- Use `UPPER_SNAKE_CASE` for template variables: `CONCEPT_TITLE`, `YYYY-MM-DD`, `SHA256_HASH`
- Frontmatter must include ALL fields from the wiki page standard (see `AGENTS.md`)
- Default `quality_score: 0` and `tier: hot` for new pages
- Include `## Sources` section at the bottom of every template

## Template Types

| Template | Page Type | Directory |
|----------|-----------|-----------|
| `concept-page.md` | `concept` | `wiki/concepts/` |
| `entity-page.md` | `entity` | `wiki/entities/` |
| `source-summary.md` | `source` | `wiki/sources/` |
| `synthesis-page.md` | `synthesis` | `wiki/synthesis/` |

## Rules

- Every template must produce a valid wiki page when placeholders are filled
- Cross-reference sections use `[[Page Title]]` wikilinks
- Keep templates focused — don't add optional sections that clutter pages
- When modifying a template, verify existing pages still conform
