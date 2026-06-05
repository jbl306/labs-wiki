# LiteParse Integration Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Add `run-llama/liteparse` as a first-class document extraction engine for labs-wiki ingest/processing without weakening raw-source provenance, MarkItDown fallbacks, Codex CLI compilation, or unattended ingest reliability.

**Architecture:** Introduce a parser adapter seam in `scripts/auto_ingest.py` so local file uploads and binary URL responses can choose LiteParse, MarkItDown, or fallback behavior through one stable interface. LiteParse should be preferred for PDFs and layout/OCR-sensitive binary documents, while existing HTML/text/GitHub/Twitter/arXiv handlers and deterministic raw content blocks remain unchanged. The first implementation should be test-gated and feature-flagged before changing production defaults.

**Tech Stack:** Python 3.12, FastAPI capture API, Docker sidecar watcher, `liteparse>=2.0.1`, existing `markitdown[...]`, pytest, `unittest.mock`, optional Tesseract/LibreOffice/ImageMagick runtime packages.

---

## Current-State Audit

### Existing ingest flow

- `wiki-ingest-api/app.py` captures uploads in `ingest_file()` by saving binaries under `raw/assets/<uuid><ext>` and writing a pointer raw source (`type: file`). It does **not** parse the document in the API process.
- `scripts/watch_raw.py` watches top-level `raw/*.md` only, deliberately ignoring `raw/assets/`; file parsing is triggered by the raw markdown stub, not by direct asset writes.
- `scripts/auto_ingest.py` owns document extraction and raw enrichment:
  - imports `MarkItDown` at lines 33-36;
  - defines MarkItDown extension/MIME constants at lines 81-120;
  - exposes `convert_file_to_markdown(path)` at lines 388-409;
  - exposes `convert_binary_response_to_markdown(content, source_url, content_type)` at lines 412-442;
  - persists deterministic file extraction blocks via `build_extracted_content_block()` / `upsert_extracted_content_block()` at lines 518-542;
  - persists deterministic URL fetch blocks via `build_fetched_content_block()` / `upsert_fetched_content_block()` at lines 476-502;
  - calls file extraction before both Copilot CLI ingest (lines 3380-3416) and legacy GitHub Models ingest (lines 3519-3565);
  - calls binary URL extraction from `fetch_url_content()` (lines 1589-1644).
- The raw-source contract in `AGENTS.md` allows automation to update only `status` plus deterministic `fetched-content` / `extracted-content` blocks. LiteParse must write through those existing block helpers, not mutate raw bodies ad hoc.

### Existing MarkItDown behavior to preserve

- MarkItDown is already used as a **helper/preprocessor**, not as a replacement for source-specific handlers.
- Existing custom URL handlers for Twitter/X, GitHub repos/gists, arXiv HTML preference, generic HTML normalization, image extraction, and model routing should remain in place.
- PDF text normalization helpers (`normalize_pdf_markdown()` and related functions) currently clean MarkItDown's PDF output. LiteParse will need its own text formatter and may optionally reuse the final meaningful-text gate.

### Current gaps this plan should close

1. Parser logic is hard-wired to MarkItDown naming and constants, making a second parser risky.
2. There are effectively no automated tests for document parser selection, deterministic raw blocks, binary URL fallback, or local file extraction.
3. Uploaded PDFs may not receive high reasoning effort because `_compute_effort_for_raw()` checks frontmatter `source`, not the raw body's `Original filename:` / asset reference.
4. `--refresh-fetch` refreshes file extraction in the Copilot CLI backend but not the legacy backend.
5. `Dockerfile.auto-ingest` copies selected scripts but not imported helper modules (`checkpoint_classifier.py`, `checkpoint_state.py`) and would need updates for any new parser module if one is created.
6. Parser failures currently degrade softly to pointer/stub content; LiteParse integration needs explicit fallback order and logging so empty OCR/layout extraction does not silently lower ingest quality.

---

## LiteParse Research Summary

