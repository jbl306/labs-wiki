#!/usr/bin/env python3
"""Idempotently migrate legacy synthesis pages to the strict evidence contract.

The migration never invents a source. It reconstructs claim-level support only
from wikilinks already present in each insight, intersects those linked pages
with declared raw provenance, and moves claims with no recoverable support out
of Key Insights.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path
from typing import Any

import yaml

from audit_synthesis import (
    INSIGHT_RE,
    WIKILINK_RE,
    _insight_supporting_pages,
    _normalized_page_title,
    _normalized_raw_source,
    parse_frontmatter_text,
    section_body,
    source_origin_family,
)

ROOT = Path(__file__).resolve().parent.parent
HASH_RE = re.compile(r"^(?:sha256:)?[0-9a-fA-F]{64}$")
SUPPORT_RE = re.compile(r"\s+(?:—\s+)?supported\s+by\s+.+$", re.IGNORECASE)


def _page_provenance(root: Path) -> tuple[dict[str, set[str]], dict[str, str]]:
    provenance: dict[str, set[str]] = {}
    titles: dict[str, str] = {}
    for page in (root / "wiki").rglob("*.md"):
        if page.name in {"index.md", "log.md"}:
            continue
        frontmatter, _body = parse_frontmatter_text(page.read_text(errors="replace"))
        title = str(frontmatter.get("title") or "").strip()
        if not title:
            continue
        key = _normalized_page_title(title)
        titles[key] = title
        valid: set[str] = set()
        sources = frontmatter.get("sources")
        if isinstance(sources, list):
            for source in sources:
                normalized = _normalized_raw_source(root, source)
                if normalized and normalized[0].is_file():
                    valid.add(normalized[1])
        provenance[key] = valid
    return provenance, titles


def _replace_section(body: str, name: str, replacement: str) -> str:
    pattern = re.compile(
        rf"(^##\s+{re.escape(name)}\s*$\n)(.*?)(?=^##\s+|\Z)",
        flags=re.MULTILINE | re.DOTALL | re.IGNORECASE,
    )
    if not pattern.search(body):
        return body.rstrip() + f"\n\n## {name}\n\n{replacement.strip()}\n"
    return pattern.sub(lambda match: match.group(1) + "\n" + replacement.strip() + "\n\n", body, count=1)


def _insert_evidence_map(body: str, evidence_map: str) -> str:
    if re.search(r"^##\s+Evidence Map\s*$", body, re.MULTILINE | re.IGNORECASE):
        return _replace_section(body, "Evidence Map", evidence_map)
    marker = re.search(r"^##\s+Open Questions\s*$", body, re.MULTILINE | re.IGNORECASE)
    block = f"## Evidence Map\n\n{evidence_map.strip()}\n\n"
    if marker:
        return body[: marker.start()] + block + body[marker.start() :]
    return body.rstrip() + "\n\n" + block


def _already_strict(frontmatter: dict[str, Any], body: str) -> bool:
    return (
        frontmatter.get("evidence_scope") in {"cross-source", "within-source"}
        and isinstance(frontmatter.get("evidence_source_count"), int)
        and isinstance(frontmatter.get("evidence_origin_family_count"), int)
        and isinstance(frontmatter.get("source_hash"), str)
        and bool(HASH_RE.fullmatch(frontmatter["source_hash"]))
        and bool(re.search(r"^##\s+Evidence Map\s*$", body, re.MULTILINE | re.IGNORECASE))
    )


def migrate_page(
    path: Path,
    root: Path,
    provenance: dict[str, set[str]],
    canonical_titles: dict[str, str],
) -> bool:
    original = path.read_text()
    frontmatter, body = parse_frontmatter_text(original)
    if not frontmatter or _already_strict(frontmatter, body):
        return False

    raw_values = frontmatter.get("sources")
    raw_sources: list[str] = []
    if isinstance(raw_values, list):
        for value in raw_values:
            normalized = _normalized_raw_source(root, value)
            if normalized and normalized[0].is_file() and normalized[1] not in raw_sources:
                raw_sources.append(normalized[1])
    declared = set(raw_sources)
    families = {
        source_origin_family(root / source)
        for source in raw_sources
        if (root / source).is_file()
    }
    families.discard("missing")

    migrated_insights: list[str] = []
    evidence_rows: list[str] = []
    pending_claims: list[str] = []
    for insight in INSIGHT_RE.findall(section_body(body, "Key Insights")):
        candidates = _insight_supporting_pages(insight) or WIKILINK_RE.findall(insight)
        claim = SUPPORT_RE.sub("", insight).strip()
        # Markdown table parsing treats a link alias pipe as a cell boundary;
        # preserve the canonical target while dropping display aliases.
        claim = re.sub(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]", r"[[\1]]", claim)

        supporting_titles: list[str] = []
        supporting_raw: set[str] = set()
        for candidate in candidates:
            key = _normalized_page_title(candidate)
            page_sources = provenance.get(key, set()).intersection(declared)
            if not page_sources:
                continue
            title = canonical_titles.get(key, candidate.strip())
            if title not in supporting_titles:
                supporting_titles.append(title)
            supporting_raw.update(page_sources)

        if not supporting_titles or not supporting_raw:
            pending_claims.append(claim.replace("**", ""))
            continue

        support = ", ".join(f"[[{title}]]" for title in supporting_titles)
        migrated_insights.append(f"{claim} — supported by {support}")
        raw_refs = ", ".join(f"`{source}`" for source in sorted(supporting_raw))
        evidence_rows.append(
            "| "
            + claim
            + " | "
            + support
            + " | "
            + raw_refs
            + " | Legacy mapping reconstructed from existing wikilinks and declared provenance; verify semantics. |"
        )

    key_insights = "\n".join(
        f"{index}. {insight}" for index, insight in enumerate(migrated_insights, start=1)
    ) or "_No legacy claim has recoverable claim-level support._"
    body = _replace_section(body, "Key Insights", key_insights)

    evidence_map = "\n".join(
        [
            "| Insight | Supporting pages | Raw provenance | Confidence / limits |",
            "|---|---|---|---|",
            *evidence_rows,
        ]
    )
    body = _insert_evidence_map(body, evidence_map)

    if pending_claims:
        pending = "\n".join(f"- {claim}" for claim in pending_claims)
        if not re.search(r"^##\s+Legacy Claims Pending Evidence\s*$", body, re.MULTILINE):
            marker = re.search(r"^##\s+Sources\s*$", body, re.MULTILINE | re.IGNORECASE)
            block = (
                "## Legacy Claims Pending Evidence\n\n"
                "These retained claims are not Key Insights until claim-level support is supplied.\n\n"
                f"{pending}\n\n"
            )
            body = body[: marker.start()] + block + body[marker.start() :] if marker else body.rstrip() + "\n\n" + block

    frontmatter["source_hash"] = hashlib.sha256("\n".join(sorted(raw_sources)).encode()).hexdigest()
    frontmatter["sources"] = raw_sources
    frontmatter["evidence_scope"] = "cross-source" if len(families) >= 2 else "within-source"
    frontmatter["evidence_source_count"] = len(raw_sources)
    frontmatter["evidence_origin_family_count"] = len(families)

    rendered_frontmatter = yaml.safe_dump(
        frontmatter,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
    ).rstrip()
    migrated = f"---\n{rendered_frontmatter}\n---\n\n{body.strip()}\n"
    if migrated == original:
        return False
    path.write_text(migrated)
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--check", action="store_true", help="Report pending migrations without writing")
    args = parser.parse_args()
    root = args.root.resolve()
    provenance, titles = _page_provenance(root)
    changed: list[str] = []
    for path in sorted((root / "wiki" / "synthesis").glob("*.md")):
        if args.check:
            frontmatter, body = parse_frontmatter_text(path.read_text(errors="replace"))
            if not _already_strict(frontmatter, body):
                changed.append(path.relative_to(root).as_posix())
            continue
        if migrate_page(path, root, provenance, titles):
            changed.append(path.relative_to(root).as_posix())
    print(f"synthesis migration: {len(changed)} page(s) {'pending' if args.check else 'updated'}")
    for relative in changed:
        print(relative)
    return 1 if args.check and changed else 0


if __name__ == "__main__":
    sys.exit(main())
