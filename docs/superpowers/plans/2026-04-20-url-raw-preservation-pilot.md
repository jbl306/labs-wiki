# URL Raw Preservation Pilot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Persist fetched URL article content into `raw/`, add a safe targeted re-ingest path, and run a 3-page pilot that proves whether richer durable source bodies improve wiki fidelity.

**Architecture:** Extend `scripts/auto_ingest.py` in three places: normalize live URL fetches into a richer text form, upsert that normalized body into a deterministic fetched-content block inside each URL raw file, and let forced manual re-ingest reuse that durable body while bypassing the normal status/hash gates for pilot files. Keep checkpoint behavior unchanged, disable synthesis during the pilot to save quota, and capture the before/after evaluation in `reports/url-raw-preservation-pilot.md`.

**Tech Stack:** Python 3.12, `httpx`, `openai`, `watchdog`, `pyyaml`, `rapidfuzz`, `beautifulsoup4`, markdown docs, generated wiki pages

---

## File Structure

- `scripts/auto_ingest.py` — add richer HTML normalization, fetched-content block read/write helpers, persisted-content fallback, and `--force` re-ingest support.
- `scripts/requirements-auto-ingest.txt` — add `beautifulsoup4` for structure-aware HTML parsing without inventing a custom parser.
- `README.md` — document that URL sources now persist fetched content into `raw/` and show the targeted `--force` re-ingest command.
- `docs/workflows.md` — document the manual pilot/backfill workflow with `AUTO_INGEST_MAX_SYNTHESIS_PER_INGEST=0`.
- `AGENTS.md` — relax the raw-layer immutability rule to allow the deterministic fetched-content block for URL sources.
- `.github/instructions/raw-sources.instructions.md` — mirror the same raw-source exception so agent guidance stays consistent.
- `reports/url-raw-preservation-pilot.md` — record pilot targets, raw-preservation checks, wiki-depth changes, and rollout recommendation.
- `raw/2026-04-20-agents-that-remember-introducing-agent-memory.md` — text-heavy pilot raw file.
- `raw/2026-04-08-lightgbm-light-gradient-boosting-machine-geeksforgeeks.md` — table/tutorial-heavy pilot raw file.
- `raw/2026-04-16-251004618v3pdf.md` — figure/equation-heavy pilot raw file via arXiv HTML rewrite.
- `wiki/sources/agents-that-remember-introducing-agent-memory.md` — generated source page to compare before/after for the text-heavy pilot.
- `wiki/sources/lightgbm-light-gradient-boosting-machine-geeksforgeeks.md` — generated source page to compare before/after for the table/tutorial-heavy pilot.
- `wiki/sources/agentic-context-engineering-evolving-contexts-for-self-improving-language-models.md` — generated source page to compare before/after for the paper/figure-heavy pilot.

### Task 1: Create the isolated worktree and capture the pilot baseline

**Files:**
- Create: `/home/jbl/projects/labs-wiki/.worktrees/url-raw-preservation-pilot/` (Git worktree)
- Review: `raw/2026-04-20-agents-that-remember-introducing-agent-memory.md`
- Review: `raw/2026-04-08-lightgbm-light-gradient-boosting-machine-geeksforgeeks.md`
- Review: `raw/2026-04-16-251004618v3pdf.md`
- Review: `wiki/sources/agents-that-remember-introducing-agent-memory.md`
- Review: `wiki/sources/lightgbm-light-gradient-boosting-machine-geeksforgeeks.md`
- Review: `wiki/sources/agentic-context-engineering-evolving-contexts-for-self-improving-language-models.md`

- [ ] **Step 1: Create the feature worktree**

```bash
cd /home/jbl/projects/labs-wiki
git fetch origin --prune
git worktree add .worktrees/url-raw-preservation-pilot -b feature/url-raw-preservation-pilot origin/main
cd .worktrees/url-raw-preservation-pilot
git status --short --branch
```

Expected: a clean `feature/url-raw-preservation-pilot` worktree based on `origin/main`.

- [ ] **Step 2: Confirm the pilot raw files are still URL stubs**

