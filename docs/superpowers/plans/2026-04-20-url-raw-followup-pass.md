# URL Raw Follow-Up Pass Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Improve the first URL raw preservation rollout by fixing the three follow-up items from the pilot report, validating on the flagged LightGBM article plus one non-GeeksforGeeks article, and writing a GitHub Models-aware backfill strategy.

**Architecture:** Keep the changes surgical inside `scripts/auto_ingest.py`. Add a better HTML content-root selection layer, add ranked image selection for generic HTML, and add a manual validation-run mode so refresh-only review passes do not spam `wiki/log.md`. Then run two targeted reruns with quota-safe settings and capture the outcome plus rollout strategy in reports.

**Tech Stack:** Python 3.12, BeautifulSoup4, httpx, GitHub Models API, existing `auto_ingest.py` CLI, Markdown reports.

---

### Task 1: Improve HTML article extraction

**Files:**
- Modify: `scripts/auto_ingest.py`
- Validate: `scripts/auto_ingest.py --help`, `python3 -m py_compile scripts/auto_ingest.py`

- [ ] **Step 1: Add a content-root selection helper for HTML pages**

Create a helper that prefers article-like containers before falling back to the full document. Target selectors should include `article`, `main`, `[role=main]`, `[itemprop=articleBody]`, `.article-body`, `.article-content`, `.entry-content`, `.post-content`, `.content`, and `#content`. Score candidates by text density and paragraph/list/table presence so the GeeksforGeeks `.content` block wins over the whole page.

- [ ] **Step 2: Normalize only the chosen content root**

Update `normalize_html_document()` so it works from the chosen root instead of the entire parsed document. Preserve headings, lists, code blocks, and tables, but strip obvious chrome nodes such as `nav`, `header`, `footer`, `aside`, `form`, and hidden accessibility-only elements.

- [ ] **Step 3: Keep normalization lossless enough for durable raw snapshots**

Do not globally dedupe short lines. Preserve repeated short lines when they come from real content such as lists, table rows, captions, or footnotes.

- [ ] **Step 4: Run baseline validation**

Run:

```bash
/tmp/labs-wiki-followup-venv/bin/python -m py_compile scripts/auto_ingest.py
/tmp/labs-wiki-followup-venv/bin/python scripts/auto_ingest.py --help >/dev/null
```

Expected: both commands succeed with no traceback.

### Task 2: Improve image ranking and add validation-run logging policy

**Files:**
- Modify: `scripts/auto_ingest.py`
- Modify: `README.md`
- Modify: `docs/workflows.md`
- Modify: `AGENTS.md`

- [ ] **Step 1: Replace first-hit image capture with ranked selection**

Keep `og:image`, but score generic `<img>` candidates instead of taking the first non-logo hits. Penalize icons, badges, app-store buttons, tiny assets, and obvious site chrome. Prefer article-local images, large images, `figure` children, and images whose alt text is substantive.

- [ ] **Step 2: Add a manual validation-run mode**

Add a CLI flag for targeted validation reruns, e.g. `--validation-run`, that requires `--force`. It should still update raw snapshots and regenerated pages, but it should suppress normal ingest log spam and notifications so refresh-only review passes do not pollute `wiki/log.md`.

- [ ] **Step 3: Document the policy**

Update the docs so manual validation guidance uses the new validation flag for review-only reruns. Keep the default ingest path unchanged for normal production operation.

- [ ] **Step 4: Run validation for the changed CLI**

Run:

```bash
/tmp/labs-wiki-followup-venv/bin/python scripts/auto_ingest.py --help >/dev/null
```

Expected: help text includes the new validation flag and exits successfully.

### Task 3: Run targeted follow-up validation

**Files:**
- Refresh: `raw/2026-04-08-lightgbm-light-gradient-boosting-machine-geeksforgeeks.md`
- Refresh: `raw/2026-04-20-cloudflare-launches-code-mode-mcp-server-to-optimize-token-u.md`
- Review: matching `wiki/sources/*.md`, `wiki/index.md`

- [ ] **Step 1: Refresh the flagged GeeksforGeeks raw**

Run:

```bash
AUTO_INGEST_MAX_SYNTHESIS_PER_INGEST=0 /tmp/labs-wiki-followup-venv/bin/python scripts/auto_ingest.py raw/2026-04-08-lightgbm-light-gradient-boosting-machine-geeksforgeeks.md --project-root . --force --refresh-fetch --validation-run --token "$TOKEN"
```

Expected: the fetched-content block is replaced once, boilerplate is reduced, and ranked images no longer prefer app-store badges.

- [ ] **Step 2: Refresh one non-GeeksforGeeks article**

Use:

```bash
raw/2026-04-20-cloudflare-launches-code-mode-mcp-server-to-optimize-token-u.md
```

Run the same validation-mode refresh command against that raw file.

- [ ] **Step 3: Inspect raw + source outputs**

Verify:

```bash
rg "fetched-content:(start|end)" raw/2026-04-08-lightgbm-light-gradient-boosting-machine-geeksforgeeks.md raw/2026-04-20-cloudflare-launches-code-mode-mcp-server-to-optimize-token-u.md -n
```

Expected: one start marker and one end marker per raw. Review the top of each raw file and the regenerated source pages to confirm extraction and image ranking improved.

### Task 4: Write the follow-up report and backfill strategy

**Files:**
- Create: `reports/url-raw-followup-pass.md`
- Create: `reports/url-raw-backfill-strategy.md`

- [ ] **Step 1: Write the implementation/validation report**

Capture what changed, how the two validation articles behaved, and whether the three follow-up items are resolved or still partial.

- [ ] **Step 2: Review GitHub Models guidance and write the backfill strategy**

Ground the strategy in current GitHub Models API constraints: rate-limit headers, retry behavior, free-tier pacing, lighter-vs-heavier model choices, and how `AUTO_INGEST_MAX_SYNTHESIS_PER_INGEST` should differ for high-value backfill, synthesis passes, and a full historical backfill.

- [ ] **Step 3: Include three rollout lanes**

The strategy report must include:

1. high-value targeted backfill,
2. synthesis-focused backfill, and
3. full backfill.

Each lane should define scope, pacing, synthesis settings, validation expectations, and when to stop or escalate.

### Task 5: Final verification and branch completion

**Files:**
- Verify changed files in the current worktree only

- [ ] **Step 1: Run final validation**

Run:

```bash
/tmp/labs-wiki-followup-venv/bin/python -m py_compile scripts/auto_ingest.py
/tmp/labs-wiki-followup-venv/bin/python scripts/auto_ingest.py --help >/dev/null
/tmp/labs-wiki-followup-venv/bin/python scripts/lint_wiki.py
docker build -f Dockerfile.auto-ingest -t labs-wiki-auto-ingest-followup-test .
```

Expected: all commands succeed.

- [ ] **Step 2: Commit, push, create PR, and merge**

Use the normal branch-finishing workflow after code review. Clean up the worktree after merge.
