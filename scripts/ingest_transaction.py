#!/usr/bin/env python3
"""Transactional publication for read-only agent ingest proposals."""

from __future__ import annotations

import hashlib
import fcntl
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

from compile_index import compile_index
from wiki_schema import parse_page_text, validate_page

PROPOSAL_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "status": {"type": "string", "enum": ["success", "failed"]},
        "source_path": {"type": "string"},
        "page_mutations": {
            "type": "array",
            "maxItems": 16,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "path": {"type": "string"},
                    "operation": {"type": "string", "enum": ["create", "update"]},
                    "content": {"type": "string", "minLength": 1},
                },
                "required": ["path", "operation", "content"],
            },
        },
        "duplicates_avoided": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "candidate": {"type": "string"},
                    "linked_to": {"type": "string"},
                },
                "required": ["candidate", "linked_to"],
            },
        },
        "kg_facts": {
            "type": "array",
            "maxItems": 50,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "subject": {"type": "string"},
                    "predicate": {"type": "string"},
                    "object": {"type": "string"},
                    "source_closet": {"type": "string"},
                    "valid_from": {"type": ["string", "null"]},
                },
                "required": [
                    "subject",
                    "predicate",
                    "object",
                    "source_closet",
                    "valid_from",
                ],
            },
        },
        "notes": {"type": "string"},
    },
    "required": [
        "status",
        "source_path",
        "page_mutations",
        "duplicates_avoided",
        "kg_facts",
        "notes",
    ],
}

PAGE_PATH_RE = re.compile(
    r"^wiki/(?P<category>sources|concepts|entities|synthesis)/[a-z0-9][a-z0-9-]*\.md$"
)
CATEGORY_TYPE = {
    "sources": "source",
    "concepts": "concept",
    "entities": "entity",
    "synthesis": "synthesis",
}


class ProposalError(ValueError):
    """Raised when a model proposal is unsafe or violates the wiki contract."""


def _normalize_source_hash(value: object) -> str:
    text = str(value or "").strip().lower()
    if text.startswith("sha256:"):
        text = text.removeprefix("sha256:")
    return text if re.fullmatch(r"[0-9a-f]{64}", text) else ""


def _normalized_title(value: object) -> str:
    """Normalize case and whitespace without erasing meaningful punctuation."""
    return " ".join(str(value or "").casefold().split())


def _merge_unique_list(existing: object, proposed: object) -> list[Any]:
    """Preserve ordered metadata values while removing exact duplicates."""
    merged: list[Any] = []
    for values in (existing, proposed):
        if not isinstance(values, list):
            continue
        for value in values:
            if value not in merged:
                merged.append(value)
    return merged


def _normalized_upstream_identity(value: object) -> str:
    """Return a stable identity for URLs that name the same upstream document."""
    text = str(value or "").strip()
    if not text:
        return ""
    try:
        parsed = urllib.parse.urlsplit(text)
    except ValueError:
        return ""
    host = (parsed.hostname or "").casefold()
    if host in {"arxiv.org", "www.arxiv.org"}:
        match = re.fullmatch(r"/(?:abs|pdf)/(.+)", parsed.path, re.IGNORECASE)
        if match:
            arxiv_id = re.sub(r"\.pdf$", "", match.group(1), flags=re.IGNORECASE)
            arxiv_id = re.sub(r"v\d+$", "", arxiv_id, flags=re.IGNORECASE)
            if re.fullmatch(
                r"(?:\d{4}\.\d{4,5}|[a-z][a-z0-9.-]*/\d{7})",
                arxiv_id,
                re.IGNORECASE,
            ):
                return f"arxiv:{arxiv_id.casefold()}"
    if parsed.scheme.casefold() not in {"http", "https"} or not host:
        return ""
    try:
        port = f":{parsed.port}" if parsed.port else ""
    except ValueError:
        return ""
    path = parsed.path.rstrip("/") or "/"
    return urllib.parse.urlunsplit(
        (parsed.scheme.casefold(), host + port, path, parsed.query, "")
    )


