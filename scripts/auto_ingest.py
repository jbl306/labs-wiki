#!/usr/bin/env python3
"""
Auto-ingest: Process raw wiki sources through an LLM pipeline.

Reads a raw markdown source from raw/, extracts concepts/entities via
GitHub Models API (GPT-4.1), generates wiki pages, and updates the index.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import html
import json
import logging
import os
import re
import subprocess
import sys
import textwrap
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup
from openai import OpenAI

try:
    from rapidfuzz import fuzz as _rf_fuzz
    _FUZZ_AVAILABLE = True
except ImportError:  # pragma: no cover
    _rf_fuzz = None
    _FUZZ_AVAILABLE = False

from checkpoint_classifier import (
    COMPRESS,
    RETAIN,
    SKIP,
    classify_checkpoint,
    resolve_retention,
)
from checkpoint_state import derive_knowledge_state, is_planning_only_checkpoint

log = logging.getLogger("auto-ingest")

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

GITHUB_MODELS_URL = os.environ.get(
    "GITHUB_MODELS_URL", "https://models.github.ai/inference"
)
DEFAULT_MODEL = "gpt-4.1"
MAX_RETRIES = 3
URL_FETCH_TIMEOUT = 30
MAX_IMAGES = 5  # Max images to process per source for vision
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB max per image download
FETCHED_CONTENT_START = "<!-- fetched-content:start -->"
FETCHED_CONTENT_END = "<!-- fetched-content:end -->"


@dataclass(frozen=True)
class UrlFetchResult:
    text: str
    image_urls: list[str]
    resolved_url: str | None = None
    content_type: str | None = None


def _env_str(*names: str, default: str = "") -> str:
    """Return the first non-empty environment variable value."""
    for name in names:
        value = os.environ.get(name, "").strip()
        if value:
            return value
    return default


def _fetched_content_pattern() -> re.Pattern[str]:
    return re.compile(
        rf"\n?{re.escape(FETCHED_CONTENT_START)}\n.*?\n{re.escape(FETCHED_CONTENT_END)}\n?",
        flags=re.S,
    )


def strip_fetched_content_block(body: str) -> str:
    return re.sub(_fetched_content_pattern(), "\n", body).strip()


def extract_manual_notes(body: str, source_url: str | None) -> str:
    raw_body = strip_fetched_content_block(body)
    if not raw_body:
        return ""
    lines = raw_body.splitlines()
    if source_url and lines and lines[0].strip() == source_url.strip():
        lines = lines[1:]
    return "\n".join(line.rstrip() for line in lines).strip()


def read_persisted_fetched_content(body: str) -> tuple[str | None, dict[str, object]]:
    pattern = re.compile(
        rf"{re.escape(FETCHED_CONTENT_START)}\n(.*?)\n{re.escape(FETCHED_CONTENT_END)}",
        flags=re.S,
    )
    match = pattern.search(body)
    if not match:
        return None, {}

    metadata: dict[str, object] = {}
    text_lines: list[str] = []
    in_text = False

    for line in match.group(1).splitlines():
        stripped = line.strip()
        if stripped == "## Fetched Content":
            in_text = True
            continue
        if not in_text and stripped.startswith("- "):
            key, _, value = stripped[2:].partition(":")
            parsed_key = key.strip()
            parsed_value = value.strip()
            if parsed_key == "image_urls":
                try:
                    metadata[parsed_key] = json.loads(parsed_value)
                except json.JSONDecodeError:
                    metadata[parsed_key] = []
            else:
                metadata[parsed_key] = parsed_value
            continue
        if in_text:
            text_lines.append(line)

    text = "\n".join(text_lines).strip()
    return (text or None), metadata


def build_fetched_content_block(
    *,
    fetched_at: str,
    source_url: str,
    resolved_url: str | None,
    content_type: str | None,
    image_urls: list[str],
    text: str,
) -> str:
    lines = [
        FETCHED_CONTENT_START,
        "## Fetched Metadata",
        f"- fetched_at: {fetched_at}",
        f"- source_url: {source_url}",
        f"- resolved_url: {resolved_url or source_url}",
        f"- content_type: {content_type or 'unknown'}",
        f"- image_urls: {json.dumps(image_urls)}",
        "",
        "## Fetched Content",
        text.strip(),
        FETCHED_CONTENT_END,
    ]
    return "\n".join(lines).rstrip() + "\n"


def upsert_fetched_content_block(raw_text: str, block: str) -> str:
    pattern = _fetched_content_pattern()
    cleaned = pattern.sub("\n", raw_text).rstrip()
    if cleaned:
        return cleaned + "\n\n" + block
    return block


def build_url_ingest_content(
    *,
    body: str,
    source_url: str | None,
    persisted_text: str | None,
) -> str:
    manual_notes = extract_manual_notes(body, source_url)
    parts: list[str] = []
    if persisted_text:
        parts.append(persisted_text.strip())
    if manual_notes:
        if persisted_text:
            parts.append(f"## Manual Notes\n{manual_notes}")
        else:
            parts.append(manual_notes)
    if parts:
        return "\n\n".join(parts).strip()
    return strip_fetched_content_block(body).strip()


def is_meaningful_fetched_body(text: str, source_url: str | None) -> bool:
    cleaned = text.strip()
    if not cleaned:
        return False
    if source_url and cleaned == source_url.strip():
        return False
    if cleaned.startswith("[PDF document at ") and "content could not be extracted" in cleaned:
        return False
    compressed = re.sub(r"\s+", "", cleaned)
    return len(compressed) >= 30


_IMG_PENALIZE = re.compile(
    r"logo|icon|favicon|badge|avatar|sprite"
    r"|app[_-]?store|google[_-]?play|download[_-]?on[_-]?the|get[_-]?it[_-]?on"
    r"|btn|button|banner|ad[_\-/]|promo|pixel|tracking|1x1",
    re.I,
)
_IMG_PREFER_PATH = re.compile(
    r"/articles?/|/posts?/|/images?/|/content/|/media/|/uploads?/|/figures?/",
    re.I,
)


def _parse_img_dimension(value: str | None) -> int | None:
    if not value:
        return None
    match = re.search(r"\d+", value)
    if not match:
        return None
    return int(match.group(0))


def _parse_dimension_from_src(src: str) -> tuple[int | None, int | None]:
    match = re.search(r"(?<!\d)(\d{2,4})x(\d{2,4})(?!\d)", src)
    if not match:
        return None, None
    return int(match.group(1)), int(match.group(2))


def _extract_img_src(tag) -> str:
    src = (
        tag.get("src")
        or tag.get("data-src")
        or tag.get("data-lazy-src")
        or tag.get("data-original")
    )
    if src:
        return src
    srcset = tag.get("srcset") or tag.get("data-srcset")
    if not srcset:
        return ""
    candidates = [part.strip().split()[0] for part in srcset.split(",") if part.strip()]
    return candidates[-1] if candidates else ""


def _resolve_image_url(src: str, base_url: str) -> str:
    return urljoin(base_url, src) if not src.startswith(("http://", "https://")) else src


def _score_img(
    src: str,
    alt: str,
    in_figure: bool,
    in_article_root: bool,
    width: int | None,
    height: int | None,
    *,
    is_og_image: bool = False,
) -> float:
    """Score an <img> as an article-content image. Higher is better."""
    if src.startswith("data:"):
        return -1000.0
    score = 0.0
    if _IMG_PENALIZE.search(src) or _IMG_PENALIZE.search(alt):
        score -= 50.0
    if src.lower().endswith(".svg") and not in_figure and not in_article_root:
        score -= 20.0
    if _IMG_PREFER_PATH.search(src):
        score += 20.0
    if in_figure:
        score += 15.0
    if in_article_root:
        score += 10.0
    alt_words = len(alt.split())
    if alt_words >= 4:
        score += 10.0
    elif alt_words >= 2:
        score += 5.0
    elif alt_words == 0:
        score -= 5.0
    if is_og_image:
        score += 8.0
    if width and height:
        largest = max(width, height)
        smallest = max(min(width, height), 1)
        aspect_ratio = largest / smallest
        if not in_article_root and largest <= 256 and aspect_ratio <= 1.2:
            score -= 25.0
        elif not in_article_root and largest <= 320 and aspect_ratio <= 1.2:
            score -= 12.0
        area = width * height
        if area >= 200_000:
            score += 12.0
        elif area >= 80_000:
            score += 6.0
        elif area <= 12_000:
            score -= 20.0
        elif area <= 32_000:
            score -= 8.0
        if width >= 800 or height >= 800:
            score += 4.0
    elif width or height:
        largest = max(width or 0, height or 0)
        if largest >= 800:
            score += 4.0
        elif largest <= 120:
            score -= 12.0
    return score


def extract_image_urls(raw_html: str, page_url: str) -> list[str]:
    soup = BeautifulSoup(raw_html, "html.parser")
    base_tag = soup.find("base", href=True)
    base_url = urljoin(page_url, base_tag["href"]) if base_tag else page_url

    scored: list[tuple[float, str]] = []
    og_match = re.search(
        r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']',
        raw_html,
        flags=re.I,
    )
    if not og_match:
        og_match = re.search(
            r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']',
            raw_html,
            flags=re.I,
        )
    if og_match:
        og_src = _resolve_image_url(og_match.group(1), base_url)
        og_width, og_height = _parse_dimension_from_src(og_src)
        scored.append((
            _score_img(
                og_src,
                "",
                False,
                False,
                og_width,
                og_height,
                is_og_image=True,
            ),
            og_src,
        ))

    # Score all <img> tags; prefer article-local and figure images
    article_root = _select_content_root(soup)
    article_img_ids = {id(img) for img in article_root.find_all("img")}
    for img in soup.find_all("img"):
        src = _extract_img_src(img)
        if not src or src.startswith("data:"):
            continue
        resolved_src = _resolve_image_url(src, base_url)
        alt = img.get("alt", "")
        in_figure = bool(img.parent and img.parent.name == "figure")
        in_article_root = id(img) in article_img_ids
        width = _parse_img_dimension(img.get("width"))
        height = _parse_img_dimension(img.get("height"))
        if not width and not height:
            width, height = _parse_dimension_from_src(resolved_src)
        score = _score_img(resolved_src, alt, in_figure, in_article_root, width, height)
        scored.append((score, resolved_src))

    image_urls: list[str] = []
    seen: set[str] = set()
    for score, src in sorted(scored, key=lambda x: x[0], reverse=True):
        if score < -10.0:
            continue
        if src not in seen:
            image_urls.append(src)
            seen.add(src)
        if len(image_urls) >= MAX_IMAGES:
            break

    return image_urls[:MAX_IMAGES]


_CONTENT_ROOT_SELECTORS = [
    "article",
    "main",
    "[role='main']",
    "[itemprop='articleBody']",
    ".article-body",
    ".article-content",
    ".entry-content",
    ".post-content",
    ".content",
    "#content",
]


def _score_content_root(tag) -> float:
    """Score a BeautifulSoup tag as an article content root. Higher is better."""
    text = tag.get_text(" ", strip=True)
    text_len = len(text)
    if text_len < 100:
        return 0.0
    html_len = len(str(tag))
    density = text_len / max(html_len, 1)
    p_count = len(tag.find_all("p"))
    li_count = len(tag.find_all("li"))
    table_count = len(tag.find_all("table"))
    pre_count = len(tag.find_all("pre"))
    h_count = sum(len(tag.find_all(f"h{i}")) for i in range(1, 7))
    score = (
        density * 50
        + min(p_count, 20) * 2
        + min(li_count, 30) * 1
        + min(table_count, 10) * 3
        + min(pre_count, 10) * 3
        + min(h_count, 15) * 2
        + min(text_len, 10_000) / 200
    )
    return score


def _select_content_root(soup: BeautifulSoup):
    """Select the best article-like content root from a parsed document.

    Tries selectors in _CONTENT_ROOT_SELECTORS, scores each candidate by
    text density and structural richness, and returns the highest-scoring
    match. Falls back to <body> (or the soup root) when no candidate
    clears the minimum quality bar.
    """
    candidates: list[tuple[float, object]] = []
    for selector in _CONTENT_ROOT_SELECTORS:
        for tag in soup.select(selector):
            score = _score_content_root(tag)
            if score > 0:
                candidates.append((score, tag))
    if candidates:
        return max(candidates, key=lambda x: x[0])[1]
    body = soup.find("body")
    return body if body else soup


def _serialize_html_table(table) -> str:
    rows: list[list[str]] = []
    for tr in table.find_all("tr"):
        cells = [cell.get_text(" ", strip=True) for cell in tr.find_all(["th", "td"])]
        if cells:
            rows.append(cells)
    if not rows:
        return ""

    width = max(len(row) for row in rows)
    normalized_rows = [row + [""] * (width - len(row)) for row in rows]
    header = normalized_rows[0]
    divider = ["---"] * width
    body_rows = normalized_rows[1:]
    markdown_rows = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(divider) + " |",
    ]
    markdown_rows.extend("| " + " | ".join(row) + " |" for row in body_rows)
    return "\n".join(markdown_rows)


def normalize_html_document(raw_html: str) -> str:
    soup = BeautifulSoup(raw_html, "html.parser")
    # Strip script/style/noscript globally before root selection
    for node in soup(["script", "style", "noscript"]):
        node.decompose()
    for node in soup.select("[aria-hidden='true'], .visually-hidden, .sr-only"):
        node.decompose()

    # Select article-like content root (e.g. GeeksforGeeks .content wins over body)
    root = _select_content_root(soup)

    # Strip structural chrome from within the selected root
    for node in root(["nav", "header", "footer", "aside", "form"]):
        node.decompose()
    for br in root.find_all("br"):
        br.replace_with("\n")

    for table in root.find_all("table"):
        table_md = _serialize_html_table(table)
        if table_md:
            table.replace_with("\n" + table_md + "\n")
        else:
            table.decompose()

    for tag_name in ("h1", "h2", "h3", "h4", "h5", "h6"):
        for tag in root.find_all(tag_name):
            level = int(tag_name[1])
            tag.replace_with("\n" + ("#" * level) + " " + tag.get_text(" ", strip=True) + "\n")

    for pre in root.find_all("pre"):
        pre.replace_with("\n```\n" + pre.get_text("\n", strip=False).strip() + "\n```\n")

    for code in root.find_all("code"):
        if code.parent.name != "pre":
            code.replace_with("`" + code.get_text(" ", strip=True) + "`")

    for li in root.find_all("li"):
        li.replace_with("\n- " + li.get_text(" ", strip=True))

    text = root.get_text("\n")
    text = html.unescape(text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    # Preserve all non-empty lines; no global short-line deduplication so
    # lists, table rows, captions, and footnotes survive verbatim.
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines).strip()[:50_000]


MODEL_DEFAULT = _env_str("GITHUB_MODELS_MODEL_DEFAULT", "GITHUB_MODELS_MODEL", default=DEFAULT_MODEL)
MODEL_LIGHT = _env_str("GITHUB_MODELS_MODEL_LIGHT", default=MODEL_DEFAULT)
MODEL_VISION = _env_str("GITHUB_MODELS_MODEL_VISION", default=MODEL_DEFAULT)
MAX_SOURCE_CHARS_DEFAULT = int(os.environ.get("AUTO_INGEST_MAX_SOURCE_CHARS_DEFAULT", "30000"))
MAX_SOURCE_CHARS_LIGHT = int(os.environ.get("AUTO_INGEST_MAX_SOURCE_CHARS_LIGHT", "18000"))
MAX_SOURCE_CHARS_VISION = int(os.environ.get("AUTO_INGEST_MAX_SOURCE_CHARS_VISION", "24000"))
INCLUDE_EXISTING_PAGES_CONTEXT = os.environ.get(
    "AUTO_INGEST_INCLUDE_EXISTING_PAGES_CONTEXT", "1"
).strip().lower() not in {"0", "false", "no"}


@dataclass(frozen=True)
class IngestRoute:
    lane: str
    model: str
    priority: int
    max_source_chars: int
    source_class: str
    checkpoint_class: str = ""
    retention_mode: str = RETAIN


def classify_ingest_route(
    fm: dict,
    *,
    has_images: bool = False,
    model_override: str | None = None,
    body: str | None = None,
) -> IngestRoute:
    """Classify a raw source into a model lane + queue priority.

    Priority is ascending: lower numbers are processed first. Interactive/user-
    supplied sources should win ahead of backlog-style promotions from sessions.
    """
    source = str(fm.get("source", "")).strip().lower()
    source_type = str(fm.get("type", "text")).strip().lower()
    source_url = str(fm.get("url", "")).strip().lower()
    tags = fm.get("tags", []) if isinstance(fm.get("tags"), list) else []
    tags_lower = {str(tag).strip().lower() for tag in tags}

    if model_override:
        return IngestRoute(
            lane="override",
            model=model_override,
            priority=0,
            max_source_chars=MAX_SOURCE_CHARS_DEFAULT,
            source_class="manual-override",
        )

    if has_images:
        return IngestRoute(
            lane="vision",
            model=MODEL_VISION,
            priority=0,
            max_source_chars=MAX_SOURCE_CHARS_VISION,
            source_class="vision-source",
        )

    if source == "copilot-session-curator" or "copilot-session" in tags_lower:
        # Honour the class written by the curator if present; otherwise
        # re-classify from the title + body so legacy/backlog imports still
        # benefit from retention logic.
        cp_class = str(fm.get("checkpoint_class", "")).strip().lower()
        if cp_class not in {"durable-architecture", "durable-debugging",
                            "durable-workflow", "project-progress",
                            "low-signal"}:
            classification = classify_checkpoint(
                str(fm.get("title", "")),
                body or "",
            )
            cp_class = classification.cls
        retention = str(fm.get("retention_mode", "")).strip().lower()
        if retention not in {RETAIN, COMPRESS, SKIP}:
            retention = resolve_retention(cp_class)
        return IngestRoute(
            lane="light",
            model=MODEL_LIGHT,
            priority=30,
            max_source_chars=MAX_SOURCE_CHARS_LIGHT,
            source_class="copilot-session-checkpoint",
            checkpoint_class=cp_class,
            retention_mode=retention,
        )

    if source == "mempalace-bridge" or "mempalace" in tags_lower:
        return IngestRoute(
            lane="light",
            model=MODEL_LIGHT,
            priority=20,
            max_source_chars=MAX_SOURCE_CHARS_LIGHT,
            source_class="mempalace-export",
        )

    if source_type == "url" or source_url:
        return IngestRoute(
            lane="default",
            model=MODEL_DEFAULT,
            priority=0,
            max_source_chars=MAX_SOURCE_CHARS_DEFAULT,
            source_class="url-source",
        )

    return IngestRoute(
        lane="default",
        model=MODEL_DEFAULT,
        priority=10,
        max_source_chars=MAX_SOURCE_CHARS_DEFAULT,
        source_class="text-source",
    )


# ---------------------------------------------------------------------------
# Frontmatter helpers
# ---------------------------------------------------------------------------


def parse_frontmatter(path: Path) -> tuple[dict, str]:
    """Return (frontmatter_dict, body) from a markdown file."""
    content = path.read_text()
    if not content.startswith("---"):
        return {}, content

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content

    fm: dict = {}
    current_key: str | None = None
    current_list: list[str] | None = None

    for line in parts[1].strip().split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        # List item under a key
        if stripped.startswith("- ") and current_key is not None:
            if current_list is None:
                current_list = []
            current_list.append(stripped[2:].strip().strip('"').strip("'"))
            fm[current_key] = current_list
            continue

        # Key: value line
        if ":" in stripped:
            # Save pending list
            if current_list is not None:
                current_list = None

            key, _, value = stripped.partition(":")
            key = key.strip()
            value = value.strip()

            if value == "" or value == "[]":
                current_key = key
                if value == "[]":
                    fm[key] = []
                    current_list = None
                else:
                    current_list = []
                continue

            # Inline list: [a, b, c]
            if value.startswith("[") and value.endswith("]"):
                items = [
                    v.strip().strip('"').strip("'")
                    for v in value[1:-1].split(",")
                    if v.strip()
                ]
                fm[key] = items
                current_key = key
                current_list = None
                continue

            fm[key] = value.strip('"').strip("'")
            current_key = key
            current_list = None

    return fm, parts[2].strip()


def slugify(title: str) -> str:
    """Convert a title to a kebab-case filename slug."""
    s = title.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s.strip("-")[:80]


def compute_sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


# ---------------------------------------------------------------------------
# GitHub repo tree crawling
# ---------------------------------------------------------------------------

# File extensions worth fetching from repos (lowercase)
_CRAWL_EXTENSIONS = {
    ".md", ".txt", ".rst",                         # docs
    ".py", ".js", ".ts", ".go", ".rs", ".sh",      # code
    ".yml", ".yaml", ".toml", ".json", ".ini",      # config
    ".cfg", ".env.example", ".conf",                # config
}
# Exact filenames to always include (case-insensitive match)
_CRAWL_EXACT = {
    "dockerfile", "makefile", "justfile", "procfile",
    "caddyfile", "gemfile", "rakefile",
    ".env.example", ".gitignore", "license",
}
# Directories to prioritise (contents fetched first)
_PRIORITY_DIRS = ("docs", "doc", "documentation", "guides", "wiki")
# Max individual file size (chars) to include
_MAX_FILE_CHARS = 8_000


def _should_crawl(path: str) -> bool:
    """Return True if a tree entry is worth fetching."""
    name = path.rsplit("/", 1)[-1].lower()
    if name in _CRAWL_EXACT:
        return True
    _, ext = os.path.splitext(name)
    return ext.lower() in _CRAWL_EXTENSIONS


def _priority_sort_key(path: str) -> tuple[int, str]:
    """Sort key: priority dirs first, then docs, then alphabetical."""
    lower = path.lower()
    parts = lower.split("/")
    # Top-level priority dirs first
    if any(p in _PRIORITY_DIRS for p in parts):
        return (0, lower)
    # Root-level files next
    if "/" not in path:
        return (1, lower)
    return (2, lower)


def _crawl_github_tree(
    owner: str,
    repo: str,
    headers: dict[str, str],
    budget: int = 30_000,
) -> list[str]:
    """Recursively crawl a GitHub repo and return file contents as sections.

    Uses the Git Trees API (single request) then fetches individual files
    via the raw content endpoint.  Stays within *budget* total characters.
    """
    # 1. Get recursive tree (single API call)
    tree_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/HEAD?recursive=1"
    try:
        resp = httpx.get(
            tree_url, headers=headers,
            follow_redirects=True, timeout=URL_FETCH_TIMEOUT,
        )
        resp.raise_for_status()
    except Exception as e:
        log.warning("GitHub tree API failed for %s/%s: %s", owner, repo, e)
        return []

    tree = resp.json().get("tree", [])

    # 2. Filter to crawlable blobs (skip README — already fetched)
    candidates = [
        entry["path"]
        for entry in tree
        if entry.get("type") == "blob"
        and _should_crawl(entry["path"])
        and entry["path"].lower() not in ("readme.md", "readme.txt", "readme.rst", "readme")
    ]
    candidates.sort(key=_priority_sort_key)

    log.info(
        "GitHub tree crawl: %d total entries, %d crawlable files",
        len(tree), len(candidates),
    )

    # 3. Fetch file contents within budget
    parts: list[str] = []
    used = 0
    raw_headers = {**headers, "Accept": "application/vnd.github.raw+json"}

    for fpath in candidates:
        if used >= budget:
            remaining = len(candidates) - len(parts)
            parts.append(f"\n(… {remaining} more files omitted due to size limit)")
            break

        raw_url = (
            f"https://api.github.com/repos/{owner}/{repo}/contents/{fpath}"
        )
        try:
            file_resp = httpx.get(
                raw_url, headers=raw_headers,
                follow_redirects=True, timeout=15,
            )
            file_resp.raise_for_status()
        except Exception as e:
            log.debug("Skipping %s: %s", fpath, e)
            continue

        text = file_resp.text[:_MAX_FILE_CHARS]
        section = f"\n## File: {fpath}\n\n```\n{text}\n```\n"
        parts.append(section)
        used += len(section)
        log.debug("Crawled %s (%d chars, budget %d/%d)", fpath, len(text), used, budget)

    log.info("GitHub crawl fetched %d files (%d chars)", len(parts), used)
    return parts


# ---------------------------------------------------------------------------
# URL content fetching
# ---------------------------------------------------------------------------


def fetch_url_content(url: str) -> UrlFetchResult:
    """Fetch text content from a URL.

    Handles Twitter/X, GitHub repos, GitHub gists, and generic HTML.
    """
    # --- arxiv handler: rewrite /pdf/ and /abs/ to /html/ for full text ---
    arxiv_match = re.match(
        r"https?://arxiv\.org/(?:pdf|abs)/(\d+\.\d+)(?:v\d+)?(?:\.pdf)?$", url
    )
    if arxiv_match:
        paper_id = arxiv_match.group(1)
        html_url = f"https://arxiv.org/html/{paper_id}"
        log.info("arxiv detected — rewriting to HTML: %s → %s", url, html_url)
        try:
            resp = httpx.get(
                html_url,
                headers={"User-Agent": "Mozilla/5.0 (compatible; labs-wiki-bot/1.0)"},
                follow_redirects=True,
                timeout=URL_FETCH_TIMEOUT,
            )
            resp.raise_for_status()
            if "html" in resp.headers.get("content-type", ""):
                log.info("arxiv HTML version available, fetching full paper")
                return fetch_url_content(html_url)
        except Exception:
            pass
        # Fallback: fetch the abstract page
        abs_url = f"https://arxiv.org/abs/{paper_id}"
        log.warning("arxiv HTML not available for %s, falling back to abstract", paper_id)
        return fetch_url_content(abs_url)

    # --- t.co redirect handler ---
    if re.match(r"https?://t\.co/", url):
        log.info("Resolving t.co redirect: %s", url)
        try:
            resp = httpx.head(url, follow_redirects=True, timeout=URL_FETCH_TIMEOUT)
            resolved = str(resp.url)
            log.info("t.co resolved to: %s", resolved)
            return fetch_url_content(resolved)
        except Exception as e:
            log.warning("Failed to resolve t.co URL %s: %s", url, e)
            return UrlFetchResult(text="", image_urls=[], resolved_url=url, content_type=None)

    # --- Twitter/X handler ---
    twitter_pattern = re.match(
        r"https?://(?:(?:www\.)?(?:twitter\.com|x\.com)|[fv]xtwitter\.com)/([^/]+)/status/(\d+)",
        url,
    )
    if twitter_pattern:
        _user, tweet_id = twitter_pattern.groups()
        log.info("Fetching tweet via fxtwitter API: %s", tweet_id)
        try:
            api_url = f"https://api.fxtwitter.com/i/status/{tweet_id}"
            resp = httpx.get(
                api_url,
                follow_redirects=True,
                timeout=URL_FETCH_TIMEOUT,
                headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"},
            )
            resp.raise_for_status()
            data = resp.json()
            tweet = data.get("tweet", {})

            author = tweet.get("author", {})
            author_name = author.get("name", "Unknown")
            screen_name = author.get("screen_name", "")
            created_at = tweet.get("created_at", "")
            text = tweet.get("text", "")

            parts = [
                f"Tweet by {author_name} (@{screen_name})",
                f"Date: {created_at}" if created_at else "",
                "",
                text,
            ]

            # Quoted tweet
            quote = tweet.get("quote")
            if quote:
                q_author = quote.get("author", {})
                parts.append("")
                parts.append(
                    f"> Quoting @{q_author.get('screen_name', '?')}: {quote.get('text', '')}"
                )

            image_urls: list[str] = []
            media = tweet.get("media", {})
            if media:
                photos = media.get("photos", [])
                for photo in photos[:MAX_IMAGES]:
                    photo_url = photo.get("url", "")
                    if photo_url:
                        image_urls.append(photo_url)

            content = "\n".join(p for p in parts)
            return UrlFetchResult(
                text=content[:50_000],
                image_urls=image_urls,
                resolved_url=url,
                content_type="application/json",
            )
        except Exception as e:
            log.warning("fxtwitter API failed for %s: %s", tweet_id, e)
            return UrlFetchResult(text="", image_urls=[], resolved_url=url, content_type=None)

    # --- GitHub repo handler ---
    clean_url = re.sub(r"[?#].*$", "", url)
    repo_match = re.match(r"https?://github\.com/([^/]+)/([^/]+)/?$", clean_url)
    if repo_match:
        owner, repo = repo_match.groups()
        log.info("Fetching GitHub repo info: %s/%s", owner, repo)
        gh_token = os.environ.get("GITHUB_TOKEN", "") or os.environ.get(
            "GITHUB_MODELS_TOKEN", ""
        )
        gh_headers: dict[str, str] = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "labs-wiki-bot/1.0",
        }
        if gh_token:
            gh_headers["Authorization"] = f"Bearer {gh_token}"

        parts = []
        try:
            repo_resp = httpx.get(
                f"https://api.github.com/repos/{owner}/{repo}",
                headers=gh_headers,
                follow_redirects=True,
                timeout=URL_FETCH_TIMEOUT,
            )
            repo_resp.raise_for_status()
            info = repo_resp.json()
            parts.append(f"Repository: {info.get('full_name', f'{owner}/{repo}')}")
            parts.append(f"Description: {info.get('description', 'N/A')}")
            parts.append(f"Stars: {info.get('stargazers_count', 0)}")
            parts.append(f"Language: {info.get('language', 'N/A')}")
            topics = info.get("topics", [])
            if topics:
                parts.append(f"Topics: {', '.join(topics)}")
            parts.append("")
        except Exception as e:
            log.warning("GitHub repo API failed for %s/%s: %s", owner, repo, e)
            parts.append(f"Repository: {owner}/{repo}")
            parts.append("")

        # Fetch README
        try:
            readme_headers = {**gh_headers, "Accept": "application/vnd.github.raw+json"}
            readme_resp = httpx.get(
                f"https://api.github.com/repos/{owner}/{repo}/readme",
                headers=readme_headers,
                follow_redirects=True,
                timeout=URL_FETCH_TIMEOUT,
            )
            readme_resp.raise_for_status()
            parts.append("## README\n")
            parts.append(readme_resp.text[:20_000])
        except Exception as e:
            log.warning("GitHub README fetch failed for %s/%s: %s", owner, repo, e)

        # Crawl repo tree for additional files
        try:
            parts.extend(
                _crawl_github_tree(owner, repo, gh_headers, budget=30_000)
            )
        except Exception as e:
            log.warning("GitHub tree crawl failed for %s/%s: %s", owner, repo, e)

        return UrlFetchResult(
            text="\n".join(parts)[:50_000],
            image_urls=[],
            resolved_url=url,
            content_type="application/vnd.github+json",
        )

    # --- GitHub gist handler ---
    gist_match = re.match(
        r"https://gist\.github\.com/([^/]+)/([a-f0-9]+)", url
    )
    if gist_match:
        user, gist_id = gist_match.groups()
        raw_url = f"https://gist.githubusercontent.com/{user}/{gist_id}/raw"
        log.info("Fetching GitHub gist raw content: %s", raw_url)
        resp = httpx.get(raw_url, follow_redirects=True, timeout=URL_FETCH_TIMEOUT)
        resp.raise_for_status()
        return UrlFetchResult(
            text=resp.text,
            image_urls=[],
            resolved_url=str(resp.url),
            content_type=resp.headers.get("content-type"),
        )

    # --- Default HTML handler ---
    log.info("Fetching URL content: %s", url)
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; labs-wiki-bot/1.0)",
        "Accept": "text/html,text/plain,application/json",
    }
    resp = httpx.get(url, headers=headers, follow_redirects=True, timeout=URL_FETCH_TIMEOUT)
    resp.raise_for_status()

    content_type = resp.headers.get("content-type", "")

    # Reject binary formats that can't be meaningfully parsed as text
    if "application/pdf" in content_type:
        log.warning("URL returned PDF binary (unsupported): %s", url)
        return UrlFetchResult(
            text=f"[PDF document at {url} — content could not be extracted]",
            image_urls=[],
            resolved_url=str(resp.url),
            content_type=content_type,
        )

    if "html" in content_type:
        raw_html = resp.text
        return UrlFetchResult(
            text=normalize_html_document(raw_html),
            image_urls=extract_image_urls(raw_html, str(resp.url)),
            resolved_url=str(resp.url),
            content_type=content_type,
        )

    return UrlFetchResult(
        text=resp.text[:50_000],
        image_urls=[],
        resolved_url=str(resp.url),
        content_type=content_type,
    )


def download_images_as_base64(image_urls: list[str], max_count: int = MAX_IMAGES) -> list[str]:
    """Download images and return as base64 data URIs for vision API."""
    results: list[str] = []
    for img_url in image_urls[:max_count]:
        try:
            resp = httpx.get(
                img_url,
                follow_redirects=True,
                timeout=15,
                headers={"User-Agent": "Mozilla/5.0 (compatible; labs-wiki-bot/1.0)"},
            )
            resp.raise_for_status()

            ct = resp.headers.get("content-type", "")
            mime = ct.split(";")[0].strip()
            # Vision API only supports raster formats
            _VISION_MIMES = {"image/png", "image/jpeg", "image/webp", "image/gif"}
            if mime not in _VISION_MIMES:
                log.warning("Skipping unsupported image format %s for %s", mime, img_url)
                continue

            if len(resp.content) > MAX_IMAGE_SIZE:
                log.warning("Skipping oversized image (%d bytes): %s", len(resp.content), img_url)
                continue

            mime = ct.split(";")[0].strip()
            b64 = base64.b64encode(resp.content).decode("ascii")
            results.append(f"data:{mime};base64,{b64}")
            log.debug("Encoded image (%d bytes): %s", len(resp.content), img_url)
        except Exception as e:
            log.warning("Failed to download image %s: %s", img_url, e)
    return results


# ---------------------------------------------------------------------------
# Existing wiki state
# ---------------------------------------------------------------------------


def get_existing_pages(wiki_dir: Path) -> dict[str, str]:
    """Return {title: relative_path} for all existing wiki pages."""
    pages: dict[str, str] = {}
    for category in ("sources", "concepts", "entities", "synthesis"):
        cat_dir = wiki_dir / category
        if not cat_dir.exists():
            continue
        for page in cat_dir.glob("*.md"):
            if page.name in ("index.md", "log.md", ".gitkeep"):
                continue
            fm, _ = parse_frontmatter(page)
            title = fm.get("title", page.stem.replace("-", " ").title())
            pages[title] = str(page.relative_to(wiki_dir.parent))
    return pages


FUZZY_MERGE_THRESHOLD = 85  # token_set_ratio score above this triggers a merge


def find_fuzzy_match(
    new_title: str,
    category: str,
    wiki_dir: Path,
    threshold: int = FUZZY_MERGE_THRESHOLD,
) -> Path | None:
    """Find an existing page in `wiki_dir/<category>/` whose title fuzzy-matches.

    Returns the matched Path or None. Used to prevent the LLM from creating
    near-duplicate concept/entity pages (e.g. "Linear Regression" vs
    "Linear Regression Algorithm").
    """
    if not _FUZZ_AVAILABLE or not new_title:
        return None
    cat_dir = wiki_dir / category
    if not cat_dir.exists():
        return None
    best_score = 0
    best_path: Path | None = None
    for page in cat_dir.glob("*.md"):
        if page.name in ("index.md", "log.md", ".gitkeep"):
            continue
        try:
            fm, _ = parse_frontmatter(page)
        except Exception:
            continue
        existing_title = fm.get("title") or page.stem.replace("-", " ").title()
        score = _rf_fuzz.token_set_ratio(new_title.lower(), str(existing_title).lower())
        if score > best_score:
            best_score = score
            best_path = page
    if best_score >= threshold and best_path is not None:
        return best_path
    return None


def check_already_processed(wiki_dir: Path, source_hash: str) -> bool:
    """Check if a source with this hash has already been processed."""
    sources_dir = wiki_dir / "sources"
    if not sources_dir.exists():
        return False
    for page in sources_dir.glob("*.md"):
        fm, _ = parse_frontmatter(page)
        if fm.get("source_hash") == source_hash:
            log.info("Source already processed (hash match): %s", page.name)
            return True
    return False


# ---------------------------------------------------------------------------
# LLM extraction
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = textwrap.dedent("""\
    You are a knowledge extraction agent for a personal wiki system.
    Given a source document, you extract structured knowledge that will
    become standalone wiki pages — each page should be a useful reference
    on its own, not just a pointer back to the source.

    ## Rules
    1. Extract CONCEPTS — ideas, techniques, patterns, methodologies
    2. Extract ENTITIES — tools, people, organizations, datasets, models
    3. Write a SOURCE SUMMARY — concise overview of the document
    4. Suggest SYNTHESIS opportunities when the source overlaps with existing wiki pages
    5. Every claim must be grounded in the source — no hallucination
    6. Use Title Case for all titles (e.g., "Rotary Position Embedding")
    7. Slugs are kebab-case (e.g., "rotary-position-embedding")
    8. If the source is short or is just a link/stub, extract what you can — it's OK to have few or no concepts/entities
    9. If images are included, describe any charts, diagrams, code screenshots, or text visible in them
    10. For chart/diagram images, extract the underlying data and relationships shown
    11. Note in the output when information came from an image rather than text

    ## CRITICAL: Provenance & Accuracy
    - Do NOT reference external URLs, websites, or resources that are not mentioned in the source document
    - Do NOT fabricate dates: use null for created_year/publication_date if not explicitly stated in the source
    - Do NOT cite external sources (e.g., Wikipedia, GeeksforGeeks) in concept/entity descriptions — only cite the raw source
    - For related_concepts in concepts: only reference concepts you are extracting OR that appear in the EXISTING WIKI PAGES list
    - For entities: fill in related_entities with other entities from THIS SAME source (e.g., co-authors, related tools)

    ## CRITICAL: Depth Over Breadth
    - Extract at most 3-4 concepts — pick the MOST important ones and go deep
    - Write THOROUGH, DETAILED content for each concept — aim for 5+ substantial paragraphs in how_it_works
    - Include specific details: formulas (use LaTeX where appropriate), algorithm pseudocode, step-by-step processes, complexity analysis
    - Transfer ALL useful information from the source into the extraction — don't summarize away details
    - If the source contains code examples, pseudocode, or mathematical notation, PRESERVE them verbatim
    - If the source contains performance characteristics (time/space complexity), include them in key_properties
    - Each concept should read as a standalone mini-article that someone could learn from WITHOUT reading the source
    - how_it_works should explain the WHY, not just the WHAT — include intuition, trade-offs, and edge cases
    - A concept with 500+ words in how_it_works is better than 5 concepts with 50 words each

    ## Synthesis Suggestions
    Look at the EXISTING WIKI PAGES list provided. If the current source covers topics
    that OVERLAP or CONTRAST with concepts already in the wiki, suggest synthesis pages.
    Good synthesis candidates:
    - Two algorithms that solve the same problem differently (e.g., SVM vs Decision Tree)
    - Competing approaches or frameworks
    - Evolution of a technique (old approach vs new approach)
    - Trade-off analysis (e.g., accuracy vs interpretability)
    Only suggest synthesis when there is genuine overlap — do NOT force it. Max 2 suggestions.
    Leave the array empty if nothing warrants comparison.

    ## Output Format
    Return ONLY valid JSON matching this schema (no markdown fencing):
    {
      "source_summary": {
        "title": "Source Title",
        "summary": "2-3 sentence summary of the source",
        "key_points": ["point 1", "point 2", "point 3"],
        "author": "Author name or null",
        "publication_date": "Date or null",
        "source_type": "article|paper|video|note|gist|guide|tweet|repo",
        "notable_quotes": [{"quote": "...", "attribution": "..."}]
      },
      "concepts": [
        {
          "title": "Concept Title",
          "slug": "concept-slug",
          "overview": "2-4 sentence explanation establishing what this is and why it matters",
          "how_it_works": "Multi-paragraph detailed explanation (5+ paragraphs). Include the mechanism, algorithm steps, mathematical formulas, intuition for WHY it works, and internal logic. Use markdown formatting (lists, bold, code blocks, LaTeX). Cover edge cases and trade-offs.",
          "key_properties": [
            {"name": "Property", "description": "Detailed description with specifics (e.g., 'Time Complexity: O(n log n) for training, O(log n) for prediction')"}
          ],
          "limitations": "Known weaknesses, failure modes, or assumptions that can break down. Be specific — include when and why it fails.",
          "example": "A concrete example, use case walkthrough, or pseudocode snippet showing how this works in practice. Use markdown code blocks if appropriate.",
          "visual_description": "Description of any diagram, chart, or figure from the source that illustrates this concept. Null if no relevant image.",
          "related_concepts": [{"title": "Other Concept", "relationship": "how they relate"}],
          "practical_applications": "Specific real-world uses with enough detail to understand when and why to apply this",
          "tags": ["tag1", "tag2"]
        }
      ],
      "entities": [
        {
          "title": "Entity Name",
          "slug": "entity-slug",
          "overview": "2-3 sentence description with specific, substantive detail — not just a one-liner",
          "entity_type": "Tool|Person|Organization|Dataset|Model|Framework",
          "created_year": "Year or null — ONLY if explicitly stated in source, otherwise null",
          "creator": "Creator or null — ONLY if explicitly stated in source, otherwise null",
          "url": "Official URL or null — ONLY if a real, verified URL appears in the source",
          "status": "Active|Deprecated|Historical",
          "relevance": "Why this matters in 2-3 sentences with specific details from the source",
          "associated_concepts": [{"title": "...", "relationship": "..."}],
          "related_entities": [{"title": "Other Entity From This Source", "relationship": "e.g., co-author, sub-project, parent org"}],
          "tags": ["tag1", "tag2"]
        }
      ],
      "synthesis_suggestions": [
        {
          "title": "Synthesis Page Title (e.g., Decision Trees vs Random Forests)",
          "slug": "synthesis-slug",
          "question": "The cross-cutting question this synthesis answers",
          "concepts_to_compare": ["Existing Wiki Page Title 1", "Existing Wiki Page Title 2"],
          "dimensions": ["dimension 1 to compare", "dimension 2", "dimension 3"],
          "rationale": "Why this comparison adds value to the wiki"
        }
      ],
      "tags": ["tag1", "tag2"]
    }