Research target: <https://github.com/run-llama/liteparse> at commit `ae1ae83f527b016d4f318ee27023381109702425` (`main`, tags `python-v2.0.1`, `node-v2.0.1`).

### Capabilities relevant to labs-wiki

- Install/import: `pip install liteparse`; `from liteparse import LiteParse`; Python `>=3.10`; latest observed PyPI version `2.0.1`.
- Primary API:

  ```python
  from liteparse import LiteParse

  parser = LiteParse(ocr_enabled=False, quiet=True, max_pages=1000)
  result = parser.parse("document.pdf")  # path
  result = parser.parse(pdf_bytes)       # bytes
  text = result.text
  pages = result.pages
  ```

- Python output shape: `ParseResult(text, pages)`; pages include `page_num`, `width`, `height`, `text`, and `text_items`; text items include `text`, `x`, `y`, `width`, `height`, optional `font_name`, `font_size`, `confidence`.
- CLI/JSON output exposes pages and text-item bounding boxes. Coordinates are top-left origin in PDF points (72 DPI); useful later for visual citations, but first integration should emit plain deterministic text only.
- OCR defaults: OCR is enabled by default upstream, default language `eng`, selective OCR on pages with little text or embedded images, default `max_pages=1000`, `dpi=150`.
- Supports PDF directly and converts many Office/presentation/spreadsheet/image formats via external tools.

### Constraints and cautions

- LiteParse is **not a Markdown converter**. It emits text/layout JSON; labs-wiki must format page text into durable markdown-ish text before sending to the compile backend.
- Markdown/text files should not route to LiteParse. Keep existing direct text/MarkItDown behavior for `.md`, `.txt`, `.html`, `.json`, etc.
- For upload bytes, preserving file extension is safer than raw bytes for Office formats; route local assets by path rather than by bytes.
- Runtime dependencies matter:
  - Python wheels include/copy PDFium support.
  - Office conversion needs LibreOffice.
  - Image conversion needs ImageMagick; some SVG-like conversion may need Ghostscript.
  - OCR needs Tesseract/tessdata or a configured OCR server.
- LiteParse is synchronous from Python's perspective and creates an async runtime internally. In labs-wiki this is acceptable in the sidecar worker path; if ever added to FastAPI request handling, run it off the event loop.
- Security posture: upstream says validation, sandboxing, timeouts, concurrency/resource limits are the deployer's responsibility. Keep existing download size limits and add local parse timeouts if using subprocess CLI later.
- Upstream maturity notes: repo created 2026-02-09, active through 2026-05-27, PyPI classifier says beta. There is a license inconsistency: root repo/Cargo/npm are Apache-2.0 while Python metadata says MIT. Treat as a pre-merge legal note if redistributing container images externally.

### Recommended product decision

Use LiteParse as a **PDF/layout/OCR extraction engine behind a parser adapter**, not as a wholesale MarkItDown replacement.

Default rollout should be:

1. Add adapter + tests with default `WIKI_DOCUMENT_PARSER=auto` still safe and reversible.
2. Enable LiteParse for PDFs first (`.pdf` local files and binary PDF URLs).
3. Keep MarkItDown fallback for non-PDF Office formats until Docker dependencies and quality comparisons prove LiteParse is better there.
4. Add parser metadata to deterministic extracted/fetched blocks so future audits can see which engine produced a raw snapshot.

---

## Target Outcome

After implementation:

- A new parser adapter chooses LiteParse vs MarkItDown deterministically for local assets and binary URL responses.
- Raw `fetched-content` and `extracted-content` blocks include parser metadata (`parser`, `parser_version`) while preserving existing block markers and compile flow.
- PDFs can be extracted through LiteParse with optional OCR, then fed into the existing Codex CLI compile flow (with Copilot CLI / GitHub Models retained only as compatibility backends).
- MarkItDown remains available as fallback and for formats LiteParse does not handle well for markdown-oriented extraction.
- Parser behavior is covered by unit tests that mock both LiteParse and MarkItDown; tests do not require real PDF/Office parsing.
- Docker image and requirements include all runtime files/packages needed for the selected first rollout.
- Upload PDFs and binary PDF URLs receive high reasoning effort and refresh semantics are consistent across both ingest backends.

