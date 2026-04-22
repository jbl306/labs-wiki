#!/usr/bin/env python3
"""Promote wiki pages between consolidation tiers per docs/memory-model.md.

Rules (never demote):
  * hot → established      when last_verified is set AND inbound degree ≥ 1
  * established → core     when inbound degree ≥ 3 AND quality_score ≥ 70
                           (skipped with a warning if quality_score absent)

Modes:
  --dry-run (default)  print proposed transitions, exit 0, write nothing
  --apply              rewrite frontmatter `tier:` and append a log line per
                       transition to wiki/log.md

Idempotent: re-running --apply against a freshly-promoted corpus reports 0
transitions.

Inputs:
  GRAPH_PATH env var, else wiki-graph-api/.cache/graph.json if present, else
  wiki-graph-api/graph.json. (The live builder writes to wiki/graph/graph.json
  in this repo; that path is also honored as a final fallback.)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = REPO_ROOT / "wiki"
LOG_PATH = WIKI_DIR / "log.md"

GRAPH_CANDIDATES = [
    REPO_ROOT / "wiki-graph-api" / ".cache" / "graph.json",
    REPO_ROOT / "wiki-graph-api" / "graph.json",
    REPO_ROOT / "wiki" / "graph" / "graph.json",
]

# Tier ordering for "never demote" enforcement.
TIER_ORDER = {"archive": 0, "hot": 1, "established": 2, "core": 3, "workflow": 4}


def resolve_graph_path() -> Path:
    env = os.environ.get("GRAPH_PATH")
    if env:
        p = Path(env)
        if p.exists():
            return p
        print(f"warning: GRAPH_PATH={env} does not exist; falling back", file=sys.stderr)
    for c in GRAPH_CANDIDATES:
        if c.exists():
            return c
    raise FileNotFoundError(
        "no graph.json found. Set GRAPH_PATH or build the graph first. "
        f"Tried: {[str(c) for c in GRAPH_CANDIDATES]}"
    )


def load_graph(path: Path) -> dict:
    with path.open() as f:
        return json.load(f)


def inbound_degree_map(graph: dict) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for edge in graph.get("edges", []) or graph.get("links", []):
        tgt = edge.get("target")
        if tgt:
            counts[tgt] += 1
    return counts


def split_frontmatter(text: str) -> tuple[dict | None, str, str]:
    """Return (frontmatter_dict, frontmatter_raw, body). dict is None when no FM."""
    if not text.startswith("---\n"):
        return None, "", text
    end = text.find("\n---", 4)
    if end == -1:
        return None, "", text
    raw = text[4:end]
    body = text[end + len("\n---") :]
    if body.startswith("\n"):
        body = body[1:]
    try:
        data = yaml.safe_load(raw) or {}
        if not isinstance(data, dict):
            return None, "", text
    except yaml.YAMLError:
        return None, "", text
    return data, raw, body


def rewrite_tier(path: Path, new_tier: str) -> None:
    text = path.read_text()
    fm, raw, body = split_frontmatter(text)
    if fm is None:
        raise ValueError(f"no parseable frontmatter in {path}")
    fm["tier"] = new_tier
    new_fm = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True).rstrip() + "\n"
    path.write_text(f"---\n{new_fm}---\n{body}")


def append_log(slug: str, old: str, new: str) -> None:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = f"{ts}: tier-promotion: {slug}: {old} → {new}\n"
    with LOG_PATH.open("a") as f:
        f.write(line)


def evaluate_node(node: dict, inbound: int) -> tuple[str | None, str]:
    """Return (proposed_new_tier or None, reason)."""
    current = (node.get("tier") or "").strip()
    last_verified = node.get("last_verified")
    quality = node.get("quality_score")

    if current == "hot" and last_verified and inbound >= 1:
        return "established", f"last_verified={last_verified}, inbound={inbound}"

    if current == "established":
        if inbound < 3:
            return None, f"inbound={inbound} < 3"
        if quality is None:
            print(
                f"warning: skipping core promotion for {node.get('id')}: quality_score missing",
                file=sys.stderr,
            )
            return None, "quality_score absent"
        if quality >= 70:
            return "core", f"inbound={inbound}, quality_score={quality}"
        return None, f"quality_score={quality} < 70"

    return None, "no rule applies"


def page_path_for_node(node: dict) -> Path | None:
    rel = node.get("path") or (node.get("id", "") + ".md")
    if not rel.endswith(".md"):
        rel = rel + ".md"
    candidate = WIKI_DIR / rel
    return candidate if candidate.exists() else None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    grp = ap.add_mutually_exclusive_group()
    grp.add_argument("--dry-run", action="store_true", default=True)
    grp.add_argument("--apply", dest="apply_changes", action="store_true")
    args = ap.parse_args()

    apply_changes = bool(args.apply_changes)
    if apply_changes:
        args.dry_run = False

    graph_path = resolve_graph_path()
    print(f"graph: {graph_path}")
    graph = load_graph(graph_path)
    inbound = inbound_degree_map(graph)

    transitions: list[tuple[str, str, str, Path]] = []
    skipped_missing_file = 0

    for node in graph.get("nodes", []):
        node_id = node.get("id")
        if not node_id:
            continue
        new_tier, reason = evaluate_node(node, inbound.get(node_id, 0))
        if new_tier is None:
            continue
        current = (node.get("tier") or "").strip()
        if TIER_ORDER.get(new_tier, 0) <= TIER_ORDER.get(current, 0):
            continue  # never demote
        page = page_path_for_node(node)
        if page is None:
            skipped_missing_file += 1
            continue
        transitions.append((node_id, current, new_tier, page))

    counts: Counter[str] = Counter()
    for node_id, current, new_tier, page in transitions:
        key = f"{current} → {new_tier}"
        counts[key] += 1
        slug = node_id
        if args.dry_run:
            print(f"[dry-run] {slug}: {current} → {new_tier}")
        else:
            rewrite_tier(page, new_tier)
            append_log(slug, current, new_tier)
            print(f"[apply]   {slug}: {current} → {new_tier}")

    print()
    print("Summary:")
    if not counts:
        print("  0 transitions")
    else:
        for transition, n in sorted(counts.items()):
            print(f"  {transition}: {n}")
    print(f"  total: {sum(counts.values())}")
    if skipped_missing_file:
        print(f"  skipped (page file not found): {skipped_missing_file}")
    print(f"  mode: {'apply' if apply_changes else 'dry-run'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
