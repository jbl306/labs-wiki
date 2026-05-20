- id: obs-2026-05-01-001
  status: RESOLVED
  type: improve-existing-skill
  skill: github-instruction-labs-wiki-github-raw-sources
  summary: "arXiv /html/ 404 pages were being treated as full-paper content, causing abstract-only fetched-content snapshots."
  evidence:
    - "2026-04-28-260109113v1pdf.md stored resolved_url https://arxiv.org/abs/2601.09113 and only pointer/abstract text before repair."
    - "Direct fetch of https://arxiv.org/html/2601.09113 returned HTTP 404 while PDF fallback produced full-paper text."
  suggested_update: "When documenting arXiv ingest behavior, explicitly require validating arXiv HTML responses before treating them as full text, then falling back to PDF-to-markdown."
  source: "session"
- id: obs-2026-05-01-002
  status: RESOLVED
  type: improve-existing-skill
  skill: copilot-agent-labs-wiki-github-wiki-ingest
  summary: "Durable fetched-content snapshots must preserve full translated document text; truncating MarkItDown output breaks later re-ingest quality."
  evidence:
    - "Top-level arXiv raws were capped around 50k chars even when full HTML/PDF content exceeded that length."
    - "Removing truncation let repaired raws store 90k-245k chars of fetched content and eliminated pointer-only snapshots."
  suggested_update: "For deterministic raw snapshots, store the full fetched/extracted body and rely on downstream max_source_chars limits only when prompting models."
  source: "session"
- id: obs-2026-05-01-003
  status: RESOLVED
  type: improve-existing-skill
  skill: copilot-agent-labs-wiki-github-wiki-ingest
  summary: "PDF-derived raw snapshots need targeted post-processing to remove extraction noise before persisting."
  evidence:
    - "Representative arXiv PDF conversions contained vertical single-character metadata, broken URLs, `(cid:...)` markers, and split tokens like `Reasoning Ban k` / `M aT T S`."
    - "Adding PDF-only normalization in auto_ingest.py improved fetched previews without changing HTML ingest behavior."
  suggested_update: "Document a PDF-cleanup pass after MarkItDown conversion for `.pdf` inputs, focused on artifact removal rather than aggressive reflow."
  source: "session"