""")


def call_llm(
    content: str,
    source_title: str,
    source_url: str | None,
    existing_pages: dict[str, str],
    token: str,
    model: str,
    *,
    max_source_chars: int = MAX_SOURCE_CHARS_DEFAULT,
    images: list[str] | None = None,
) -> dict:
    """Call GitHub Models API to extract knowledge from source content."""
    client = OpenAI(base_url=GITHUB_MODELS_URL, api_key=token)

    if INCLUDE_EXISTING_PAGES_CONTEXT:
        existing_list = "\n".join(
            f"- {title} ({path})" for title, path in sorted(existing_pages.items())
        )
        if not existing_list:
            existing_list = "(no existing pages yet)"
    else:
        existing_list = "(existing wiki page context suppressed for this ingest run)"

    user_prompt = f"""## Source Document
Title: {source_title}
{"URL: " + source_url if source_url else ""}

## Existing Wiki Pages (for cross-referencing, avoid duplicates)
{existing_list}

## Content
{content[:max_source_chars]}"""

    # Build user message: multimodal if images present, plain text otherwise
    if images:
        user_content: list[dict] = [{"type": "text", "text": user_prompt}]
        for img_uri in images:
            user_content.append({"type": "image_url", "image_url": {"url": img_uri}})
        user_message: str | list[dict] = user_content
    else:
        user_message = user_prompt

    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            log.info("LLM call attempt %d/%d (model: %s)", attempt, MAX_RETRIES, model)
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_message},
                ],
                temperature=0.3,
                max_tokens=16000,
                response_format={"type": "json_object"},
            )
            raw = response.choices[0].message.content
            return json.loads(raw)
        except Exception as e:
            message = str(e).lower()
            status_code = getattr(e, "status_code", None)
            if "budget limit" in message and (status_code == 403 or "403" in message):
                raise RuntimeError(f"GitHub Models budget limit reached: {e}") from e
            last_error = e
            log.warning("LLM call attempt %d failed: %s", attempt, e)
            if attempt < MAX_RETRIES:
                import time
                time.sleep(2 ** attempt)

    raise RuntimeError(f"LLM call failed after {MAX_RETRIES} attempts: {last_error}")


# ---------------------------------------------------------------------------
# Synthesis LLM call
# ---------------------------------------------------------------------------

SYNTHESIS_SYSTEM_PROMPT = textwrap.dedent("""\
    You are a synthesis writer for a personal knowledge wiki.
    Given two or more wiki concept/entity pages, you produce a SYNTHESIS page
    that compares, contrasts, and connects them.

    ## Rules
    1. Every claim must be grounded in the provided wiki pages — no hallucination
    2. Be SPECIFIC — use concrete details, numbers, formulas from the source pages
    3. The synthesis should answer a clear question (provided in the prompt)
    4. Include a structured comparison table with 4-6 meaningful dimensions
    5. The Analysis section should be 3-5 paragraphs identifying patterns,
       trade-offs, and practical decision criteria
    6. Key Insights should be non-obvious observations that emerge from the comparison
    7. Open Questions should identify genuine gaps where more sources are needed

    ## Output Format
    Return ONLY valid JSON (no markdown fencing):
    {
      "title": "Synthesis Title",
      "question": "The cross-cutting question this answers",
      "summary": "2-3 sentence answer to the question",
      "comparison": [
        {
          "dimension": "Dimension Name",
          "entries": [
            {"concept": "Concept A", "description": "How A handles this"},
            {"concept": "Concept B", "description": "How B handles this"}
          ]
        }
      ],
      "analysis": "3-5 paragraph deep analysis in markdown. Cover: when to choose each, performance trade-offs, common misconceptions, how they complement each other.",
      "key_insights": [
        {"insight": "Non-obvious observation", "supporting_pages": ["Page Title 1", "Page Title 2"]}
      ],
      "open_questions": ["Question 1", "Question 2"],
      "tags": ["tag1", "tag2"]
    }