def _source_identities(frontmatter: dict[str, Any], project_root: Path) -> set[str]:
    """Resolve normalized upstream identities from a page's raw provenance."""
    identities: set[str] = set()
    raw_root = (project_root / "raw").resolve()
    for value in frontmatter.get("sources", []):
        relative = Path(str(value or ""))
        if relative.is_absolute():
            continue
        raw_path = (project_root / relative).resolve()
        if not raw_path.is_relative_to(raw_root) or not raw_path.is_file():
            continue
        raw_frontmatter, _body, error = parse_page_text(raw_path.read_text())
        if error:
            continue
        identity = _normalized_upstream_identity(raw_frontmatter.get("url"))
        if identity:
            identities.add(identity)
    return identities


def _raw_upstream_identity(raw_path: Path) -> str:
    """Read the identity of the raw capture currently being finalized."""
    frontmatter, _body, error = parse_page_text(raw_path.read_text())
    if error:
        return ""
    return _normalized_upstream_identity(frontmatter.get("url"))


def _merge_racing_body(existing_body: str, proposed_body: str) -> str:
    """Retain content committed by the first racer and append genuinely new content."""
    existing = existing_body.strip()
    proposed = proposed_body.strip()
    if not existing:
        return proposed
    if not proposed or proposed in existing:
        return existing
    if existing in proposed:
        return proposed
    proposed_lines = proposed.splitlines()
    if proposed_lines and proposed_lines[0].startswith("# "):
        proposed_lines = proposed_lines[1:]
        while proposed_lines and not proposed_lines[0].strip():
            proposed_lines.pop(0)
    addition = "\n".join(proposed_lines).strip()
    return f"{existing}\n\n{addition}" if addition else existing


def _validate_source_provenance_expansion(
    existing_frontmatter: dict[str, Any],
    proposed_frontmatter: dict[str, Any],
    project_root: Path,
    raw_path: Path,
    current_identity: str,
    relative: str,
) -> None:
    """Reject untrusted provenance that would expand a source's identity set."""
    existing_sources = {
        str(value) for value in existing_frontmatter.get("sources", [])
    }
    raw_relative = raw_path.resolve().relative_to(project_root.resolve()).as_posix()
    raw_root = (project_root / "raw").resolve()
    for value in proposed_frontmatter.get("sources", []):
        source = str(value)
        if source in existing_sources or source == raw_relative:
            continue
        candidate = (project_root / source).resolve()
        if not candidate.is_relative_to(raw_root) or not candidate.is_file():
            raise ProposalError(
                f"source mutation contains unrelated provenance: {relative}"
            )
        candidate_identity = _raw_upstream_identity(candidate)
        if not current_identity or candidate_identity != current_identity:
            raise ProposalError(
                f"source mutation contains unrelated provenance: {relative}"
            )


