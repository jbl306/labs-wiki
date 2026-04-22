# labs-wiki — Progress Tracker

> Full implementation tracker with feature tiers, phased delivery, validation gates, and test cases.
> Source plan: [plans/labs-wiki.md](../plans/labs-wiki.md)

---

## Feature Tiers

### Tier 1: Core (Must-Have)

These features define the minimum viable wiki. Nothing ships without all 10 complete.

| # | Feature | Phase | Status | Validated |
|---|---------|-------|--------|-----------|
| 1 | Three-layer architecture (`raw/` → `wiki/` → schema) | P1 | ✅ Done | ✅ |
| 2 | Hash-based incremental compilation (SHA-256 in frontmatter) | P2 | ✅ Done | ✅ |
| 3 | Two-phase ingest pipeline (extract → compile) | P2 | ✅ Done | ✅ |
| 4 | Structured audit log (`log.md` with YAML entries) | P2 | ✅ Done | ✅ |
| 5 | Index with summaries (`index.md` — LLM-navigable) | P2 | ✅ Done | ✅ |
| 6 | Health lint system (orphans, broken links, stale pages) | P2 | ✅ Done | ✅ |
| 7 | Wikilink cross-references (`[[concept]]`) | P2 | ✅ Done | ✅ |
| 8 | Portable Agent Skills (SKILL.md + YAML frontmatter) | P2 | ✅ Done | ✅ |
| 9 | Provenance tracking (`sources:` in frontmatter) | P2 | ✅ Done | ✅ |
| 10 | Staleness detection (`source_hash` + `last_verified`) | P2 | ✅ Done | ✅ |

### Tier 2: Enhanced (Should-Have)

These features elevate from functional to polished. Target for v1.0 release.

| # | Feature | Phase | Status | Validated |
|---|---------|-------|--------|-----------|
| 11 | Idempotent setup wizard (`/wiki-setup` skill) | P2 | ✅ Done | ✅ |
| 12 | Sub-organized wiki (`sources/`, `concepts/`, `entities/`, `synthesis/`) | P1 | ✅ Done | ✅ |
| 13 | Multi-tool bootstrap (`setup.sh` — symlinks + configs) | P3 | ✅ Done | ✅ |
| 14 | Agent personas (eight-agent set in `.github/agents/`) | P1 | ✅ Done | ✅ |
| 15 | Orchestrator meta-skill (`/wiki-orchestrate`) | P2 | ✅ Done | ✅ |
| 16 | Quality scoring (0-100 per page via lint) | P2 | 🟡 In progress (R3 reworking rubric) | 🟡 |
| 17 | Context cost optimization (topic clustering in index) | P3 | ✅ Done | ✅ |
| 18 | Hook-driven automation (post-edit triggers) | P2 | ✅ Done | ✅ |

### Tier 3: Advanced (Nice-to-Have)

Post-v1.0 enhancements. Build only after Tiers 1-2 are solid.

| # | Feature | Phase | Status | Validated |
|---|---------|-------|--------|-----------|
| 19 | Freshness decay (Ebbinghaus-inspired, 90-day flag) | P3 | 🟡 In progress | 🟡 |
| 20 | Consolidation tiers (hot → established → core → workflow) | P3 | 🟡 In progress (R7 promotion cron landed; rubric pending) | 🟡 |
| 21 | Hybrid retrieval (BM25 → vector when wiki > 100 pages) | P3 | 🟡 In progress | 🟡 |
| 22 | Web/URL extraction (ingest from URLs, not just files) | P5 | ⬜ Pending | ⬜ |
| 23 | Obsidian integration (graph view, Dataview, vault config) | P4 | ⬜ Pending | ⬜ |
| 24 | OpenMemory MCP bridge (connect to homelab memory service) | P5 | ⬜ Pending | ⬜ |
| 25 | Python utility scripts (`scaffold.py`, `lint_wiki.py`, `compile_index.py`) | P3 | ⬜ Pending | ⬜ |

---

