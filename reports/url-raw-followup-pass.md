# URL Raw Follow-Up Pass

## Goal

Close the three gaps left by the first URL raw preservation pilot:

1. reduce noisy boilerplate on tutorial-style HTML pages,
2. improve generic HTML image ranking, and
3. stop refresh-only validation reruns from polluting `wiki/log.md` and notifications.

## What changed

- `scripts/auto_ingest.py` now scores article-like HTML roots and normalizes the best candidate instead of flattening the whole page.
- Generic image extraction now ranks candidates from `src`, lazy-load attributes, and `srcset` instead of taking first-hit results.
- Image scoring now:
  - penalizes logos, badges, app-store assets, trackers, and other chrome,
  - rewards article-local and `figure` images,
  - uses width and height when present or inferable from the URL, and
  - penalizes small square non-article assets so `og:image` logos do not slip through.
- `--validation-run` remains a single-file rerun mode, requires `--force`, updates raws and pages, and suppresses `wiki/log.md` append plus ntfy noise.
- `README.md`, `docs/workflows.md`, and `AGENTS.md` now describe validation-run as a targeted single-file review tool.

## Validation setup

All validation reruns used:

```bash
AUTO_INGEST_MAX_SYNTHESIS_PER_INGEST=0
```

Targets:

| Source | Why it matters |
|---|---|
| `raw/2026-04-08-lightgbm-light-gradient-boosting-machine-geeksforgeeks.md` | Noisy tutorial page with bad logo/app-store image selection in the pilot |
| `raw/2026-04-20-cloudflare-launches-code-mode-mcp-server-to-optimize-token-u.md` | Non-GeeksforGeeks article with many unrelated `100x100` thumbnails ahead of the article image |

## Validation gates

The follow-up implementation passed:

- `python3 -m py_compile scripts/auto_ingest.py`
- `python3 scripts/auto_ingest.py --help`
- CLI negative check: `--force --validation-run` without `raw_file` now fails instead of widening into a batch rerun path

## Results

| Source | Before | After | Outcome |
|---|---|---|---|
| LightGBM / GeeksforGeeks | fetched body still carried page noise; `image_urls` preferred logo + store assets | fetched body now starts with article content and section structure; `image_urls: []`; rerun no longer enters the vision lane | improved and safe |
| Cloudflare / InfoQ | raw was still a URL stub; generic ranking would surface article image plus unrelated `100x100` thumbnails | fetched block persisted; `image_urls` reduced to the article image plus one header image; rerun kept the vision lane with only 2 relevant images | improved |

## Evidence

### LightGBM / GeeksforGeeks

- Current fetched block:
  - starts with article text, not nav boilerplate,
  - preserves section headings such as `## Prerequisites` and `## LightGBM Core Parameters`,
  - stores `image_urls: []`, which is better than sending a known bad logo into the vision lane.
- Current rerun route:
  - pilot: vision lane because bad logo images were captured,
  - follow-up: default text lane because no trustworthy article image remained.

### Cloudflare / InfoQ

- Current fetched block now stores:
  - the large article image,
  - the page header image,
  - and drops the unrelated `100x100` sidebar thumbnails.
- The source page regenerated successfully from the persisted block.

### Validation-run logging policy

- The validation reruns rebuilt pages and `wiki/index.md`.
- They did **not** append entries for the two validation raws to `wiki/log.md`.
- They did **not** send ntfy notifications.

## Resolution status for the three follow-up items

| Follow-up item | Status | Notes |
|---|---|---|
| Better article-body extraction for noisy tutorial sites | mostly resolved | GeeksforGeeks improved materially; InfoQ still carries some residual publication chrome near the top and bottom |
| Better generic HTML image ranking | resolved for tested pages | GeeksforGeeks now drops the bad logo; InfoQ keeps only the relevant article visuals |
| Refresh-only audit-log policy | resolved | `--validation-run` now behaves like a review-only rerun without audit noise |

## Remaining limitations

1. Article extraction is still heuristic. InfoQ keeps some chrome such as `InfoQ Homepage`, author-module text, and related-content/footer material in the persisted block.
2. Image ranking is now safer, but some pages may still have no trustworthy image candidate. In those cases the correct result is an empty list, not a forced vision run.
3. The validation mode is intentionally manual and single-file scoped. It is not a bulk rerun tool.

## Pros

- Removes the worst image-ranking failure from the pilot.
- Keeps validation reruns auditable without making `wiki/log.md` noisy.
- Preserves section structure well enough for durable raw snapshots.
- Uses a safer precision-first image policy for generic HTML pages.

## Cons

- Some news/editorial pages still keep publication chrome in the fetched block.
- Empty `image_urls` means some pages will lose vision enrichment unless a real article image exists.
- Validation still requires explicit manual targeting.

## Recommendation

Ship this follow-up on top of the pilot behavior. It closes the two clearest operational problems from the pilot and turns validation reruns into a usable review workflow.

Do not treat article extraction as finished. The next improvement should target residual chrome removal for article pages that wrap the story in author, audio, newsletter, and related-content modules.
