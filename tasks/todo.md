# PDF formatting cleanup plan

- [x] Inspect representative PDF ingest output and classify formatting defects
- [x] Patch `scripts/auto_ingest.py` PDF cleanup so converted text preserves readable paragraphs/titles while removing vertical letter dumps and similar extraction noise
- [x] Verify cleanup on representative arXiv PDFs with both HTML and PDF fallback paths

## Review

- Root causes were PDF-extraction artifacts, not translation logic: vertical single-character metadata dumps, spaced-out acronyms/words, `(cid:...)` markers, NUL bytes, and broken URLs from MarkItDown output.
- Added targeted PDF normalization in `scripts/auto_ingest.py` for `.pdf` conversions only, keeping HTML normalization untouched.
- Verification on representative arXiv PDFs shows major improvements: bad abstract-page fallback avoided, URLs repaired, vertical metadata mostly removed, and names/terms like `ReasoningBank` / `MaTTS` normalized.
- Remaining limitations are inherent to PDF text extraction (e.g. some line wraps and occasional page-number lines may remain), but formatting is substantially cleaner than before.
