---
title: milla-jovovich/mempalace
type: source
created: '2026-04-21'
last_verified: '2026-04-21'
source_hash: 4115e693a8792354734b4787ecc07e7c46fda61b3c6c67260af0d7efcc0f9df0
sources:
- raw/2026-04-11-httpsgithubcommilla-jovovichmempalace.md
source_url: https://github.com/milla-jovovich/mempalace
tags:
- ai
- chromadb
- github
- llm
- mcp
- memory
- python
tier: warm
knowledge_state: ingested
ingest_method: self-synthesis-no-llm
quality_score: 50
---

# milla-jovovich/mempalace

## Summary

The best-benchmarked open-source AI memory system. And it's free.

## Repository Info

- **Source URL**: https://github.com/milla-jovovich/mempalace
- **Stars**: 48804
- **Primary language**: Python
- **Topics**: ai, chromadb, llm, mcp, memory, python

## README Excerpt

> [!CAUTION]
> **Scam alert.** The only official sources for MemPalace are this
> [GitHub repository](https://github.com/MemPalace/mempalace), the
> [PyPI package](https://pypi.org/project/mempalace/), and the docs site at
> **[mempalaceofficial.com](https://mempalaceofficial.com)**. Any other
> domain — including `mempalace.tech` — is an impostor and may distribute
> malware. Details and timeline: [docs/HISTORY.md](docs/HISTORY.md).

<div align="center">

<img src="assets/mempalace_logo.png" alt="MemPalace" width="240">

# MemPalace

Local-first AI memory. Verbatim storage, pluggable backend, 96.6% R@5 raw on LongMemEval — zero API calls.

[![][version-shield]][release-link]
[![][python-shield]][python-link]
[![][license-shield]][license-link]
[![][discord-shield]][discord-link]

</div>

---

## Activity Snapshot

### Recent Releases

### v3.3.2 (2026-04-21)
### Recent Commits

- 2026-04-22 9b35d9f Ben Sigman: Merge pull request #661 from jphein/perf/graph-cache
- 2026-04-22 23ee2a0 Ben Sigman: Merge pull request #673 from jphein/feat/deterministic-hook-save
- 2026-04-22 02aafc0 Ben Sigman: Merge pull request #1021 from jphein/upstream-fix/silent-save-visibility
- 2026-04-22 810f9a5 Ben Sigman: Merge pull request #851 from vnguyen-lexipol/fix/status-paginate-large-palaces
- 2026-04-21 74e9cbc jp: feat: deterministic hook saves — zero data loss via silent Python API
- 2026-04-21 1b00f93 Igor Lins e Silva: Merge pull request #833 from MemPalace/fix/hooks-python-resolution
- 2026-04-13 48eb627 Igor Lins e Silva: fix(hooks): MEMPAL_PYTHON override for .sh hooks' internal python3 calls
- 2026-04-21 5522d34 Igor Lins e Silva: Merge pull request #340 from messelink/fix/mcp-pipx-compat
- 2026-04-16 9e53228 Pim Messelink: test: update test_cli assertions for mempalace-mcp entry point
- 2026-04-16 982d421 Pim Messelink: fix: update mempalace mcp command to use mempalace-mcp entry point
- 2026-04-16 67a0677 Pim Messelink: fix: use mempalace CLI in top-level hook scripts
- 2026-04-09 be89e49 Pim Messelink: fix: use mempalace CLI in hook scripts instead of python3 -m
- 2026-04-09 9f5b8f5 Pim Messelink: fix: add mempalace-mcp console entry point for pipx/uv compatibility
- 2026-04-21 4fb0ee5 Igor Lins e Silva: Merge pull request #942 from fatkobra/fix-hooks-resolve-claude-plugin
- 2026-04-21 1a180cd Igor Lins e Silva: Merge pull request #1051 from itfarrier/feat/i18n-belarusian
- 2026-04-21 6d42f61 Igor Lins e Silva: Merge pull request #1001 from mvalentsev/feat/i18n-de-es-fr-entity
- 2026-04-21 2a5914b Igor Lins e Silva: Merge pull request #945 from lmanchu/feat/zh-entity-detection
- 2026-04-19 54c314d Dzmitry Padabed: feat(i18n): add Belarusian
- 2026-04-19 d657626 jp: style: ruff format — collapse AttributeError log call to single line
- 2026-04-19 2629ae5 jp: fix(hooks): default silent_guard=True — config-read failure must not suppress saves
### Open Issues (top 10)

- #1082 MCP tool_search returns "Error finding id" when wing-scoped to a convos-mined wing (CLI works, unscoped MCP works) (by raphaelsamy)
- #1049 Hooks and MCP server break in projects with Python venv (hardcoded `python3`) (by sergesha)
- #1093 v3.3.2 release defect: `mempalace-mcp` entry point missing from `pyproject.toml` despite `plugin.json` requiring it — MCP server fails to start on fresh install (by jphein)
- #101 feat: Multipass -- multi-hop paths through the Mem Palace (by M0nkeyFl0wer)
- #1092 Concurrent writers (hooks + MCP server + CLI) corrupt the palace on chromadb 1.5.8 — sparse-file bloat + SIGSEGV (by AndreyBelyy)
- #1088 proposal: concurrent mining via ThreadPoolExecutor + `bulk_check_mined()` pre-fetch (by jphein)
- #1091 Runaway HNSW index explosion (582 GB link_lists.bin) on add_drawer to new room in large wing (by marcel10100)
- #1083 Stop + PreCompact hooks auto-run `mempalace mine` on chat transcript parent with default flags → polluted mega-wing, no opt-out (by raphaelsamy)
- #357 Parallel mining corrupts ChromaDB HNSW index — no warning, silent failure (by fubak)
### Recently Merged PRs (top 10)

- #661 perf: graph cache with write-invalidation in build_graph() (merged 2026-04-22)
- #673 feat: deterministic hook saves — zero data loss via silent Python API (merged 2026-04-22)
- #1021 fix(hooks): restore silent-save visibility on Claude Code 2.1.114 (merged 2026-04-22)
- #851 fix(status): paginate metadata fetch to support large palaces (merged 2026-04-22)
- #833 fix(hooks): real python-resolution for .sh hooks, with MEMPAL_PYTHON override (merged 2026-04-21)
- #340 fix: add mempalace-mcp entry point for pipx/uv compatibility (merged 2026-04-21)
- #942 fix(hooks): resolve Claude plugin hook runner cross-platform (merged 2026-04-21)
- #1051 feat(i18n): add Belarusian (merged 2026-04-21)
- #1001 feat(i18n): add entity detection to German, Spanish, and French locales (merged 2026-04-21)
- #945 feat(i18n): add Traditional + Simplified Chinese entity detection (merged 2026-04-21)

## Crawled Files

Source dump in `raw/2026-04-11-httpsgithubcommilla-jovovichmempalace.md` includes:

- `.claude-plugin/README.md`
- `.codex-plugin/README.md`
- `.gitignore`
- `benchmarks/README.md`
- `hooks/README.md`
- `LICENSE`
- `mempalace/README.md`
- `pyproject.toml`
- `tests/benchmarks/README.md`
- `website/.gitignore`
- `website/package.json`
- `docs/CLOSETS.md`
- `docs/HISTORY.md`
- `docs/rfcs/002-source-adapter-plugin-spec.md`
- `examples/basic_mining.py`
- `examples/convo_import.py`
- `examples/gemini_cli_setup.md`
- `examples/HOOKS_TUTORIAL.md`
- `examples/mcp_setup.md`
- `.pre-commit-config.yaml`
- `AGENTS.md`
- `CHANGELOG.md`