```bash
cd /home/jbl/projects/labs-wiki/.worktrees/url-raw-preservation-pilot
sed -n '1,40p' raw/2026-04-20-agents-that-remember-introducing-agent-memory.md
sed -n '1,40p' raw/2026-04-08-lightgbm-light-gradient-boosting-machine-geeksforgeeks.md
sed -n '1,40p' raw/2026-04-16-251004618v3pdf.md
```

Expected: each file shows frontmatter plus a bare URL body, with no fetched-content block yet.

- [ ] **Step 3: Capture the baseline source-page excerpts for later comparison**

```bash
cd /home/jbl/projects/labs-wiki/.worktrees/url-raw-preservation-pilot
sed -n '1,90p' wiki/sources/agents-that-remember-introducing-agent-memory.md
sed -n '1,90p' wiki/sources/lightgbm-light-gradient-boosting-machine-geeksforgeeks.md
sed -n '1,90p' wiki/sources/agentic-context-engineering-evolving-contexts-for-self-improving-language-models.md
```

Expected: source pages render correctly and give you the before-state for the final report.

- [ ] **Step 4: Commit the worktree setup only if Git created helper metadata you want to keep**

```bash
cd /home/jbl/projects/labs-wiki/.worktrees/url-raw-preservation-pilot
git status --short
```

Expected: no tracked file changes yet; do not create a commit here unless something unexpected was generated.

### Task 2: Add richer URL normalization and deterministic fetched-content block helpers

**Files:**
- Modify: `scripts/requirements-auto-ingest.txt`
- Modify: `scripts/auto_ingest.py`

- [ ] **Step 1: Add BeautifulSoup to the auto-ingest dependency set**

```text
openai>=1.30.0
watchdog>=4.0.0
httpx>=0.27.0
pyyaml>=6.0.0
rapidfuzz>=3.0.0
beautifulsoup4>=4.12.0
```

- [ ] **Step 2: Install the updated auto-ingest dependencies in the worktree environment**

```bash
cd /home/jbl/projects/labs-wiki/.worktrees/url-raw-preservation-pilot
pip install -r scripts/requirements-auto-ingest.txt
```

Expected: `beautifulsoup4` installs cleanly alongside the existing ingest dependencies.

- [ ] **Step 3: Add the fetched-content constants, dataclass, and raw-block helpers near the URL fetch section**

```python
import html
from dataclasses import dataclass
from bs4 import BeautifulSoup

FETCHED_BLOCK_START = "<!-- fetched-content:start -->"
FETCHED_BLOCK_END = "<!-- fetched-content:end -->"


@dataclass
class UrlFetchResult:
    text: str
    image_urls: list[str]
    resolved_url: str | None
    content_type: str | None


def strip_fetched_content_block(body: str) -> str:
    pattern = re.compile(
        rf"\n?{re.escape(FETCHED_BLOCK_START)}.*?{re.escape(FETCHED_BLOCK_END)}\n?",
        flags=re.S,
    )
    cleaned = re.sub(pattern, "\n", body).strip()
    return cleaned + "\n" if cleaned else ""


def read_persisted_fetched_content(body: str) -> tuple[str | None, dict[str, str]]:
    pattern = re.compile(
        rf"{re.escape(FETCHED_BLOCK_START)}\n(.*?)\n{re.escape(FETCHED_BLOCK_END)}",
        flags=re.S,
    )
    match = pattern.search(body)
    if not match:
        return None, {}
    block = match.group(1)
    metadata: dict[str, str] = {}
    text_lines: list[str] = []
    in_text = False
    for line in block.splitlines():
        if line.strip() == "## Fetched Content":
            in_text = True
            continue
        if not in_text and line.startswith("- "):
            key, _, value = line[2:].partition(":")
            metadata[key.strip()] = value.strip()
        elif in_text:
            text_lines.append(line)
    text = "\n".join(text_lines).strip()
    return (text or None), metadata


def build_fetched_content_block(
    *,
    fetched_at: str,
    source_url: str,
    resolved_url: str | None,
    content_type: str | None,
    text: str,
) -> str:
    meta_lines = [
        FETCHED_BLOCK_START,
        "## Fetched Metadata",
        f"- fetched_at: {fetched_at}",
        f"- source_url: {source_url}",
        f"- resolved_url: {resolved_url or source_url}",
        f"- content_type: {content_type or 'unknown'}",
        "",
        "## Fetched Content",
        text.strip(),
        FETCHED_BLOCK_END,
    ]
    return "\n".join(meta_lines).rstrip() + "\n"


def upsert_fetched_content_block(raw_text: str, block: str) -> str:
    pattern = re.compile(
        rf"\n?{re.escape(FETCHED_BLOCK_START)}.*?{re.escape(FETCHED_BLOCK_END)}\n?",
        flags=re.S,
    )
    if pattern.search(raw_text):
        updated = re.sub(pattern, "\n" + block, raw_text).rstrip() + "\n"
    else:
        updated = raw_text.rstrip() + "\n\n" + block
    return updated
```