def _reconcile_existing_page_create(
    canonical: Path,
    proposed_content: str,
    relative: str,
    expected_type: str,
    project_root: Path,
    raw_path: Path,
    expected_source_hash: str | None,
) -> str:
    """Turn a stale create proposal into a provenance-preserving upsert.

    Concurrent ingests can both build proposals before either transaction
    publishes. Once the first proposal commits, the second proposal's exact
    source/concept/entity paths are stale. A same-type, same-title collision is
    recoverable only when the current raw capture's upstream identity matches or,
    when that raw has no URL identity, its source hash matches. Source pages take
    the richer proposed body; concept/entity pages retain the first racer's body
    and append the second racer's new content. Prior provenance and accumulated
    metadata remain attached. Synthesis pages are intentionally excluded because
    merging their source lists also requires recomputing and re-auditing
    claim-level evidence counts.
    """
    existing_frontmatter, existing_body, existing_error = parse_page_text(
        canonical.read_text()
    )
    proposed_frontmatter, proposed_body, proposed_error = parse_page_text(proposed_content)
    if existing_error or proposed_error:
        detail = existing_error or proposed_error
        raise ProposalError(f"cannot reconcile existing page {relative}: {detail}")
    if (
        existing_frontmatter.get("type") != expected_type
        or proposed_frontmatter.get("type") != expected_type
    ):
        raise ProposalError(f"create mutation targets an existing page: {relative}")

    existing_title = _normalized_title(existing_frontmatter.get("title"))
    proposed_title = _normalized_title(proposed_frontmatter.get("title"))
    if not existing_title or existing_title != proposed_title:
        raise ProposalError(
            f"create mutation conflicts with a differently titled existing page: {relative}"
        )
    existing_hash = _normalize_source_hash(existing_frontmatter.get("source_hash"))
    proposed_hash = _normalize_source_hash(proposed_frontmatter.get("source_hash"))
    deterministic_hash = _normalize_source_hash(expected_source_hash)
    if expected_source_hash is not None and not deterministic_hash:
        raise ProposalError("deterministic current-raw hash is invalid")
    if not deterministic_hash:
        raise ProposalError(
            f"reconciliation requires the deterministic current-raw hash: {relative}"
        )
    if deterministic_hash and proposed_hash != deterministic_hash:
        raise ProposalError(
            f"reconciled page source_hash does not match the deterministic current-raw hash: {relative}"
        )
    raw_relative = raw_path.resolve().relative_to(project_root.resolve()).as_posix()
    if raw_relative not in {str(value) for value in proposed_frontmatter.get("sources", [])}:
        raise ProposalError(
            f"reconciled page provenance must include the current raw capture: {raw_relative}"
        )
    current_identity = _raw_upstream_identity(raw_path)
    matching_hash = bool(
        deterministic_hash and existing_hash == deterministic_hash
    )
    existing_identities = _source_identities(existing_frontmatter, project_root)
    matching_identity = bool(
        current_identity
        and (
            existing_identities == {current_identity}
            if expected_type == "source"
            else current_identity in existing_identities
        )
    )
    if (current_identity and not matching_identity) or (
        not current_identity and not matching_hash
    ):
        raise ProposalError(
            f"create mutation conflicts with an existing {expected_type} page having a different upstream identity: {relative}"
        )
    if expected_type == "source":
        _validate_source_provenance_expansion(
            existing_frontmatter,
            proposed_frontmatter,
            project_root,
            raw_path,
            current_identity,
            relative,
        )

    merged_frontmatter = dict(existing_frontmatter)
    merged_frontmatter.update(proposed_frontmatter)
    if existing_frontmatter.get("created"):
        merged_frontmatter["created"] = existing_frontmatter["created"]
    if existing_frontmatter.get("tier"):
        merged_frontmatter["tier"] = existing_frontmatter["tier"]
    if "quality_score" in existing_frontmatter:
        merged_frontmatter["quality_score"] = existing_frontmatter["quality_score"]
    for field in ("sources", "concepts", "related", "tags"):
        merged_frontmatter[field] = _merge_unique_list(
            existing_frontmatter.get(field), proposed_frontmatter.get(field)
        )

    rendered_frontmatter = yaml.safe_dump(
        merged_frontmatter,
        sort_keys=False,
        allow_unicode=True,
    ).strip()
    body = (
        proposed_body.strip()
        if expected_type == "source"
        else _merge_racing_body(existing_body, proposed_body)
    )
    return f"---\n{rendered_frontmatter}\n---\n\n{body.rstrip()}\n"


