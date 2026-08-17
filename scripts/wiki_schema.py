#!/usr/bin/env python3
"""Shared strict schema validation for canonical Labs Wiki pages."""

from __future__ import annotations

import datetime as dt
import re
from pathlib import Path
from typing import Any

import yaml

VALID_TYPES = {"source", "concept", "entity", "synthesis"}
TYPE_DIR_MAP = {
    "source": "sources",
    "concept": "concepts",
    "entity": "entities",
    "synthesis": "synthesis",
}
REQUIRED_FIELDS = (
    "title",
    "type",
    "created",
    "last_verified",
    "source_hash",
    "sources",
    "concepts",
    "related",
    "tier",
    "tags",
)
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
HASH_RE = re.compile(r"^[0-9a-f]{64}$")


def parse_page_text(text: str) -> tuple[dict[str, Any], str, str | None]:
    """Parse YAML frontmatter and return ``(frontmatter, body, error)``."""
    if not text.startswith("---\n"):
        return {}, text, "missing YAML frontmatter"
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text, "unterminated YAML frontmatter"
    try:
        frontmatter = yaml.safe_load(text[4:end]) or {}
    except yaml.YAMLError as exc:
        return {}, text, f"invalid YAML frontmatter: {exc}"
    if not isinstance(frontmatter, dict):
        return {}, text, "frontmatter must be a mapping"
    return frontmatter, text[end + 4 :].lstrip("\n"), None


def _is_iso_date(value: object) -> bool:
    if isinstance(value, dt.datetime):
        return True
    if isinstance(value, dt.date):
        return True
    return bool(DATE_RE.fullmatch(str(value or "").strip()))


def _raw_source_path(repo_root: Path, value: object) -> Path | None:
    text = str(value or "").strip()
    candidate = Path(text)
    if not text or candidate.is_absolute() or candidate.suffix.casefold() != ".md":
        return None
    root = repo_root.resolve()
    raw_root = (root / "raw").resolve()
    resolved = (root / candidate).resolve()
    if not resolved.is_relative_to(raw_root):
        return None
    return resolved


def validate_page_text(
    text: str,
    path: Path,
    repo_root: Path,
    *,
    expected_type: str | None = None,
) -> list[str]:
    """Validate one proposed page without trusting model-written metadata."""
    frontmatter, body, parse_error = parse_page_text(text)
    errors: list[str] = []
    if parse_error:
        return [parse_error]

    for field in REQUIRED_FIELDS:
        if field not in frontmatter:
            errors.append(f"missing required field {field!r}")

    title = frontmatter.get("title")
    if not isinstance(title, str) or not title.strip():
        errors.append("title must be a non-empty string")

    page_type = frontmatter.get("type")
    if page_type not in VALID_TYPES:
        errors.append(f"type must be one of {sorted(VALID_TYPES)}")
    if expected_type and page_type != expected_type:
        errors.append(f"type must be {expected_type!r} for this proposal field")
    if page_type in TYPE_DIR_MAP:
        try:
            rel = path.resolve().relative_to((repo_root / "wiki").resolve())
        except ValueError:
            errors.append("page path must be under wiki/")
        else:
            if not rel.parts or rel.parts[0] != TYPE_DIR_MAP[page_type]:
                errors.append(
                    f"type {page_type!r} must be stored under wiki/{TYPE_DIR_MAP[page_type]}/"
                )

    for field in ("created", "last_verified"):
        if not _is_iso_date(frontmatter.get(field)):
            errors.append(f"{field} must be an ISO YYYY-MM-DD date")

    source_hash = frontmatter.get("source_hash")
    if not isinstance(source_hash, str) or not HASH_RE.fullmatch(source_hash.strip()):
        errors.append("source_hash must be a full SHA-256 hex digest")

    sources = frontmatter.get("sources")
    if not isinstance(sources, list) or not sources:
        errors.append("sources must be a non-empty list")
    else:
        for source in sources:
            resolved = _raw_source_path(repo_root, source)
            if resolved is None:
                errors.append(f"sources entry must be a contained raw/*.md path: {source!r}")
            elif not resolved.is_file():
                errors.append(f"sources entry does not exist: {source!r}")

    for field in ("concepts", "related", "tags"):
        if not isinstance(frontmatter.get(field), list):
            errors.append(f"{field} must be a list")

    tier = frontmatter.get("tier")
    if not isinstance(tier, str) or not tier.strip():
        errors.append("tier must be a non-empty string")

    if not re.search(r"(?m)^#\s+\S", body):
        errors.append("body must contain a non-empty H1 heading")
    primary_section = {
        "source": "## Summary",
        "concept": "## Overview",
        "entity": "## Overview",
    }.get(str(page_type))
    if primary_section and not re.search(
        rf"(?m)^{re.escape(primary_section)}\s*$", body
    ):
        errors.append(f"{page_type} body must contain {primary_section!r}")

    if page_type == "synthesis":
        scope = frontmatter.get("evidence_scope")
        if scope not in {"cross-source", "within-source"}:
            errors.append("evidence_scope must be cross-source or within-source")
        for field in ("evidence_source_count", "evidence_origin_family_count"):
            value = frontmatter.get(field)
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                errors.append(f"{field} must be a non-negative integer")

    return errors


def validate_page(
    path: Path,
    repo_root: Path,
    *,
    expected_type: str | None = None,
) -> list[str]:
    """Validate a page on disk and return actionable error strings."""
    if not path.is_file():
        return [f"page does not exist: {path}"]
    return validate_page_text(
        path.read_text(errors="replace"),
        path,
        repo_root,
        expected_type=expected_type,
    )
