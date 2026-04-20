# URL Raw Backfill Strategy

## Goal

Define a backfill plan that improves high-value URL raws without overrunning the GitHub Models free tier.

## Constraints from GitHub Models

GitHub's current documentation says free GitHub Models usage is rate-limited by:

- requests per minute,
- requests per day,
- tokens per request, and
- concurrent requests.

Source: <https://docs.github.com/en/github-models/use-github-models/prototyping-with-ai-models#rate-limits>

For free-tier usage, the current published limits are:

| Tier | Requests/minute | Requests/day | Tokens/request | Concurrent requests |
|---|---:|---:|---|---:|
| Low | 15 | 150 | 8000 in / 4000 out | 5 |
| High | 10 | 50 | 8000 in / 4000 out | 2 |
| Embedding | 15 | 150 | 64000 | 5 |

These limits are explicitly for experimentation and are subject to change. GitHub also states that paid usage unlocks production-grade limits. Source: <https://docs.github.com/en/billing/concepts/product-billing/github-models>

For paid planning, GitHub's current pricing reference lists:

- OpenAI GPT-4.1: $2.00 per 1M input token units, $8.00 per 1M output token units
- OpenAI GPT-4.1-mini: $0.40 per 1M input token units, $1.60 per 1M output token units

Source: <https://docs.github.com/en/billing/reference/models-multipliers-and-costs>

## Working assumptions for labs-wiki

1. URL refreshes that keep image analysis on the vision-capable lane should be treated as **high-tier** work for quota planning.
2. Text-only refreshes can usually stay on a cheaper lane.
3. Synthesis creation is not free just because the source refresh already happened; every synthesis is another model call.
4. The free tier is suitable for curated backfill and evaluation, not a blind historical sweep.

## Operating rules

1. Keep `AUTO_INGEST_MAX_SYNTHESIS_PER_INGEST=0` for normal backfill refreshes unless the run is explicitly a synthesis batch.
2. Use `--force --refresh-fetch --validation-run` for spot-check reruns during tuning so audit noise stays low.
3. Reserve image-bearing reruns for pages where images materially improve the wiki page.
4. Stop a batch after repeated `429` responses, not after the whole queue fails.
5. Treat every batch as sampled QA, not fire-and-forget ingestion.

## Lane 1: High-value targeted backfill

**Use when:** a URL source is strategically important, clearly degraded, or likely to compound into many downstream wiki reads.

| Item | Policy |
|---|---|
| Scope | Hand-picked URLs only: foundational papers, durable architecture posts, core tool docs, high-signal tutorials |
| Daily budget | 5-10 refreshes/day on free tier |
| Model posture | Prefer text/default lane; use vision only when a real article image or figure set matters |
| Synthesis setting | `AUTO_INGEST_MAX_SYNTHESIS_PER_INGEST=0` |
| Validation | Review every item's fetched block and regenerated source page |
| Stop condition | Stop the batch on repeated `429`s, obvious extraction regressions, or bad image selection |

**Why this lane first:** it spends quota only where better raws clearly improve future re-ingest and search quality.

## Lane 2: Synthesis-focused backfill

**Use when:** the goal is not just better source pages, but better cross-page synthesis coverage.

| Item | Policy |
|---|---|
| Scope | Small curated clusters, usually 3-5 related sources per concept family |
| Daily budget | 1-2 clusters/day on free tier |
| Model posture | Refresh sources first; then run a limited synthesis pass |
| Synthesis setting | Refresh pass: `AUTO_INGEST_MAX_SYNTHESIS_PER_INGEST=0`; synthesis pass: raise to `1` for the curated run |
| Validation | Review the cluster's source pages plus the generated synthesis page |
| Stop condition | Stop if the synthesis page is generic, redundant, or clearly not worth the extra request |

**Recommended workflow:**

1. refresh the candidate source raws without synthesis,
2. inspect whether the improved raws actually deepen concept coverage,
3. run one synthesis pass only on clusters that now have enough substance.

This keeps synthesis as a second-stage multiplier, not a default tax on every refresh.

## Lane 3: Full historical backfill

**Use when:** the objective is broad historical normalization of URL raws across the repository.

| Item | Policy |
|---|---|
| Scope | Large-scale refresh across old URL raws |
| Daily budget | **Not recommended on free tier** beyond a slow pilot slice |
| Model posture | Prefer low/default text lanes first; hold vision-heavy sources for a later paid/BYOK phase |
| Synthesis setting | `AUTO_INGEST_MAX_SYNTHESIS_PER_INGEST=0` during bulk refresh |
| Validation | Sample review every batch; keep a running tracker of pass/fail patterns |
| Stop condition | Stop immediately on sustained rate limits, rising extraction regressions, or queue growth that outpaces review |

**Recommendation:** do not run a true full backfill on the free tier. Use a paid GitHub Models plan or BYOK first.

If a historical sweep must begin before that:

1. start with a narrow pilot slice,
2. exclude vision-heavy pages,
3. cap the run well below the published daily limit, and
4. require sampled manual review before expanding scope.

## Suggested sequence

1. Run Lane 1 now on a small set of high-value URLs.
2. Use those results to identify clusters worth Lane 2 synthesis work.
3. Defer Lane 3 until paid usage or BYOK is enabled.

## Practical free-tier policy

For the current repo, the safest default is:

- targeted reruns first,
- no bulk synthesis during refresh,
- no blind historical sweep,
- and vision only when ranked image selection finds real article imagery.

That policy matches the pilot and follow-up results: the work is valuable, but the quota is better spent on precise repairs than on mass refreshes.