def _reconcile_existing_page_update(
    canonical: Path,
    proposed_content: str,
    relative: str,
    expected_type: str,
    project_root: Path,
    raw_path: Path,
    expected_source_hash: str | None,
) -> str:
    """Validate and merge an untrusted update against canonical page state.

    Updates may enrich concepts, entities, and synthesis pages with a new raw
    source, so those page types do not require an existing upstream identity
    match. Source pages represent one upstream document and therefore do.
    Every update is still bound to current-raw provenance and its deterministic
    preflight hash, and accumulated canonical state cannot be erased.
    """
    existing_frontmatter, existing_body, existing_error = parse_page_text(
        canonical.read_text()
    )
    proposed_frontmatter, proposed_body, proposed_error = parse_page_text(proposed_content)
    if existing_error or proposed_error:
        detail = existing_error or proposed_error
        raise ProposalError(f"cannot reconcile existing page {relative}: {detail}")
    if (
        existing_frontmatter.get("type") != expected_type
        or proposed_frontmatter.get("type") != expected_type
    ):
        raise ProposalError(f"update mutation conflicts with page type: {relative}")

    existing_title = _normalized_title(existing_frontmatter.get("title"))
    proposed_title = _normalized_title(proposed_frontmatter.get("title"))
    if not existing_title or existing_title != proposed_title:
        raise ProposalError(
            f"update mutation conflicts with a differently titled existing page: {relative}"
        )

    deterministic_hash = _normalize_source_hash(expected_source_hash)
    proposed_hash = _normalize_source_hash(proposed_frontmatter.get("source_hash"))
    if expected_source_hash is not None and not deterministic_hash:
        raise ProposalError("deterministic current-raw hash is invalid")
    if not deterministic_hash:
        raise ProposalError(
            f"update requires the deterministic current-raw hash: {relative}"
        )
    if proposed_hash != deterministic_hash:
        raise ProposalError(
            f"updated page source_hash does not match the deterministic current-raw hash: {relative}"
        )

    raw_relative = raw_path.resolve().relative_to(project_root.resolve()).as_posix()
    if raw_relative not in {str(value) for value in proposed_frontmatter.get("sources", [])}:
        raise ProposalError(
            f"updated page provenance must include the current raw capture: {raw_relative}"
        )

    if expected_type == "source":
        existing_hash = _normalize_source_hash(existing_frontmatter.get("source_hash"))
        current_identity = _raw_upstream_identity(raw_path)
        matching_hash = existing_hash == deterministic_hash
        existing_identities = _source_identities(existing_frontmatter, project_root)
        matching_identity = bool(
            current_identity and existing_identities == {current_identity}
        )
        if (current_identity and not matching_identity) or (
            not current_identity and not matching_hash
        ):
            raise ProposalError(
                f"update mutation conflicts with an existing source page having a different upstream identity: {relative}"
            )
        _validate_source_provenance_expansion(
            existing_frontmatter,
            proposed_frontmatter,
            project_root,
            raw_path,
            current_identity,
            relative,
        )

    merged_frontmatter = dict(existing_frontmatter)
    merged_frontmatter.update(proposed_frontmatter)
    if existing_frontmatter.get("created"):
        merged_frontmatter["created"] = existing_frontmatter["created"]
    if existing_frontmatter.get("tier"):
        merged_frontmatter["tier"] = existing_frontmatter["tier"]
    if "quality_score" in existing_frontmatter:
        merged_frontmatter["quality_score"] = existing_frontmatter["quality_score"]
    for field in ("sources", "concepts", "related", "tags"):
        merged_frontmatter[field] = _merge_unique_list(
            existing_frontmatter.get(field), proposed_frontmatter.get(field)
        )

    rendered_frontmatter = yaml.safe_dump(
        merged_frontmatter,
        sort_keys=False,
        allow_unicode=True,
    ).strip()
    body = _merge_racing_body(existing_body, proposed_body)
    return f"---\n{rendered_frontmatter}\n---\n\n{body.rstrip()}\n"


def _schema_errors(proposal: dict[str, Any]) -> list[str]:
    errors = sorted(
        Draft202012Validator(PROPOSAL_SCHEMA).iter_errors(proposal),
        key=lambda error: tuple(str(part) for part in error.absolute_path),
    )
    return [
        f"proposal schema at {'.'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
        for error in errors
    ]