## Phase 1: Foundation

> **Goal:** Repo skeleton with all directories, config files, templates, and agent personas.
> **Depends on:** Nothing — this is the starting point.

### Tasks

| ID | Task | Tier | Status | Notes |
|----|------|------|--------|-------|
| P1-01 | `repo-setup` — Create full directory structure, LICENSE, .gitignore | T1 | ⬜ Pending | All dirs: raw/, raw/assets/, wiki/sources|concepts|entities|synthesis/, agents/, templates/, scripts/, docs/, .github/skills/wiki-*/, .github/hooks/, .github/workflows/ |
| P1-02 | `readme` — README with architecture diagram, quickstart, memory model | T1 | ⬜ Pending | Include mermaid diagram of three-layer architecture + capture channels |
| P1-03 | `schema` — AGENTS.md universal schema | T1 | ⬜ Pending | Wiki conventions, page formats, naming rules, ingest/query/lint/update workflows, frontmatter standards, agent persona references |
| P1-04 | `copilot-instructions` — .github/copilot-instructions.md | T2 | ⬜ Pending | Compact always-on instructions pointing to AGENTS.md, VS Code-specific behaviors |
| P1-05 | `opencode-config` — opencode.json agent/model config | T2 | ⬜ Pending | Primary wiki-maintainer agent + research subagent, model assignments, tool permissions |
| P1-06 | `templates` — Page templates with frontmatter standards | T1 | ⬜ Pending | source-summary.md, concept-page.md, entity-page.md, synthesis-page.md — all with full frontmatter (provenance, staleness, quality) |
| P1-07 | `agent-personas` — agents/ directory with 4 persona specs | T2 | ⬜ Pending | researcher.md, compiler.md, curator.md, auditor.md — each with identity, priority hierarchy, activation triggers, allowed tools |

### Validation Gate: P1 ✅

All of these must pass before proceeding to Phase 2:

| # | Test | Command / Check | Expected Result |
|---|------|-----------------|-----------------|
| P1-V01 | Directory structure complete | `find . -type d \| sort` | All planned directories exist (raw/, raw/assets/, wiki/sources/, wiki/concepts/, wiki/entities/, wiki/synthesis/, agents/, templates/, scripts/, docs/, .github/skills/wiki-setup/, wiki-ingest/, wiki-query/, wiki-lint/, wiki-update/, wiki-orchestrate/, .github/hooks/, .github/workflows/, wiki-ingest-api/, plans/, tasks/) |
| P1-V02 | Required root files exist | `ls README.md LICENSE .gitignore AGENTS.md opencode.json` | All 5 files present, non-empty |
| P1-V03 | AGENTS.md contains all workflow sections | `grep -c '## ' AGENTS.md` | Sections for: conventions, ingest workflow, query workflow, lint workflow, update workflow, frontmatter standard, agent personas |
| P1-V04 | copilot-instructions.md exists and references AGENTS.md | `grep 'AGENTS.md' .github/copilot-instructions.md` | At least 1 match |
| P1-V05 | opencode.json is valid JSON | `python3 -c "import json; json.load(open('opencode.json'))"` | Exit code 0 |
| P1-V06 | All 4 templates have required frontmatter fields | `for f in templates/*.md; do grep -l 'title:\|type:\|sources:\|source_hash:\|quality_score:' "$f"; done` | All templates contain: title, type, sources, source_hash, quality_score |
| P1-V07 | All 4 agent personas have required sections | `for f in agents/*.md; do grep -c '## Identity\|## Priority Hierarchy\|## Activation\|## Allowed Tools' "$f"; done` | Each file has 4 matches (all sections present) |
| P1-V08 | .gitignore excludes .env and node_modules | `grep -c '\.env$\|node_modules' .gitignore` | At least 2 matches |
| P1-V09 | Git repo clean after setup | `git status --porcelain` | Empty output (everything committed) |
| P1-V10 | README renders without errors | Open README.md in VS Code preview or `python3 -c "import markdown; markdown.markdown(open('README.md').read())"` | No parse errors, mermaid diagram block present |

