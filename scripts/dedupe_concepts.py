#!/usr/bin/env python3
"""One-shot semantic dedupe audit (R2).

Embeds every wiki/concepts/ and wiki/entities/ page (title + first 500 chars
of body), greedily clusters at cosine ≥ 0.85, and writes a Markdown report
to reports/dedupe-candidates-<YYYY-MM-DD>.md. Read-only — does NOT auto-merge.

Falls back to rapidfuzz token_set_ratio when sentence-transformers is not
available. The fallback is documented in the report header.
"""

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path

# --- Optional deps -----------------------------------------------------------

try:
    from sentence_transformers import SentenceTransformer  # type: ignore
    import numpy as _np  # type: ignore
    _ST_AVAILABLE = True
except Exception:  # pragma: no cover — env-dependent
    SentenceTransformer = None  # type: ignore
    _np = None  # type: ignore
    _ST_AVAILABLE = False

try:
    from rapidfuzz import fuzz as _rf_fuzz  # type: ignore
    _FUZZ_AVAILABLE = True
except Exception:  # pragma: no cover
    _rf_fuzz = None  # type: ignore
    _FUZZ_AVAILABLE = False


THRESHOLD = 0.85
BODY_CHARS = 500
MODEL_NAME = "all-MiniLM-L6-v2"


# --- Frontmatter (minimal, mirror auto_ingest.parse_frontmatter shape) -------

def parse_frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text(errors="ignore")
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    fm: dict = {}
    for line in parts[1].strip().split("\n"):
        s = line.strip()
        if ":" not in s or s.startswith("-") or s.startswith("#"):
            continue
        k, _, v = s.partition(":")
        fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm, parts[2]


# --- Load all candidate pages ------------------------------------------------

def load_pages(wiki_dir: Path) -> list[dict]:
    pages: list[dict] = []
    for sub in ("concepts", "entities"):
        d = wiki_dir / sub
        if not d.exists():
            continue
        for p in sorted(d.glob("*.md")):
            if p.name in ("index.md", "log.md", ".gitkeep"):
                continue
            fm, body = parse_frontmatter(p)
            title = fm.get("title") or p.stem.replace("-", " ").title()
            pages.append({
                "path": p,
                "rel": str(p.relative_to(wiki_dir.parent)),
                "category": sub,
                "title": title,
                "leading": (body or "")[:BODY_CHARS],
                "last_verified": fm.get("last_verified", ""),
                "slug": p.stem,
            })
    return pages


# --- Embedding / similarity --------------------------------------------------

def embed_all(pages: list[dict]):
    """Return numpy matrix [n, d] of normalized embeddings, or None."""
    if not _ST_AVAILABLE:
        return None
    model = SentenceTransformer(MODEL_NAME)
    texts = [f"{p['title']}\n{p['leading']}" for p in pages]
    vecs = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
    return _np.asarray(vecs, dtype="float32")


def pairwise_similarity(pages: list[dict], matrix) -> list[tuple[int, int, float]]:
    """Return [(i, j, score), ...] for i<j with score ≥ THRESHOLD."""
    hits: list[tuple[int, int, float]] = []
    n = len(pages)
    if matrix is not None:
        sims = matrix @ matrix.T
        for i in range(n):
            for j in range(i + 1, n):
                s = float(sims[i, j])
                if s >= THRESHOLD:
                    hits.append((i, j, s))
    else:
        if not _FUZZ_AVAILABLE:
            return hits
        thr = int(THRESHOLD * 100)
        for i in range(n):
            for j in range(i + 1, n):
                a = pages[i]["title"].lower()
                b = pages[j]["title"].lower()
                s = _rf_fuzz.token_set_ratio(a, b)
                if s >= thr:
                    hits.append((i, j, s / 100.0))
    return hits


# --- Greedy clustering -------------------------------------------------------

def greedy_cluster(n: int, hits: list[tuple[int, int, float]]) -> list[set[int]]:
    """Union-find over pairs above threshold."""
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for i, j, _s in hits:
        union(i, j)

    clusters: dict[int, set[int]] = {}
    for idx in range(n):
        clusters.setdefault(find(idx), set()).add(idx)
    # Only return clusters with >1 member
    return [members for members in clusters.values() if len(members) > 1]


# --- Winner heuristic --------------------------------------------------------

def pick_winner(cluster: list[dict]) -> dict:
    """Oldest last_verified, then shortest slug."""
    def key(p: dict) -> tuple:
        lv = p.get("last_verified", "") or "9999-99-99"
        return (lv, len(p["slug"]))
    return sorted(cluster, key=key)[0]


# --- Report ------------------------------------------------------------------