- [ ] **Step 4: Replace the lossy HTML stripping logic with structure-aware normalization**

```python
def extract_image_urls(raw_html: str, page_url: str) -> list[str]:
    image_urls: list[str] = []
    og_match = re.search(
        r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']',
        raw_html,
        flags=re.I,
    )
    if og_match:
        image_urls.append(og_match.group(1))

    skip_img_patterns = re.compile(r"logo|icon|favicon|badge|avatar|sprite|\.svg", re.I)
    for img_src in re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', raw_html, flags=re.I):
        if img_src.startswith("data:") or skip_img_patterns.search(img_src):
            continue
        if img_src not in image_urls:
            image_urls.append(img_src)
        if len(image_urls) >= MAX_IMAGES:
            break

    if not page_url.endswith("/"):
        page_url += "/"
    return [
        urljoin(page_url, img) if not img.startswith(("http://", "https://")) else img
        for img in image_urls[:MAX_IMAGES]
    ]


def is_meaningful_fetched_body(text: str, source_url: str | None) -> bool:
    cleaned = text.strip()
    if len(cleaned) < 200:
        return False
    if source_url and cleaned == source_url.strip():
        return False
    if cleaned.startswith("[PDF document at ") and "content could not be extracted" in cleaned:
        return False
    return True


def _serialize_html_table(table) -> str:
    rows: list[list[str]] = []
    for tr in table.find_all("tr"):
        cells = [cell.get_text(" ", strip=True) for cell in tr.find_all(["th", "td"])]
        if cells:
            rows.append(cells)
    if not rows:
        return ""
    header = rows[0]
    divider = ["---"] * len(header)
    body_rows = rows[1:]
    markdown_rows = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(divider) + " |",
    ]
    markdown_rows.extend("| " + " | ".join(row) + " |" for row in body_rows)
    return "\n".join(markdown_rows)


def normalize_html_document(raw_html: str) -> str:
    soup = BeautifulSoup(raw_html, "html.parser")
    for node in soup(["script", "style", "noscript", "nav", "header", "footer", "aside", "form"]):
        node.decompose()
    for node in soup.select("[aria-hidden='true'], .visually-hidden, .sr-only"):
        node.decompose()

    for table in soup.find_all("table"):
        table_md = _serialize_html_table(table)
        if table_md:
            table.replace_with("\n" + table_md + "\n")

    for tag_name in ("h1", "h2", "h3", "h4", "h5", "h6"):
        for tag in soup.find_all(tag_name):
            level = int(tag_name[1])
            tag.replace_with("\n" + ("#" * level) + " " + tag.get_text(" ", strip=True) + "\n")

    for pre in soup.find_all("pre"):
        pre.replace_with("\n```\n" + pre.get_text("\n", strip=False).strip() + "\n```\n")

    for code in soup.find_all("code"):
        if code.parent.name != "pre":
            code.replace_with("`" + code.get_text(" ", strip=True) + "`")

    for li in soup.find_all("li"):
        li.replace_with("\n- " + li.get_text(" ", strip=True))

    text = soup.get_text("\n")
    text = html.unescape(text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    lines: list[str] = []
    seen_short_lines: set[str] = set()
    for line in text.splitlines():
        cleaned = line.strip()
        if not cleaned:
            continue
        if len(cleaned.split()) <= 6:
            if cleaned in seen_short_lines:
                continue
            seen_short_lines.add(cleaned)
        lines.append(cleaned)
    return "\n".join(lines).strip()[:50_000]
```

