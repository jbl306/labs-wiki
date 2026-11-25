#!/usr/bin/env python3
"""Replay wiki/.kg-pending.jsonl into MemPalace.

The auto-ingest container can't talk to the MemPalace MCP, so it appends
KG facts to a JSONL sidecar instead. This script (run on the host) drains
that file by calling `KnowledgeGraph.add_triple` directly. Successfully
applied facts are removed; failures stay for the next run.

Usage:
    python scripts/replay_kg_facts.py             # uses default palace
    python scripts/replay_kg_facts.py --dry-run

Requires the `mempalace` package to be importable (e.g. run via pipx-managed
venv: /home/jbl/.local/share/pipx/venvs/mempalace/bin/python).
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
PENDING = REPO / "wiki" / ".kg-pending.jsonl"


def auto_commit_wiki() -> bool:
    """Commit periodic wiki and raw snapshots without touching other staged paths."""
    try:
        subprocess.run(
            ["git", "-C", str(REPO), "add", "wiki", "raw"],
            check=True, capture_output=True,
        )
        diff = subprocess.run(
            ["git", "-C", str(REPO), "diff", "--cached", "--quiet", "--", "wiki", "raw"],
            capture_output=True,
        )
        if diff.returncode == 0:
            return True  # nothing staged
        if diff.returncode != 1:
            diff.check_returncode()
        msg = (
            "wiki(auto-ingest): periodic snapshot\n\n"
            "Auto-committed by scripts/replay_kg_facts.py cron."
        )
        subprocess.run(
            ["git", "-C", str(REPO), "commit", "--only", "-m", msg, "--", "wiki", "raw"],
            check=True, capture_output=True,
        )
        print("[commit] staged wiki/raw changes committed")
        return True
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or b"").decode(errors="replace").strip()
        print(f"[commit] failed: {detail[:200] or str(exc)}", file=sys.stderr)
    except OSError as exc:
        print(f"[commit] failed: {exc}", file=sys.stderr)
    return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default=str(PENDING), help="Path to JSONL")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"No pending facts at {path}", file=sys.stderr)
        if not args.dry_run and not auto_commit_wiki():
            return 1
        return 0

    try:
        from mempalace.knowledge_graph import KnowledgeGraph
    except ImportError:
        print(
            "mempalace not importable; run with the mempalace venv:\n"
            "  /home/jbl/.local/share/pipx/venvs/mempalace/bin/python "
            f"{Path(__file__).relative_to(REPO)}",
            file=sys.stderr,
        )
        return 2

    kg = KnowledgeGraph() if not args.dry_run else None

    applied = 0
    remaining: list[str] = []
    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line:
            continue
        try:
            fact = json.loads(line)
        except json.JSONDecodeError as e:
            print(f"[skip] bad JSON: {e} | {line[:120]}", file=sys.stderr)
            remaining.append(raw_line)
            continue

        subject = fact.get("subject")
        predicate = fact.get("predicate")
        obj = fact.get("object")
        if not (subject and predicate and obj):
            print(f"[skip] missing subject/predicate/object: {line[:120]}",
                  file=sys.stderr)
            remaining.append(raw_line)
            continue

        if args.dry_run:
            print(f"[dry] {subject} --[{predicate}]--> {obj}")
            applied += 1
            continue

        try:
            kg.add_triple(
                subject=subject,
                predicate=predicate,
                obj=obj,
                source_closet=fact.get("source_closet"),
                valid_from=fact.get("valid_from"),
            )
            applied += 1
        except Exception as exc:  # keep for retry
            print(f"[fail] {subject}/{predicate}/{obj}: {exc}", file=sys.stderr)
            remaining.append(raw_line)

    if not args.dry_run:
        if remaining:
            path.write_text("\n".join(remaining) + "\n")
        else:
            path.unlink()
        if kg is not None:
            kg.close()

    print(f"Replayed {applied} fact(s); {len(remaining)} remaining.")
    if not args.dry_run and not auto_commit_wiki():
        return 1
    return 0 if not remaining else 1


if __name__ == "__main__":
    sys.exit(main())
