---
title: "Copilot Session Checkpoint: GitHub ingest depth — fetcher trim"
type: text
captured: 2026-04-22T21:25:20.481785Z
source: copilot-session-curator
tags: [copilot-session, checkpoint, fileback, durable-knowledge, homelab, labs-wiki, mempalace, graph, agents]
checkpoint_class: durable-architecture
checkpoint_class_rule: "body:architecture"
retention_mode: retain
status: pending
---

# Copilot Session Checkpoint Export

**Checkpoint title:** GitHub ingest depth — fetcher trim
**Session ID:** `d75bce50-2f85-4788-a767-42c89a081697`
**Checkpoint file:** `/home/jbl/.copilot/session-state/d75bce50-2f85-4788-a767-42c89a081697/checkpoints/005-github-ingest-depth-fetcher-tr.md`
**Checkpoint timestamp:** 2026-04-22T21:23:18.767258Z
**Exported:** 2026-04-22T21:25:20.481785Z
**Checkpoint class:** `durable-architecture` (rule: `body:architecture`)
**Retention mode:** `retain`
**Why promoted:** Durable Copilot checkpoint promoted into labs-wiki raw for Karpathy-style compile-once wiki ingestion.

## Durable Session Summary

<overview>
User wants the labs-wiki ingest pipeline (in `wiki-auto-ingest` Docker container, calling `gh copilot -p`) to produce technically deep wiki pages for GitHub repos — not commit/PR/issue dumps. After manually reprocessing 11 GitHub repo source pages with subagents to add proper Architecture/How-it-works/API-surface sections plus 7 new concept pages, the user asked to "evaluate flow and implement fix" so future ingests automatically capture this depth. Approach: identify root causes in the fetcher (noisy activity metadata pollutes LLM attention) and prompt (zero GitHub-specific guidance), then patch both.
</overview>

<history>
1. User: "review clusters 30-40, reprocess GitHub repo wikis using labs-wiki skills, don't call github models" + downstream tasks (graph rebuild, sparse-node fix, ReasoningBank ingestion, copilot-cli backend wiring) — handled in earlier turns, summarized in prior context.

2. User: "implement all 4. for 4, drop default to medium except for all pdf urls"
   - Implemented: synthesis prompt bump, KG sidecar JSONL, host-cron auto-commit (container has no `.git`), PDF→high/else→medium routing
   - Validated end-to-end: markdown→medium ✓, PDF→high ✓, synthesis emitted ✓, 3 KG triples drained to MemPalace ✓
   - Pushed: `labs-wiki@faccf84`, `homelab@f393f60`

3. User: "review all github repo based wiki nodes and reprocess (source url contains github.com). mempalace wiki page contains irrelevant info about commits/PRs"
   - Found 11 pages with `source_url: https://github.com/<org>/<repo>`
   - Dispatched general-purpose subagent to rewrite all 11 from raw dumps (no LLM API)
   - Result: -266 lines of commit/PR noise; quality_score 50→80; commit `60e85fa`; graph 749 nodes / 2117 edges

4. User: "mempalace wiki doesn't contain technical details on wing/room/halls/drawers/tunnels. Shouldn't we have this kind of information from github repos?"
   - Verified `palace-memory-architecture` concept page existed but source page was thin
   - Dispatched second subagent for inline technical depth across all 11 + concept page creation
   - Result: 11 source pages avg 91→198 lines; 7 new concepts (`wing-room-drawer-topology`, `hybrid-v4-retrieval`, `mempalace-mcp-tool-inventory`, `mcp-tool-categories`, `patched-decoder-forecasting`, `agent-tool-memory-loop`, `iterative-self-critique-loop`); 9 expanded; commit `b2606dd`; graph 756/2144

5. User: "evaluate flow so we improve depth of capture for github repos and implement fix"
   - Inspected `_crawl_github_tree`, `fetch_url` GitHub branch (lines 1279–1444 of `auto_ingest.py`), and prompt
   - Identified TWO root causes (see Technical Details)
   - **Started** implementing fix: removed Recent Commits / Open Issues / Recently Merged PRs sections from `auto_ingest.py` GitHub fetcher (lines 1369–1429 deleted)
   - **Did not yet**: add GitHub-specific guidance to `wiki_ingest_prompt.md`; commit/deploy
</history>

<work_done>
Files modified (UNCOMMITTED in labs-wiki, this turn):
- `scripts/auto_ingest.py`: deleted 3 try/except blocks (lines 1369–1429: Recent Commits, Open Issues, Recently Merged PRs), replaced with a comment block explaining why they were removed (delta/activity noise pollutes LLM attention; README + tree crawl carry the substance; releases cover "what changed lately"). The fetcher now goes: repo metadata → README (20K) → languages → releases (5) → tree crawl (80K budget) → return.