""")

MAX_SYNTHESIS_PER_INGEST = max(
    0,
    int(os.environ.get("AUTO_INGEST_MAX_SYNTHESIS_PER_INGEST", "2")),
)

# Checkpoint-family synthesis trigger: minimum number of checkpoint sources
# (including the freshly-ingested one) that must share concepts before we
# auto-suggest a cross-checkpoint synthesis. Default shared=1 because the
# current concept extractor produces hyper-specific concepts that almost never
# repeat verbatim across checkpoints (52 checkpoints / 140 unique concepts /
# max 2 hits per concept on the existing corpus). Operators with denser concept
# graphs can raise this via env.
CHECKPOINT_FAMILY_MIN_SIZE = max(
    2,
    int(os.environ.get("AUTO_INGEST_CHECKPOINT_FAMILY_MIN", "3")),
)
CHECKPOINT_FAMILY_MIN_SHARED = max(
    1,
    int(os.environ.get("AUTO_INGEST_CHECKPOINT_FAMILY_SHARED", "1")),
)


def find_checkpoint_family(
    wiki_dir: Path,
    concept_slugs: list[str],
    exclude_slug: str | None = None,
) -> list[tuple[Path, set[str]]]:
    """Find existing checkpoint source pages that share >= CHECKPOINT_FAMILY_MIN_SHARED
    concepts with the given slug list.

    Returns a list of (path, shared_slugs) tuples, sorted by overlap size descending.
    """
    if not concept_slugs:
        return []
    target = set(concept_slugs)
    fam: list[tuple[Path, set[str]]] = []
    sources_dir = wiki_dir / "sources"
    if not sources_dir.is_dir():
        return []
    for src in sources_dir.glob("copilot-session-checkpoint-*.md"):
        if exclude_slug and src.stem == exclude_slug:
            continue
        try:
            fm, _ = parse_frontmatter(src)
        except Exception:
            continue
        their = fm.get("concepts") or []
        if not isinstance(their, list):
            continue
        shared = target & set(their)
        if len(shared) >= CHECKPOINT_FAMILY_MIN_SHARED:
            fam.append((src, shared))
    fam.sort(key=lambda x: len(x[1]), reverse=True)
    return fam


def call_llm_synthesis(
    concept_pages: dict[str, str],
    question: str,
    dimensions: list[str],
    token: str,
    model: str,
) -> dict | None:
    """Call LLM to generate synthesis content from existing wiki pages.

    Args:
        concept_pages: {title: page_content} for the pages to compare
        question: The cross-cutting question to answer
        dimensions: Suggested comparison dimensions
        token: API token
        model: Model ID

    Returns:
        Parsed JSON synthesis or None on failure.
    """
    client = OpenAI(base_url=GITHUB_MODELS_URL, api_key=token)

    pages_text = "\n\n---\n\n".join(
        f"## {title}\n\n{content}" for title, content in concept_pages.items()
    )

    user_prompt = f"""## Synthesis Task