def _normalized_mutation_path(root: Path, value: object) -> tuple[str, Path, str]:
    text = str(value or "").strip()
    match = PAGE_PATH_RE.fullmatch(text)
    if not match:
        raise ProposalError(f"invalid canonical page path: {text!r}")
    path = (root / text).resolve()
    if not path.is_relative_to((root / "wiki").resolve()):
        raise ProposalError(f"proposal path escapes wiki/: {text!r}")
    return text, path, CATEGORY_TYPE[match.group("category")]


def _prevalidate_proposal(
    proposal: dict[str, Any], project_root: Path
) -> list[tuple[str, Path, str]]:
    """Reject malformed/unsafe proposals before touching candidate paths."""
    errors = _schema_errors(proposal)
    if errors:
        raise ProposalError("; ".join(errors))
    if proposal.get("status") != "success":
        raise ProposalError(f"agent returned status={proposal.get('status')!r}")
    return [
        _normalized_mutation_path(project_root, mutation["path"])
        for mutation in proposal["page_mutations"]
    ]


def _copy_transaction_inputs(project_root: Path, stage_root: Path) -> None:
    shutil.copytree(project_root / "wiki", stage_root / "wiki", dirs_exist_ok=True)
    (stage_root / "raw").mkdir(parents=True, exist_ok=True)
    for source in (project_root / "raw").rglob("*.md"):
        relative = source.relative_to(project_root)
        destination = stage_root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    tracker = project_root / "reports" / "checkpoint-graph-tracker.md"
    if tracker.is_file():
        destination = stage_root / "reports" / tracker.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(tracker, destination)


def _write_mutations(
    proposal: dict[str, Any],
    project_root: Path,
    stage_root: Path,
    raw_path: Path,
    expected_source_hash: str | None = None,
) -> list[str]:
    validated_paths = _prevalidate_proposal(proposal, project_root)

    source_path = str(proposal.get("source_path") or "")
    seen: set[str] = set()
    mutation_paths: list[str] = []
    source_mutations = 0
    for mutation, (relative, canonical, expected_type) in zip(
        proposal["page_mutations"], validated_paths, strict=True
    ):
        if relative in seen:
            raise ProposalError(f"duplicate mutation path: {relative}")
        seen.add(relative)
        operation = mutation["operation"]
        content = mutation["content"]
        if operation == "create" and canonical.exists():
            if expected_type not in {"source", "concept", "entity"}:
                raise ProposalError(f"create mutation targets an existing page: {relative}")
            if expected_type == "source" and relative != source_path:
                raise ProposalError(f"create mutation targets an existing page: {relative}")
            content = _reconcile_existing_page_create(
                canonical,
                content,
                relative,
                expected_type,
                project_root,
                raw_path,
                expected_source_hash,
            )
        if operation == "update":
            if not canonical.is_file():
                raise ProposalError(f"update mutation targets a missing page: {relative}")
            content = _reconcile_existing_page_update(
                canonical,
                content,
                relative,
                expected_type,
                project_root,
                raw_path,
                expected_source_hash,
            )
        if expected_type == "source":
            source_mutations += 1
            if relative != source_path:
                raise ProposalError("source_path must name the single source page mutation")
            proposed_frontmatter, _proposed_body, proposed_error = parse_page_text(content)
            if proposed_error:
                raise ProposalError(f"{relative}: {proposed_error}")
            existing_frontmatter: dict[str, Any] = {}
            if canonical.is_file():
                existing_frontmatter, _existing_body, existing_error = parse_page_text(
                    canonical.read_text()
                )
                if existing_error:
                    raise ProposalError(f"{relative}: {existing_error}")
            _validate_source_provenance_expansion(
                existing_frontmatter,
                proposed_frontmatter,
                project_root,
                raw_path,
                _raw_upstream_identity(raw_path),
                relative,
            )

        staged = stage_root / relative
        staged.parent.mkdir(parents=True, exist_ok=True)
        staged.write_text(content)
        page_errors = validate_page(staged, stage_root, expected_type=expected_type)
        if page_errors:
            raise ProposalError(f"{relative}: " + "; ".join(page_errors))
        mutation_paths.append(relative)

    if source_mutations != 1 or source_path not in seen:
        raise ProposalError("a successful proposal must contain exactly one source page mutation")

    expected_raw = raw_path.resolve().relative_to(project_root.resolve()).as_posix()
    source_frontmatter, _body, parse_error = parse_page_text((stage_root / source_path).read_text())
    if parse_error or expected_raw not in {str(value) for value in source_frontmatter.get("sources", [])}:
        raise ProposalError(f"source page provenance must include {expected_raw}")
    if expected_source_hash and _normalize_source_hash(
        source_frontmatter.get("source_hash")
    ) != _normalize_source_hash(expected_source_hash):
        raise ProposalError("source page source_hash does not match the deterministic preflight hash")

    for relative in mutation_paths:
        if relative.startswith("wiki/synthesis/"):
            from audit_synthesis import audit_page

            audit = audit_page(stage_root / relative, stage_root, strict=True)
            if not audit.passed:
                codes = ", ".join(finding.code for finding in audit.findings)
                raise ProposalError(
                    f"strict synthesis audit failed for {relative}: score={audit.score}; {codes}"
                )

    return mutation_paths


