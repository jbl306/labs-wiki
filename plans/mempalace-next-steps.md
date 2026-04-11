# MemPalace Next Steps

Post-deployment roadmap extracted from [mempalace-evaluation.md](mempalace-evaluation.md) Phases 2-4.

**Status:** Phase 1 (Deploy & Mine) is complete. Phase 2 (Migrate & Retire) is complete.

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

---

## Phase 3: Deepen Integration

### 3.1 Mine Conversation History

Export and mine existing AI conversation sessions for long-term memory.

```bash
# If Claude Code conversations are exported to a directory:
mempalace mine ~/conversations --mode convos
```

**Priority:** Medium — conversations contain decisions, debugging patterns, and architecture choices not captured in code.

### 3.2 Wiki Context Injection (L2 Layer)

Add labs-wiki content to MemPalace's L2 on-demand layer so conversations can pull from compiled wiki knowledge.

**Approach:** Write a script that exports key wiki concepts as MemPalace drawers in a `labs_wiki_knowledge` wing. Run periodically after wiki updates.

```bash
# Concept: wiki pages → mempalace drawers
for page in wiki/concepts/*.md wiki/synthesis/*.md; do
    content=$(cat "$page")
    wing="labs_wiki_knowledge"
    room=$(basename "$page" .md)
    mempalace add-drawer --wing "$wing" --room "$room" --content "$content"
done
```

**Priority:** High — this closes the labs-wiki → MemPalace direction of the bridge.

### 3.3 Unified Entity Namespace

Ensure entities in labs-wiki and MemPalace KG don't diverge:
- labs-wiki entity pages use `[[Entity Name]]` wikilinks
- MemPalace KG uses subject/object strings
- Create a mapping convention: wiki entity slug ↔ KG entity name

**Priority:** Low — natural naming tends to converge. Only formalize if drift becomes apparent.

---

## Phase 4: Advanced Features

### 4.1 Auto-Save Hooks

Configure hooks for Claude Code sessions to auto-save context:

```bash
mempalace hook --setup  # if supported in v3.1.0
```

Hooks:
- **Stop hook:** Every 15 human exchanges → save key topics/decisions
- **PreCompact hook:** Before context compaction → comprehensive save
- **Session-start:** Initialize state tracking

**Priority:** High — this is the main mechanism for MemPalace to capture conversational memory without manual intervention.

### 4.2 Agent-Specific Wings

Create dedicated wings for different AI agent roles:

| Wing | Purpose |
|------|---------|
| `code_reviewer` | Code review patterns, recurring issues |
| `architect` | Architecture decisions, tradeoffs |
| `ops` | Infrastructure incidents, runbooks |
| `debugger` | Debugging sessions, root causes |

Mine role-specific conversations into the appropriate wing.

**Priority:** Medium — useful once conversation mining is active.

### 4.3 Palace Graph Exploration

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

### Remove Stale Grafana Panels
`config/grafana/dashboards/docker-services.json` still references `qdrant`, `openmemory-mcp`, `openmemory-ui` containers. These panels will show empty data. Either:
- Remove the memory section from the dashboard
- Replace with MemPalace stats (palace size, drawer count) if exposable

### Delete OpenMemory Data (After 30-Day Hold)
After verifying MemPalace works reliably:
```bash
# On the server (not dev machine)
rm -rf /opt/homelab/data/qdrant/
rm -rf /opt/homelab/data/openmemory/
rm -rf /opt/homelab/config/openmemory/
```

### Re-mine After Major Changes
Set a cadence to re-mine projects after significant changes:
```bash
mempalace mine ~/projects/homelab
mempalace mine ~/projects/labs-wiki
```

Consider a cron job or post-commit hook for automated re-mining.

---

## Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-04-10 | Option A: Native install | ChromaDB works better natively; no Docker overhead |
| 2026-04-10 | Skip AAAK dialect | Raw mode benchmarks 96.6% vs 84.2% R@5 |
| 2026-04-10 | One-way bridge first | MemPalace → labs-wiki is simpler and higher value |
| 2026-04-10 | Exclude credential memory | Grafana admin password not migrated (security) |
| 2026-04-10 | CLI-only (no web UI) | MCP tools + CLI sufficient for single-user palace |