Question: {question}

Suggested comparison dimensions: {', '.join(dimensions)}

## Wiki Pages to Synthesize

{pages_text[:25_000]}"""

    try:
        log.info("Synthesis LLM call (model: %s, pages: %d)", model, len(concept_pages))
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYNTHESIS_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,
            max_tokens=8000,
            response_format={"type": "json_object"},
        )
        raw = response.choices[0].message.content
        return json.loads(raw)
    except Exception as e:
        log.warning("Synthesis LLM call failed: %s", e)
        return None


# ---------------------------------------------------------------------------
# Wiki page generation
# ---------------------------------------------------------------------------


def generate_source_page(
    extraction: dict,
    raw_path: str,
    source_hash: str,
    source_url: str | None,
    today: str,
    raw_tags: list[str],
    *,
    checkpoint_class: str = "",
    retention_mode: str = RETAIN,
    knowledge_state: str = "",
) -> tuple[str, str]:
    """Generate source summary page. Returns (filename, content)."""
    ss = extraction["source_summary"]
    title = ss["title"]
    slug = slugify(title)
    filename = f"{slug}.md"

    concept_slugs = [c["slug"] for c in extraction.get("concepts", [])]
    concept_links = [
        f'  - "[[{c["title"]}]]"' for c in extraction.get("concepts", [])
    ]
    entity_links = [
        f'  - "[[{e["title"]}]]"' for e in extraction.get("entities", [])
    ]
    related = concept_links + entity_links

    tags = list(set(raw_tags + extraction.get("tags", [])))

    # Key points
    key_points = "\n".join(f"- {p}" for p in ss.get("key_points", []))

    # Concepts extracted
    concepts_section = "\n".join(
        f'- **[[{c["title"]}]]** — {c["overview"]}'
        for c in extraction.get("concepts", [])
    )

    # Entities mentioned
    entities_section = "\n".join(
        f'- **[[{e["title"]}]]** — {e["overview"]}'
        for e in extraction.get("entities", [])
    )

    # Quotes
    quotes_section = "\n".join(
        f'> "{q["quote"]}" — {q["attribution"]}'
        for q in ss.get("notable_quotes", [])
    )

    # Tier defaults to "hot" for new source pages but compressed checkpoints
    # land in "archive" so they don't bubble up in hot.md / surfacing lists.
    page_tier = "archive" if (checkpoint_class and retention_mode == COMPRESS) else "hot"

    extra_fm: list[str] = []
    if checkpoint_class:
        extra_fm.append(f"checkpoint_class: {checkpoint_class}")
        extra_fm.append(f"retention_mode: {retention_mode}")
    if knowledge_state:
        extra_fm.append(f"knowledge_state: {knowledge_state}")
    extra_fm_block = ("\n" + "\n".join(extra_fm)) if extra_fm else ""

    content = f"""---
