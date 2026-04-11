# MemPalace Next Steps

Post-deployment roadmap extracted from [mempalace-evaluation.md](mempalace-evaluation.md) Phases 2-4.

**Status:** Phase 1-4 complete. All actionable items implemented (2026-04-11). See [implementation report](mempalace-implementation-report.md).

---

## Completed ✅

- [x] Install MemPalace v3.1.0 via pipx
- [x] Initialize palace with identity and config
- [x] Mine labs-wiki (2,208 drawers) and homelab (998 drawers)
- [x] Configure MCP server for Copilot CLI (19 tools, stdio transport)
- [x] Export 49 OpenMemory memories into `openmemory_archive` wing
- [x] Remove OpenMemory from compose, deploy, setup, backup
- [x] Update OpenCode MCP config
- [x] Create bridge script (mempalace-bridge.sh)
- [x] Create docs/12-mempalace-setup.md
- [x] Validate compose config, search, MCP server
- [x] **Mine 50 Copilot CLI sessions** — 3,776 drawers in `copilot_sessions` wing (2026-04-11)
- [x] **Wiki → MemPalace injection** — 158 wiki pages (85 concepts, 52 entities, 21 synthesis) in `labs_wiki_knowledge` wing (2026-04-11)
- [x] **Bootstrap agent wings** — 4 wings (copilot_cli, opencode, code_reviewer, ops) with 12 rooms (2026-04-11)
- [x] **Grafana cleanup** — Removed stale AI & Memory row with qdrant/openmemory panels (2026-04-11)
- [x] **Re-mine cron job** — Weekly Sunday 3am cron via `mempalace-remine.sh` (2026-04-11)
- [x] **Wiki injection script** — `scripts/wiki_to_mempalace.py` for repeatable injection (2026-04-11)

---

## Phase 3: Deepen Integration ✅

### 3.1 Mine Conversation History ✅

**Completed 2026-04-11.** Mined all 50 Copilot CLI sessions (200 files → 3,776 drawers) into `copilot_sessions` wing.

```bash
# Re-mine (handled by weekly cron):
mempalace mine ~/.copilot/session-state --mode convos --wing copilot_sessions
```

> **Note:** OpenCode sessions (`~/.opencode/`) don't contain conversation exports yet — only package metadata. Will be mined when session data accumulates.

### 3.2 Wiki Context Injection (L2 Layer) ✅

**Completed 2026-04-11.** Created `scripts/wiki_to_mempalace.py` — injects 158 wiki pages (concepts + synthesis + entities) into `labs_wiki_knowledge` wing. Included in weekly re-mine cron.

```bash
# Manual run:
/home/jbl/.local/share/pipx/venvs/mempalace/bin/python scripts/wiki_to_mempalace.py
```

### 3.3 Unified Entity Namespace

Ensure entities in labs-wiki and MemPalace KG don't diverge:
- labs-wiki entity pages use `[[Entity Name]]` wikilinks
- MemPalace KG uses subject/object strings
- Create a mapping convention: wiki entity slug ↔ KG entity name

**Priority:** Low — natural naming tends to converge. Only formalize if drift becomes apparent.

---

## Phase 4: Advanced Features

### 4.1 Auto-Save Hooks ✅ (via cron)

**Completed 2026-04-11.** Weekly re-mine cron job replaces per-session hooks:

```bash
# Cron entry (Sunday 3am):
0 3 * * 0 /home/jbl/projects/homelab/scripts/mempalace-remine.sh
```

Mines: homelab, labs-wiki, Copilot CLI sessions, and wiki pages.

> **Note:** `mempalace hook run` only supports `--harness claude-code` and `--harness codex` — no Copilot CLI or OpenCode harness. Cron-based re-mining is the practical alternative until upstream adds support.

### 4.2 Agent-Specific Wings ✅

**Completed 2026-04-11.** Bootstrapped 4 wings with 12 rooms:

| Wing | Purpose |
|------|---------|
| `copilot_cli` | Copilot CLI session decisions, task patterns |
| `opencode` | OpenCode session context, multi-turn debugging |
| `code_reviewer` | Code review patterns, recurring issues |
| `ops` | Infrastructure incidents, runbooks |

Both Copilot CLI and OpenCode connect via MemPalace MCP — diary entries and drawer writes from either client land in the shared palace. Wing names distinguish the source.

### 4.3 Palace Graph Exploration — Deferred

The palace graph connects rooms across wings via shared entities ("tunnels"). Use this for:
- Cross-project knowledge discovery
- Finding unexpected connections between domains
- Surfacing relevant context from unrelated projects

```bash
mempalace traverse homelab/documentation --max-hops 2
mempalace find-tunnels --wing-a homelab --wing-b labs_wiki
```

**Priority:** Low — this is a discovery tool, not a workflow blocker.

### 4.4 AAAK Dialect Evaluation

The AAAK compression format achieves ~30x reduction but benchmarks show 84.2% vs 96.6% R@5 compared to raw mode. The evaluation doc recommends skipping for now.

**Decision:** Skip AAAK unless storage becomes a concern (currently ~50MB for 3,200+ drawers).

### 4.5 Web Viewer

MemPalace has no web UI (unlike OpenMemory's `openmemory-ui`). Options:
1. **Accept CLI-only** — MCP tools and CLI search are sufficient
2. **Build simple viewer** — Static HTML that reads palace status/search results
3. **Integrate with Grafana** — Add palace stats to existing monitoring dashboard

**Priority:** Low — CLI + MCP covers all use cases. Consider if browsing becomes a frequent need.

---

## Cleanup Tasks

### Remove Stale Grafana Panels ✅
**Completed 2026-04-11.** Removed entire "🧠 AI & Memory" row from `config/grafana/dashboards/docker-services.json`. The row targeted `qdrant|openmemory-mcp|openmemory-ui` containers that no longer exist.

### Delete OpenMemory Data (After 30-Day Hold)
After verifying MemPalace works reliably (hold until 2026-05-10):
```bash
# On the server (not dev machine)
rm -rf /opt/homelab/data/qdrant/
rm -rf /opt/homelab/data/openmemory/
rm -rf /opt/homelab/config/openmemory/
```

### Re-mine After Major Changes ✅
**Completed 2026-04-11.** Weekly cron job (`mempalace-remine.sh`) re-mines homelab, labs-wiki, Copilot sessions, and wiki pages every Sunday at 3am.

---

## Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-04-10 | Option A: Native install | ChromaDB works better natively; no Docker overhead |
| 2026-04-10 | Skip AAAK dialect | Raw mode benchmarks 96.6% vs 84.2% R@5 |
| 2026-04-10 | One-way bridge first | MemPalace → labs-wiki is simpler and higher value |
| 2026-04-10 | Exclude credential memory | Grafana admin password not migrated (security) |
| 2026-04-10 | CLI-only (no web UI) | MCP tools + CLI sufficient for single-user palace |