- [ ] **Step 5: Update `fetch_url_content()` to return the richer fetch payload**

Keep the existing branch-detection logic in `fetch_url_content()`. Change only the function signature and each branch's return value so the current handlers keep working but all of them return `UrlFetchResult`.

```python
def fetch_url_content(url: str) -> UrlFetchResult:
    """Fetch text content from a URL and return normalized text plus metadata."""
```

Use these exact return shapes in the existing branches:

```python
# Twitter / X branch
return UrlFetchResult(
    text="\n".join(parts),
    image_urls=image_urls,
    resolved_url=url,
    content_type="application/json",
)

# GitHub repository branch
return UrlFetchResult(
    text="\n\n".join(repo_parts),
    image_urls=[],
    resolved_url=url,
    content_type="application/vnd.github+json",
)

# GitHub gist branch
return UrlFetchResult(
    text=resp.text,
    image_urls=[],
    resolved_url=str(resp.url),
    content_type=resp.headers.get("content-type"),
)

# Generic HTML branch
return UrlFetchResult(
    text=normalize_html_document(raw_html),
    image_urls=extract_image_urls(raw_html, str(resp.url)),
    resolved_url=str(resp.url),
    content_type=content_type,
)

# Generic plain-text branch
return UrlFetchResult(
    text=resp.text[:50_000],
    image_urls=[],
    resolved_url=str(resp.url),
    content_type=content_type,
)

# Failure / fallback branches must also return UrlFetchResult, not tuples:
return UrlFetchResult(text="", image_urls=[], resolved_url=url, content_type=None)
```

- [ ] **Step 6: Run a syntax check before wiring the ingest flow**

```bash
cd /home/jbl/projects/labs-wiki/.worktrees/url-raw-preservation-pilot
python3 -m py_compile scripts/auto_ingest.py
```

Expected: no syntax errors.

- [ ] **Step 7: Do not commit yet; the call site still expects the old tuple contract until Task 3 lands**

```bash
cd /home/jbl/projects/labs-wiki/.worktrees/url-raw-preservation-pilot
git diff -- scripts/requirements-auto-ingest.txt scripts/auto_ingest.py | cat
```

Expected: only the helper-layer changes are pending; keep them uncommitted until Task 3 updates `ingest_raw_source()`.

### Task 3: Wire durable raw persistence, persisted fallback, and explicit re-ingest controls

**Files:**
- Modify: `scripts/auto_ingest.py`

- [ ] **Step 1: Extend `ingest_raw_source()` so forced runs bypass the status guard**

```python
def ingest_raw_source(
    raw_path: Path,
    project_root: Path,
    token: str,
    model: str | None = None,
    *,
    force: bool = False,
    refresh_fetch: bool = False,
) -> bool:
    log.info("Processing: %s", raw_path)
    fm, body = parse_frontmatter(raw_path)
    if not fm:
        log.error("No frontmatter found in %s", raw_path)
        return False
    status = fm.get("status", "pending")
    if status != "pending" and not force:
        log.info("Skipping %s (status: %s)", raw_path.name, status)
        return False
```

- [ ] **Step 2: Replace the existing `# For URL sources, fetch the actual content` block with durable raw-first logic**

