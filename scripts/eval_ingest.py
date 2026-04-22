#!/usr/bin/env python3
"""End-to-end ingest evaluation harness (R18).

Lite mode: instead of calling the LLM, walks the existing wiki output produced
by prior ingests of each fixture's raw source and scores it against
expected concepts, entities, sources, and dates.

Usage:
    python3 scripts/eval_ingest.py \
        --fixtures tests/eval_fixtures/sources.json \
        --report-out reports/eval-ingest-2026-04-21.json
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterable

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from lint_wiki import (  # noqa: E402  (path-injected import)
    build_wikilink_lookup,
    find_wikilinks,
    wikilink_exists,
)


def parse_frontmatter(path: Path) -> dict | None:
    """Full-fidelity YAML frontmatter parser (preserves list-valued fields)."""
    try:
        content = path.read_text()
    except Exception:
        return None
    if not content.startswith("---"):
        return None
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None
    try:
        loaded = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return None
    return loaded if isinstance(loaded, dict) else None

WIKI_DIR = REPO_ROOT / "wiki"
SECTIONS = ("concepts", "sources", "entities", "synthesis")

# Score thresholds — fixture "passes" when all are satisfied.
THRESHOLDS = {
    "concept_count_min_ratio": 1.0,   # all expected concepts must reference the source
    "broken_link_count_max": 0,
    "date_accuracy_min": 1.0,         # 100% of expected dates must be present, none drifted
    "entity_completeness_min": 1.0,   # all expected entities must exist
}


def _list_pages(section: str) -> list[Path]:
    section_dir = WIKI_DIR / section
    if not section_dir.exists():
        return []
    return sorted(section_dir.glob("*.md"))


def _all_pages() -> list[Path]:
    pages: list[Path] = []
    for section in SECTIONS:
        pages.extend(_list_pages(section))
    return pages


def _fm_sources(fm: dict | None) -> list[str]:
    if not fm:
        return []
    raw = fm.get("sources") or []
    if isinstance(raw, str):
        return [raw]
    return [str(s) for s in raw if s]


def _fm_concepts(fm: dict | None) -> list[str]:
    if not fm:
        return []
    raw = fm.get("concepts") or []
    if isinstance(raw, str):
        return [raw]
    return [str(s) for s in raw if s]


def _entity_index() -> set[str]:
    """Slug stems of every wiki/entities/*.md page."""
    return {p.stem for p in _list_pages("entities")}


def _entity_matches(expected: str, entity_stems: set[str]) -> bool:
    """Exact stem match, or any entity stem that contains the expected slug.

    Supports cases like expected='karpathy' matching
    'karpathy-compile-once-wiki-principle'.
    """
    if expected in entity_stems:
        return True
    for stem in entity_stems:
        # word-boundary-ish match on slugs separated by '-'
        parts = stem.split("-")
        if expected in parts:
            return True
        if stem.startswith(f"{expected}-") or stem.endswith(f"-{expected}"):
            return True
    return False


def _pages_referencing_raw(raw_md_path: str) -> list[Path]:
    """Wiki pages whose frontmatter `sources:` contains raw_md_path."""
    matches: list[Path] = []
    for page in _all_pages():
        fm = parse_frontmatter(page)
        if raw_md_path in _fm_sources(fm):
            matches.append(page)
    return matches


def _expected_dates_present(dates_iso: Iterable[str], pages: list[Path]) -> tuple[int, int, list[str]]:
    """Return (matched, total_expected, drift_notes)."""
    expected = list(dates_iso)
    if not expected:
        return (0, 0, [])

    expected_dates: list[date] = []
    for d in expected:
        try:
            expected_dates.append(datetime.strptime(d, "%Y-%m-%d").date())
        except ValueError:
            expected_dates.append(date.min)

    observed: set[date] = set()
    for page in pages:
        fm = parse_frontmatter(page) or {}
        for field in ("created", "last_verified"):
            val = fm.get(field)
            if isinstance(val, date):
                observed.add(val)
            elif isinstance(val, str):
                try:
                    observed.add(datetime.strptime(val[:10], "%Y-%m-%d").date())
                except ValueError:
                    pass

    matched = sum(1 for d in expected_dates if d in observed)
    drift_notes: list[str] = []
    for exp in expected_dates:
        if exp in observed:
            continue
        # find nearest observed date in same month/year for a drift hint
        nearest = None
        for o in observed:
            if o.year == exp.year and o.month == exp.month:
                nearest = o
                break
        if nearest:
            drift_notes.append(f"expected {exp.isoformat()} drifted to {nearest.isoformat()}")
        else:
            drift_notes.append(f"expected {exp.isoformat()} not found in any page frontmatter")
    return (matched, len(expected_dates), drift_notes)


def evaluate_fixture(fx: dict[str, Any]) -> dict[str, Any]:
    name = fx["name"]
    raw_md_path = fx["raw_md_path"]
    expected_concepts: list[str] = list(fx.get("expected_concepts", []))
    expected_entities: list[str] = list(fx.get("expected_entities", []))
    expected_min_sources: int = int(fx.get("expected_min_sources", 1))
    expected_dates: list[str] = list(fx.get("expected_dates", []))

    pages = _pages_referencing_raw(raw_md_path)
    if not pages:
        return {
            "name": name,
            "raw_md_path": raw_md_path,
            "status": "skipped",
            "reason": "no historical output",
            "passed": False,
        }

    # ---- concept_count ----------------------------------------------------
    concept_pages = [p for p in pages if p.parent.name == "concepts"]
    concept_slugs_present = {p.stem for p in concept_pages}
    # Also gather concepts named in any source/synthesis page that lists this raw.
    declared_concepts: set[str] = set()
    for p in pages:
        fm = parse_frontmatter(p)
        for c in _fm_concepts(fm):
            declared_concepts.add(c)
    all_concepts = concept_slugs_present | declared_concepts

    matched_concepts = [c for c in expected_concepts if c in all_concepts]
    concept_count = len(all_concepts)
    concept_min_ratio = (
        len(matched_concepts) / len(expected_concepts) if expected_concepts else 1.0
    )

    # ---- broken_link_count -----------------------------------------------
    all_wiki_pages = _all_pages()
    titles, slugs = build_wikilink_lookup(all_wiki_pages)
    broken_links: list[dict[str, str]] = []
    for p in pages:
        for link in find_wikilinks(p):
            if not wikilink_exists(link, titles, slugs):
                broken_links.append({"page": str(p.relative_to(REPO_ROOT)), "link": link})

    # ---- date_accuracy ---------------------------------------------------
    matched_dates, total_dates, drift_notes = _expected_dates_present(expected_dates, pages)
    date_accuracy = matched_dates / total_dates if total_dates else 1.0

    # ---- entity_completeness ---------------------------------------------
    entity_stems = _entity_index()
    entity_results = {e: _entity_matches(e, entity_stems) for e in expected_entities}
    entity_completeness = (
        sum(1 for ok in entity_results.values() if ok) / len(entity_results)
        if entity_results
        else 1.0
    )

    # ---- min_sources -----------------------------------------------------
    source_pages = [p for p in pages if p.parent.name == "sources"]
    sources_count = len(source_pages)

    passed = (
        concept_min_ratio >= THRESHOLDS["concept_count_min_ratio"]
        and len(broken_links) <= THRESHOLDS["broken_link_count_max"]
        and date_accuracy >= THRESHOLDS["date_accuracy_min"]
        and entity_completeness >= THRESHOLDS["entity_completeness_min"]
        and sources_count >= expected_min_sources
    )

    return {
        "name": name,
        "raw_md_path": raw_md_path,
        "status": "evaluated",
        "passed": passed,
        "pages_considered": [str(p.relative_to(REPO_ROOT)) for p in pages],
        "scores": {
            "concept_count": concept_count,
            "expected_concepts_matched": matched_concepts,
            "expected_concepts_missing": [c for c in expected_concepts if c not in all_concepts],
            "concept_min_ratio": round(concept_min_ratio, 3),
            "broken_link_count": len(broken_links),
            "broken_links": broken_links,
            "date_accuracy": round(date_accuracy, 3),
            "date_drift_notes": drift_notes,
            "entity_completeness": round(entity_completeness, 3),
            "entity_results": entity_results,
            "sources_count": sources_count,
            "expected_min_sources": expected_min_sources,
        },
    }


def render_markdown_summary(report: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append(f"# Ingest Eval Summary — {report['generated']}")
    lines.append("")
    lines.append(f"Fixtures: {report['totals']['total']} | "
                 f"passed: {report['totals']['passed']} | "
                 f"failed: {report['totals']['failed']} | "
                 f"skipped: {report['totals']['skipped']}")
    lines.append("")
    lines.append("| Fixture | Status | Concepts ✓ | Broken links | Date acc | Entities ✓ | Sources |")
    lines.append("|---|---|---|---|---|---|---|")
    for r in report["fixtures"]:
        if r["status"] == "skipped":
            lines.append(f"| {r['name']} | skipped ({r['reason']}) | — | — | — | — | — |")
            continue
        s = r["scores"]
        status = "PASS" if r["passed"] else "FAIL"
        lines.append(
            f"| {r['name']} | {status} | "
            f"{len(s['expected_concepts_matched'])}/"
            f"{len(s['expected_concepts_matched']) + len(s['expected_concepts_missing'])} | "
            f"{s['broken_link_count']} | {s['date_accuracy']} | "
            f"{int(s['entity_completeness'] * 100)}% | "
            f"{s['sources_count']}/{s['expected_min_sources']} |"
        )
    lines.append("")
    for r in report["fixtures"]:
        if r["status"] == "skipped" or r["passed"]:
            continue
        lines.append(f"## ✗ {r['name']}")
        s = r["scores"]
        if s["expected_concepts_missing"]:
            lines.append(f"- missing concepts: {s['expected_concepts_missing']}")
        if s["broken_links"]:
            lines.append(f"- broken links ({s['broken_link_count']}):")
            for bl in s["broken_links"][:10]:
                lines.append(f"  - `{bl['page']}` → [[{bl['link']}]]")
        if s["date_drift_notes"]:
            lines.append(f"- date drift: {s['date_drift_notes']}")
        missing_ents = [e for e, ok in s["entity_results"].items() if not ok]
        if missing_ents:
            lines.append(f"- missing entities: {missing_ents}")
        if s["sources_count"] < s["expected_min_sources"]:
            lines.append(f"- sources_count {s['sources_count']} < expected {s['expected_min_sources']}")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixtures", required=True, type=Path)
    ap.add_argument("--report-out", required=True, type=Path)
    args = ap.parse_args()

    fixtures = json.loads(args.fixtures.read_text())
    results = [evaluate_fixture(fx) for fx in fixtures]

    totals = {
        "total": len(results),
        "passed": sum(1 for r in results if r.get("passed")),
        "failed": sum(1 for r in results if r.get("status") == "evaluated" and not r.get("passed")),
        "skipped": sum(1 for r in results if r.get("status") == "skipped"),
    }
    report = {
        "generated": date.today().isoformat(),
        "fixtures_file": str(args.fixtures),
        "thresholds": THRESHOLDS,
        "totals": totals,
        "fixtures": results,
    }

    args.report_out.parent.mkdir(parents=True, exist_ok=True)
    args.report_out.write_text(json.dumps(report, indent=2, sort_keys=False))

    print(render_markdown_summary(report))

    all_ok = totals["failed"] == 0 and totals["skipped"] == 0
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