---

## Phase 2: Skills & Automation

> **Goal:** All 6 skills defined and functional, hooks configured.
> **Depends on:** Phase 1 (schema + templates must exist for skills to reference).

### Tasks

| ID | Task | Tier | Status | Notes |
|----|------|------|--------|-------|
| P2-01 | `skill-setup` — wiki-setup SKILL.md | T2 | ⬜ Pending | Idempotent wizard: validate structure, create missing dirs, generate tool configs. Safe to re-run. |
| P2-02 | `skill-ingest` — wiki-ingest SKILL.md | T1 | ⬜ Pending | Two-phase pipeline: (1) hash check + concept extraction, (2) page generation with cross-refs. Updates index.md + log.md. |
| P2-03 | `skill-query` — wiki-query SKILL.md | T1 | ⬜ Pending | Read index.md → identify relevant pages → read pages → synthesize answer. Support topic-scoped queries. |
| P2-04 | `skill-lint` — wiki-lint SKILL.md | T1 | ⬜ Pending | Checks: orphan pages, broken `[[wikilinks]]`, missing frontmatter fields, stale pages (>90 days), quality scoring 0-100. |
| P2-05 | `skill-update` — wiki-update SKILL.md | T1 | ⬜ Pending | Revise existing pages: update source_hash, bump last_verified, maintain provenance chain, update cross-refs. |
| P2-06 | `skill-orchestrate` — wiki-orchestrate SKILL.md | T2 | ⬜ Pending | Meta-skill: ingest all pending → lint → fix issues → rebuild index. Coordinates multi-step workflows. |
| P2-07 | `hooks` — .github/hooks/post-edit.json | T2 | ⬜ Pending | Post-edit triggers: auto-rebuild index when wiki/ pages change, detect drift from schema. |

### Validation Gate: P2 ✅

| # | Test | Command / Check | Expected Result |
|---|------|-----------------|-----------------|
| P2-V01 | All 6 SKILL.md files exist | `find .github/skills -name 'SKILL.md' \| wc -l` | 6 files |
| P2-V02 | Every SKILL.md has valid YAML frontmatter | `for f in .github/skills/*/SKILL.md; do python3 -c "import yaml; yaml.safe_load(open('$f').read().split('---')[1])"; done` | All exit code 0 |
| P2-V03 | SKILL.md frontmatter has required fields | `for f in .github/skills/*/SKILL.md; do grep -l 'name:\|description:\|allowed-tools:' "$f"; done` | All 6 files match |
| P2-V04 | wiki-ingest references two-phase pipeline | `grep -i 'phase\|extract.*compile\|hash' .github/skills/wiki-ingest/SKILL.md` | At least 2 matches — confirms two-phase + hash-based skip |
| P2-V05 | wiki-lint references quality scoring | `grep -i 'quality\|score\|0-100\|staleness' .github/skills/wiki-lint/SKILL.md` | At least 2 matches |
| P2-V06 | wiki-query references index.md | `grep 'index.md' .github/skills/wiki-query/SKILL.md` | At least 1 match |
| P2-V07 | wiki-update references provenance | `grep -i 'provenance\|source_hash\|last_verified' .github/skills/wiki-update/SKILL.md` | At least 2 matches |
| P2-V08 | wiki-orchestrate references other skills | `grep -i 'ingest\|lint\|update\|index' .github/skills/wiki-orchestrate/SKILL.md` | At least 3 matches |
| P2-V09 | Hooks config is valid JSON | `python3 -c "import json; json.load(open('.github/hooks/post-edit.json'))"` | Exit code 0 |
| P2-V10 | No duplicate skill names in frontmatter | `for f in .github/skills/*/SKILL.md; do grep '^name:' "$f"; done \| sort \| uniq -d` | Empty output (no duplicates) |

---

## Phase 3: Tooling

> **Goal:** Python scripts for offline/CI use, setup.sh for bootstrapping.
> **Depends on:** Phase 1. Can run in parallel with Phase 2.