```python
    source_body = strip_fetched_content_block(body)
    manual_notes = source_body.strip()
    if source_type == "url" and source_url and manual_notes == source_url:
        manual_notes = ""
    persisted_text, _persisted_meta = read_persisted_fetched_content(body)
    content_parts = [part for part in (persisted_text, manual_notes) if part]
    content = "\n\n".join(content_parts) if content_parts else source_body
    image_urls: list[str] = []

    if source_type == "url" and source_url and (refresh_fetch or not persisted_text):
        fetch = fetch_url_content(source_url)
        normalized_fetch = fetch.text.strip()
        if not is_meaningful_fetched_body(normalized_fetch, source_url):
            raise RuntimeError(
                f"Fetched body too thin to persist for {raw_path.name}; "
                "leave the raw body unchanged and let the existing failed-status path report it."
            )

        updated_raw = upsert_fetched_content_block(
            raw_path.read_text(),
            build_fetched_content_block(
                fetched_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
                source_url=source_url,
                resolved_url=fetch.resolved_url,
                content_type=fetch.content_type,
                text=normalized_fetch,
            ),
        )
        raw_path.write_text(updated_raw)
        content = normalized_fetch
        image_urls = fetch.image_urls
    elif source_type == "url" and persisted_text:
        log.info("Using persisted fetched-content block for %s", raw_path.name)
        content = "\n\n".join(part for part in (persisted_text, manual_notes) if part)
```

- [ ] **Step 3: Make the hash short-circuit skip only on non-forced runs**

```python
    source_hash = compute_sha256(content)
    wiki_dir = project_root / "wiki"

    if not force and check_already_processed(wiki_dir, source_hash):
        log.info("Already processed, updating status only")
        update_raw_status(raw_path, "ingested")
        return True
```

- [ ] **Step 4: Add the CLI flags and pass them through `main()` without breaking batch mode**

```python
parser.add_argument(
    "--force",
    action="store_true",
    help="Reprocess a specific raw file even if status/source_hash already mark it as ingested",
)
parser.add_argument(
    "--refresh-fetch",
    action="store_true",
    help="Re-fetch a URL source and replace its fetched-content block instead of using the persisted block",
)
args = parser.parse_args()
project_root = Path(args.project_root).resolve()

if args.raw_file:
    raw_file = Path(args.raw_file)
    if not raw_file.is_absolute():
        raw_file = project_root / raw_file
    try:
        ok = ingest_raw_source(
            raw_file,
            project_root,
            args.token,
            args.model,
            force=args.force,
            refresh_fetch=args.refresh_fetch,
        )
    except Exception:
        log.exception("Failed to process %s", raw_file.name)
        update_raw_status(raw_file, "failed")
        send_ntfy(
            f"❌ Wiki ingest failed: {raw_file.name}",
            f"Error processing {raw_file.name}. Check logs.",
            tags="warning",
        )
        raise SystemExit(1)
    raise SystemExit(0 if ok else 1)
```

- [ ] **Step 5: Run targeted validation on the new force path without touching the pilot files yet**

```bash
cd /home/jbl/projects/labs-wiki/.worktrees/url-raw-preservation-pilot
python3 -m py_compile scripts/auto_ingest.py
python3 scripts/auto_ingest.py --help | sed -n '1,80p'
docker build -f Dockerfile.auto-ingest -t labs-wiki-auto-ingest-test .
```

Expected: both `--force` and `--refresh-fetch` appear in help output, `auto_ingest.py` still compiles cleanly, and the Docker image still builds with the new dependency set.

- [ ] **Step 6: Commit the ingest-flow wiring**

```bash
cd /home/jbl/projects/labs-wiki/.worktrees/url-raw-preservation-pilot
git add scripts/requirements-auto-ingest.txt scripts/auto_ingest.py
git commit -m "feat: add durable URL raw preservation"
```

### Task 4: Document the new raw-preservation and pilot re-ingest workflow

**Files:**
- Modify: `README.md`
- Modify: `docs/workflows.md`
- Modify: `AGENTS.md`
- Modify: `.github/instructions/raw-sources.instructions.md`

- [ ] **Step 1: Update the raw-source rules so the new fetched-content block is explicitly allowed**

```markdown
URL sources may append a deterministic fetched-content block written by `scripts/auto_ingest.py`. That block is part of the durable raw source and may be replaced on refresh. Manual notes outside the block must remain untouched.
```

- [ ] **Step 2: Add a README note that URL ingests now persist fetched content into raw**