---

## Parser Routing Classification

| Flow/Input | Current path | LiteParse target | Fallback | Notes |
|------------|--------------|------------------|----------|-------|
| Uploaded PDF (`type: file`, asset `.pdf`) | `convert_file_to_markdown()` via MarkItDown | **Yes, first rollout** | MarkItDown, then no extracted block | Best fit: layout/OCR-sensitive local path. |
| Binary PDF URL | `convert_binary_response_to_markdown()` via MarkItDown stream | **Yes, first rollout** | MarkItDown, then placeholder | Preserve `MAX_DOCUMENT_DOWNLOAD_SIZE`. |
| arXiv `/abs` / `/pdf` | Prefer `/html`, fallback PDF conversion | **Only fallback PDF branch** | MarkItDown | Do not disrupt arXiv HTML preference. |
| DOCX/PPTX/XLSX uploads | MarkItDown | Later opt-in only | MarkItDown | LiteParse needs LibreOffice conversion and may lose markdown/table semantics. |
| Images | Vision lane / image URL extraction | Later explicit experiment only | Existing vision path | LiteParse can OCR images, but labs-wiki already has multimodal vision handling. |
| HTML/Markdown/text/JSON/XML | HTML/text handlers / MarkItDown constants | **No** | Existing behavior | LiteParse is not useful for these. |
| GitHub/Twitter/Gist URLs | Custom handlers | **No** | Existing behavior | Keep domain-specific handlers. |

---

## Implementation Tasks

### Task 1: Create focused parser regression tests around current behavior

**Objective:** Lock down the current public behavior before introducing LiteParse.

**Files:**
- Create: `tests/test_document_parsers.py`
- Modify: none yet

**Steps:**
1. Add a test import harness that prepends `scripts/` to `sys.path` and imports `auto_ingest`.
2. Test unsupported local suffix returns `(None, None)`.
3. Mock `get_markitdown_converter()` and test `.docx` local conversion returns text and content type.
4. Mock a failing MarkItDown converter and test binary PDF URL conversion returns `None` rather than raising.
5. Run `python3 -m pytest tests/test_document_parsers.py -q`; expected PASS.
6. Commit: `git commit -m "test: cover document parser conversion seam"`.

Example assertions:

```python
def test_convert_file_to_markdown_unsupported_suffix(tmp_path):
    path = tmp_path / "document.bin"
    path.write_bytes(b"not supported")
    assert auto_ingest.convert_file_to_markdown(path) == (None, None)
```

---

### Task 2: Add parser metadata support to deterministic content blocks

**Objective:** Let raw snapshots record which parser produced the durable body without changing existing block markers or compile behavior.

**Files:**
- Modify: `scripts/auto_ingest.py` around `build_fetched_content_block()` and `build_extracted_content_block()`
- Test: `tests/test_document_parsers.py`

**Steps:**
1. Add optional keyword args `parser: str | None = None` and `parser_version: str | None = None` to both block builders.
2. Add metadata lines only when present:

   ```python
   if parser:
       lines.append(f"- parser: {parser}")
   if parser_version:
       lines.append(f"- parser_version: {parser_version}")
   ```

3. Add tests that `read_persisted_extracted_content()` and `read_persisted_fetched_content()` round-trip `parser` and `parser_version` metadata.
4. Run `python3 -m pytest tests/test_document_parsers.py -q`; expected PASS.
5. Commit: `git commit -m "feat: record parser metadata in raw content blocks"`.

---

### Task 3: Introduce a `DocumentParseResult` adapter type and parser-selection helpers

**Objective:** Create a narrow parser abstraction while preserving existing function signatures used by the ingest pipeline.

**Files:**
- Modify: `scripts/auto_ingest.py`
- Test: `tests/test_document_parsers.py`