### Tasks

| ID | Task | Tier | Status | Notes |
|----|------|------|--------|-------|
| P3-01 | `scaffold-script` — scripts/scaffold.py | T3 | ⬜ Pending | Initialize wiki structure: create dirs, seed index.md + log.md, validate existing structure. Idempotent. |
| P3-02 | `lint-script` — scripts/lint_wiki.py | T3 | ⬜ Pending | Standalone lint: broken `[[wikilinks]]`, orphan pages, missing frontmatter, staleness (>90d last_verified), quality heuristic scoring. Exit code 0 = clean, 1 = issues found. |
| P3-03 | `index-script` — scripts/compile_index.py | T3 | ⬜ Pending | Rebuild index.md from wiki/ pages: extract title + type + summary from frontmatter, cluster by topic, write sorted index. |
| P3-04 | `setup-script` — setup.sh | T2 | ⬜ Pending | Bootstrap: create .opencode/skills/ symlink → .github/skills/, validate Python deps, check tool versions (copilot, opencode), print status. |

### Validation Gate: P3 ✅

| # | Test | Command / Check | Expected Result |
|---|------|-----------------|-----------------|
| P3-V01 | scaffold.py runs without error on empty wiki | `python3 scripts/scaffold.py --wiki-dir wiki/` | Exit code 0, creates wiki/index.md + wiki/log.md if missing |
| P3-V02 | scaffold.py is idempotent | `python3 scripts/scaffold.py && python3 scripts/scaffold.py` | Second run exits 0, no duplicate content |
| P3-V03 | lint_wiki.py exits 0 on clean wiki | Create a valid wiki page with full frontmatter → `python3 scripts/lint_wiki.py` | Exit code 0, no issues reported |
| P3-V04 | lint_wiki.py detects broken wikilink | Create page with `[[nonexistent]]` → `python3 scripts/lint_wiki.py` | Exit code 1, reports broken link |
| P3-V05 | lint_wiki.py detects missing frontmatter | Create page without `sources:` field → `python3 scripts/lint_wiki.py` | Exit code 1, reports missing field |
| P3-V06 | lint_wiki.py detects stale page | Create page with `last_verified: 2025-01-01` → `python3 scripts/lint_wiki.py` | Exit code 1, reports stale (>90 days) |
| P3-V07 | compile_index.py generates valid index | Add 3 wiki pages → `python3 scripts/compile_index.py` → `cat wiki/index.md` | Contains 3 entries with titles and summaries, topic-clustered |
| P3-V08 | setup.sh creates symlink | `bash setup.sh && ls -la .opencode/skills/` | Symlink pointing to ../.github/skills |
| P3-V09 | setup.sh is idempotent | `bash setup.sh && bash setup.sh` | Second run succeeds, no errors |
| P3-V10 | All scripts have correct shebang/imports | `head -1 scripts/*.py scripts/*.sh` | Python: `#!/usr/bin/env python3` or no shebang (module). Shell: `#!/usr/bin/env bash` |
| P3-V11 | Python scripts pass basic syntax check | `python3 -m py_compile scripts/scaffold.py scripts/lint_wiki.py scripts/compile_index.py` | Exit code 0 for all |

---

## Phase 4: Documentation

> **Goal:** Complete docs/ directory covering architecture, memory model, workflows, tool setup, Obsidian.
> **Depends on:** Phase 1. Can run in parallel with Phase 2-3.

### Tasks