```markdown
The `wiki-auto-ingest` pipeline now writes a deterministic fetched-content block back into `raw/` for `type: url` sources. That block stores the normalized body used for extraction, plus fetch metadata, so later re-ingest and audits do not depend on a fresh network fetch.
```

- [ ] **Step 3: Add the exact manual pilot command to the README**

```text
# Reprocess an already-ingested URL source that does not yet have a fetched-content block
AUTO_INGEST_MAX_SYNTHESIS_PER_INGEST=0 \
python3 scripts/auto_ingest.py raw/2026-04-20-agents-that-remember-introducing-agent-memory.md \
  --project-root . \
  --force
```

- [ ] **Step 4: Update `docs/workflows.md` to describe forced targeted re-ingest**

```text
For quota-sensitive backfills of already-ingested URL sources that do not yet have a fetched-content block, disable synthesis suggestions and force a single-file re-ingest:

AUTO_INGEST_MAX_SYNTHESIS_PER_INGEST=0 \
python3 scripts/auto_ingest.py raw/2026-04-08-lightgbm-light-gradient-boosting-machine-geeksforgeeks.md \
  --project-root . \
  --force

To replace an existing fetched-content block with a fresh network fetch later, add `--refresh-fetch` to the same command.
```

- [ ] **Step 5: Inspect the docs diff for clarity and accuracy**

```bash
cd /home/jbl/projects/labs-wiki/.worktrees/url-raw-preservation-pilot
git --no-pager diff -- README.md docs/workflows.md AGENTS.md .github/instructions/raw-sources.instructions.md | cat
```

Expected: user-facing docs and agent instructions all allow the deterministic fetched-content block and describe the correct re-ingest commands.

- [ ] **Step 6: Commit the doc updates**

```bash
cd /home/jbl/projects/labs-wiki/.worktrees/url-raw-preservation-pilot
git add README.md docs/workflows.md AGENTS.md .github/instructions/raw-sources.instructions.md
git commit -m "docs: allow deterministic URL raw preservation"
```

### Task 5: Run the 3-page pilot and write the evaluation report

**Files:**
- Create: `reports/url-raw-preservation-pilot.md`
- Modify: `raw/2026-04-20-agents-that-remember-introducing-agent-memory.md`
- Modify: `raw/2026-04-08-lightgbm-light-gradient-boosting-machine-geeksforgeeks.md`
- Modify: `raw/2026-04-16-251004618v3pdf.md`
- Modify: `wiki/log.md`
- Modify: `wiki/index.md`
- Review and modify: the actual regenerated source pages under `wiki/sources/` reported by `git status --short wiki/sources` after each pilot run
- Review: any additional downstream wiki pages that change naturally during the pilot, but do not add overwrite logic for shared concept/entity pages in this limited rollout

- [ ] **Step 1: Re-ingest the text-heavy pilot file with synthesis disabled**

```bash
cd /home/jbl/projects/labs-wiki/.worktrees/url-raw-preservation-pilot
AUTO_INGEST_MAX_SYNTHESIS_PER_INGEST=0 \
python3 scripts/auto_ingest.py raw/2026-04-20-agents-that-remember-introducing-agent-memory.md \
  --project-root . \
  --force
```

Expected: the raw file gains one fetched-content block and the linked wiki source page is regenerated.

- [ ] **Step 2: Re-ingest the table/tutorial-heavy pilot file with synthesis disabled**

```bash
cd /home/jbl/projects/labs-wiki/.worktrees/url-raw-preservation-pilot
AUTO_INGEST_MAX_SYNTHESIS_PER_INGEST=0 \
python3 scripts/auto_ingest.py raw/2026-04-08-lightgbm-light-gradient-boosting-machine-geeksforgeeks.md \
  --project-root . \
  --force
```

Expected: the raw file gains one fetched-content block with headings/table structure retained, and the linked source/concept pages refresh.

- [ ] **Step 3: Re-ingest the figure/equation-heavy pilot file with synthesis disabled**

```bash
cd /home/jbl/projects/labs-wiki/.worktrees/url-raw-preservation-pilot
AUTO_INGEST_MAX_SYNTHESIS_PER_INGEST=0 \
python3 scripts/auto_ingest.py raw/2026-04-16-251004618v3pdf.md \
  --project-root . \
  --force
```

