# Wiki Audit Log

> Structured log of all wiki operations. Each entry is a YAML block.
> Appended by `/wiki-ingest`, `/wiki-update`, `/wiki-lint`, `/wiki-orchestrate`.

```yaml
- timestamp: 2026-04-07T04:00:00Z
  operation: setup
  agent: system
  targets:
    - wiki/index.md
    - wiki/log.md
  source: initial-setup
  status: success
  notes: "Wiki initialized — directory structure, schema, skills, scripts, docs, and ingest API created."
```