def _append_kg_facts(stage_root: Path, facts: list[dict[str, Any]]) -> str | None:
    if not facts:
        return None
    path = stage_root / "wiki" / ".kg-pending.jsonl"
    existing = path.read_text() if path.exists() else ""
    lines = [json.dumps(fact, sort_keys=True) for fact in facts]
    path.write_text(existing.rstrip("\n") + ("\n" if existing.strip() else "") + "\n".join(lines) + "\n")
    return "wiki/.kg-pending.jsonl"


def _append_log(
    stage_root: Path,
    *,
    backend: str,
    raw_relative: str,
    targets: list[str],
    notes: str,
) -> None:
    path = stage_root / "wiki" / "log.md"
    content = path.read_text() if path.exists() else "# Wiki Log\n\n```yaml\n"
    content = content.rstrip()
    if content.endswith("```"):
        content = content[:-3].rstrip()
    escaped_notes = notes.replace('"', "'").replace("\n", " ")
    target_lines = "\n".join(f"    - {target}" for target in targets)
    block = (
        f"\n- timestamp: {datetime.now(timezone.utc).isoformat(timespec='seconds')}\n"
        "  operation: ingest\n"
        f"  agent: {backend}\n"
        "  targets:\n"
        f"{target_lines}\n"
        f"  source: {raw_relative}\n"
        "  status: success\n"
        f"  notes: \"{escaped_notes}\"\n"
        "```\n"
    )
    path.write_text(content + block)


def _update_staged_raw_status(stage_raw: Path) -> None:
    text = stage_raw.read_text()
    updated, count = re.subn(
        r"^(status:\s*).*$",
        r"\g<1>ingested",
        text,
        count=1,
        flags=re.MULTILINE,
    )
    if count != 1:
        raise ProposalError("raw source is missing exactly one status field")
    stage_raw.write_text(updated)


