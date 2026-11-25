#!/usr/bin/env python3
"""
Wiki MCP Server — exposes labs-wiki as searchable tools for all AI agents.

Provides three local file-system tools, one authenticated ingest proxy, plus
six wiki-graph-api proxies:

  Local (read wiki/ directly):
    - wiki_search:               full-text search across wiki pages
    - wiki_read:                 read a specific wiki page by name or path
    - wiki_list:                 list all wiki pages from the index

  Graph (HTTP → wiki-graph-api, base URL via WIKI_GRAPH_API_BASE_URL,
  default http://localhost:8765):
    - wiki_graph_neighbors:      depth-N neighbours of a node
    - wiki_graph_shortest_path:  undirected BFS path between two nodes
    - wiki_graph_communities:    community summary
    - wiki_graph_god_nodes:      top-degree load-bearing nodes
    - wiki_graph_surprises:      cross-community edges
    - wiki_graph_query:          NL semantic query (R14 endpoint)

  Capture (HTTP → wiki-ingest-api, configured with
  WIKI_INGEST_API_BASE_URL and WIKI_INGEST_API_TOKEN):
    - wiki_capture:              authenticated URL/text/note capture

Transport: stdio for MCP clients
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from ipaddress import ip_address
from pathlib import Path, PurePosixPath
from typing import Literal
from urllib.parse import urlsplit

import httpx
from mcp.server.fastmcp import FastMCP

WIKI_ROOT = Path(os.environ.get("WIKI_ROOT", Path(__file__).parent.parent))
WIKI_DIR = WIKI_ROOT / "wiki"
INDEX_PATH = WIKI_DIR / "index.md"

GRAPH_API_BASE = os.environ.get("WIKI_GRAPH_API_BASE_URL", "http://localhost:8765").rstrip("/")
GRAPH_API_TIMEOUT = float(os.environ.get("WIKI_GRAPH_API_TIMEOUT", "10"))
CAPTURE_API_TIMEOUT = 5.0
CAPTURE_MAX_BASE_URL = 2048
CAPTURE_MAX_TOKEN = 4096
CAPTURE_MAX_CONTENT = 20_000
CAPTURE_MAX_TITLE = 200
CAPTURE_MAX_TAGS = 20
CAPTURE_MAX_TAG = 50
CAPTURE_MAX_SOURCE = 100
CAPTURE_MAX_RESPONSE_PATH = 512
CAPTURE_MAX_OUTPUT = 4_096
CAPTURE_TYPES = {"url", "text", "note"}

PAGE_OWNER = os.environ.get("WIKI_PAGE_OWNER", "labs-wiki")
DEFAULT_RESPONSE_CHAR_BUDGET = 12_000
MAX_RESPONSE_CHAR_BUDGET = 100_000

mcp = FastMCP("labs-wiki")


def _graph_get(path: str, params: dict[str, object] | None = None) -> dict | list:
    """GET wiki-graph-api endpoint and return parsed JSON or raise."""
    url = f"{GRAPH_API_BASE}{path}"
    with httpx.Client(timeout=GRAPH_API_TIMEOUT) as client:
        resp = client.get(url, params=params)
        resp.raise_for_status()
        return resp.json()


def _graph_post(path: str, body: dict) -> dict | list:
    url = f"{GRAPH_API_BASE}{path}"
    with httpx.Client(timeout=GRAPH_API_TIMEOUT) as client:
        resp = client.post(url, json=body)
        resp.raise_for_status()
        return resp.json()


def _graph_error(action: str, exc: Exception) -> str:
    return f"wiki-graph-api {action} failed against {GRAPH_API_BASE}: {exc}"


def _capture_error(message: str) -> str:
    return f"wiki capture {message}"[:CAPTURE_MAX_OUTPUT]


def _capture_config() -> tuple[str, str] | str:
    base_url = os.environ.get("WIKI_INGEST_API_BASE_URL", "")
    token = os.environ.get("WIKI_INGEST_API_TOKEN", "")

    if not base_url:
        return _capture_error(
            "configuration invalid: WIKI_INGEST_API_BASE_URL is required"
        )
    if not token:
        return _capture_error(
            "configuration invalid: WIKI_INGEST_API_TOKEN is required"
        )
    if (
        len(base_url) > CAPTURE_MAX_BASE_URL
        or base_url != base_url.strip()
        or any(char.isspace() or ord(char) < 32 or ord(char) == 127 for char in base_url)
    ):
        return _capture_error("configuration invalid: base URL is malformed")
    if (
        len(token) > CAPTURE_MAX_TOKEN
        or token != token.strip()
        or any(char.isspace() or ord(char) < 32 or ord(char) == 127 for char in token)
        or token.lower().startswith("bearer ")
    ):
        return _capture_error("configuration invalid: token is malformed")

    try:
        parsed = urlsplit(base_url)
        _ = parsed.port
        hostname = parsed.hostname
    except ValueError:
        return _capture_error("configuration invalid: base URL is malformed")
    if (
        parsed.scheme not in {"http", "https"}
        or not hostname
        or parsed.username is not None
        or parsed.password is not None
        or parsed.query
        or parsed.fragment
    ):
        return _capture_error("configuration invalid: base URL is malformed")
    if parsed.scheme == "http":
        try:
            loopback = hostname.lower() == "localhost" or ip_address(hostname).is_loopback
        except ValueError:
            loopback = hostname.lower() == "localhost"
        if not loopback:
            return _capture_error(
                "configuration invalid: HTTPS is required except for loopback HTTP"
            )

    return base_url.rstrip("/"), token


def _capture_label_valid(value: object, limit: int) -> bool:
    return (
        isinstance(value, str)
        and len(value) <= limit
        and not any(ord(char) < 32 or ord(char) == 127 for char in value)
    )


def _capture_validate(
    capture_type: object,
    content: object,
    title: object,
    tags: object,
    source: object,
) -> str | None:
    if not isinstance(capture_type, str) or capture_type not in CAPTURE_TYPES:
        return _capture_error("invalid input: type must be url, text, or note")
    if not isinstance(content, str) or not content.strip():
        return _capture_error("invalid input: content is required")
    if len(content) > CAPTURE_MAX_CONTENT:
        return _capture_error("invalid input: content exceeds its size limit")
    if title is not None and not _capture_label_valid(title, CAPTURE_MAX_TITLE):
        return _capture_error("invalid input: title exceeds its size limit")
    if not _capture_label_valid(source, CAPTURE_MAX_SOURCE) or not source:
        return _capture_error("invalid input: source is required or malformed")
    if not isinstance(tags, list) or len(tags) > CAPTURE_MAX_TAGS:
        return _capture_error("invalid input: tags exceed their size limit")
    if any(not _capture_label_valid(tag, CAPTURE_MAX_TAG) or not tag for tag in tags):
        return _capture_error("invalid input: tags contain a malformed value")
    return None


def _capture_response_path_valid(value: object) -> bool:
    if (
        not isinstance(value, str)
        or not value
        or len(value) > CAPTURE_MAX_RESPONSE_PATH
        or "\\" in value
        or any(ord(char) < 32 or ord(char) == 127 for char in value)
    ):
        return False
    path = PurePosixPath(value)
    return (
        not path.is_absolute()
        and str(path) == value
        and len(path.parts) == 2
        and path.parts[0] == "raw"
        and ".." not in path.parts
        and path.suffix == ".md"
    )


@mcp.tool()
def wiki_capture(
    type: Literal["url", "text", "note"],
    content: str,
    title: str | None = None,
    tags: list[str] | None = None,
    source: str = "codex-mcp",
) -> str:
    """Capture a URL, text, or note through the authenticated wiki ingest API.

    The client must set ``WIKI_INGEST_API_BASE_URL`` and
    ``WIKI_INGEST_API_TOKEN``. The API client is never contacted until all
    inputs and configuration have passed validation.
    """
    normalized_tags = [] if tags is None else tags
    validation_error = _capture_validate(type, content, title, normalized_tags, source)
    if validation_error:
        return validation_error

    config = _capture_config()
    if isinstance(config, str):
        return config
    base_url, token = config
    payload: dict[str, object] = {
        "type": type,
        "content": content,
        "tags": normalized_tags,
        "source": source,
    }
    if title is not None:
        payload["title"] = title

    try:
        with httpx.Client(timeout=CAPTURE_API_TIMEOUT) as client:
            response = client.post(
                f"{base_url}/api/ingest",
                json=payload,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                },
            )
            response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        status_code = getattr(exc.response, "status_code", "unknown")
        if not isinstance(status_code, int):
            status_code = "unknown"
        return _capture_error(f"failed: ingest API returned HTTP {status_code}")
    except httpx.RequestError:
        return _capture_error("failed: network error contacting ingest API")
    except Exception:
        return _capture_error("failed: request could not be completed")

    try:
        result = response.json()
    except Exception:
        return _capture_error("failed: invalid response from ingest API")
    if (
        not isinstance(result, dict)
        or result.get("status") != "ok"
        or not _capture_response_path_valid(result.get("path"))
    ):
        return _capture_error("failed: invalid response from ingest API")
    if token in result["path"]:
        return "wiki ingest succeeded"

    return _capture_error(f"succeeded: {result['path']}")


def _is_wiki_page(path: Path) -> bool:
    """Only admit Markdown files whose resolved location stays inside wiki/."""
    try:
        resolved = path.resolve()
    except (OSError, RuntimeError, ValueError):
        return False
    return (
        resolved.is_relative_to(WIKI_DIR.resolve())
        and resolved.suffix == ".md"
        and resolved.is_file()
    )


def _find_pages() -> list[Path]:
    """Return all .md files in wiki/ excluding index.md and log.md."""
    if not WIKI_DIR.exists():
        return []
    return sorted(
        p
        for p in WIKI_DIR.rglob("*.md")
        if p.name not in ("index.md", "log.md") and _is_wiki_page(p)
    )


def _extract_frontmatter(text: str) -> dict[str, str]:
    """Extract YAML frontmatter as a simple key-value dict."""
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}
    result = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" ") and not line.startswith("-"):
            key, _, val = line.partition(":")
            result[key.strip()] = val.strip().strip('"').strip("'")
    return result


def _page_summary(path: Path) -> str:
    """Return a one-line summary: relative path, title, type."""
    text = path.read_text(errors="replace")
    fm = _extract_frontmatter(text)
    rel = path.relative_to(WIKI_ROOT)
    title = fm.get("title", path.stem.replace("-", " ").title())
    ptype = fm.get("type", "unknown")
    return f"{rel} — {title} ({ptype})"


@mcp.tool()
def wiki_list() -> str:
    """List all pages in the labs-wiki knowledge base.

    Returns a catalog of every wiki page with its path, title, and type.
    Use this to discover what knowledge is available before searching or reading.
    """
    pages = _find_pages()
    if not pages:
        return "No wiki pages found."

    lines = [f"# Labs-Wiki — {len(pages)} pages\n"]
    by_type: dict[str, list[str]] = {}
    for p in pages:
        text = p.read_text(errors="replace")
        fm = _extract_frontmatter(text)
        ptype = fm.get("type", "other")
        title = fm.get("title", p.stem.replace("-", " ").title())
        rel = str(p.relative_to(WIKI_ROOT))
        by_type.setdefault(ptype, []).append(f"- **{title}** — `{rel}`")

    for ptype in ["concept", "entity", "source", "synthesis", "other"]:
        items = by_type.get(ptype, [])
        if items:
            lines.append(f"\n## {ptype.title()}s ({len(items)})")
            lines.extend(sorted(items))

    return "\n".join(lines)


@mcp.tool()
def wiki_search(query: str) -> str:
    """Search labs-wiki pages for a topic or keyword.

    Performs case-insensitive full-text search across all wiki page titles,
    content, and frontmatter. Returns matching excerpts with context.

    Args:
        query: Search term or phrase (e.g., "attention mechanism", "transformer")
    """
    pages = _find_pages()
    if not pages:
        return "No wiki pages found."

    query_lower = query.lower()
    terms = query_lower.split()
    results: list[tuple[int, str]] = []

    for p in pages:
        text = p.read_text(errors="replace")
        text_lower = text.lower()

        # Score: title match (high), frontmatter match (medium), body match (low)
        score = 0
        fm = _extract_frontmatter(text)
        title = fm.get("title", "").lower()

        for term in terms:
            if term in title:
                score += 10
            if term in text_lower:
                score += 1
                score += text_lower.count(term)

        if score == 0:
            continue

        # Extract relevant excerpt
        rel = str(p.relative_to(WIKI_ROOT))
        page_title = fm.get("title", p.stem.replace("-", " ").title())
        ptype = fm.get("type", "unknown")

        # Find best matching paragraph
        paragraphs = text.split("\n\n")
        best_para = ""
        best_score = 0
        for para in paragraphs:
            if para.startswith("---"):
                continue
            para_score = sum(para.lower().count(t) for t in terms)
            if para_score > best_score:
                best_score = para_score
                best_para = para.strip()

        excerpt = best_para[:500] + ("..." if len(best_para) > 500 else "")
        entry = f"### {page_title} ({ptype})\n`{rel}`\n\n{excerpt}"
        results.append((score, entry))

    if not results:
        return f'No wiki pages match "{query}". Use wiki_list to see available pages.'

    results.sort(key=lambda x: -x[0])
    top = results[:10]

    header = f'# Search: "{query}" — {len(results)} match{"es" if len(results) != 1 else ""}\n'
    return header + "\n\n---\n\n".join(entry for _, entry in top)


def _read_page_bytes(path: Path) -> tuple[bytes, str]:
    """Use one file version for both the byte digest and the displayed text."""
    raw = path.read_bytes()
    text = raw.decode("utf-8", errors="replace").replace("\r\n", "\n").replace("\r", "\n")
    return raw, text


def _page_metadata(path: Path, raw: bytes, text: str) -> dict[str, object]:
    """Return deterministic identity and revision metadata for a page."""
    relative = path.resolve().relative_to(WIKI_ROOT.resolve()).as_posix()
    frontmatter = _extract_frontmatter(text)
    stable_id = frontmatter.get("stable_id") or frontmatter.get("record_id")
    if not stable_id:
        stable_id = hashlib.sha256(
            f"{PAGE_OWNER}:{relative}".encode("utf-8")
        ).hexdigest()
    revision = f"sha256:{hashlib.sha256(raw).hexdigest()}"
    return {
        "owner": PAGE_OWNER,
        "path": relative,
        "stable_id": stable_id,
        "revision": revision,
        "title": frontmatter.get("title", path.stem.replace("-", " ").title()),
        "type": frontmatter.get("type", "unknown"),
        "line_count": len(text.splitlines()),
    }


def _citation(metadata: dict[str, object], start_line: int = 1, end_line: int | None = None) -> str:
    """Format a stable, revision-pinned citation for tool output."""
    if end_line is None:
        end_line = int(metadata["line_count"])
    locator = f"#L{start_line}-L{end_line}" if end_line else ""
    return (
        f"{metadata['owner']}:{metadata['path']}{locator} "
        f"(stable_id={metadata['stable_id']}; revision={metadata['revision']})"
    )


def _response_budget(value: int | None) -> tuple[int | None, str | None]:
    configured = os.environ.get("WIKI_RESPONSE_CHAR_BUDGET")
    try:
        configured_budget = (
            DEFAULT_RESPONSE_CHAR_BUDGET if configured is None else int(configured)
        )
    except ValueError:
        return None, "Invalid WIKI_RESPONSE_CHAR_BUDGET configuration."
    if not 256 <= configured_budget <= MAX_RESPONSE_CHAR_BUDGET:
        return None, "Invalid WIKI_RESPONSE_CHAR_BUDGET configuration."
    if value is None:
        return configured_budget, None
    if isinstance(value, bool) or not isinstance(value, int) or value < 256:
        return None, "Invalid max_chars: expected an integer of at least 256."
    return min(value, configured_budget), None


def _bounded_message(message: str, budget: int) -> str:
    """Keep diagnostic responses inside the same caller-selected budget."""
    if len(message) <= budget:
        return message
    return message[: max(1, budget - 1)] + "…"


def _section_bounds(lines: list[str], section: str) -> tuple[int, int] | None:
    wanted = section.strip().lstrip("#").strip().casefold()
    if not wanted:
        return None
    start = None
    level = 0
    delimiter = ""
    for index, line in enumerate(lines):
        fence = re.match(r"^ {0,3}(`{3,}|~{3,})([^\n]*)", line)
        if delimiter:
            if fence and fence[1].startswith(delimiter) and not fence[2].strip():
                delimiter = ""
            continue
        if fence:
            delimiter = fence[1]
            continue
        heading = re.match(r"^ {0,3}(#{1,6})[ \t]+(.+?)\s*$", line)
        if heading is None:
            continue
        heading_level = len(heading[1])
        if start is not None:
            if heading_level <= level:
                return start, index
        elif re.sub(r"[ \t]+#+$", "", heading[2]).strip().casefold() == wanted:
            start, level = index, heading_level
    return (start, len(lines)) if start is not None else None


def _read_lines(
    text: str,
    section: str | None,
    start_line: int | None,
    end_line: int | None,
) -> tuple[str | None, int, int, str | None]:
    lines = text.splitlines(keepends=True)
    lower = 0
    upper = len(lines)
    if section is not None:
        bounds = _section_bounds(lines, section)
        if bounds is None:
            return None, 0, 0, f'Section "{section}" not found.'
        lower, upper = bounds
    if start_line is not None:
        if isinstance(start_line, bool) or not isinstance(start_line, int) or start_line < 1:
            return None, 0, 0, "Invalid start_line: expected a positive integer."
        lower = max(lower, start_line - 1)
    if end_line is not None:
        if isinstance(end_line, bool) or not isinstance(end_line, int) or end_line < 1:
            return None, 0, 0, "Invalid end_line: expected a positive integer."
        upper = min(upper, end_line)
    if not lines:
        return None, 0, 0, "Page is empty."
    if upper <= lower:
        return None, 0, 0, "Invalid line range: no lines in the requested selection."
    selected = "".join(lines[lower:upper])
    return selected, lower + 1, upper, None


def _read_output(
    metadata: dict[str, object],
    text: str,
    section: str | None,
    start_line: int | None,
    end_line: int | None,
    budget: int,
    start_column: int,
) -> str:
    selected, selected_start, selected_end, error = _read_lines(
        text, section, start_line, end_line
    )
    if error:
        return _bounded_message(error, budget)
    assert selected is not None
    if isinstance(start_column, bool) or not isinstance(start_column, int) or start_column < 1:
        return "Invalid start_column: expected a positive integer."
    first_line = selected.partition("\n")[0]
    if start_column - 1 > len(first_line):
        return "Invalid start_column: outside the selected line."
    selected = selected[start_column - 1:]

    def header(last_line: int) -> str:
        return (
            f"# {metadata['path']}\n\n"
            f"Owner: {metadata['owner']}\n"
            f"Stable ID: {metadata['stable_id']}\n"
            f"Revision: {metadata['revision']}\n"
            f"Citation: {_citation(metadata, selected_start, last_line)}\n\n"
            "Content:\n"
        )

    prefix = header(selected_end)
    if len(prefix) + len(selected) <= budget:
        return prefix + selected

    def marker(line: int, column: int) -> str:
        return f"\n\n[content truncated; continue with start_line={line}, start_column={column}]"

    # Reserve enough room for the longest possible cursor before cutting the content.
    room = budget - len(prefix) - len(marker(selected_end + 1, start_column + len(selected)))
    if room < 1:
        return "max_chars too small for a cited read with continuation; increase max_chars."
    chunk = selected[:room]
    line = selected_start + chunk.count("\n")
    column = len(chunk.rsplit("\n", 1)[1]) + 1 if "\n" in chunk else start_column + len(chunk)
    last_line = line - 1 if chunk.endswith("\n") else line
    return header(last_line) + chunk + marker(line, column)


@mcp.tool()
def wiki_read(
    page: str,
    section: str | None = None,
    start_line: int | None = None,
    end_line: int | None = None,
    owner: str | None = None,
    page_type: str | None = None,
    max_chars: int | None = None,
    start_column: int = 1,
) -> str:
    """Read a specific wiki page by name or path.

    Args:
        start_column: One-based character within the starting line for continuation.
        page: Page name (e.g., "attention-mechanisms"), title (e.g., "Attention Mechanisms"),
              or relative path (e.g., "wiki/concepts/attention-mechanisms.md")
    """
    unbounded = (
        all(arg is None for arg in (section, start_line, end_line, owner, page_type, max_chars))
        and start_column == 1 and "WIKI_RESPONSE_CHAR_BUDGET" not in os.environ
    )
    budget, error = _response_budget(max_chars)
    if error:
        return error
    if owner is not None and owner != PAGE_OWNER:
        return _bounded_message(
            f'Page "{page}" not found for owner "{owner}".', budget
        )
    if page_type is not None and (not isinstance(page_type, str) or not page_type.strip()):
        return "Invalid page_type filter."
    assert budget is not None

    wanted_type = page_type.strip().casefold() if page_type is not None else None

    # Try direct path first. Generated cache/history views remain available here
    # when named explicitly, while normal discovery excludes them.
    candidates = [
        WIKI_ROOT / page,
        WIKI_DIR / page,
        WIKI_DIR / f"{page}.md",
    ]

    # Try slug matching across all subdirs
    slug = page.lower().replace(" ", "-").replace("_", "-")
    slug = re.sub(r"[^a-z0-9-]", "", slug)
    for subdir in ["concepts", "entities", "sources", "synthesis"]:
        candidates.append(WIKI_DIR / subdir / f"{slug}.md")

    for candidate in candidates:
        if _is_wiki_page(candidate):
            raw, content = _read_page_bytes(candidate)
            if unbounded:
                return f"# {candidate.resolve().relative_to(WIKI_ROOT.resolve())}\n\n{content}"
            metadata = _page_metadata(candidate, raw, content)
            if wanted_type is not None and str(metadata["type"]).casefold() != wanted_type:
                continue
            return _read_output(metadata, content, section, start_line, end_line, budget, start_column)

    # Only scan page contents when direct path and slug lookups miss.
    matches = []
    for p in _find_pages():
        raw, text = _read_page_bytes(p)
        fm = _extract_frontmatter(text)
        if wanted_type is not None and fm.get("type", "unknown").casefold() != wanted_type:
            continue
        if fm.get("title", "").lower() == page.lower() or p.stem == slug:
            if unbounded:
                return f"# {p.resolve().relative_to(WIKI_ROOT.resolve())}\n\n{text}"
            metadata = _page_metadata(p, raw, text)
            return _read_output(metadata, text, section, start_line, end_line, budget, start_column)

        if slug in p.stem:
            matches.append(str(p.relative_to(WIKI_ROOT)))

    if matches:
        return _bounded_message(
            f'Page "{page}" not found. Did you mean:\n'
            + "\n".join(f"- {m}" for m in matches),
            budget,
        )

    scope = f' for page_type "{page_type}"' if wanted_type is not None else ""
    return _bounded_message(
        f'Page "{page}" not found{scope}. Use wiki_list to see available pages.', budget
    )


# ---------------------------------------------------------------------------
# R16 — Graph tools (HTTP proxy to wiki-graph-api)
# ---------------------------------------------------------------------------

@mcp.tool()
def wiki_graph_neighbors(node_id: str, depth: int = 1) -> str:
    """Return the depth-N neighbours of a graph node as JSON.

    Uses GET /graph/neighbors/{node_id}?depth=N on wiki-graph-api.
    Args:
        node_id: Full node id, e.g. ``concepts/attention-mechanisms``.
        depth:   Hops to expand (default 1, capped server-side).
    """
    try:
        data = _graph_get(
            f"/graph/neighbors/{node_id}",
            params={"depth": depth},
        )
    except Exception as e:
        return _graph_error("neighbors", e)
    return json.dumps(data, indent=2)


@mcp.tool()
def wiki_graph_shortest_path(a: str, b: str) -> str:
    """Undirected BFS shortest path between two graph nodes.

    Uses GET /graph/shortest_path?a=...&b=... on wiki-graph-api.
    Returns ``{"path": [...], "length": N}`` (length=-1 if unreachable).
    """
    try:
        data = _graph_get("/graph/shortest_path", params={"a": a, "b": b})
    except Exception as e:
        return _graph_error("shortest_path", e)
    return json.dumps(data, indent=2)


@mcp.tool()
def wiki_graph_communities(limit: int = 10) -> str:
    """Top-N detected communities (size-ranked) in the wiki graph.

    Uses GET /graph/communities. ``limit`` truncates client-side.
    """
    try:
        data = _graph_get("/graph/communities")
    except Exception as e:
        return _graph_error("communities", e)
    items = data.get("communities", []) if isinstance(data, dict) else data
    return json.dumps(items[: max(1, limit)], indent=2)


@mcp.tool()
def wiki_graph_god_nodes(limit: int = 10) -> str:
    """Highest-degree 'god nodes' — load-bearing entities/concepts.

    Uses GET /graph/god-nodes. ``limit`` truncates the response client-side.
    """
    try:
        data = _graph_get("/graph/god-nodes")
    except Exception as e:
        return _graph_error("god_nodes", e)
    items = data.get("god_nodes", []) if isinstance(data, dict) else data
    return json.dumps(items[: max(1, limit)], indent=2)


@mcp.tool()
def wiki_graph_surprises(limit: int = 10) -> str:
    """Top cross-community edges — unexpected bridges between clusters.

    Uses GET /graph/surprises. ``limit`` truncates client-side.
    """
    try:
        data = _graph_get("/graph/surprises")
    except Exception as e:
        return _graph_error("surprises", e)
    items = data.get("surprises", []) if isinstance(data, dict) else data
    return json.dumps(items[: max(1, limit)], indent=2)


@mcp.tool()
def wiki_graph_query(q: str, k: int = 10) -> str:
    """Semantic NL query over the wiki graph (R14 endpoint).

    Uses POST /graph/query{q,k}. Returns the top-K matching nodes plus the
    union of their 1-hop neighbourhoods. Embedding backend is reported in
    ``backend`` (one of sentence-transformers, tfidf, none).

    Args:
        q: Natural-language question (e.g. "how do we score checkpoint health?").
        k: Number of top matches to return (default 10).
    """
    try:
        data = _graph_post("/graph/query", {"q": q, "k": k})
    except Exception as e:
        return _graph_error("query", e)
    return json.dumps(data, indent=2)


if __name__ == "__main__":
    mcp.run(transport="stdio")