title: "{title}"
type: source
created: {today}
last_verified: {today}
source_hash: "{source_hash}"
sources:
  - {raw_path}
quality_score: 0
concepts:
{chr(10).join('  - ' + s for s in concept_slugs) if concept_slugs else '  []'}
related:
{chr(10).join(related) if related else '  []'}
tier: {page_tier}{extra_fm_block}
tags: [{', '.join(tags)}]
---

# {title}

## Summary

{ss.get("summary", "No summary available.")}

## Key Points

{key_points or "- No key points extracted."}

## Concepts Extracted

{concepts_section or "No concepts extracted."}

## Entities Mentioned

{entities_section or "No entities mentioned."}

## Notable Quotes

{quotes_section or "No notable quotes."}

## Source Details

| Field | Value |
|-------|-------|
| Original | `{raw_path}` |
| Type | {ss.get("source_type", "unknown")} |
| Author | {ss.get("author") or "Unknown"} |
| Date | {ss.get("publication_date") or "Unknown"} |
| URL | {source_url or "N/A"} |
"""
    return filename, content


def normalize_checkpoint_source_page(
    page_path: Path,
    checkpoint_class: str,
    retention_mode: str,
    knowledge_state: str = "",
) -> None:
    """Ensure checkpoint source pages carry class/retention/tier frontmatter."""
    if not checkpoint_class or not page_path.exists():
        return

    content = page_path.read_text()
    if not content.startswith("---"):
        return

    parts = content.split("---", 2)
    if len(parts) < 3:
        return

    frontmatter_lines = parts[1].strip().split("\n")
    body = parts[2]
    desired = {
        "checkpoint_class": checkpoint_class,
        "retention_mode": retention_mode,
        "tier": "archive" if retention_mode == COMPRESS else "hot",
    }
    if knowledge_state:
        desired["knowledge_state"] = knowledge_state

    def upsert(lines: list[str], key: str, value: str) -> list[str]:
        prefix = f"{key}:"
        for idx, line in enumerate(lines):
            if line.strip().startswith(prefix):
                lines[idx] = f"{key}: {value}"
                return lines
        insert_at = len(lines)
        for idx, line in enumerate(lines):
            if line.strip().startswith("tags:"):
                insert_at = idx
                break
        lines.insert(insert_at, f"{key}: {value}")
        return lines

    updated_lines = list(frontmatter_lines)
    for key, value in desired.items():
        updated_lines = upsert(updated_lines, key, value)

    normalized = "---\n" + "\n".join(updated_lines) + "\n---" + body
    if normalized != content:
        page_path.write_text(normalized)


def generate_concept_page(
    concept: dict,
    raw_path: str,
    source_hash: str,
    source_title: str,
    today: str,
) -> tuple[str, str]:
    """Generate a concept wiki page. Returns (filename, content)."""
    title = concept["title"]
    slug = concept["slug"]
    filename = f"{slug}.md"

    related_concepts = concept.get("related_concepts", [])
    related_links = [f'  - "[[{r["title"]}]]"' for r in related_concepts]
    related_links.append(f'  - "[[{source_title}]]"')

    relationships = "\n".join(
        f'- **[[{r["title"]}]]** — {r["relationship"]}'
        for r in related_concepts
    )

    properties = "\n".join(
        f'- **{p["name"]}:** {p["description"]}'
        for p in concept.get("key_properties", [])
    )

    content = f"""---
title: "{title}"
type: concept
created: {today}
last_verified: {today}
source_hash: "{source_hash}"
sources:
  - {raw_path}
quality_score: 0
concepts:
  - {slug}
related:
{chr(10).join(related_links)}
tier: hot
tags: [{', '.join(concept.get("tags", []))}]
---

# {title}

## Overview

{concept.get("overview", "No overview available.")}

## How It Works

{concept.get("how_it_works", "Details not yet available.")}

## Key Properties