def _build_graph(stage_root: Path, runtime_scripts: Path | None = None) -> None:
    runtime_root = runtime_scripts or Path(__file__).resolve().parent
    builder = runtime_root / "graph_builder.py"
    if not builder.is_file():
        candidates = (
            runtime_root.parent / "wiki-graph-api" / "graph_builder.py",
            stage_root.parent / "wiki-graph-api" / "graph_builder.py",
        )
        builder = next((candidate for candidate in candidates if candidate.is_file()), builder)
        if not builder.is_file():
            raise FileNotFoundError("graph_builder.py is unavailable to ingest finalization")
    graph_path = stage_root / "wiki" / "graph" / "graph.json"
    tracker_path = stage_root / "reports" / "checkpoint-graph-tracker.md"
    subprocess.run(
        [
            sys.executable,
            str(builder),
            "--wiki",
            str(stage_root / "wiki"),
            "--cache",
            str(stage_root / ".graph_cache"),
            "--out",
            str(graph_path),
            "--tracker",
            str(tracker_path),
        ],
        check=True,
        timeout=300,
    )
    payload = json.loads(graph_path.read_text())
    nodes = payload.get("nodes")
    edges = payload.get("edges")
    if not isinstance(nodes, list) or not isinstance(edges, list):
        raise RuntimeError("graph builder produced an invalid artifact")
    node_ids = [node.get("id") for node in nodes if isinstance(node, dict)]
    if (
        len(node_ids) != len(nodes)
        or any(not isinstance(node_id, str) or not node_id for node_id in node_ids)
        or len(set(node_ids)) != len(node_ids)
        or payload.get("node_count") != len(nodes)
        or payload.get("edge_count") != len(edges)
    ):
        raise RuntimeError("graph builder produced invalid node/edge counts or IDs")
    node_id_set = set(node_ids)
    if any(
        not isinstance(edge, dict)
        or edge.get("source") not in node_id_set
        or edge.get("target") not in node_id_set
        for edge in edges
    ):
        raise RuntimeError("graph builder produced an edge with a missing endpoint")
    if payload.get("source_signature") != _compute_wiki_signature(stage_root / "wiki"):
        raise RuntimeError("graph source_signature does not match the staged wiki")
    if not tracker_path.is_file():
        raise RuntimeError("graph builder did not produce the checkpoint tracker")


def _compute_wiki_signature(wiki_dir: Path) -> str:
    """Mirror the graph builder's deterministic source signature contract."""
    digest = hashlib.sha256()
    count = 0
    for page in sorted(wiki_dir.rglob("*.md")):
        if page.name in {"index.md", "hot.md", "log.md"}:
            continue
        if "/.obsidian/" in page.as_posix() or "/meta/" in page.as_posix():
            continue
        relative = page.relative_to(wiki_dir).as_posix()
        digest.update(relative.encode("utf-8", errors="ignore"))
        digest.update(b"\0")
        digest.update(hashlib.sha256(page.read_bytes()).hexdigest().encode())
        digest.update(b"\n")
        count += 1
    digest.update(f"count={count}".encode())
    return digest.hexdigest()


def _digest_or_none(path: Path) -> str | None:
    if not path.exists():
        return None
    if not path.is_file():
        raise ProposalError(f"transaction target is not a file: {path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _atomic_publish(
    project_root: Path,
    stage_root: Path,
    relative_paths: list[str],
    before: dict[str, str | None],
) -> None:
    unique_paths = list(dict.fromkeys(relative_paths))
    for relative in unique_paths:
        if _digest_or_none(project_root / relative) != before.get(relative):
            raise ProposalError(f"concurrent change detected before publish: {relative}")

    originals: dict[str, bytes | None] = {
        relative: (project_root / relative).read_bytes()
        if (project_root / relative).is_file()
        else None
        for relative in unique_paths
    }
    published: list[str] = []
    try:
        for relative in unique_paths:
            source = stage_root / relative
            if not source.is_file():
                raise ProposalError(f"staged transaction artifact is missing: {relative}")
            destination = project_root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            fd, temp_name = tempfile.mkstemp(prefix=f".{destination.name}.", dir=destination.parent)
            try:
                with os.fdopen(fd, "wb") as handle:
                    handle.write(source.read_bytes())
                    handle.flush()
                    os.fsync(handle.fileno())
                os.replace(temp_name, destination)
            finally:
                if os.path.exists(temp_name):
                    os.unlink(temp_name)
            published.append(relative)
    except Exception:
        for relative in reversed(published):
            destination = project_root / relative
            original = originals[relative]
            if original is None:
                destination.unlink(missing_ok=True)
            else:
                destination.write_bytes(original)
        raise