**Steps:**
1. Add optional LiteParse import near MarkItDown:

   ```python
   try:
       from liteparse import LiteParse
   except ImportError:  # pragma: no cover
       LiteParse = None
   ```

2. Add:

   ```python
   @dataclass(frozen=True)
   class DocumentParseResult:
       text: str
       content_type: str | None
       parser: str
       parser_version: str | None = None
   ```

3. Add `LITEPARSE_FILE_EXTENSIONS = {".pdf"}`, `LITEPARSE_BINARY_URL_EXTENSIONS = {".pdf"}`, and `LITEPARSE_BINARY_MIME_TYPES = {"application/pdf"}` for the first rollout.
4. Add `get_document_parser_mode()` reading `WIKI_DOCUMENT_PARSER=auto|markitdown|liteparse|liteparse-first` and falling back to `auto` on invalid values.
5. Add `is_liteparse_ocr_enabled()` reading `WIKI_LITEPARSE_OCR` and `get_liteparse_parser()` constructing a singleton `LiteParse(ocr_enabled=..., quiet=True, max_pages=...)`.
6. Add `get_liteparse_version()`, but do not assert strict version because upstream `__version__` may lag package metadata.
7. Add tests for parser mode defaults and invalid values.
8. Run tests; commit: `git commit -m "feat: add document parser adapter scaffolding"`.

---

### Task 4: Implement LiteParse local-file extraction for PDFs

**Objective:** Extract uploaded/local PDFs with LiteParse when enabled while keeping MarkItDown fallback.

**Files:**
- Modify: `scripts/auto_ingest.py`
- Test: `tests/test_document_parsers.py`

**Steps:**
1. Add a deterministic formatter:

   ```python
   def format_liteparse_result(parse_result) -> str:
       pages = getattr(parse_result, "pages", None) or []
       if pages:
           chunks = []
           for page in pages:
               page_num = getattr(page, "page_num", None)
               page_text = (getattr(page, "text", "") or "").strip()
               if not page_text:
                   continue
               chunks.append(f"## Page {page_num}\n\n{page_text}" if page_num is not None else page_text)
           return "\n\n".join(chunks).strip()
       return (getattr(parse_result, "text", "") or "").strip()
   ```

2. Add `convert_file_with_liteparse(path) -> DocumentParseResult | None` for `.pdf` only.
3. Refactor the current MarkItDown logic into `convert_file_with_markitdown(path) -> DocumentParseResult | None`.
4. Add `convert_file_to_document_text(path) -> DocumentParseResult | None` with routing:
   - `auto`: LiteParse for `.pdf`, fallback MarkItDown;
   - `liteparse-first`: try LiteParse, fallback MarkItDown;
   - `liteparse`: LiteParse only;
   - `markitdown`: MarkItDown only.
5. Keep `convert_file_to_markdown(path)` as a compatibility wrapper returning `(text, content_type)`.
6. Update both file extraction call sites in `ingest_raw_source()` to use `convert_file_to_document_text()` and pass parser metadata into `build_extracted_content_block()`.
7. Add mocked tests for LiteParse PDF success and LiteParse-empty -> MarkItDown fallback.
8. Run tests; commit: `git commit -m "feat: parse uploaded PDFs with liteparse adapter"`.

---

### Task 5: Implement LiteParse binary-URL extraction for PDFs

**Objective:** Use LiteParse for downloaded binary PDFs while preserving size limits, placeholders, and MarkItDown fallback.

**Files:**
- Modify: `scripts/auto_ingest.py`
- Test: `tests/test_document_parsers.py`