{properties or "No key properties identified."}
"""

    # Optional sections — only include if present
    limitations = concept.get("limitations")
    if limitations:
        content += f"""
## Limitations

{limitations}
"""

    example = concept.get("example")
    if example:
        content += f"""
## Example

{example}
"""

    visual = concept.get("visual_description")
    if visual:
        content += f"""
## Visual

{visual}
"""

    content += f"""
## Relationship to Other Concepts

{relationships or "No relationships identified yet."}

## Practical Applications

{concept.get("practical_applications", "Applications not yet documented.")}

## Sources

- [[{source_title}]] — primary source for this concept
"""
    return filename, content


def generate_entity_page(
    entity: dict,
    raw_path: str,
    source_hash: str,
    source_title: str,
    today: str,
    all_entities: list[dict] | None = None,
) -> tuple[str, str]:
    """Generate an entity wiki page. Returns (filename, content).

    Args:
        all_entities: Other entities from the same ingest for reciprocal linking.
    """
    title = entity["title"]
    slug = entity["slug"]
    filename = f"{slug}.md"

    assoc = entity.get("associated_concepts", [])
    related_links = [f'  - "[[{a["title"]}]]"' for a in assoc]
    related_links.append(f'  - "[[{source_title}]]"')

    assoc_section = "\n".join(
        f'- **[[{a["title"]}]]** — {a["relationship"]}' for a in assoc
    )

    # Related entities: from LLM extraction + reciprocal links from same batch
    related_ents = list(entity.get("related_entities", []))
    if all_entities:
        existing_titles = {re["title"] for re in related_ents}
        for other in all_entities:
            if other["title"] != title and other["title"] not in existing_titles:
                related_ents.append({
                    "title": other["title"],
                    "relationship": f"co-mentioned in source ({other.get('entity_type', 'entity')})",
                })
                existing_titles.add(other["title"])

    # Add related entity links to frontmatter
    for re_ent in related_ents:
        link = f'  - "[[{re_ent["title"]}]]"'
        if link not in related_links:
            related_links.append(link)

    related_ents_section = "\n".join(
        f'- **[[{re["title"]}]]** — {re["relationship"]}' for re in related_ents
    ) if related_ents else "No related entities documented yet."

    content = f"""---
title: "{title}"
type: entity
created: {today}
last_verified: {today}
source_hash: "{source_hash}"
sources:
  - {raw_path}
quality_score: 0
concepts:
  - {slug}
related:
{chr(10).join(related_links)}
tier: hot
tags: [{', '.join(entity.get("tags", []))}]
---

# {title}

## Overview

{entity.get("overview", "No overview available.")}

## Key Facts

| Field | Value |
|-------|-------|
| Type | {entity.get("entity_type", "Unknown")} |
| Created | {entity.get("created_year") or "Unknown"} |
| Creator | {entity.get("creator") or "Unknown"} |
| URL | {entity.get("url") or "N/A"} |
| Status | {entity.get("status", "Unknown")} |

## Relevance

{entity.get("relevance", "Relevance not yet documented.")}

## Associated Concepts

{assoc_section or "No associated concepts documented."}

## Related Entities

{related_ents_section}

## Sources

- [[{source_title}]] — where this entity was mentioned
"""
    return filename, content


def generate_synthesis_page(
    synthesis: dict,
    raw_paths: list[str],
    source_titles: list[str],
    today: str,
    *,
    extra_frontmatter: dict[str, str] | None = None,
) -> tuple[str, str]:
    """Generate a synthesis wiki page. Returns (filename, content)."""
    title = synthesis.get("title", "Untitled Synthesis")
    slug = slugify(title)
    filename = f"{slug}.md"

    # Build comparison table
    comparison = synthesis.get("comparison", [])
    if comparison:
        # Determine concept columns from first entry
        concepts = [e["concept"] for e in comparison[0].get("entries", [])]
        if not concepts:
            table = "No comparison dimensions available."
            comparison = []  # reset so downstream loops don't break
        else:
            header = "| Dimension | " + " | ".join(f"[[{c}]]" for c in concepts) + " |"
            sep = "|-----------|" + "|".join("---------------------|" for _ in concepts)
            rows = []
            for dim in comparison:
                descs = [e["description"] for e in dim.get("entries", [])]
                rows.append(f"| {dim['dimension']} | " + " | ".join(descs) + " |")
            table = "\n".join([header, sep] + rows)
    else:
        table = "No comparison dimensions available."

    # Key insights
    insights = synthesis.get("key_insights", [])
    insights_section = "\n".join(
        f'{i + 1}. **{ins["insight"]}** — supported by '
        + ", ".join(f'[[{p}]]' for p in ins.get("supporting_pages", []))
        for i, ins in enumerate(insights)
    ) or "No key insights identified."

    # Open questions
    open_qs = synthesis.get("open_questions", [])
    oq_section = "\n".join(f"- {q}" for q in open_qs) or "- No open questions identified."

    # Sources section
    sources_section = "\n".join(f"- [[{t}]]" for t in source_titles)

    # Related links
    all_related = list(set(source_titles + [
        e["concept"]
        for dim in comparison
        for e in dim.get("entries", [])
    ]))
    related_links = "\n".join(f'  - "[[{r}]]"' for r in all_related)

    # Concept slugs from compared items
    concept_slugs = list(set(
        slugify(e["concept"])
        for dim in comparison
        for e in dim.get("entries", [])
    ))

    tags = synthesis.get("tags", [])

    sources_fm = "\n".join(f"  - {rp}" for rp in raw_paths)
    extra_fm_lines = [
        f"{key}: {value}"
        for key, value in (extra_frontmatter or {}).items()
        if str(value).strip()
    ]
    extra_fm_block = ("\n" + "\n".join(extra_fm_lines)) if extra_fm_lines else ""

    content = f"""---
title: "{title}"
type: synthesis
created: {today}
last_verified: {today}
source_hash: "synthesis-generated"
sources:
{sources_fm}
quality_score: 0
concepts:
{chr(10).join('  - ' + s for s in concept_slugs) if concept_slugs else '  []'}
related:
{related_links if related_links else '  []'}
tier: hot{extra_fm_block}
tags: [{', '.join(tags)}]
---

# {title}

## Question

{synthesis.get("question", "Cross-cutting comparison.")}

## Summary

{synthesis.get("summary", "Summary not available.")}

## Comparison

{table}

## Analysis

{synthesis.get("analysis", "Analysis not yet available.")}

## Key Insights

{insights_section}

## Open Questions

{oq_section}

## Sources

{sources_section}
"""
    return filename, content


# ---------------------------------------------------------------------------
# Post-processing: wikilink validation, dedup, quality scoring
# ---------------------------------------------------------------------------


def _get_all_valid_titles(wiki_dir: Path) -> set[str]:
    """Collect all page titles from the wiki."""
    titles: set[str] = set()
    for category in ("sources", "concepts", "entities", "synthesis"):
        cat_dir = wiki_dir / category
        if not cat_dir.exists():
            continue
        for page in cat_dir.glob("*.md"):
            if page.name in ("index.md", "log.md", ".gitkeep"):
                continue
            fm, _ = parse_frontmatter(page)
            title = fm.get("title", "")
            if title:
                titles.add(title)
    return titles


def _wikilink_slug(text: str) -> str:
    """Normalize a wikilink target to the same slug shape used by graph_builder."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text.strip("-")


def _build_wikilink_lookup(wiki_dir: Path) -> tuple[set[str], set[str]]:
    """Return exact-title and slug-based wikilink targets that resolve in the wiki."""
    titles: set[str] = set()
    slugs: set[str] = set()
    for category in ("sources", "concepts", "entities", "synthesis"):
        cat_dir = wiki_dir / category
        if not cat_dir.exists():
            continue
        for page in cat_dir.glob("*.md"):
            if page.name in ("index.md", "hot.md", "log.md", ".gitkeep"):
                continue
            fm, _ = parse_frontmatter(page)
            title = str(fm.get("title") or page.stem.replace("-", " ").title())
            titles.add(title)
            slugs.add(_wikilink_slug(title))
            slugs.add(_wikilink_slug(page.stem))
    return titles, slugs


def _wikilink_target_exists(target: str, valid_titles: set[str], valid_slugs: set[str]) -> bool:
    """Return True when a wikilink target resolves by title or filename slug."""
    key = target.strip()
    return key in valid_titles or _wikilink_slug(key) in valid_slugs


def _compute_quality_score(
    fm: dict,
    has_wikilinks: bool,
    has_related: bool,
) -> int:
    """Compute 0-100 quality score (mirrors lint_wiki.py logic)."""
    score = 0
    required = ["title", "type", "created", "sources"]
    required_present = sum(1 for f in required if f in fm)
    score += int(25 * required_present / len(required))

    if has_wikilinks or has_related:
        score += 25

    if fm.get("sources") and fm["sources"] != "":
        score += 25

    # Freshly created pages are not stale
    score += 25

    return score


def postprocess_created_pages(
    wiki_dir: Path,
    created_pages: list[str],
    project_root: Path,
) -> None:
    """Post-process newly created pages: fix wikilinks, dedup, score.

    1. Validate wikilinks against all existing page titles
    2. Remove self-referential links
    3. Deduplicate related: entries
    4. Compute and write quality_score
    """
    valid_titles, valid_slugs = _build_wikilink_lookup(wiki_dir)
    log.info(
        "Post-processing %d pages (%d valid titles in wiki)",
        len(created_pages), len(valid_titles),
    )

    for rel_path in created_pages:
        page_path = project_root / rel_path
        if not page_path.exists():
            continue

        content = page_path.read_text()
        if not content.startswith("---"):
            continue

        parts = content.split("---", 2)
        if len(parts) < 3:
            continue

        frontmatter_text = parts[1]
        body = parts[2]

        # --- Parse the page title ---
        page_title = ""
        for line in frontmatter_text.strip().split("\n"):
            if line.strip().startswith("title:"):
                page_title = line.split(":", 1)[1].strip().strip('"').strip("'")
                break

        # --- Fix body wikilinks: remove broken ones ---
        def _replace_wikilink(m: re.Match) -> str:
            link_title = m.group(1)
            if link_title == page_title:
                # Self-reference — remove the wikilink, keep the text
                return link_title
            if not _wikilink_target_exists(link_title, valid_titles, valid_slugs):
                # Broken link — keep the text, drop the brackets
                return link_title
            return m.group(0)

        body = re.sub(r"\[\[([^\]]+)\]\]", _replace_wikilink, body)

        # --- Fix frontmatter related: entries ---
        new_fm_lines = []
        in_related = False
        seen_related: set[str] = set()

        for line in frontmatter_text.strip().split("\n"):
            stripped = line.strip()

            if stripped == "related:":
                in_related = True
                new_fm_lines.append(line)
                continue

            if in_related and stripped.startswith("- "):
                # Extract title from "[[Title]]" in the related entry
                link_match = re.search(r"\[\[([^\]]+)\]\]", stripped)
                if link_match:
                    link_title = link_match.group(1)

                    # Skip self-references
                    if link_title == page_title:
                        continue

                    # Skip broken links
                    if not _wikilink_target_exists(link_title, valid_titles, valid_slugs):
                        continue

                    # Skip duplicates
                    if link_title in seen_related:
                        continue

                    seen_related.add(link_title)

                new_fm_lines.append(line)
                continue

            if in_related and not stripped.startswith("- "):
                in_related = False
                # If no valid related entries remain, add empty marker
                if not seen_related:
                    # Check if the last line was "related:"
                    if new_fm_lines and new_fm_lines[-1].strip() == "related:":
                        new_fm_lines.append("  []")

            new_fm_lines.append(line)

        # --- Compute quality score ---
        fm, _ = parse_frontmatter(page_path)
        wikilinks = re.findall(r"\[\[([^\]]+)\]\]", body)
        has_wikilinks = len(wikilinks) > 0
        has_related = len(seen_related) > 0
        score = _compute_quality_score(fm, has_wikilinks, has_related)

        # Update quality_score in frontmatter
        updated_fm_lines = []
        for line in new_fm_lines:
            if line.strip().startswith("quality_score:"):
                updated_fm_lines.append(f"quality_score: {score}")
            else:
                updated_fm_lines.append(line)
        new_fm_lines = updated_fm_lines

        # Reassemble the page
        new_content = "---\n" + "\n".join(new_fm_lines) + "\n---" + body
        page_path.write_text(new_content)
        log.info("Post-processed %s (score: %d, valid links: %d)", rel_path, score, len(seen_related))