def rebuild_graph_artifacts(
    project_root: Path,
    runtime_scripts: Path | None = None,
) -> None:
    """Rebuild and validate canonical graph artifacts as a finalization gate."""
    runtime_root = runtime_scripts or Path(__file__).resolve().parent
    if not (runtime_root / "graph_builder.py").is_file():
        runtime_root = project_root / "wiki-graph-api"
    _build_graph(project_root.resolve(), runtime_root)


def _prepare_and_publish_locked(
    proposal: dict[str, Any],
    project_root: Path,
    raw_path: Path,
    *,
    backend: str,
    validation_run: bool,
    runtime_scripts: Path | None = None,
    expected_source_hash: str | None = None,
) -> list[str]:
    """Validate, derive, and atomically publish one complete ingest transaction."""
    project_root = project_root.resolve()
    raw_path = raw_path.resolve()
    raw_relative = raw_path.relative_to(project_root).as_posix()
    runtime_root = runtime_scripts or Path(__file__).resolve().parent
    validated_paths = _prevalidate_proposal(proposal, project_root)

    candidate_paths = [
        relative for relative, _canonical, _expected_type in validated_paths
    ]
    candidate_paths.extend(
        [raw_relative, "wiki/index.md", "wiki/graph/graph.json", "reports/checkpoint-graph-tracker.md"]
    )
    if proposal.get("kg_facts"):
        candidate_paths.append("wiki/.kg-pending.jsonl")
    if not validation_run:
        candidate_paths.append("wiki/log.md")
    candidate_paths = [path for path in dict.fromkeys(candidate_paths) if path]
    before = {relative: _digest_or_none(project_root / relative) for relative in candidate_paths}

    with tempfile.TemporaryDirectory(prefix="labs-wiki-ingest-") as tmp:
        stage_root = Path(tmp) / "repo"
        _copy_transaction_inputs(project_root, stage_root)
        mutation_paths = _write_mutations(
            proposal,
            project_root,
            stage_root,
            raw_path,
            expected_source_hash=expected_source_hash,
        )
        kg_path = _append_kg_facts(stage_root, proposal.get("kg_facts", []))

        index_path = stage_root / "wiki" / "index.md"
        index_path.write_text(compile_index(str(stage_root)))
        _build_graph(stage_root, runtime_root)

        staged_raw = stage_root / raw_relative
        _update_staged_raw_status(staged_raw)
        final_paths = [
            *mutation_paths,
            "wiki/index.md",
            "wiki/graph/graph.json",
            "reports/checkpoint-graph-tracker.md",
            raw_relative,
        ]
        if kg_path:
            final_paths.append(kg_path)
        if not validation_run:
            _append_log(
                stage_root,
                backend=backend,
                raw_relative=raw_relative,
                targets=mutation_paths,
                notes=str(proposal.get("notes") or ""),
            )
            final_paths.append("wiki/log.md")

        _atomic_publish(project_root, stage_root, final_paths, before)
        return list(dict.fromkeys(final_paths))


def prepare_and_publish(
    proposal: dict[str, Any],
    project_root: Path,
    raw_path: Path,
    *,
    backend: str,
    validation_run: bool,
    runtime_scripts: Path | None = None,
    expected_source_hash: str | None = None,
) -> list[str]:
    """Serialize ingest finalization and atomically publish one proposal."""
    project_root = project_root.resolve()
    lock_id = hashlib.sha256(str(project_root).encode()).hexdigest()[:16]
    lock_path = Path(tempfile.gettempdir()) / f"labs-wiki-ingest-{lock_id}.lock"
    with lock_path.open("a+") as lock_handle:
        fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX)
        try:
            return _prepare_and_publish_locked(
                proposal,
                project_root,
                raw_path,
                backend=backend,
                validation_run=validation_run,
                runtime_scripts=runtime_scripts,
                expected_source_hash=expected_source_hash,
            )
        finally:
            fcntl.flock(lock_handle.fileno(), fcntl.LOCK_UN)
