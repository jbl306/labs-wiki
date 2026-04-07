---
applyTo: "scripts/**/*.py"
---
# Python Script Standards

Scripts in `scripts/` are wiki infrastructure utilities.

## Conventions

- Python 3.10+ with type hints on all function signatures
- Use `pathlib.Path` for file operations, not `os.path`
- Parse YAML frontmatter with `yaml.safe_load()` — handle missing frontmatter gracefully
- Wiki root is always the repo root (use `Path(__file__).resolve().parent.parent`)
- All scripts must be runnable standalone: `python3 scripts/<name>.py`
- Use `argparse` for CLI arguments
- Print structured output (not walls of text)

## Key Paths

```python
WIKI_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = WIKI_ROOT / "raw"
WIKI_DIR = WIKI_ROOT / "wiki"
TEMPLATES_DIR = WIKI_ROOT / "templates"
INDEX_PATH = WIKI_DIR / "index.md"
LOG_PATH = WIKI_DIR / "log.md"
```

## Existing Scripts

- `lint_wiki.py` — Health checks (frontmatter, wikilinks, orphans, staleness, quality scores)
- `compile_index.py` — Rebuild `wiki/index.md` from all wiki pages
- `scaffold.py` — Create missing directories and seed files

Follow the patterns established in these scripts when adding new ones.