# ---------------------------------------------------------------------------
# Log + index
# ---------------------------------------------------------------------------


def append_log(log_path: Path, entry: dict) -> None:
    """Append a YAML log entry to wiki/log.md."""
    content = log_path.read_text() if log_path.exists() else ""
    # Strip trailing ``` if present (the log wraps entries in a yaml block)
    content = content.rstrip()
    if content.endswith("```"):
        content = content[:-3].rstrip()

    targets_yaml = "\n".join(f"    - {t}" for t in entry["targets"])
    block = f"""
- timestamp: {entry["timestamp"]}
  operation: {entry["operation"]}
  agent: auto-ingest
  targets:
{targets_yaml}
  source: {entry["source"]}
  status: {entry["status"]}
  notes: "{entry["notes"]}"
```
"""
    log_path.write_text(content + "\n" + block)


def rebuild_index(project_root: Path) -> None:
    """Run compile_index.py to rebuild wiki/index.md."""
    script = project_root / "scripts" / "compile_index.py"
    if script.exists():
        log.info("Rebuilding wiki/index.md")
        subprocess.run(
            [sys.executable, str(script), "--wiki-dir", str(project_root)],
            check=True,
        )
    else:
        log.warning("compile_index.py not found at %s", script)


def update_raw_status(raw_path: Path, new_status: str) -> None:
    """Update the status field in a raw source's frontmatter."""
    content = raw_path.read_text()
    updated = re.sub(
        r"^(status:\s*).*$",
        f"\\g<1>{new_status}",
        content,
        count=1,
        flags=re.MULTILINE,
    )
    raw_path.write_text(updated)


# ---------------------------------------------------------------------------
# Notification
# ---------------------------------------------------------------------------


def send_ntfy(title: str, message: str, tags: str = "books") -> None:
    """Send a notification via ntfy if configured."""
    server = os.environ.get("NTFY_SERVER", "")
    topic = os.environ.get("NTFY_TOPIC", "")
    if not server or not topic:
        return
    try:
        httpx.post(
            f"{server}/{topic}",
            content=message.encode("utf-8"),
            headers={"Title": title.encode("utf-8").decode("ascii", errors="replace"), "Tags": tags},
            timeout=10,
        )
    except Exception as e:
        log.warning("ntfy notification failed: %s", e)


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------


def ingest_raw_source(
    raw_path: Path,
    project_root: Path,
    token: str,
    model: str | None = None,
    *,
    force: bool = False,
    refresh_fetch: bool = False,
    validation_run: bool = False,
) -> bool:
    """Process a single raw source file. Returns True on success."""
    log.info("Processing: %s", raw_path)

    # Parse raw source
    fm, body = parse_frontmatter(raw_path)
    if not fm:
        log.error("No frontmatter found in %s", raw_path)
        return False

    status = fm.get("status", "pending")
    if status != "pending" and not force:
        log.info("Skipping %s (status: %s)", raw_path.name, status)
        return False

    title = fm.get("title", raw_path.stem)
    source_type = fm.get("type", "text")
    source_url = fm.get("url")
    raw_tags = fm.get("tags", []) if isinstance(fm.get("tags"), list) else []
    route = classify_ingest_route(fm, model_override=model, body=body)

    # For URL sources, prefer the durable fetched-content block. Only fetch
    # when the raw file has never been enriched or the caller explicitly asks
    # to refresh the persisted block.
    content = body
    image_urls: list[str] = []
    persisted_text: str | None = None
    if source_type == "url" and source_url:
        persisted_text, persisted_metadata = read_persisted_fetched_content(body)
        should_fetch = refresh_fetch or not persisted_text
        live_fetch_succeeded = False
        try:
            if should_fetch:
                fetch_result = fetch_url_content(source_url)
                if is_meaningful_fetched_body(fetch_result.text, source_url):
                    persisted_text = fetch_result.text.strip()
                    image_urls = fetch_result.image_urls
                    persisted_metadata = {
                        "image_urls": fetch_result.image_urls,
                    }
                    live_fetch_succeeded = True
                    updated_raw = upsert_fetched_content_block(
                        raw_path.read_text(),
                        build_fetched_content_block(
                            fetched_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
                            source_url=source_url,
                            resolved_url=fetch_result.resolved_url,
                            content_type=fetch_result.content_type,
                            image_urls=fetch_result.image_urls,
                            text=persisted_text,
                        ),
                    )
                    raw_path.write_text(updated_raw)
                    log.info(
                        "Persisted %d chars of fetched content for %s",
                        len(persisted_text),
                        raw_path.name,
                    )
                else:
                    log.warning(
                        "Fetched URL content for %s was not meaningful; leaving raw content unchanged",
                        source_url,
                    )
        except Exception as e:
            log.error("Failed to fetch URL %s: %s", source_url, e)
        if persisted_text and not image_urls and not live_fetch_succeeded:
            persisted_image_urls = persisted_metadata.get("image_urls", [])
            if isinstance(persisted_image_urls, list):
                image_urls = [str(url) for url in persisted_image_urls[:MAX_IMAGES] if str(url)]
        content = build_url_ingest_content(
            body=body,
            source_url=source_url,
            persisted_text=persisted_text,
        )

    # Download and encode images for vision
    images_b64: list[str] = []
    if image_urls:
        log.info("Downloading %d images for vision analysis...", len(image_urls))
        images_b64 = download_images_as_base64(image_urls)
        log.info("Successfully encoded %d images", len(images_b64))
    route = classify_ingest_route(fm, has_images=bool(images_b64), model_override=model, body=body)
    log.info(
        "Ingest route: class=%s lane=%s model=%s priority=%d images=%s checkpoint_class=%s retention=%s",
        route.source_class,
        route.lane,
        route.model,
        route.priority,
        bool(images_b64),
        route.checkpoint_class or "-",
        route.retention_mode,
    )

    if not content or len(content.strip()) < 10:
        log.warning("Source content too short for meaningful extraction")

    # Retention: skip checkpoints classified as low-signal (or whatever the
    # operator has overridden to skip via LABS_WIKI_CHECKPOINT_RETENTION_OVERRIDES).
    # No LLM call, no source page; raw is marked so we don't retry it.
    if route.retention_mode == SKIP:
        log.info(
            "Skipping ingest for %s (checkpoint_class=%s retention=skip)",
            raw_path.name,
            route.checkpoint_class or "-",
        )
        update_raw_status(raw_path, "ingested-skipped")
        return True

    # Compute hash & check incremental
    source_hash = compute_sha256(content)
    wiki_dir = project_root / "wiki"

    if not force and check_already_processed(wiki_dir, source_hash):
        log.info("Already processed, updating status only")
        update_raw_status(raw_path, "ingested")
        return True

    # Get existing wiki state
    existing_pages = get_existing_pages(wiki_dir)

    # LLM extraction
    log.info("Calling LLM for extraction...")
    extraction = call_llm(
        content,
        title,
        source_url,
        existing_pages,
        token,
        route.model,
        max_source_chars=route.max_source_chars,
        images=images_b64,
    )

    planning_only = is_planning_only_checkpoint(
        title,
        body,
        route.checkpoint_class,
        route.retention_mode,
    )
    if planning_only:
        log.info(
            "Planning-only checkpoint detected for %s; keeping archived source summary only",
            raw_path.name,
        )
        extraction["concepts"] = []
        extraction["entities"] = []
        extraction["synthesis_suggestions"] = []
        if "planning-only" not in raw_tags:
            raw_tags = raw_tags + ["planning-only"]

    knowledge_state = derive_knowledge_state(
        title,
        body,
        route.checkpoint_class,
        route.retention_mode,
    )
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    raw_rel = str(raw_path.relative_to(project_root))
    source_title = extraction["source_summary"]["title"]

    created_pages: list[str] = []

    # Generate source summary page
    src_filename, src_content = generate_source_page(
        extraction, raw_rel, source_hash, source_url, today, raw_tags,
        checkpoint_class=route.checkpoint_class,
        retention_mode=route.retention_mode,
        knowledge_state=knowledge_state,
    )
    src_path = wiki_dir / "sources" / src_filename
    src_path.parent.mkdir(parents=True, exist_ok=True)
    src_path.write_text(src_content)
    normalize_checkpoint_source_page(
        src_path,
        route.checkpoint_class,
        route.retention_mode,
        knowledge_state,
    )
    created_pages.append(f"wiki/sources/{src_filename}")
    log.info("Created: wiki/sources/%s", src_filename)

    # Generate concept pages
    for concept in extraction.get("concepts", []):
        filename, page_content = generate_concept_page(
            concept, raw_rel, source_hash, source_title, today,
        )
        concept_path = wiki_dir / "concepts" / filename
        concept_path.parent.mkdir(parents=True, exist_ok=True)

        # Fuzzy-dedupe: redirect to a near-duplicate existing page if any.
        if not concept_path.exists():
            fuzzy_hit = find_fuzzy_match(concept["title"], "concepts", wiki_dir)
            if fuzzy_hit is not None:
                log.info(
                    "Fuzzy-merge: '%s' → existing %s (skipping new file %s)",
                    concept["title"], fuzzy_hit.name, filename,
                )
                concept_path = fuzzy_hit
                filename = fuzzy_hit.name

        if concept_path.exists():
            # Merge: append source reference to existing page
            existing = concept_path.read_text()
            if raw_rel not in existing:
                merge_line = f"\n- [[{source_title}]] — additional source\n"
                existing = existing.rstrip() + merge_line
                # Add raw path to sources in frontmatter
                existing = existing.replace(
                    "sources:", f"sources:\n  - {raw_rel}", 1
                )
                concept_path.write_text(existing)
                log.info("Merged into existing: wiki/concepts/%s", filename)
        else:
            concept_path.write_text(page_content)
            log.info("Created: wiki/concepts/%s", filename)

        created_pages.append(f"wiki/concepts/{filename}")

    # Generate entity pages
    all_entities = extraction.get("entities", [])
    for entity in all_entities:
        filename, page_content = generate_entity_page(
            entity, raw_rel, source_hash, source_title, today,
            all_entities=all_entities,
        )
        entity_path = wiki_dir / "entities" / filename
        entity_path.parent.mkdir(parents=True, exist_ok=True)

        if not entity_path.exists():
            fuzzy_hit = find_fuzzy_match(entity["title"], "entities", wiki_dir)
            if fuzzy_hit is not None:
                log.info(
                    "Fuzzy-merge: '%s' → existing %s (skipping new file %s)",
                    entity["title"], fuzzy_hit.name, filename,
                )
                entity_path = fuzzy_hit
                filename = fuzzy_hit.name

        if entity_path.exists():
            existing = entity_path.read_text()
            if raw_rel not in existing:
                merge_line = f"\n- [[{source_title}]] — additional source\n"
                existing = existing.rstrip() + merge_line
                existing = existing.replace(
                    "sources:", f"sources:\n  - {raw_rel}", 1
                )
                entity_path.write_text(existing)
                log.info("Merged into existing: wiki/entities/%s", filename)
        else:
            entity_path.write_text(page_content)
            log.info("Created: wiki/entities/%s", filename)

        created_pages.append(f"wiki/entities/{filename}")

    # ------------------------------------------------------------------
    # Phase 3: checkpoint-family synthesis trigger
    # If this is a durable checkpoint and there are >= CHECKPOINT_FAMILY_MIN_SIZE
    # checkpoints (incl. self) sharing concepts, append a synthesis suggestion so
    # the existing call_llm_synthesis loop picks it up.
    # ------------------------------------------------------------------
    if (
        route.checkpoint_class
        and route.checkpoint_class.startswith("durable-")
        and route.retention_mode != SKIP
    ):
        own_concept_slugs = [
            c["slug"] for c in extraction.get("concepts", []) if c.get("slug")
        ]
        if len(own_concept_slugs) >= CHECKPOINT_FAMILY_MIN_SHARED:
            family = find_checkpoint_family(
                wiki_dir,
                own_concept_slugs,
                exclude_slug=Path(src_filename).stem,
            )
            if len(family) + 1 >= CHECKPOINT_FAMILY_MIN_SIZE:
                tally: Counter[str] = Counter()
                for _, shared in family:
                    for s in shared:
                        tally[s] += 1
                top_slugs = [slug for slug, _ in tally.most_common(3)]
                if top_slugs:
                    anchor = top_slugs[0].replace("-", " ")
                    syn_title = f"Recurring checkpoint patterns: {anchor}"
                    syn_slug = slugify(syn_title)
                    syn_path = wiki_dir / "synthesis" / f"{syn_slug}.md"
                    if syn_path.exists():
                        log.info(
                            "Checkpoint family of %d touching %s already has synthesis %s",
                            len(family) + 1, top_slugs, syn_path.name,
                        )
                    else:
                        # Resolve concept titles for compare list (slug -> title)
                        compare_titles: list[str] = []
                        for slug in top_slugs:
                            cp = wiki_dir / "concepts" / f"{slug}.md"
                            if cp.exists():
                                cfm, _ = parse_frontmatter(cp)
                                compare_titles.append(
                                    cfm.get("title") or slug.replace("-", " ").title()
                                )
                            else:
                                compare_titles.append(slug.replace("-", " ").title())
                        suggestion = {
                            "title": syn_title,
                            "slug": syn_slug,
                            "question": (
                                f"What recurring decisions, fixes, and patterns "
                                f"appear across the {len(family) + 1} session "
                                f"checkpoints touching {', '.join(compare_titles)}?"
                            ),
                            "concepts_to_compare": compare_titles,
                            "dimensions": ["Approach", "Outcome", "Lessons"],
                        }
                        extraction.setdefault("synthesis_suggestions", []).append(
                            suggestion
                        )
                        log.info(
                            "Checkpoint family trigger: %d members on %s -> queued synthesis '%s'",
                            len(family) + 1, top_slugs, syn_title,
                        )

    # Generate synthesis pages from suggestions
    synthesis_count = 0
    suggestions = extraction.get("synthesis_suggestions", [])
    for suggestion in suggestions[:MAX_SYNTHESIS_PER_INGEST]:
        syn_slug = slugify(suggestion.get("title", ""))
        if not syn_slug:
            continue

        # Skip if synthesis page already exists
        syn_path = wiki_dir / "synthesis" / f"{syn_slug}.md"
        if syn_path.exists():
            log.info("Synthesis already exists: %s", syn_path.name)
            continue

        # Resolve concept pages to compare — look in wiki for matching titles
        concepts_to_compare = suggestion.get("concepts_to_compare", [])
        concept_pages: dict[str, str] = {}
        for concept_title in concepts_to_compare:
            # Search in existing wiki pages
            cslug = slugify(concept_title)
            for category in ("concepts", "entities", "sources"):
                candidate = wiki_dir / category / f"{cslug}.md"
                if candidate.exists():
                    _, page_body = parse_frontmatter(candidate)
                    concept_pages[concept_title] = page_body
                    break

        if len(concept_pages) < 2:
            log.info(
                "Skipping synthesis '%s' — only %d/%d pages found",
                suggestion["title"], len(concept_pages), len(concepts_to_compare),
            )
            continue

        # Call LLM to generate synthesis content
        synthesis_result = call_llm_synthesis(
            concept_pages=concept_pages,
            question=suggestion.get("question", suggestion["title"]),
            dimensions=suggestion.get("dimensions", []),
            token=token,
            model=model,
        )
        if not synthesis_result:
            continue

        # Collect raw paths from the compared pages' sources
        syn_raw_paths = [raw_rel]
        syn_source_titles = [source_title]
        for concept_title in concept_pages:
            cslug = slugify(concept_title)
            for category in ("concepts", "entities", "sources"):
                candidate = wiki_dir / category / f"{cslug}.md"
                if candidate.exists():
                    cfm, _ = parse_frontmatter(candidate)
                    for src in cfm.get("sources", []):
                        if src not in syn_raw_paths:
                            syn_raw_paths.append(src)
                    break
            if concept_title not in syn_source_titles:
                syn_source_titles.append(concept_title)

        syn_filename, syn_content = generate_synthesis_page(
            synthesis_result, syn_raw_paths, syn_source_titles, today,
        )
        syn_path = wiki_dir / "synthesis" / syn_filename
        syn_path.parent.mkdir(parents=True, exist_ok=True)
        syn_path.write_text(syn_content)
        created_pages.append(f"wiki/synthesis/{syn_filename}")
        synthesis_count += 1
        log.info("Created synthesis: wiki/synthesis/%s", syn_filename)

    # Post-process: validate wikilinks, dedup, compute quality scores
    postprocess_created_pages(wiki_dir, created_pages, project_root)

    if validation_run:
        # Validation runs update raw snapshots and pages but do not append to
        # wiki/log.md or send ntfy notifications so review reruns don't pollute
        # the audit trail.
        log.info("Validation run — skipping log.md append and ntfy notification")
    else:
        # Append to log
        log_path = wiki_dir / "log.md"
        append_log(log_path, {
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "operation": "ingest",
            "targets": created_pages,
            "source": raw_rel,
            "status": "success",
            "notes": f"Auto-ingested {len(created_pages)} pages ({len(extraction.get('concepts', []))} concepts, {len(extraction.get('entities', []))} entities, {synthesis_count} synthesis)",
        })
        # Notify
        send_ntfy(
            f"Wiki: {source_title}",
            f"Ingested {len(created_pages)} pages from {raw_path.name}",
            tags="books,white_check_mark",
        )

    # Rebuild index
    rebuild_index(project_root)

    # Mark raw source as ingested
    update_raw_status(raw_path, "ingested")

    log.info(
        "✅ Ingested %s → %d pages created",
        raw_path.name,
        len(created_pages),
    )
    return True