**Steps:**
1. Add `_is_liteparse_binary_url(source_url, content_type)` using suffix or MIME type.
2. Add `convert_binary_response_with_liteparse(content, source_url, content_type) -> DocumentParseResult | None` using `parser.parse(content)`.
3. Refactor current MarkItDown binary stream logic into `convert_binary_response_with_markitdown(...) -> DocumentParseResult | None`.
4. Add `convert_binary_response_to_document_text(...) -> DocumentParseResult | None` with the same routing semantics as local files.
5. Keep `convert_binary_response_to_markdown(...) -> str | None` as a compatibility wrapper.
6. Extend `UrlFetchResult` with optional `parser` and `parser_version` fields.
7. In `fetch_url_content()` binary branch, call the rich conversion function and return parser metadata with `UrlFetchResult`.
8. Pass parser metadata into `build_fetched_content_block()` at fetched-content call sites.
9. Add mocked tests for binary PDF LiteParse success and fallback behavior.
10. Run tests; commit: `git commit -m "feat: parse binary PDF URLs with liteparse"`.

---

### Task 6: Fix PDF effort routing and refresh semantics

**Objective:** Ensure LiteParse-produced PDF content gets high-effort compilation and parser refresh behaves consistently.

**Files:**
- Modify: `scripts/auto_ingest.py`
- Test: `tests/test_document_parsers.py`

**Steps:**
1. Add `is_pdf_file_raw(fm, body)` that checks:
   - frontmatter URL/source;
   - `parse_file_asset_reference(body)` asset path;
   - `Original filename:`;
   - persisted extracted metadata (`asset_path`, `original_filename`, `content_type`).
2. Change `_compute_effort_for_raw(fm)` to `_compute_effort_for_raw(fm, body=None)` and return `high` for uploaded PDF file raws.
3. Update call site to `_compute_effort_for_raw(fm, body)`.
4. Change legacy backend file extraction condition from `(force or not persisted_text)` to `(refresh_fetch or force or not persisted_text)` to match Copilot CLI backend.
5. Add tests for uploaded PDF body -> `high` and non-PDF file body -> `medium`.
6. Run tests; commit: `git commit -m "fix: route uploaded PDFs to high-effort ingest"`.

---

### Task 7: Update dependencies and Docker runtime deliberately

**Objective:** Make the auto-ingest environment capable of importing LiteParse and running the selected PDF-first path.

**Files:**
- Modify: `scripts/requirements-auto-ingest.txt`
- Modify: `Dockerfile.auto-ingest`
- Optionally modify: `README.md` / `AGENTS.md` for env var docs

**Steps:**
1. Add dependency:

   ```text
   liteparse>=2.0.1,<3
   ```

2. Keep MarkItDown dependency for fallback.
3. For OCR-capable PDF path, install Tesseract in Docker only if production wants `WIKI_LITEPARSE_OCR=1`. Recommended first rollout keeps `WIKI_LITEPARSE_OCR=0`; if installing now, add `tesseract-ocr tesseract-ocr-eng`.
4. Do **not** install LibreOffice/ImageMagick/Ghostscript in the first PDF-only rollout unless Office/image parsing is enabled.
5. Fix Dockerfile selective copy drift by either:
   - replacing selected script copies with `COPY scripts/ /app/scripts/`, or
   - explicitly adding `checkpoint_classifier.py`, `checkpoint_state.py`, and any new parser helper modules.
6. Verify:

   ```bash
   cd /home/jbl/projects/labs-wiki
   python3 -m pip install -r scripts/requirements-auto-ingest.txt
   python3 - <<'PY'
   from liteparse import LiteParse
   print('liteparse import ok', LiteParse)
   PY
   docker build -f Dockerfile.auto-ingest -t labs-wiki-auto-ingest:liteparse-test .
   ```

7. Commit: `git commit -m "build: add liteparse to auto-ingest runtime"`.

---

### Task 8: Add a small real-parser smoke script

**Objective:** Verify LiteParse can import and optionally parse one PDF in the project environment without making unit tests depend on heavyweight document parsing.

**Files:**
- Create: `scripts/smoke_liteparse.py`