| ID | Task | Tier | Status | Notes |
|----|------|------|--------|-------|
| P4-01 | `arch-doc` — docs/architecture.md | T1 | ⬜ Pending | Mermaid diagrams: three-layer data flow, two-phase ingest pipeline, capture channel architecture. Explain each layer. |
| P4-02 | `memory-doc` — docs/memory-model.md | T2 | ⬜ Pending | Staleness tracking, provenance chains, quality scoring, consolidation tiers (hot → established → core → workflow), Ebbinghaus decay. |
| P4-03 | `workflow-doc` — docs/workflows.md | T1 | ⬜ Pending | Step-by-step guides for: ingest new source, query wiki, lint wiki, update stale page, orchestrate full pipeline. |
| P4-04 | `obsidian-doc` — docs/obsidian-setup.md | T3 | ⬜ Pending | How to open labs-wiki as Obsidian vault, recommended plugins (Dataview, Graph View), template setup. |
| P4-05 | `tool-setup-doc` — docs/tool-setup.md | T2 | ⬜ Pending | Setup instructions for VS Code + Copilot, Copilot CLI, OpenCode. Config file locations, skill discovery, troubleshooting. |

### Validation Gate: P4 ✅

| # | Test | Command / Check | Expected Result |
|---|------|-----------------|-----------------|
| P4-V01 | All 5 doc files exist | `ls docs/architecture.md docs/memory-model.md docs/workflows.md docs/obsidian-setup.md docs/tool-setup.md` | All 5 present |
| P4-V02 | architecture.md contains mermaid diagrams | `grep -c 'mermaid' docs/architecture.md` | At least 2 diagrams (three-layer + capture channels) |
| P4-V03 | memory-model.md covers all memory concepts | `grep -ic 'staleness\|provenance\|quality.score\|consolidation\|decay' docs/memory-model.md` | At least 5 matches (all concepts covered) |
| P4-V04 | workflows.md covers all 5 operations | `grep -ic 'ingest\|query\|lint\|update\|orchestrate' docs/workflows.md` | At least 5 matches |
| P4-V05 | tool-setup.md covers all 3 tools | `grep -ic 'vs.code\|copilot.cli\|opencode' docs/tool-setup.md` | At least 3 matches |
| P4-V06 | No broken internal links in docs | `grep -roh '\[.*\](\.\.\/[^)]*)\|\[.*\](\./[^)]*)' docs/ \| while read link; do path=$(echo "$link" \| grep -oP '\(\.?\.?/[^)]+\)' \| tr -d '()'); [ -f "$path" ] \|\| echo "BROKEN: $link"; done` | No BROKEN output |
| P4-V07 | Each doc has a title heading | `for f in docs/*.md; do head -1 "$f" \| grep -q '^# ' \|\| echo "MISSING TITLE: $f"; done` | No MISSING TITLE output |

---

## Phase 5: Multi-Device Ingestion

> **Goal:** FastAPI ingest service + all capture channels operational.
> **Depends on:** Phase 1 (raw/ directory). Can run in parallel with Phase 2-4.

### Tasks

| ID | Task | Tier | Status | Notes |
|----|------|------|--------|-------|
| P5-01 | `ingest-api` — FastAPI app (wiki-ingest-api/app.py) | T1 | ⬜ Pending | POST /api/ingest (JSON: text/url/note; multipart: file upload). GET /health. Bearer token auth. Writes to raw/ with standardized frontmatter. ntfy notification on capture. |
| P5-02 | `ingest-docker` — Dockerfile + compose stack | T1 | ⬜ Pending | wiki-ingest-api/Dockerfile, compose/compose.wiki.yml. Resource limits: 128M/0.25 CPU. Healthcheck on /health. Caddy reverse proxy label. |
| P5-03 | `ingest-cli` — Shell functions `wa` and `waf` | T1 | ⬜ Pending | wa: JSON POST (type, content, title). waf: multipart file upload. Pipe support for stdin. Include in docs/capture-sources.md. |
| P5-04 | `ingest-bookmarklet` — JavaScript bookmarklet | T2 | ⬜ Pending | One-click capture of current page URL + title. Alert on success/failure. Include in docs/capture-sources.md. |
| P5-05 | `ingest-ios-shortcut` — iOS Shortcut instructions | T2 | ⬜ Pending | Step-by-step guide for creating iOS Shortcut. Accept URL/text/image from Share Sheet → POST to API. Include screenshot walkthrough. |
| P5-06 | `ingest-github-action` — .github/workflows/ingest-from-issue.yml | T2 | ⬜ Pending | On issue labeled "ingest": extract title + body → create raw/ file → commit → close issue with confirmation comment. |
| P5-07 | `ingest-ntfy-watcher` — scripts/ntfy-wiki-watcher.sh | T3 | ⬜ Pending | Subscribe to ntfy topic → parse message → POST to ingest API. Run as systemd service or Docker sidecar. |
| P5-08 | `ingest-doc` — docs/capture-sources.md | T1 | ⬜ Pending | Setup guide for all 6 channels: API, phone, browser, CLI, GitHub Issues, ntfy. Include examples and troubleshooting. |