def process_all_pending(
    project_root: Path,
    token: str,
    model: str | None = None,
    *,
    validation_run: bool = False,
) -> int:
    """Process all pending raw sources. Returns count of processed files."""
    raw_dir = project_root / "raw"
    count = 0
    pending_files: list[tuple[int, str, Path]] = []
    for raw_file in raw_dir.glob("*.md"):
        fm, _ = parse_frontmatter(raw_file)
        if fm.get("status") == "pending":
            route = classify_ingest_route(fm, model_override=model)
            pending_files.append((route.priority, raw_file.name, raw_file))

    for _, _, raw_file in sorted(pending_files):
        try:
            if ingest_raw_source(
                raw_file,
                project_root,
                token,
                model,
                validation_run=validation_run,
            ):
                count += 1
        except Exception:
            log.exception("Failed to process %s", raw_file.name)
            update_raw_status(raw_file, "failed")
            if not validation_run:
                send_ntfy(
                    f"❌ Wiki ingest failed: {raw_file.name}",
                    f"Error processing {raw_file.name}. Check logs.",
                    tags="warning",
                )
    return count


def main() -> None:
    parser = argparse.ArgumentParser(description="Auto-ingest raw wiki sources via LLM")
    parser.add_argument(
        "raw_file",
        nargs="?",
        help="Specific raw file to process (default: process all pending)",
    )
    parser.add_argument(
        "--project-root",
        default=os.environ.get("PROJECT_ROOT", "."),
        help="Root of the labs-wiki project",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Optional explicit model override (otherwise source-based routing decides)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Process a specific raw file even if it is already marked ingested",
    )
    parser.add_argument(
        "--refresh-fetch",
        action="store_true",
        help="Re-fetch URL content and replace the persisted fetched-content block",
    )
    parser.add_argument(
        "--validation-run",
        action="store_true",
        help=(
            "Mark this as a review-only rerun (requires --force). "
            "Still updates raw snapshots and wiki pages but suppresses "
            "wiki/log.md append and ntfy notifications."
        ),
    )
    parser.add_argument(
        "--token",
        default=os.environ.get("GITHUB_MODELS_TOKEN", os.environ.get("GITHUB_TOKEN", "")),
        help="GitHub Models API token",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable debug logging",
    )
    args = parser.parse_args()
    if args.refresh_fetch and not args.force:
        parser.error("--refresh-fetch requires --force")
    if args.validation_run and not args.force:
        parser.error("--validation-run requires --force")
    if args.force and not args.raw_file:
        parser.error("--force requires a specific raw_file")
    if args.validation_run and not args.raw_file:
        parser.error("--validation-run requires a specific raw_file")
    if args.refresh_fetch and not args.raw_file:
        parser.error("--refresh-fetch requires a specific raw_file")

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    if not args.token:
        log.error("No API token. Set GITHUB_MODELS_TOKEN or pass --token")
        sys.exit(1)

    project_root = Path(args.project_root).resolve()

    if args.raw_file:
        raw_path = Path(args.raw_file)
        if not raw_path.is_absolute():
            raw_path = project_root / raw_path
        raw_path = raw_path.resolve()
        ok = ingest_raw_source(
            raw_path,
            project_root,
            args.token,
            args.model,
            force=args.force,
            refresh_fetch=args.refresh_fetch,
            validation_run=args.validation_run,
        )
        sys.exit(0 if ok else 1)
    else:
        count = process_all_pending(
            project_root,
            args.token,
            args.model,
            validation_run=args.validation_run,
        )
        log.info("Processed %d pending source(s)", count)


if __name__ == "__main__":
    main()
