# Knowledge Base Retrieval — Canonical Snippet

> This snippet is injected verbatim into every project's `AGENTS.md` by
> `labs-wiki/setup.sh --inject-snippet`. Do NOT edit the embedded copies —
> edit this file and re-run setup to propagate.

<!-- LABS-WIKI-SNIPPET-START -->
## Knowledge Base (labs-wiki + MemPalace)

Before answering domain questions, walk this retrieval ladder **cheapest first**:

1. **`~/projects/labs-wiki/wiki/hot.md`** — always-fresh recent-context cache (~600 tokens). Regenerated on every mine by the `mempalace-watcher` service. Read it first.
2. **`mempalace_search(query=<topic>, wing=<project_wing>)`** — local vector search, <100ms, no API key. Wings: `homelab`, `labs_wiki`, `labs_wiki_knowledge`, `nba_ml_engine`, `copilot_sessions`, `copilot_cli`, `opencode`, `code_reviewer`, `ops`.
3. **`wiki_search` / `wiki_read` MCP tools** — structured search over `labs-wiki/wiki/` and direct page reads. Use when a page is likely to exist.
4. **Web fetch** — only when the wiki genuinely doesn't cover it.

At session end, capture durable findings with `/wiki-save`. The watcher auto-mines within 60 seconds.

Do NOT read the wiki for unrelated generic coding questions.
<!-- LABS-WIKI-SNIPPET-END -->
