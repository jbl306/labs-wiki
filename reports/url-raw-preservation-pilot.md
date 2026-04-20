# URL Raw Preservation Pilot

## Goal

Preserve the normalized body of URL sources back into `raw/` so later re-ingest can reuse a durable snapshot instead of depending on a fresh network fetch.

## What changed

- `scripts/auto_ingest.py` now:
  - normalizes HTML with BeautifulSoup instead of flattening everything with regex,
  - writes a deterministic fetched-content block into `raw/` for `type: url` sources,
  - stores fetched image URLs in the block metadata so later reruns can still use the vision lane,
  - reuses the persisted block on rerun,
  - supports `--force` for already-ingested files, and
  - supports `--refresh-fetch` to re-fetch and replace the persisted block.
- `scripts/requirements-auto-ingest.txt` now includes `beautifulsoup4`.
- `AGENTS.md`, `.github/instructions/raw-sources.instructions.md`, `README.md`, and `docs/workflows.md` now document the fetched-content block as an allowed automated raw-file mutation for URL sources.

## Validation gates

The finished implementation passed:

- `python3 -m py_compile scripts/auto_ingest.py`
- `python3 scripts/auto_ingest.py --help`
- `docker build -f Dockerfile.auto-ingest -t labs-wiki-auto-ingest-test .`

## Pilot scope

All pilot runs used `AUTO_INGEST_MAX_SYNTHESIS_PER_INGEST=0`.

| Source | Type | Result |
|---|---|---|
| `raw/2026-04-20-agents-that-remember-introducing-agent-memory.md` | text-heavy article | fetched block persisted, source page regenerated, concept/entity coverage improved |
| `raw/2026-04-08-lightgbm-light-gradient-boosting-machine-geeksforgeeks.md` | table/tutorial-heavy article | fetched block persisted, source page regenerated, section structure survived the fetch/normalize path |
| `raw/2026-04-16-251004618v3pdf.md` | figure/equation-heavy arXiv paper | fetched block persisted, source page regenerated, refresh and non-refresh vision reruns both verified |

## Evidence

Each pilot raw file now has exactly one fetched-content block:

| Raw file | Start markers | End markers | Persisted chars | Image URLs |
|---|---:|---:|---:|---:|
| `2026-04-20-agents-that-remember-introducing-agent-memory.md` | 1 | 1 | 24,964 | 4 |
| `2026-04-08-lightgbm-light-gradient-boosting-machine-geeksforgeeks.md` | 1 | 1 | 10,296 | 3 |
| `2026-04-16-251004618v3pdf.md` | 1 | 1 | 50,497 | 5 |

Relevant file churn from the pilot:

- 3 raw files enriched with fetched-content blocks
- 3 source pages regenerated
- `wiki/index.md` updated
- `wiki/log.md` updated

Diff summary for the pilot artifacts:

- `1594` insertions
- `48` deletions

## What improved

### 1. Raw now contains the durable source we actually ingest

Before the pilot, these URL raw files held little more than frontmatter plus the original URL. After the pilot, the normalized article or paper body lives in `raw/`, which makes re-ingest auditable and reproducible.

### 2. Source pages got materially better

- The Cloudflare Agent Memory article now produces a detailed source page with stronger summaries, concepts, and entity coverage because the model sees the real article body instead of a stub URL.
- The LightGBM tutorial now preserves section structure and bullet lists well enough to recover the main algorithm, parameter, and training sections.
- The ACE arXiv paper now preserves a large structured body and can route through the vision lane with working figure downloads.

### 3. Manual reruns are now practical

`--force` lets us reprocess an already-ingested raw file without manually mutating `status:`.

`--refresh-fetch` lets us replace the fetched-content block deterministically. The pilot also verified the figure-heavy rerun case end-to-end: after refreshing the arXiv raw once, a second `--force` run without `--refresh-fetch` still downloaded 5 persisted images and stayed on the vision lane.

## Issues the pilot exposed

### 1. Relative image resolution for arXiv HTML

The first arXiv run preserved the text but resolved figure URLs incorrectly. Fix: image resolution now respects the page URL directly instead of forcing an extra trailing slash.

### 2. Regex replacement on refresh

Refreshing a fetched block with backslash-heavy content could fail during regex replacement. Fix: block replacement now uses a function-based substitute instead of a raw replacement string.

### 3. HTML normalization still pulls some boilerplate

The LightGBM raw snapshot still includes some GeeksforGeeks navigation noise near the top. The new normalization is much better than regex tag stripping, but it is not yet article-body extraction.

### 4. Image selection remains heuristic

The LightGBM page pulled store-badge style images rather than article-specific diagrams. The arXiv case is now correct, but generic HTML image ranking still needs tuning.

### 5. Repeated forced validation reruns append repeated ingest log entries

This is expected with the current pipeline, but it makes the pilot noisier to review. The arXiv validation reruns added multiple `wiki/log.md` entries because each forced refresh is treated as a real ingest.

### 6. Free-tier rate limiting is real but manageable

The final arXiv refresh hit one GitHub Models API `429 Too Many Requests` response and then succeeded on retry. The quota-safe settings helped, but a large backfill would still need pacing.

## Pros

- Preserves the real ingested source in `raw/`
- Makes reruns more reproducible
- Preserves image metadata so vision-capable reruns do not require a live refresh
- Improves source-page fidelity for long-form URLs
- Keeps the raw mutation deterministic and replace-in-place
- Works with quota-safe settings (`AUTO_INGEST_MAX_SYNTHESIS_PER_INGEST=0`)

## Cons

- HTML cleanup is still weaker than true article extraction
- Generic image selection still captures some non-content images
- Forced reruns append more audit-log noise than ideal
- Free-tier rate limits will matter on larger refresh batches
- Existing concept/entity pages are not deeply refreshed unless the ingest naturally creates or merges them

## Recommendation

Ship this as the new default behavior for URL sources, but keep the rollout conservative:

1. Keep broad backfill out of scope for now.
2. Use targeted reruns for high-value URL sources first.
3. Improve boilerplate stripping and image ranking before any large-scale historical backfill.
4. If repeated refresh runs become common, add a cleaner audit-log strategy for refresh-only validation runs.

## Recommended next steps

1. Merge this pilot branch after review.
2. Use the new flow for selective high-value URL reruns instead of mass backfill.
3. Add one follow-up pass focused on:
   - better article-body extraction for noisy tutorial sites,
   - better image ranking for generic HTML pages, and
   - a policy for refresh-only audit-log entries.