def render_report(
    pages: list[dict],
    clusters: list[set[int]],
    hits: list[tuple[int, int, float]],
    method: str,
) -> str:
    lines: list[str] = []
    today = date.today().isoformat()
    lines.append("---")
    lines.append('title: "Dedupe Candidates Audit"')
    lines.append("type: report")
    lines.append(f"generated: {today}")
    lines.append("scope: \"wiki/concepts/ + wiki/entities/ semantic clustering\"")
    lines.append("threshold: 0.85")
    lines.append(f"method: {method}")
    lines.append("---")
    lines.append("")
    lines.append("# Dedupe Candidates Audit")
    lines.append("")
    lines.append(
        f"Scanned **{len(pages)}** pages (concepts + entities). "
        f"Embedding method: **{method}**. Cosine threshold: **{THRESHOLD}** "
        f"(rapidfuzz uses scaled token_set_ratio when sentence-transformers "
        f"is unavailable)."
    )
    lines.append("")
    lines.append(
        f"Found **{len(clusters)}** merge cluster(s) covering "
        f"**{sum(len(c) for c in clusters)}** pages."
    )
    lines.append("")
    lines.append("> This is a **read-only audit**. No pages were modified.")
    lines.append("")

    if not clusters:
        lines.append("_No clusters at threshold._")
        return "\n".join(lines) + "\n"

    # Index per-pair scores for table rendering
    score_map: dict[tuple[int, int], float] = {}
    for i, j, s in hits:
        score_map[(min(i, j), max(i, j))] = s

    sorted_clusters = sorted(clusters, key=lambda c: (-len(c), min(c)))
    for cidx, members in enumerate(sorted_clusters, 1):
        members_sorted = sorted(members)
        cluster_pages = [pages[i] for i in members_sorted]
        winner = pick_winner(cluster_pages)
        lines.append(f"## Cluster {cidx} ({len(members_sorted)} pages)")
        lines.append("")
        lines.append("**Pages:**")
        lines.append("")
        for p in cluster_pages:
            marker = "🏆 " if p is winner else "   "
            lv = p.get("last_verified") or "—"
            lines.append(f"- {marker}`{p['rel']}` — *{p['title']}* (last_verified: {lv})")
        lines.append("")
        lines.append("**Pairwise similarity:**")
        lines.append("")
        lines.append("| A | B | score |")
        lines.append("|---|---|-------|")
        for a in range(len(members_sorted)):
            for b in range(a + 1, len(members_sorted)):
                i, j = members_sorted[a], members_sorted[b]
                s = score_map.get((min(i, j), max(i, j)))
                if s is None:
                    continue
                lines.append(
                    f"| `{pages[i]['slug']}` | `{pages[j]['slug']}` | {s:.3f} |"
                )
        lines.append("")
        lines.append(
            f"**Recommended winner:** `{winner['rel']}` "
            f"(oldest last_verified, then shortest slug)."
        )
        lines.append("")
        losers = [p for p in cluster_pages if p is not winner]
        loser_titles = ", ".join(f'"{l["title"]}"' for l in losers)
        lines.append(
            f"**Suggested action:** merge content of {loser_titles} into "
            f"`{winner['rel']}` (preserve sources + wikilinks), then redirect "
            f"or delete the loser slugs after the merge is verified."
        )
        lines.append("")

    return "\n".join(lines) + "\n"


# --- CLI ---------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Dedupe candidate audit (read-only).")
    parser.add_argument("--wiki-dir", default=".", help="Repo root (contains wiki/).")
    parser.add_argument(
        "--out",
        default=None,
        help="Output report path (default: reports/dedupe-candidates-<today>.md)",
    )
    args = parser.parse_args()

    root = Path(args.wiki_dir).resolve()
    wiki_dir = root / "wiki"
    if not wiki_dir.exists():
        raise SystemExit(f"wiki/ not found under {root}")

    pages = load_pages(wiki_dir)
    print(f"Loaded {len(pages)} pages from concepts/ + entities/")

    matrix = embed_all(pages)
    method = "sentence-transformers (all-MiniLM-L6-v2)" if matrix is not None else (
        "rapidfuzz token_set_ratio (fallback)" if _FUZZ_AVAILABLE else "none"
    )
    print(f"Method: {method}")

    if matrix is None and not _FUZZ_AVAILABLE:
        raise SystemExit(
            "Neither sentence-transformers nor rapidfuzz is installed; cannot run."
        )

    hits = pairwise_similarity(pages, matrix)
    print(f"Pairwise hits ≥ {THRESHOLD}: {len(hits)}")

    clusters = greedy_cluster(len(pages), hits)
    print(f"Clusters: {len(clusters)}")

    today = date.today().isoformat()
    out_path = Path(args.out) if args.out else root / "reports" / f"dedupe-candidates-{today}.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(render_report(pages, clusters, hits, method))
    print(f"Wrote {out_path.relative_to(root)}")


if __name__ == "__main__":
    main()