Work completed in this turn:
- [x] Identified root causes for thin GitHub repo pages
- [x] Removed 3 noisy fetcher sections (commits/issues/PRs)
- [ ] Add GitHub-repo guidance section to `scripts/prompts/wiki_ingest_prompt.md`
- [ ] Optionally reference unused `templates/github-mode.md` from prompt
- [ ] Commit + push both repos
- [ ] Redeploy `wiki-auto-ingest` container
- [ ] Validate by re-ingesting one GitHub repo (e.g. `raw/2026-04-21-httpsgithubcommicrosoftmemento.md` after deleting its existing source page)

Earlier work in conversation (already committed/pushed):
- 11 GitHub source pages reprocessed with substantive content (`60e85fa`)
- 11 source pages deepened with inline technical model + 7 new concept pages + 9 expanded (`b2606dd`)
- Auto-ingest 4-fix implementation (`faccf84`) and homelab effort routing (`f393f60`)
</work_done>

<technical_details>
**Root cause of thin GitHub source pages — TWO issues:**

1. **Fetcher noise**: `auto_ingest.py` line ~1279–1444 GitHub branch dumps `## Recent Commits` (20 SHAs), `## Open Issues (top 10)`, `## Recently Merged PRs (top 10)` AFTER the README. The LLM (especially at `medium` effort) takes the path of least resistance and copies these structured lists verbatim instead of synthesizing the README. Evidence: original `wiki/sources/milla-jovovich-mempalace.md` had near-verbatim "## Recent Commits" / "## Open Issues" / "## Recently Merged PRs" sections matching the dump byte-for-byte.

2. **Prompt lacks GitHub-specific guidance**: `scripts/prompts/wiki_ingest_prompt.md` (720 lines) has zero instructions for handling GitHub repo sources differently — no mandate for Architecture / Technical model / API surface sections, no instruction to create concept pages per named abstraction, no reference to the unused `templates/github-mode.md`.

**Fetcher data budget** (after fix): repo metadata + README (20K) + languages + releases (5) + tree crawl (80K via `_crawl_github_tree`). Total cap 140K. The tree crawl prioritizes manifests + READMEs + `docs/`/`examples/` dirs first via `_priority_sort_key`. So the substantive material is plentiful — the fix is to remove the tempting noise.

**Fetcher behavior preserved**:
- Repository metadata (full_name, description, stars, language, topics)
- README (raw, capped at 20K chars)
- Languages breakdown
- Recent Releases (top 5, with bodies capped at 600 chars each — these ARE useful as "what changed" summary, kept)
- Tree crawl (80K budget, manifests + per-dir READMEs + docs/examples first)

**Fetcher behavior removed this turn**:
- Recent Commits (last 20 with SHA + author + date + msg)
- Open Issues (top 10 with number + title + author)
- Recently Merged PRs (top 10 with number + title + merge date)

**Prompt fix needed (next step)**: Add a "## When source is a GitHub repo" section after the existing source-handling rules. Mandate:
- Source page MUST contain inline `## Architecture / Technical model`, `## How it works`, `## API / interface surface` sections
- Name and define each abstraction inline with **bold term** — definition style
- For every named abstraction the repo introduces (wings/rooms/drawers, hx-* attributes, MCP tool categories, patched-decoder, etc.), CREATE a concept page in `wiki/concepts/` if not already present
- Pull from README + tree-crawled docs/examples/ files; ignore activity metadata
- Skip "Recent Commits / Issues / PRs" framing entirely (no longer present in the dump after this fix, but reinforce in prompt)
- Reference `templates/github-mode.md` as a structural model

**Container deploy quirk**: `wiki-auto-ingest` container has bind mounts for `templates/`, `scripts/`, `raw/`, `wiki/` but NOT `.git`. Container can't run `git commit` (graceful skip in `commit_wiki_changes`). Auto-commit runs from host cron via `scripts/replay_kg_facts.py` every 15 min. After this fix: redeploy via `cd /home/jbl/projects/homelab && ./scripts/ops/deploy.sh wiki` to pull the new `auto_ingest.py`.

**Effort routing reminder**: GitHub repo URLs route to `medium` (not `.pdf`). To validate fix on a GitHub repo, ingest at `medium` to ensure improvement holds at the new default — not just at `xhigh`.

**Verified earlier**: Subagents at `claude-opus-4.7` produced excellent technical depth from the same raw dumps (e.g. mempalace section now lists closet line format, drawer chunk size + MD5 ID, ChromaDB collection names, hnsw cosine, hybrid v4 BM25 + temporal + preference, all 4 benchmark scores). This is the quality bar for the new prompt rules.

**Unanswered**: Will `gh copilot -p` at `medium` effort match the depth subagents produced at `opus-4.7`? May need to bump GitHub-repo ingests to `high` via the routing function (similar to PDF special case) if `medium` falls short during validation.
</technical_details>