**Steps:**
1. Add script:

   ```python
   #!/usr/bin/env python3
   from __future__ import annotations

   import argparse
   from pathlib import Path
   from liteparse import LiteParse

   def main() -> int:
       parser = argparse.ArgumentParser()
       parser.add_argument('pdf', type=Path, nargs='?', help='Optional PDF file to parse')
       parser.add_argument('--ocr', action='store_true')
       args = parser.parse_args()

       lp = LiteParse(ocr_enabled=args.ocr, quiet=True, max_pages=5)
       if args.pdf:
           result = lp.parse(args.pdf)
           text = (getattr(result, 'text', '') or '').strip()
           pages = getattr(result, 'pages', []) or []
           print(f'pages={len(pages)} chars={len(text)}')
           return 0 if text else 2
       print('liteparse import/construct ok')
       return 0

   if __name__ == '__main__':
       raise SystemExit(main())
   ```

2. Run `python3 scripts/smoke_liteparse.py`; expected `liteparse import/construct ok`.
3. Optionally run against a real sample PDF outside production `raw/`.
4. Commit: `git commit -m "test: add liteparse smoke check"`.

---

### Task 9: Validate deterministic raw enrichment without full wiki compilation

**Objective:** Prove a `type: file` raw stub receives a deterministic LiteParse extracted-content block without requiring a production ingest.

**Files:**
- Modify: `tests/test_document_parsers.py`

**Steps:**
1. Add a helper-level test that builds and upserts an extracted-content block with `parser="liteparse"`.
2. Assert `read_persisted_extracted_content()` returns text and metadata.
3. If adding an integration helper to reduce duplicated code in `ingest_raw_source()`, test that helper with temp directories and mocked parser result.
4. Do not let `watch_raw.py` or production auto-commit process test files.
5. Run tests; commit: `git commit -m "test: verify liteparse raw block enrichment"`.

---

### Task 10: Update project docs and operational notes

**Objective:** Make future operators understand the parser stack and feature flags.

**Files:**
- Modify: `AGENTS.md`
- Modify: `README.md`
- Modify: `tasks/todo.md` or `tasks/progress.md`

**Steps:**
1. Update the Auto-Ingest workflow document-binary bullet from MarkItDown-only wording to parser-stack wording:

   ```markdown
   - **Document binaries** (PDF first; selected Office formats) → parser adapter:
     LiteParse for PDF/layout/OCR-sensitive extraction when enabled, MarkItDown as fallback and for markdown-oriented Office conversion.
   ```

2. Add config docs:

   ```markdown
   **Document parser config:** `WIKI_DOCUMENT_PARSER=auto|markitdown|liteparse|liteparse-first`, `WIKI_LITEPARSE_OCR=0|1`, `WIKI_LITEPARSE_MAX_PAGES=1000`.
   ```

3. Add a compact README note: "Document extraction uses a parser adapter. PDFs can route through LiteParse for local layout-aware parsing; MarkItDown remains installed for fallback and non-PDF document conversion."
4. Update task tracker with completed planning item and follow-up validation items.
5. Commit: `git commit -m "docs: document liteparse parser adapter"`.

---

## Verification Plan

### Unit tests

Run after each code task:

```bash
cd /home/jbl/projects/labs-wiki
python3 -m pytest tests/test_document_parsers.py -q
```

Final broader test run:

```bash
cd /home/jbl/projects/labs-wiki
python3 -m pytest -q
```

Expected: all tests pass.

### Static/import checks

```bash
cd /home/jbl/projects/labs-wiki
python3 -m py_compile scripts/auto_ingest.py scripts/watch_raw.py scripts/smoke_liteparse.py
python3 scripts/smoke_liteparse.py
```

Expected: compile succeeds; smoke prints `liteparse import/construct ok`.

### Docker build

```bash
cd /home/jbl/projects/labs-wiki
docker build -f Dockerfile.auto-ingest -t labs-wiki-auto-ingest:liteparse-test .
```

Expected: build succeeds and includes `liteparse` import support.

### Manual parser quality comparison

Run against 2-3 real PDFs before enabling production default:

```bash
WIKI_DOCUMENT_PARSER=liteparse python3 scripts/smoke_liteparse.py /path/to/sample.pdf
WIKI_DOCUMENT_PARSER=markitdown python3 - <<'PY'
from pathlib import Path
import sys
sys.path.insert(0, 'scripts')
import auto_ingest
text, ct = auto_ingest.convert_file_to_markdown(Path('/path/to/sample.pdf'))
print(ct, len(text or ''))
print((text or '')[:1000])
PY
```

Compare extracted character count, heading/page readability, table/math/list preservation, downstream compile quality, runtime, and memory.

### End-to-end staging run

Use a staging copy or explicitly disabled watcher environment:

```bash
cd /home/jbl/projects/labs-wiki
WIKI_DOCUMENT_PARSER=liteparse-first \
WIKI_LITEPARSE_OCR=0 \
python3 scripts/auto_ingest.py raw/<staging-pdf-raw>.md --force --refresh-fetch --validation-run
```

Expected:

- raw file gets one `extracted-content` block with `parser: liteparse`;
- source is compiled successfully;
- `wiki/index.md` rebuilds;
- no unrelated raw/wiki files are modified except expected outputs.

---

## Risks, Tradeoffs, and Mitigations

| Risk | Why it matters | Mitigation |
|------|----------------|------------|
| LiteParse emits text, not Markdown | Downstream compiler may see weaker structure than MarkItDown for DOCX/PPTX/XLSX | PDF-first rollout; keep MarkItDown fallback; compare before expanding formats. |
| OCR/runtime dependency bloat | Docker image grows; Tesseract/LibreOffice/ImageMagick can be heavy | Default `WIKI_LITEPARSE_OCR=0`; install only Tesseract for first OCR-capable PDF path; delay LibreOffice/ImageMagick. |
| Parser output changes raw snapshots | Raw deterministic blocks may churn on parser/version changes | Record `parser` and `parser_version`; refresh only with `--refresh-fetch`/`--force`; do not re-extract automatically on every run. |
| Empty OCR or parse failure silently weakens ingest | File stubs could compile as low-quality pages | MarkItDown fallback in `auto`/`liteparse-first`; warning logs; tests for empty fallback. Consider hard failure for `WIKI_DOCUMENT_PARSER=liteparse`. |
| Upstream beta/library mismatch | LiteParse metadata has version/license inconsistencies | Pin `<3`, keep fallback, include legal note before external redistribution. |
| Dockerfile selective copy drift | New parser modules may be absent at runtime | Prefer `COPY scripts/ /app/scripts/` or explicitly copy all imports. |
| PDF high-effort routing misses uploads | Good extraction still gets medium reasoning | Fix `_compute_effort_for_raw(fm, body)` as part of rollout. |

---

## Open Questions

1. Should production default be `WIKI_DOCUMENT_PARSER=auto` with LiteParse for PDFs immediately, or should the first deploy use `WIKI_DOCUMENT_PARSER=markitdown` plus manual opt-in until sample PDFs are compared?
2. Should OCR be enabled by default for PDFs? Recommendation: no; keep `WIKI_LITEPARSE_OCR=0` until runtime cost and quality are measured.
3. Should parser metadata include parse duration and page count? Recommendation: add later if useful; first rollout should keep block metadata minimal.
4. Should LiteParse bounding boxes feed a future visual-citation system? Recommendation: yes as a separate feature, not in this integration.
5. Should MarkItDown dependency eventually be removed? Recommendation: no for now; it remains better aligned with Markdown-ish Office conversion and safe fallback behavior.

---

## Suggested Rollout Order

1. Tests + metadata + adapter scaffolding.
2. LiteParse local PDF extraction behind `WIKI_DOCUMENT_PARSER`.
3. LiteParse binary PDF URL extraction behind same adapter.
4. Docker/requirements update and smoke validation.
5. Staging comparison on real PDFs.
6. Production enablement: `WIKI_DOCUMENT_PARSER=auto`, `WIKI_LITEPARSE_OCR=0`.
7. Optional later: OCR enablement, Office conversion experiments, visual citations from bounding boxes.