### Validation Gate: P5 ✅

| # | Test | Command / Check | Expected Result |
|---|------|-----------------|-----------------|
| P5-V01 | FastAPI app starts | `cd wiki-ingest-api && pip install -r requirements.txt && python3 -c "from app import app; print('OK')"` | Prints "OK", exit code 0 |
| P5-V02 | GET /health returns 200 | `curl -s -o /dev/null -w '%{http_code}' http://localhost:8000/health` | `200` |
| P5-V03 | POST /api/ingest rejects unauthenticated | `curl -s -o /dev/null -w '%{http_code}' -X POST http://localhost:8000/api/ingest -H 'Content-Type: application/json' -d '{"type":"text","content":"test"}'` | `401` or `403` |
| P5-V04 | POST /api/ingest accepts valid text | `curl -s -X POST http://localhost:8000/api/ingest -H 'Authorization: Bearer $TOKEN' -H 'Content-Type: application/json' -d '{"type":"text","content":"test note","title":"Test"}'` | Returns `{"status":"ok","path":"raw/..."}`, file exists in raw/ |
| P5-V05 | POST /api/ingest accepts valid URL | `curl -s -X POST ... -d '{"type":"url","content":"https://example.com","title":"Example"}'` | Returns ok, raw/ file contains URL in frontmatter |
| P5-V06 | POST /api/ingest accepts file upload | `curl -s -X POST ... -F 'file=@test.png' -F 'title=Test Image'` | Returns ok, file in raw/assets/, markdown reference in raw/ |
| P5-V07 | Generated raw file has valid frontmatter | `python3 -c "import yaml; yaml.safe_load(open('raw/<generated>.md').read().split('---')[1])"` | Exit code 0, contains: title, type, captured, source, content_hash, status |
| P5-V08 | Docker build succeeds | `docker build -t wiki-ingest-api wiki-ingest-api/` | Exit code 0, image created |
| P5-V09 | Docker compose config validates | `docker compose -f compose/compose.wiki.yml config > /dev/null` | Exit code 0 |
| P5-V10 | Container healthcheck passes | `docker compose -f compose/compose.wiki.yml up -d && sleep 10 && docker inspect --format='{{.State.Health.Status}}' wiki-ingest-api` | `healthy` |
| P5-V11 | wa CLI function works | `source scripts/wa.sh && wa text "test from CLI" "CLI Test"` | Returns raw/ path, file exists |
| P5-V12 | Bookmarklet JS is syntactically valid | `node -e "eval(decodeURIComponent('...'))"` (or manual browser test) | No syntax errors |
| P5-V13 | GitHub Action workflow YAML is valid | `python3 -c "import yaml; yaml.safe_load(open('.github/workflows/ingest-from-issue.yml'))"` | Exit code 0 |
| P5-V14 | ntfy watcher script has correct shebang | `head -1 scripts/ntfy-wiki-watcher.sh` | `#!/usr/bin/env bash` |
| P5-V15 | docs/capture-sources.md covers all 6 channels | `grep -ic 'ios\|android\|bookmarklet\|cli\|github.issue\|ntfy' docs/capture-sources.md` | At least 6 matches |
| P5-V16 | API rejects oversized file (>15MB) | `dd if=/dev/zero of=/tmp/big.bin bs=1M count=20 && curl -s -X POST ... -F 'file=@/tmp/big.bin'` | Returns 413 or error message about file size |
| P5-V17 | API sanitizes malicious filename | Upload file named `../../etc/passwd` | File saved with sanitized name in raw/assets/, not path-traversed |