Expected: the arXiv HTML rewrite path still works, the raw file stores a fetched-content block, and the ACE source page regenerates.

- [ ] **Step 4: Verify each raw file contains exactly one fetched-content block**

```bash
cd /home/jbl/projects/labs-wiki/.worktrees/url-raw-preservation-pilot
python3 - <<'PY'
from pathlib import Path
files = [
    "raw/2026-04-20-agents-that-remember-introducing-agent-memory.md",
    "raw/2026-04-08-lightgbm-light-gradient-boosting-machine-geeksforgeeks.md",
    "raw/2026-04-16-251004618v3pdf.md",
]
for path_str in files:
    text = Path(path_str).read_text()
    print(path_str, text.count("<!-- fetched-content:start -->"), text.count("<!-- fetched-content:end -->"))
PY
```

Expected: each line prints `1 1`.

- [ ] **Step 5: Verify metadata fields and manual text boundaries in the enriched raw files**

```bash
cd /home/jbl/projects/labs-wiki/.worktrees/url-raw-preservation-pilot
python3 - <<'PY'
from pathlib import Path
files = [
    "raw/2026-04-20-agents-that-remember-introducing-agent-memory.md",
    "raw/2026-04-08-lightgbm-light-gradient-boosting-machine-geeksforgeeks.md",
    "raw/2026-04-16-251004618v3pdf.md",
]
for path_str in files:
    text = Path(path_str).read_text()
    print(path_str)
    print("fetched_at:", "- fetched_at:" in text)
    print("resolved_url:", "- resolved_url:" in text)
    print("content_type:", "- content_type:" in text)
    print("frontmatter_status:", "status: ingested" in text)
PY
```

Expected: each file contains `fetched_at`, `resolved_url`, and `content_type` inside the fetched-content block, and the original frontmatter still remains intact above the block.

- [ ] **Step 6: Re-run one pilot file with `--refresh-fetch` to prove the fetched-content block is replaced, not duplicated**

```bash
cd /home/jbl/projects/labs-wiki/.worktrees/url-raw-preservation-pilot
AUTO_INGEST_MAX_SYNTHESIS_PER_INGEST=0 \
python3 scripts/auto_ingest.py raw/2026-04-20-agents-that-remember-introducing-agent-memory.md \
  --project-root . \
  --force \
  --refresh-fetch
python3 - <<'PY'
from pathlib import Path
text = Path("raw/2026-04-20-agents-that-remember-introducing-agent-memory.md").read_text()
print(text.count("<!-- fetched-content:start -->"), text.count("<!-- fetched-content:end -->"))
PY
git status --short wiki/ | cat
```

Expected: the raw file still prints `1 1`, and `git status --short wiki/` reveals whether any additional wiki pages changed naturally during the pilot.

- [ ] **Step 7: Write the evaluation report with exact pilot outcomes**

Write the report only after Steps 1-6 are complete. Fill the `Per-File Findings` table with measured findings from the run; do not leave instructions or placeholder text in the committed report.

```markdown
# URL Raw Preservation Pilot Evaluation

## Pilot Set

| Shape | Raw file | Source page |
| --- | --- | --- |
| Text-heavy | `raw/2026-04-20-agents-that-remember-introducing-agent-memory.md` | `wiki/sources/agents-that-remember-introducing-agent-memory.md` |
| Table/tutorial-heavy | `raw/2026-04-08-lightgbm-light-gradient-boosting-machine-geeksforgeeks.md` | `wiki/sources/lightgbm-light-gradient-boosting-machine-geeksforgeeks.md` |
| Figure/equation-heavy | `raw/2026-04-16-251004618v3pdf.md` | `wiki/sources/agentic-context-engineering-evolving-contexts-for-self-improving-language-models.md` |

## Raw Preservation Checks

- Each pilot raw file now stores one deterministic fetched-content block.
- Live fetch metadata records `fetched_at`, `source_url`, `resolved_url`, and `content_type`.
- Re-running `--force` replaces the block instead of appending a second copy.

## Per-File Findings

| Raw file | New preserved source material | Wiki-page improvements | Remaining gaps |
| --- | --- | --- | --- |

## Recommendation

- **Roll out broadly** if all three pages gain materially better detail without noisy raw output.
- **Hold at pilot scope** if the stored raw becomes noisy or the wiki pages do not improve enough to justify the extra fetch body.
```