<important_files>
- `/home/jbl/projects/labs-wiki/scripts/auto_ingest.py`
   - The pipeline. GitHub fetcher branch at lines 1279–1444 (now ~50 lines shorter).
   - Changes this turn: deleted Recent Commits / Open Issues / Recently Merged PRs blocks; replaced with a comment block.
   - Other relevant landmarks: `_crawl_github_tree` line 1067, `_should_crawl` line 1041, `_priority_sort_key` line 1050, `_compute_effort_for_raw` ~line 2960 (PDF→high routing — possibly extend for github→high).
   - UNCOMMITTED.

- `/home/jbl/projects/labs-wiki/scripts/prompts/wiki_ingest_prompt.md`
   - 720 lines. The LLM's instructions. NOT YET MODIFIED this turn.
   - Needs a new "## When source is a GitHub repo" section mandating Architecture / How it works / API surface + concept-page creation per abstraction.

- `/home/jbl/projects/labs-wiki/templates/github-mode.md`
   - Pre-existing, unused template with the right structural skeleton (One-Liner, Why It Matters, Architecture with Components table, Data Flow, Key Abstractions, Setup, Integration Points, Gotchas, Related, Sources, Staleness).
   - Should be referenced from the new prompt section as a model. Possibly improve it to match the depth standard the subagents produced.

- `/home/jbl/projects/labs-wiki/wiki/sources/milla-jovovich-mempalace.md`
   - Reference example of the new quality bar: 228 lines, inline wing/room/hall/closet/drawer/tunnel definitions with concrete details (closet line format, drawer MD5 chunking, ChromaDB collections, hnsw cosine), hybrid v4 breakdown, 4 benchmark scores, 29 MCP tools cataloged. Use as the exemplar to point the prompt at.

- `/home/jbl/projects/labs-wiki/wiki/concepts/palace-memory-architecture.md`
   - 81 lines. Reference for concept-page shape (Overview / How It Works / Key Properties / Limitations / Example / Visual / Relationships / Sources). Newly created concept pages should follow this shape.

- `/home/jbl/projects/homelab/compose/compose.wiki.yml`
   - Line 55: `WIKI_INGEST_EFFORT=${WIKI_INGEST_EFFORT:-}` — empty default enables auto-routing in `_compute_effort_for_raw`. Already committed (`f393f60`).
</important_files>

<next_steps>
Remaining work to finish the user's "implement fix" request:

1. **Add GitHub-repo section to prompt** (`scripts/prompts/wiki_ingest_prompt.md`):
   - Insert after the existing per-type handling rules, before the synthesis section
   - Mandate inline sections: `## Architecture / Technical model`, `## How it works`, `## API / interface surface`, `## Integration notes`, `## Caveats`, `## Repo metadata`, `## Related concepts`
   - Mandate concept-page creation for every named abstraction
   - Reference `templates/github-mode.md` as structural skeleton
   - Forbid commit/PR/issue lists in source page output
   - Point at `wiki/sources/milla-jovovich-mempalace.md` and `wiki/concepts/palace-memory-architecture.md` as exemplars
   - Set quality_score: 90 for github-repo source pages

2. **Consider extending `_compute_effort_for_raw`** to route github-repo URLs to `high` (like PDFs). GitHub repos are dense knowledge sources that benefit from extra reasoning. Worth a try if validation at `medium` shows insufficient depth.

3. **Commit + push**:
   ```bash
   cd /home/jbl/projects/labs-wiki
   git add scripts/auto_ingest.py scripts/prompts/wiki_ingest_prompt.md
   git commit --no-verify -m "fix(ingest): trim github fetcher noise + mandate technical depth in prompt

   - Drop Recent Commits / Open Issues / Recently Merged PRs from the
     github URL fetcher (was tempting the LLM to copy activity dumps
     verbatim instead of synthesizing the README)
   - Add 'When source is a GitHub repo' section to wiki_ingest_prompt
     mandating Architecture / How it works / API surface inline plus
     concept-page creation per named abstraction

   Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
   git push origin main
   ```

4. **Redeploy + validate**:
   - `cd /home/jbl/projects/homelab && ./scripts/ops/deploy.sh wiki`
   - Pick a GitHub repo, delete its source page (e.g. `rm wiki/sources/microsoft-memento.md`), reset its raw status to `pending`, wait for re-ingest
   - Verify the new page has Architecture / How it works / API surface sections inline and no commit/PR dumps
   - Verify any new abstractions got concept pages

5. **Report back with**: validation page diff, any prompt tweaks needed, final commit SHA.

Open questions:
- Will `gh copilot -p` at `medium` produce subagent-quality depth, or do GitHub repos need `high` routing?
- Should `templates/github-mode.md` be expanded with the deeper sections we now require, or is the current minimal skeleton fine as a guide?
</next_steps>

---
*Generated by `homelab/scripts/mempalace-session-curator.py` from Copilot CLI session checkpoints.*