---

## Phase 6: Seed Content & Ship

> **Goal:** Initialize wiki with index + log, commit everything, push to GitHub.
> **Depends on:** All other phases complete.

### Tasks

| ID | Task | Tier | Status | Notes |
|----|------|------|--------|-------|
| P6-01 | `seed-index` — Create wiki/index.md + wiki/log.md | T1 | ⬜ Pending | index.md: empty catalog with header template. log.md: first entry documenting wiki creation. |
| P6-02 | `push` — Final commit, push to GitHub | T1 | ⬜ Pending | Verify all files committed, no secrets in tree, push to jbl306/labs-wiki. |

### Validation Gate: P6 ✅ (Final Release Gate)

| # | Test | Command / Check | Expected Result |
|---|------|-----------------|-----------------|
| P6-V01 | wiki/index.md exists and has header | `head -5 wiki/index.md` | Contains `# Index` or `# labs-wiki Index` |
| P6-V02 | wiki/log.md exists and has first entry | `cat wiki/log.md` | Contains at least one YAML-formatted log entry with timestamp |
| P6-V03 | No secrets in repo | `grep -rn 'WIKI_API_TOKEN=\|Bearer [a-zA-Z0-9]\{20,\}\|password\s*=' --include='*.md' --include='*.py' --include='*.sh' --include='*.json' --include='*.yml' .` | No real tokens/passwords (only placeholder references like `$TOKEN` or `<token>`) |
| P6-V04 | .env not tracked | `git ls-files .env` | Empty output |
| P6-V05 | Git tree clean | `git status --porcelain` | Empty output |
| P6-V06 | All files committed | `git diff --stat HEAD` | Empty output |
| P6-V07 | Remote is up to date | `git push --dry-run 2>&1` | "Everything up-to-date" or already pushed |
| P6-V08 | Full file count matches expectations | `find . -not -path './.git/*' -type f \| wc -l` | ≥ 35 files (README + LICENSE + AGENTS.md + opencode.json + setup.sh + 4 templates + 4 agents + 6 skills + 1 hook + 1 workflow + 4 scripts + 6 docs + 2 wiki seed + API files + progress.md + plan) |

---

## Cross-Phase Validation (Run After All Phases)

These end-to-end tests verify the system works as an integrated whole.

| # | Test | Description | Expected Result |
|---|------|-------------|-----------------|
| E2E-01 | **Full ingest cycle** | Drop a raw source file in `raw/`, invoke `/wiki-ingest` skill, verify wiki page created in wiki/sources/ with valid frontmatter | Wiki page exists, index.md updated, log.md has entry |
| E2E-02 | **Query finds ingested content** | After E2E-01, invoke `/wiki-query` with a question about the ingested source | Returns answer referencing the wiki page |
| E2E-03 | **Lint detects issues** | Create a page with broken `[[nonexistent-link]]` and missing `sources:` frontmatter, invoke `/wiki-lint` | Reports both issues with actionable output |
| E2E-04 | **Update preserves provenance** | Modify a raw source, invoke `/wiki-update`, verify `source_hash` changed and `last_verified` updated | Frontmatter updated, old hash replaced, log.md entry added |
| E2E-05 | **Setup wizard is idempotent** | Run `/wiki-setup` on already-configured repo | No destructive changes, all existing content preserved |
| E2E-06 | **Orchestrate full pipeline** | Add 3 raw sources, invoke `/wiki-orchestrate` | All 3 ingested, lint passes, index rebuilt, log has 3+ entries |
| E2E-07 | **API → raw/ → wiki pipeline** | POST to ingest API → verify raw/ file → invoke /wiki-ingest → verify wiki page | Complete capture-to-knowledge pipeline works end-to-end |
| E2E-08 | **CLI capture works** | Run `wa url "https://example.com" "Test"` → verify raw/ file created | File exists with correct frontmatter |
| E2E-09 | **Three-tool parity** | Open repo in VS Code, Copilot CLI, and OpenCode — verify skills discoverable in all three | All 6 skills accessible from each tool |
| E2E-10 | **Obsidian compatibility** | Open repo as Obsidian vault → verify `[[wikilinks]]` resolve, graph view shows connections | Links navigate correctly, graph renders |

