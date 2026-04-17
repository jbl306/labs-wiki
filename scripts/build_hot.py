#!/usr/bin/env python3
"""
build_hot.py — Regenerate labs-wiki/wiki/hot.md.

Zero LLM calls. Pure heuristics:

  1. Last N wiki pages modified (git log of wiki/).
  2. Last N raw/ sources captured (filesystem mtime).
  3. MemPalace wake-up output (L0+L1 context per wing).
  4. Wiki pages with `tier: hot` frontmatter.
  5. Active tasks/todo.md entries across sibling projects.

Output target: ~600-800 tokens. Runs in a few seconds.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HOME = Path.home()
REPO = Path(__file__).resolve().parent.parent  # labs-wiki/
WIKI = REPO / "wiki"
RAW = REPO / "raw"
HOT = WIKI / "hot.md"
MEMPALACE_BIN = os.environ.get("MEMPALACE_BIN", str(HOME / ".local/bin/mempalace"))

RECENT_WIKI_LIMIT = 10
RECENT_RAW_LIMIT = 10
HOT_TIER_LIMIT = 15
WAKEUP_WINGS = ("labs_wiki", "copilot_sessions", "homelab")
PROJECTS_TO_CHECK = ("homelab", "labs-wiki", "nba-ml-engine")

UTC_NOW = datetime.now(timezone.utc)


def _run(cmd: list[str], cwd: Path | None = None, timeout: int = 30) -> str:
    try:
        r = subprocess.run(
            cmd,
            cwd=str(cwd) if cwd else None,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return r.stdout or ""
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return ""


def recent_wiki_pages() -> list[tuple[str, str]]:
    """Return [(rel_path, iso_date), ...] of last N wiki pages touched."""
    out = _run(
        [
            "git",
            "-C",
            str(REPO),
            "log",
            "--pretty=format:%cI",
            "--name-only",
            "--max-count=80",
            "--",
            "wiki/",
        ]
    )
    pairs: list[tuple[str, str]] = []
    seen: set[str] = set()
    current_date = ""
    for line in out.splitlines():
        if not line.strip():
            continue
        if re.match(r"^\d{4}-\d{2}-\d{2}T", line):
            current_date = line.strip()
            continue
        if not line.endswith(".md"):
            continue
        if (
            line in seen
            or "/hot.md" in line
            or line.endswith("log.md")
            or line.endswith("index.md")
        ):
            continue
        seen.add(line)
        pairs.append((line, current_date[:10]))
        if len(pairs) >= RECENT_WIKI_LIMIT:
            break
    return pairs


def recent_raw_sources() -> list[tuple[str, str]]:
    if not RAW.exists():
        return []
    files: list[tuple[Path, float]] = []
    for p in RAW.rglob("*.md"):
        if p.name.startswith("."):
            continue
        try:
            files.append((p, p.stat().st_mtime))
        except OSError:
            continue
    files.sort(key=lambda x: x[1], reverse=True)
    out: list[tuple[str, str]] = []
    for p, mt in files[:RECENT_RAW_LIMIT]:
        date = datetime.fromtimestamp(mt, tz=timezone.utc).strftime("%Y-%m-%d")
        out.append((str(p.relative_to(REPO)), date))
    return out


def hot_tier_pages() -> list[tuple[str, str]]:
    """Find wiki pages with `tier: hot` in frontmatter."""
    out: list[tuple[str, str]] = []
    for md in WIKI.rglob("*.md"):
        if md.name in {"hot.md", "log.md", "index.md"}:
            continue
        try:
            head = md.read_text(errors="ignore")[:800]
        except OSError:
            continue
        if not head.startswith("---"):
            continue
        parts = head.split("---", 2)
        if len(parts) < 3:
            continue
        fm = parts[1]
        if re.search(r"^\s*tier:\s*hot\b", fm, re.MULTILINE):
            title_match = re.search(
                r"^\s*title:\s*[\"']?(.+?)[\"']?\s*$", fm, re.MULTILINE
            )
            title = title_match.group(1) if title_match else md.stem
            out.append((str(md.relative_to(REPO)), title))
        if len(out) >= HOT_TIER_LIMIT:
            break
    return out


def mempalace_wakeups() -> dict[str, str]:
    """Return {wing: wakeup_text} for each configured wing.

    Wake-up output includes full drawer bodies; trim to a compact summary
    (L0 room headers + a tight cap) to keep hot.md in the ~600-800 token band.
    """
    result: dict[str, str] = {}
    max_chars_per_wing = 800  # ~200 tokens each
    for wing in WAKEUP_WINGS:
        text = _run([MEMPALACE_BIN, "wake-up", "--wing", wing], timeout=20).strip()
        if not text:
            continue
        # Keep only structural lines (headers, room labels, short bullets);
        # drop long drawer-body lines that bloat the cache.
        kept: list[str] = []
        for line in text.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            # Skip very long lines (drawer bodies)
            if len(line) > 140:
                continue
            kept.append(line)
        compact = "\n".join(kept)
        if len(compact) > max_chars_per_wing:
            compact = compact[:max_chars_per_wing].rsplit("\n", 1)[0] + "\n…"
        result[wing] = compact
    return result


def active_todos() -> list[tuple[str, str]]:
    """Return [(project, first_unchecked_line), ...] from tasks/todo.md files."""
    results: list[tuple[str, str]] = []
    for proj in PROJECTS_TO_CHECK:
        todo = HOME / "projects" / proj / "tasks" / "todo.md"
        if not todo.exists():
            continue
        try:
            content = todo.read_text(errors="ignore")
        except OSError:
            continue
        for line in content.splitlines():
            m = re.match(r"^\s*-\s*\[\s\]\s+(.+)$", line)
            if m:
                results.append((proj, m.group(1).strip()[:140]))
                break
    return results


def build() -> str:
    lines: list[str] = []
    ts = UTC_NOW.isoformat(timespec="seconds")
    lines += [
        "---",
        'title: "Hot Cache — Recent Context"',
        "type: meta",
        f"generated: {ts}",
        "generator: scripts/build_hot.py",
        "ttl_hours: 24",
        "---",
        "",
        "# Hot Cache",
        "",
        "> Auto-generated. Every session, every client, reads this first.",
        f"> Regenerated: {ts}",
        "",
    ]

    # 1. Recent wiki pages
    recent = recent_wiki_pages()
    if recent:
        lines += ["## Recent Wiki Edits", ""]
        for path, date in recent:
            lines.append(f"- `{date}` — [[{Path(path).stem}]] (`{path}`)")
        lines.append("")

    # 2. Recent raw sources
    raw = recent_raw_sources()
    if raw:
        lines += ["## Recent Sources Captured", ""]
        for path, date in raw:
            lines.append(f"- `{date}` — `{path}`")
        lines.append("")

    # 3. Hot-tier pages
    hot_pages = hot_tier_pages()
    if hot_pages:
        lines += ["## Always-Hot Pages (`tier: hot`)", ""]
        for path, title in hot_pages:
            lines.append(f"- [[{title}]] → `{path}`")
        lines.append("")

    # 4. Active todos
    todos = active_todos()
    if todos:
        lines += ["## In-Progress Tasks", ""]
        for proj, item in todos:
            lines.append(f"- **{proj}**: {item}")
        lines.append("")

    # 5. MemPalace wake-ups (largest section — placed last so truncation is safe)
    wakeups = mempalace_wakeups()
    if wakeups:
        lines += ["## MemPalace Wake-Up", ""]
        for wing, text in wakeups.items():
            lines += [f"### Wing: `{wing}`", "", "```", text, "```", ""]

    lines += [
        "---",
        "",
        "*Retrieval ladder after hot.md: `mempalace_search` → `wiki_search` → `wiki_read` → web.*",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    HOT.parent.mkdir(parents=True, exist_ok=True)
    content = build()
    HOT.write_text(content)
    size = len(content)
    approx_tokens = size // 4
    print(f"hot.md written: {size} bytes (~{approx_tokens} tokens)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
