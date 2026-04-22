#!/usr/bin/env python3
"""Re-fetch GitHub raw sources with the enriched crawler and write
deterministic source pages — without calling any LLM.

Workflow per raw file matching ``url: https://github.com/<owner>/<repo>``:
  1. Run :func:`auto_ingest.fetch_url_content` to pull README + package
     manifests + commits + issues + PRs + releases + languages + topics.
  2. Replace the existing ``<!-- fetched-content -->`` block in the raw
     file in-place; refresh ``content_hash``.
  3. Materialise (or replace) ``wiki/sources/<slug>.md`` with a
     hand-templated body — Summary, Repository Info, Topics, Recent
     Activity (commits/releases/PRs/issues), Key Files. No prose
     hallucination.

Run from repo root:

    python3 scripts/refresh_github_sources.py [--dry-run]

After running, trigger the wiki-graph-api ``/internal/rebuild`` to pick
up the changes.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import re
import sys
from pathlib import Path

import yaml  # type: ignore

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import auto_ingest  # noqa: E402

RAW_DIR = ROOT / "raw"
SOURCES_DIR = ROOT / "wiki" / "sources"
LOG_PATH = ROOT / "wiki" / "log.md"

GITHUB_RE = re.compile(r"^https?://github\.com/([^/]+)/([^/?#]+)/?$")
GIST_RE = re.compile(r"^https?://gist\.github\.com/([^/]+)/([a-f0-9]+)/?$")


def _slugify(text: str, max_len: int = 80) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:max_len].rstrip("-") or "untitled"


def _split_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}, text
    fm = yaml.safe_load(text[4:end]) or {}
    return (fm if isinstance(fm, dict) else {}), text[end + 5 :]


def _parse_sections(fetched: str) -> dict[str, str]:
    """Split the fetched content text into a dict of {section_title: body}."""
    sections: dict[str, str] = {}
    current = "_intro"
    buf: list[str] = []
    for line in fetched.splitlines():
        m = re.match(r"^##\s+(.*)$", line)
        if m:
            sections[current] = "\n".join(buf).strip()
            current = m.group(1).strip()
            buf = []
        else:
            buf.append(line)
    sections[current] = "\n".join(buf).strip()
    return sections


def _intro_facts(intro: str) -> dict[str, str]:
    facts: dict[str, str] = {}
    for line in intro.splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            facts[k.strip().lower()] = v.strip()
    return facts


def _truncate(text: str, n: int) -> str:
    text = (text or "").strip()
    if len(text) <= n:
        return text
    return text[: n].rstrip() + "…"


def _build_gist_page(
    *, owner: str, gist_id: str, source_url: str,
    raw_rel_path: str, fetched_text: str,
) -> tuple[str, str, dict]:
    """Build an enriched source page for a GitHub gist (no LLM).

    Gists are typically a single text file. We surface the gist's own H1
    as the wiki page title (so existing ``[[wikilinks]]`` keep resolving),
    a short Summary derived from the first paragraph, a Repository Info
    block (gist URL, author, id, size), and an excerpt of the gist body.
    No commits/issues/PRs sections — gists don't expose those.
    """
    text = fetched_text.strip()

    # First H1 → title (e.g. ``# LLM Wiki``); fall back to "<owner>/gist".
    title_match = re.search(r"^#\s+(.+?)\s*$", text, re.M)
    title = title_match.group(1).strip() if title_match else f"{owner}/gist"

    # First non-heading paragraph after the H1 → summary. Cap at 600 chars
    # so it remains a *summary*, not a re-render of the whole gist.
    summary_body = ""
    if title_match:
        rest = text[title_match.end():].lstrip()
    else:
        rest = text
    for chunk in re.split(r"\n\s*\n", rest):
        chunk = chunk.strip()
        if not chunk or chunk.startswith("#"):
            continue
        summary_body = _truncate(chunk, 600)
        break
    if not summary_body:
        summary_body = f"GitHub gist {owner}/{gist_id}."

    today = _dt.date.today().isoformat()
    short_id = gist_id[:10]
    repo_lines = [
        f"- **Source URL**: {source_url}",
        f"- **Author**: {owner}",
        f"- **Gist ID**: `{gist_id}`",
        f"- **Content size**: {len(text):,} chars",
    ]

    content_excerpt = _truncate(text, 1800)

    body_parts = [
        f"# {title}\n",
        "## Summary\n",
        summary_body,
        "",
        "## Repository Info\n",
        "\n".join(repo_lines),
        "",
        "## Content Excerpt\n",
        content_excerpt,
        "",
        "## Crawled Files\n",
        f"Source dump in `{raw_rel_path}` includes:",
        "",
        f"- gist `{owner}/{gist_id}` (single-file gist, raw text)",
    ]
    body = "\n".join(body_parts).rstrip() + "\n"

    fm = {
        "title": title,
        "type": "source",
        "created": today,
        "last_verified": today,
        "source_hash": hashlib.sha256(body.encode()).hexdigest(),
        "sources": [raw_rel_path],
        "source_url": source_url,
        "tags": sorted({"github", "gist", owner.lower()})[:8],
        "tier": "warm",
        "knowledge_state": "ingested",
        "ingest_method": "self-synthesis-no-llm",
    }
    fm_text = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True).strip()
    page = f"---\n{fm_text}\n---\n\n{body}"
    slug = _slugify(title) or _slugify(f"{owner}-gist-{short_id}")
    return slug, page, fm


def _build_source_page(
    *, owner: str, repo: str, source_url: str,
    raw_rel_path: str, fetched_text: str,
) -> tuple[str, str, dict]:
    sections = _parse_sections(fetched_text)
    intro = _intro_facts(sections.get("_intro", ""))
    title = f"{owner}/{repo}"
    description = intro.get("description", "")
    stars = intro.get("stars", "")
    language = intro.get("language", "")
    topics = intro.get("topics", "")
    languages_breakdown = intro.get("languages", "")
    today = _dt.date.today().isoformat()

    # Summary
    summary_body = description or f"GitHub repository {title}."

    # Repository info
    repo_lines = [f"- **Source URL**: {source_url}"]
    if stars:
        repo_lines.append(f"- **Stars**: {stars}")
    if language:
        repo_lines.append(f"- **Primary language**: {language}")
    if languages_breakdown:
        repo_lines.append(f"- **Languages**: {languages_breakdown}")
    if topics:
        repo_lines.append(f"- **Topics**: {topics}")

    # Activity sections (verbatim — no synthesis)
    activity_parts: list[str] = []
    for heading in (
        "Recent Releases",
        "Recent Commits",
        "Open Issues (top 10)",
        "Recently Merged PRs (top 10)",
    ):
        if sections.get(heading):
            activity_parts.append(f"### {heading}\n\n{sections[heading].strip()}")

    # Key files — list everything we crawled, link to raw file for full
    # content. We surface README excerpt + manifest names.
    file_paths: list[str] = []
    for key in sections:
        m = re.match(r"^File:\s+(.*)$", key)
        if m:
            file_paths.append(m.group(1).strip())
    files_block = ""
    if file_paths:
        files_block = "\n".join(f"- `{p}`" for p in file_paths[:50])
        if len(file_paths) > 50:
            files_block += f"\n- *(… {len(file_paths) - 50} more files crawled)*"

    readme_excerpt = _truncate(sections.get("README", ""), 1500)

    # Tags from topics
    tag_set = set()
    if topics:
        for t in topics.split(","):
            t = t.strip().lower()
            if t:
                tag_set.add(t)
    tag_set.add("github")
    if language:
        tag_set.add(language.lower())
    tags = sorted(tag_set)[:8]

    body_parts = [f"# {title}\n", "## Summary\n", summary_body, "", "## Repository Info\n",
                  "\n".join(repo_lines)]
    if readme_excerpt:
        body_parts += ["", "## README Excerpt\n", readme_excerpt]
    if activity_parts:
        body_parts += ["", "## Activity Snapshot\n", *activity_parts]
    if files_block:
        body_parts += ["", "## Crawled Files\n",
                       "Source dump in `" + raw_rel_path + "` includes:",
                       "", files_block]
    body = "\n".join(body_parts).rstrip() + "\n"

    fm = {
        "title": title,
        "type": "source",
        "created": today,
        "last_verified": today,
        "source_hash": hashlib.sha256(body.encode()).hexdigest(),
        "sources": [raw_rel_path],
        "source_url": source_url,
        "tags": tags,
        "tier": "warm",
        "knowledge_state": "ingested",
        "ingest_method": "self-synthesis-no-llm",
    }
    fm_text = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True).strip()
    page = f"---\n{fm_text}\n---\n\n{body}"
    slug = _slugify(f"{owner}-{repo}")
    return slug, page, fm


def _refresh_raw(raw_path: Path, fetched_text: str, source_url: str,
                 resolved_url: str, content_type: str) -> None:
    text = raw_path.read_text()
    fm, body = _split_frontmatter(text)
    block = auto_ingest.build_fetched_content_block(
        fetched_at=_dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"),
        source_url=source_url,
        resolved_url=resolved_url,
        content_type=content_type,
        image_urls=[],
        text=fetched_text,
    )
    new_body = auto_ingest.upsert_fetched_content_block(body, block)
    fm["content_hash"] = "sha256:" + hashlib.sha256(fetched_text.encode()).hexdigest()
    fm["status"] = "ingested"
    fm["last_refreshed"] = _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds")
    fm_text = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True).strip()
    raw_path.write_text(f"---\n{fm_text}\n---\n\n{new_body.strip()}\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--only", default="",
                        help="Substring filter applied to the source URL.")
    args = parser.parse_args()

    # Each entry: (raw_path, url, kind, key1, key2)
    # kind is "repo" → (owner, repo); kind is "gist" → (owner, gist_id).
    raw_files: list[tuple[Path, str, str, str, str]] = []
    for p in sorted(RAW_DIR.glob("*.md")):
        text = p.read_text()
        fm, _ = _split_frontmatter(text)
        url = (fm.get("url") or "").strip()
        m = GITHUB_RE.match(url)
        if m:
            raw_files.append((p, url, "repo", m.group(1), m.group(2)))
            continue
        m = GIST_RE.match(url)
        if m:
            raw_files.append((p, url, "gist", m.group(1), m.group(2)))
    if args.only:
        raw_files = [r for r in raw_files if args.only in r[1]]
    if args.limit:
        raw_files = raw_files[: args.limit]
    print(f"[plan] {len(raw_files)} GitHub raw sources to refresh")

    SOURCES_DIR.mkdir(parents=True, exist_ok=True)
    created: list[str] = []
    for raw_path, url, kind, k1, k2 in raw_files:
        label = f"{k1}/{k2}" if kind == "repo" else f"gist:{k1}/{k2[:10]}"
        print(f"[fetch] {label}  ({raw_path.name})")
        try:
            res = auto_ingest.fetch_url_content(url)
        except Exception as e:
            print(f"  ! fetch failed: {e}")
            continue
        if not res.text or len(res.text) < 200:
            print("  ! short content; skipping")
            continue
        if kind == "repo":
            slug, page, _fm = _build_source_page(
                owner=k1, repo=k2, source_url=url,
                raw_rel_path=f"raw/{raw_path.name}",
                fetched_text=res.text,
            )
        else:
            slug, page, _fm = _build_gist_page(
                owner=k1, gist_id=k2, source_url=url,
                raw_rel_path=f"raw/{raw_path.name}",
                fetched_text=res.text,
            )
        out = SOURCES_DIR / f"{slug}.md"
        if args.dry_run:
            print(f"  [dry-run] would write {out} ({len(page)} chars) and refresh raw")
            continue
        _refresh_raw(raw_path, res.text, url, res.resolved_url or url, res.content_type or "")
        out.write_text(page)
        created.append(str(out.relative_to(ROOT)))
        print(f"  [ok] wrote {out.relative_to(ROOT)} ({len(page)} chars)")

    if created and not args.dry_run:
        with LOG_PATH.open("a") as f:
            f.write(
                f"\n## {_dt.date.today().isoformat()} — github-source-refresh\n"
                f"- operation: refresh_github_sources\n"
                f"- ingest_method: self-synthesis (no LLM)\n"
                f"- count: {len(created)}\n"
                + "\n".join(f"  - {p}" for p in created)
                + "\n"
            )
        print(f"[log] appended to {LOG_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