---

## Progress Summary

| Phase | Total Tasks | ⬜ Pending | 🔄 In Progress | ✅ Done | 🚫 Blocked |
|-------|------------|-----------|----------------|---------|------------|
| P1: Foundation | 7 | 7 | 0 | 0 | 0 |
| P2: Skills & Automation | 7 | 7 | 0 | 0 | 0 |
| P3: Tooling | 4 | 4 | 0 | 0 | 0 |
| P4: Documentation | 5 | 5 | 0 | 0 | 0 |
| P5: Multi-Device Ingestion | 8 | 8 | 0 | 0 | 0 |
| P6: Seed Content & Ship | 2 | 2 | 0 | 0 | 0 |
| **Total** | **33** | **33** | **0** | **0** | **0** |

| Tier | Features | Implemented | Validated |
|------|----------|-------------|-----------|
| T1: Core | 10 | 0 | 0 |
| T2: Enhanced | 8 | 0 | 0 |
| T3: Advanced | 7 | 0 | 0 |
| **Total** | **25** | **0** | **0** |

---

## Execution Notes

- **Parallel execution:** Phases 3, 4, and 5 can all run in parallel with Phase 2 after Phase 1 completes.
- **Minimum viable ship:** Tier 1 features (all in Phase 1-2) + Phase 6 = functional wiki without scripts/docs/multi-device.
- **Validation gates are blocking:** Do not start a dependent phase until its prerequisite gate passes.
- **Test commands are executable:** Copy-paste from this doc into terminal. All use standard tools (grep, python3, curl, docker).
- **Status key:** ⬜ Pending → 🔄 In Progress → ✅ Done → 🚫 Blocked (with reason in Notes).

---

## R1–R19 implementation progress

Tracker mirroring the SQL `recs` table for the full-review remediation work.
All entries start at 🟡 In progress; flip to ✅ Done as each commit lands and
verification passes. Source: `reports/full-review-2026-04-21.md`.

| ID | Recommendation | Owner stream | Status |
|----|---------------|--------------|--------|
| R1 | Semantic dedupe in ingest path | A | 🟡 In progress |
| R2 | One-shot dedupe sweep on existing corpus | A | 🟡 In progress |
| R3 | Replace binary quality rubric | A | 🟡 In progress |
| R4 | Restart synthesis backfill, all communities | A | 🟡 In progress |
| R5 | Demote synthesis-by-checkpoint pattern | A | 🟡 In progress |
| R6 | Graph-tracker triage agent + skill | B | 🟡 In progress |
| R7 | Tier promotion cron | B | 🟡 In progress |
| R8 | Reconcile persona docs | B | 🟡 In progress |
| R9 | `tasks/lessons.md` write hook | B | 🟡 In progress |
| R10 | Update `tasks/progress.md` | B | 🟡 In progress |
| R11 | "Update only" ingest guardrail | A | 🟡 In progress |
| R12 | Ship missing graph-UI filter set | C | 🟡 In progress |
| R13 | Path mode in graph UI | C | 🟡 In progress |
| R14 | NL query endpoint + UI box | C | 🟡 In progress |
| R15 | Cosmograph or server-precomputed layout | C | 🟡 In progress |
| R16 | Expose graph as MCP tools | C | 🟡 In progress |
| R17 | Checkpoint-health graph view | C | 🟡 In progress |
| R18 | End-to-end ingest evaluation harness | A | 🟡 In progress |
| R19 | Wiki growth as a metric (`/graph/health`) | C | 🟡 In progress |
