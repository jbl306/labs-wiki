#!/usr/bin/env python3
"""Audit synthesis pages for provenance, grounding, and editorial depth.

The general wiki linter verifies page structure. This auditor focuses on what
makes a synthesis page more valuable than a source summary: multiple evidence
threads, claim-level support, a real comparison, and a decision-shaped title.
It is deterministic so it can gate model-written pages without another model
call.
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
REQUIRED_SECTIONS = (
    "Question",
    "Summary",
    "Comparison",
    "Analysis",
    "Key Insights",
    "Open Questions",
    "Sources",
)
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)")
SECTION_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
INSIGHT_RE = re.compile(r"^\s*\d+\.\s+(.+)$", re.MULTILINE)


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    message: str


@dataclass
class AuditResult:
    path: str
    title: str
    score: int
    passed: bool
    evidence_scope: str
    source_count: int
    source_family_count: int
    insight_count: int
    grounded_insight_count: int
    findings: list[Finding]

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["findings"] = [asdict(finding) for finding in self.findings]
        return payload


def parse_frontmatter_text(text: str) -> tuple[dict[str, Any], str]:
    """Return parsed YAML frontmatter and body from a Markdown document."""
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    try:
        frontmatter = yaml.safe_load(text[4:end]) or {}
    except yaml.YAMLError:
        return {}, text
    if not isinstance(frontmatter, dict):
        return {}, text
    body = text[end + 4 :].lstrip("\n")
    return frontmatter, body


def section_body(body: str, name: str) -> str:
    """Extract one level-two Markdown section, excluding the next heading."""
    match = re.search(
        rf"^##\s+{re.escape(name)}\s*$\n(.*?)(?=^##\s+|\Z)",
        body,
        flags=re.MULTILINE | re.DOTALL | re.IGNORECASE,
    )
    return match.group(1).strip() if match else ""


def _list_value(mapping: dict[str, Any], key: str) -> list[Any]:
    """Return a defensive list copy for a YAML frontmatter field."""
    value = mapping.get(key)
    return list(value) if isinstance(value, list) else []


def _normalized_raw_source(repo_root: Path, value: object) -> tuple[Path, str] | None:
    """Resolve one declared source while containing it to repository raw Markdown."""
    text = str(value).strip()
    candidate = Path(text)
    if not text or candidate.is_absolute():
        return None
    root = repo_root.resolve()
    raw_root = (root / "raw").resolve()
    resolved = (root / candidate).resolve()
    if not resolved.is_relative_to(raw_root) or resolved.suffix.casefold() != ".md":
        return None
    return resolved, resolved.relative_to(root).as_posix()


def _normalized_claim(value: str) -> str:
    """Normalize a Key Insight or Evidence Map claim for exact row matching."""
    claim = re.split(r"\s+—\s+supported\s+by\s+", value, maxsplit=1, flags=re.IGNORECASE)[0]
    claim = claim.replace("**", "").strip()
    return re.sub(r"\s+", " ", claim).casefold()


def _normalized_page_title(value: str) -> str:
    """Normalize a wikilink target for exact support/provenance matching."""
    target = value.split("|", 1)[0].split("#", 1)[0].strip()
    return re.sub(r"\s+", " ", target).casefold()


def _insight_supporting_pages(value: str) -> list[str]:
    match = re.search(r"\s+—\s+supported\s+by\s+(.+)$", value, re.IGNORECASE)
    return WIKILINK_RE.findall(match.group(1)) if match else []


def _wiki_page_provenance(repo_root: Path) -> dict[str, set[str]]:
    """Map canonical wiki titles to valid, existing raw provenance."""
    provenance: dict[str, set[str]] = {}
    wiki_root = repo_root / "wiki"
    if not wiki_root.is_dir():
        return provenance
    for page in wiki_root.rglob("*.md"):
        if page.name in {"index.md", "log.md"}:
            continue
        frontmatter, _ = parse_frontmatter_text(page.read_text(errors="replace"))
        title = str(frontmatter.get("title") or "").strip()
        if not title:
            continue
        valid_sources: set[str] = set()
        for source in _list_value(frontmatter, "sources"):
            normalized = _normalized_raw_source(repo_root, source)
            if normalized is not None and normalized[0].is_file():
                valid_sources.add(normalized[1])
        provenance[_normalized_page_title(title)] = valid_sources
    return provenance


def _evidence_map_rows(text: str) -> dict[str, tuple[list[str], list[str]]]:
    """Parse Evidence Map rows as normalized claim -> (wikilinks, raw refs)."""
    rows: dict[str, tuple[list[str], list[str]]] = {}
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 3 or cells[0].casefold() == "insight":
            continue
        if not cells[0].strip("-: "):
            continue
        rows[_normalized_claim(cells[0])] = (
            WIKILINK_RE.findall(cells[1]),
            re.findall(r"`([^`]+)`", cells[2]),
        )
    return rows


def source_origin_family(raw_path: Path) -> str:
    """Return a coarse origin family for independence diagnostics."""
    if not raw_path.exists():
        return "missing"
    frontmatter, _ = parse_frontmatter_text(raw_path.read_text(errors="replace"))
    url = str(frontmatter.get("url") or "").strip().lower()
    if url:
        domain_match = re.match(r"https?://([^/]+)", url)
        if domain_match:
            return domain_match.group(1).removeprefix("www.")
    source = str(frontmatter.get("source") or "").strip().lower()
    if source:
        return source
    name = raw_path.name.lower()
    if "copilot-session" in name or "codex-session" in name:
        return "agent-session-checkpoints"
    return "local-capture"


def audit_page(path: Path, repo_root: Path = ROOT, *, strict: bool = False) -> AuditResult:
    """Score one synthesis page and return actionable findings."""
    text = path.read_text(errors="replace")
    frontmatter, body = parse_frontmatter_text(text)
    findings: list[Finding] = []
    score = 0

    title = str(frontmatter.get("title") or path.stem.replace("-", " ").title())
    sources = _list_value(frontmatter, "sources")
    unique_sources = list(dict.fromkeys(str(source).strip() for source in sources))
    normalized_sources = [_normalized_raw_source(repo_root, source) for source in unique_sources]
    invalid_sources = [
        source for source, normalized in zip(unique_sources, normalized_sources, strict=True)
        if normalized is None
    ]
    valid_sources = [normalized for normalized in normalized_sources if normalized is not None]
    source_paths = [source_path for source_path, _relative in valid_sources]
    declared_source_paths = {relative for _source_path, relative in valid_sources}
    source_count = len(unique_sources)
    families = {source_origin_family(source_path) for source_path in source_paths}
    families.discard("missing")
    source_family_count = len(families)
    # "Cross-source" means independent origins, not merely multiple files.
    # Several checkpoints emitted by one agent/session channel are one evidence
    # family and must not be presented as independent corroboration.
    inferred_scope = "cross-source" if source_family_count >= 2 else "within-source"
    declared_scope = str(frontmatter.get("evidence_scope") or "").strip()

    required_frontmatter = ("title", "type", "sources", "concepts", "related")
    present_frontmatter = sum(bool(frontmatter.get(key)) for key in required_frontmatter)
    score += round(15 * present_frontmatter / len(required_frontmatter))
    if frontmatter.get("type") != "synthesis":
        findings.append(Finding("error", "wrong-type", "frontmatter type must be synthesis"))

    if strict:
        if invalid_sources:
            findings.append(
                Finding(
                    "error",
                    "invalid-provenance-path",
                    "sources must be relative raw/*.md paths contained in the repository: "
                    + ", ".join(repr(source) for source in invalid_sources),
                )
            )
        if declared_scope not in {"cross-source", "within-source"}:
            findings.append(
                Finding("error", "missing-evidence-scope", "declare evidence_scope in frontmatter")
            )
        declared_count = frontmatter.get("evidence_source_count")
        if declared_count != source_count:
            findings.append(
                Finding(
                    "error",
                    "evidence-count-mismatch",
                    f"evidence_source_count={declared_count!r}, but sources contains {source_count} unique paths",
                )
            )
        declared_family_count = frontmatter.get("evidence_origin_family_count")
        if declared_family_count != source_family_count:
            findings.append(
                Finding(
                    "error",
                    "evidence-family-count-mismatch",
                    f"evidence_origin_family_count={declared_family_count!r}, but provenance resolves to {source_family_count} origin families",
                )
            )
        if declared_scope == "cross-source" and source_family_count < 2:
            findings.append(
                Finding(
                    "error",
                    "cross-source-not-independent",
                    "cross-source synthesis requires at least two independent origin families",
                )
            )
    elif not declared_scope:
        findings.append(
            Finding("warning", "legacy-evidence-schema", "missing evidence_scope/evidence_source_count")
        )

    sections = {section.casefold() for section in SECTION_RE.findall(body)}
    present_sections = sum(section.casefold() in sections for section in REQUIRED_SECTIONS)
    structure_denominator = len(REQUIRED_SECTIONS) + (1 if strict else 0)
    structure_numerator = present_sections + (1 if "evidence map" in sections else 0)
    score += round(20 * min(structure_numerator, structure_denominator) / structure_denominator)
    missing_sections = [section for section in REQUIRED_SECTIONS if section.casefold() not in sections]
    if missing_sections:
        findings.append(
            Finding("error", "missing-sections", f"missing sections: {', '.join(missing_sections)}")
        )
    if strict and "evidence map" not in sections:
        findings.append(
            Finding("error", "missing-evidence-map", "strict synthesis pages require ## Evidence Map")
        )

    existing_sources = sum(source_path.is_file() for source_path in source_paths)
    if source_count:
        score += round(10 * existing_sources / source_count)
    missing_source_count = source_count - existing_sources
    if missing_source_count:
        findings.append(
            Finding(
                "error",
                "missing-provenance",
                f"{missing_source_count} of {source_count} raw source paths are invalid or do not exist",
            )
        )
    score += 10 if source_count >= 2 else (5 if source_count == 1 else 0)
    if source_count < 2:
        findings.append(
            Finding(
                "warning",
                "single-source",
                "within-source synthesis; seek an independent source before treating it as cross-source",
            )
        )
    elif source_family_count < 2:
        findings.append(
            Finding(
                "warning",
                "single-origin-family",
                "multiple raw files come from one coarse origin family",
            )
        )
    if declared_scope and declared_scope != inferred_scope:
        findings.append(
            Finding(
                "error",
                "scope-mismatch",
                f"declared {declared_scope}, inferred {inferred_scope} from raw source count",
            )
        )

    insights = INSIGHT_RE.findall(section_body(body, "Key Insights"))
    grounded = [
        insight
        for insight in insights
        if "supported by" in insight.casefold() and WIKILINK_RE.search(insight)
    ]
    insight_count = len(insights)
    grounded_insight_count = len(grounded)
    score += 5 if 3 <= insight_count <= 5 else min(insight_count, 3)
    if insights:
        score += round(10 * grounded_insight_count / len(insights))
    evidence_map = section_body(body, "Evidence Map")
    evidence_rows = _evidence_map_rows(evidence_map)
    page_provenance = _wiki_page_provenance(repo_root)
    invalid_evidence_claims: list[str] = []
    missing_evidence_claims: list[str] = []
    for insight in insights:
        claim = _normalized_claim(insight)
        row = evidence_rows.get(claim)
        if row is None:
            missing_evidence_claims.append(claim)
            continue
        supporting_pages, raw_refs = row
        insight_pages = {
            _normalized_page_title(page) for page in _insight_supporting_pages(insight)
        }
        row_pages = {_normalized_page_title(page) for page in supporting_pages}
        row_is_valid = bool(row_pages and raw_refs) and row_pages == insight_pages
        supporting_sources: dict[str, set[str]] = {}
        for page_title in row_pages:
            page_sources = page_provenance.get(page_title)
            if page_sources is None:
                row_is_valid = False
            else:
                supporting_sources[page_title] = page_sources

        normalized_refs: set[str] = set()
        for raw_ref in raw_refs:
            normalized = _normalized_raw_source(repo_root, raw_ref)
            if normalized is None:
                row_is_valid = False
                continue
            raw_path, relative = normalized
            if relative not in declared_source_paths or not raw_path.is_file():
                row_is_valid = False
            else:
                normalized_refs.add(relative)

        allowed_refs = set().union(*supporting_sources.values()) if supporting_sources else set()
        if not normalized_refs.issubset(allowed_refs):
            row_is_valid = False
        if any(
            not normalized_refs.intersection(page_sources)
            for page_sources in supporting_sources.values()
        ):
            row_is_valid = False
        if not row_is_valid:
            invalid_evidence_claims.append(claim)
    evidence_map_complete = bool(insights) and not missing_evidence_claims and not invalid_evidence_claims
    if evidence_map_complete:
        score += 5
    elif not strict and grounded_insight_count == insight_count and insight_count:
        score += 5
    if strict and missing_evidence_claims:
        findings.append(
            Finding(
                "error",
                "evidence-map-coverage",
                f"Evidence Map is missing {len(missing_evidence_claims)} Key Insight row(s)",
            )
        )
    if strict and invalid_evidence_claims:
        findings.append(
            Finding(
                "error",
                "invalid-evidence-map-provenance",
                f"{len(invalid_evidence_claims)} Evidence Map row(s) have mismatched supporting pages or provenance",
            )
        )
    if grounded_insight_count != insight_count:
        findings.append(
            Finding(
                "error" if strict else "warning",
                "ungrounded-insights",
                f"{insight_count - grounded_insight_count} of {insight_count} key insights lack supported-by wikilinks",
            )
        )

    comparison = section_body(body, "Comparison")
    concepts = _list_value(frontmatter, "concepts")
    if re.search(r"^\|.+\|$", comparison, re.MULTILINE):
        score += 5
    else:
        findings.append(Finding("error", "missing-comparison-table", "Comparison needs a table"))
    if len(set(str(concept) for concept in concepts)) >= 2:
        score += 5
    else:
        findings.append(Finding("warning", "narrow-comparison", "fewer than two concepts declared"))
    analysis_words = len(re.findall(r"\b\w+\b", section_body(body, "Analysis")))
    if analysis_words >= 200:
        score += 5
    elif analysis_words >= 100:
        score += 3
    else:
        findings.append(
            Finding("warning", "thin-analysis", f"Analysis has only {analysis_words} words")
        )

    title_ok = len(title) <= 100 and not title.casefold().startswith("recurring checkpoint patterns:")
    if title_ok:
        score += 5
    else:
        findings.append(
            Finding(
                "warning",
                "mechanism-shaped-title",
                "use a topic/decision-shaped title of at most 100 characters",
            )
        )
    if len(section_body(body, "Summary").split()) >= 25:
        score += 3
    if len(re.findall(r"^-\s+", section_body(body, "Open Questions"), re.MULTILINE)) >= 1:
        score += 2

    score = max(0, min(100, score))
    errors = [finding for finding in findings if finding.severity == "error"]
    return AuditResult(
        path=str(path.relative_to(repo_root)) if path.is_relative_to(repo_root) else str(path),
        title=title,
        score=score,
        passed=score >= 80 and not errors,
        evidence_scope=declared_scope or inferred_scope,
        source_count=source_count,
        source_family_count=source_family_count,
        insight_count=insight_count,
        grounded_insight_count=grounded_insight_count,
        findings=findings,
    )


def summarize(results: list[AuditResult]) -> dict[str, Any]:
    """Aggregate page-level audits into corpus-level synthesis metrics."""
    scores = [result.score for result in results]
    scopes = Counter(result.evidence_scope for result in results)

    def has_code(result: AuditResult, code: str) -> bool:
        return any(finding.code == code for finding in result.findings)

    return {
        "pages": len(results),
        "passed": sum(result.passed for result in results),
        "failed": sum(not result.passed for result in results),
        "score_mean": round(statistics.mean(scores), 1) if scores else 0,
        "score_median": round(statistics.median(scores), 1) if scores else 0,
        "score_below_85": sum(result.score < 85 for result in results),
        "score_below_90": sum(result.score < 90 for result in results),
        "evidence_scopes": dict(scopes),
        "strict_contract_pages": sum(
            not has_code(result, "legacy-evidence-schema") for result in results
        ),
        "single_source_pages": sum(result.source_count < 2 for result in results),
        "single_origin_family_pages": sum(
            result.source_family_count < 2 for result in results
        ),
        "mechanism_shaped_titles": sum(
            has_code(result, "mechanism-shaped-title") for result in results
        ),
        "fully_grounded_pages": sum(
            result.insight_count > 0
            and result.insight_count == result.grounded_insight_count
            for result in results
        ),
        "ungrounded_pages": sum(
            result.insight_count == 0
            or result.insight_count != result.grounded_insight_count
            for result in results
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--page", type=Path, action="append", default=[])
    parser.add_argument("--wiki-dir", type=Path, default=ROOT / "wiki")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--fail-under", type=int, default=None)
    args = parser.parse_args()

    pages = args.page or sorted((args.wiki_dir / "synthesis").glob("*.md"))
    results = [audit_page(path.resolve(), ROOT, strict=args.strict) for path in pages]
    payload = {
        "summary": summarize(results),
        "results": [result.to_dict() for result in results],
    }
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(rendered)
    else:
        print(rendered, end="")

    if args.fail_under is not None and any(result.score < args.fail_under for result in results):
        return 1
    if args.strict and any(not result.passed for result in results):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())