- [ ] **Step 8: Inspect the pilot diff before final validation**

```bash
cd /home/jbl/projects/labs-wiki/.worktrees/url-raw-preservation-pilot
git --no-pager diff origin/main -- \
  scripts/requirements-auto-ingest.txt \
  scripts/auto_ingest.py \
  README.md \
  docs/workflows.md \
  reports/url-raw-preservation-pilot.md \
  raw/2026-04-20-agents-that-remember-introducing-agent-memory.md \
  raw/2026-04-08-lightgbm-light-gradient-boosting-machine-geeksforgeeks.md \
  raw/2026-04-16-251004618v3pdf.md \
  wiki/log.md \
  wiki/index.md \
  wiki/sources \
  wiki | cat
```

Expected: the branch-vs-main diff shows helper/code/doc changes, three enriched raw files, `wiki/log.md`, `wiki/index.md`, the refreshed source pages, any additional wiki pages that changed naturally, and the evaluation report.

- [ ] **Step 9: Commit the pilot artifacts**

```bash
cd /home/jbl/projects/labs-wiki/.worktrees/url-raw-preservation-pilot
git add \
  scripts/requirements-auto-ingest.txt \
  scripts/auto_ingest.py \
  README.md \
  docs/workflows.md \
  reports/url-raw-preservation-pilot.md \
  raw/2026-04-20-agents-that-remember-introducing-agent-memory.md \
  raw/2026-04-08-lightgbm-light-gradient-boosting-machine-geeksforgeeks.md \
  raw/2026-04-16-251004618v3pdf.md \
  wiki/log.md \
  wiki/index.md \
  wiki/sources \
  wiki
git commit -m "feat: run URL raw preservation pilot"
```

### Task 6: Final validation and handoff

**Files:**
- Review: `scripts/auto_ingest.py`
- Review: `reports/url-raw-preservation-pilot.md`

- [ ] **Step 1: Run the final validation commands**

```bash
cd /home/jbl/projects/labs-wiki/.worktrees/url-raw-preservation-pilot
python3 -m py_compile scripts/auto_ingest.py
docker build -f Dockerfile.auto-ingest -t labs-wiki-auto-ingest-test .
git status --short
```

Expected: `auto_ingest.py` still compiles, the Docker image still builds, and `git status` is clean because Task 5 already committed the planned pilot changes.

- [ ] **Step 2: Push the branch and open the review path**

```bash
cd /home/jbl/projects/labs-wiki/.worktrees/url-raw-preservation-pilot
git push -u origin feature/url-raw-preservation-pilot
gh pr create --base main --head feature/url-raw-preservation-pilot \
  --title "feat: preserve fetched URL content in raw" \
  --body "## Summary
- persist normalized URL fetch content back into raw
- add a force re-ingest path for targeted pilot reruns
- run a 3-page evaluation and capture the results

## Validation
- python3 -m py_compile scripts/auto_ingest.py
- AUTO_INGEST_MAX_SYNTHESIS_PER_INGEST=0 python3 scripts/auto_ingest.py raw/2026-04-20-agents-that-remember-introducing-agent-memory.md --project-root . --force
- AUTO_INGEST_MAX_SYNTHESIS_PER_INGEST=0 python3 scripts/auto_ingest.py raw/2026-04-08-lightgbm-light-gradient-boosting-machine-geeksforgeeks.md --project-root . --force
- AUTO_INGEST_MAX_SYNTHESIS_PER_INGEST=0 python3 scripts/auto_ingest.py raw/2026-04-16-251004618v3pdf.md --project-root . --force"
```

Expected: the feature branch is pushed and ready for review/merge.
