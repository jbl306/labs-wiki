# URL Raw Preservation Pilot Design

## Problem

`labs-wiki` produces strong pages from checkpoint raw because those raw files preserve rich source material. Many URL-derived raw files do not. They often store only frontmatter and a source URL, even though the ingest pipeline fetches article text at runtime. That design makes later re-ingest, audit, and wiki expansion depend on another network fetch instead of durable local source material. It also leaves concept, entity, and synthesis pages thinner than they should be.

## Goal

Preserve fetched URL article content back into `raw/` so future ingest runs have a durable source body, then run a small pilot on three representative URL pages to measure whether wiki fidelity improves for text, tables, and image- or chart-heavy content.

## Non-goals

- Do not change checkpoint raw export behavior.
- Do not run a broad corpus backfill.
- Do not redesign templates in this change.
- Do not introduce a new scoring system in this change.

## Recommended Approach

Modify `scripts/auto_ingest.py` so successful URL fetches write a deterministic fetched-content section into the corresponding raw markdown file. Keep the existing frontmatter and any manual source notes intact. Then run a targeted backfill on three non-checkpoint pages:

1. one text-heavy article,
2. one table-heavy article, and
3. one image-, chart-, or diagram-heavy article.

This change fixes the source-of-truth problem at the raw layer. It improves future ingest runs and keeps the pilot within the GitHub Models free-tier budget.

## Why This Approach

Three options were considered:

1. **Persist fetched content into `raw/`.** This is the recommended option because it makes raw the durable source of truth, improves re-ingest and audit, and aligns URL sources with the richer checkpoint model.
2. **Store fetched content in a separate cache.** This keeps raw files smaller, but it splits the durable source across two places and makes later review harder.
3. **Keep raw thin and rely on live fetches.** This is the smallest immediate change, but it preserves the current failure mode and weakens reproducibility.

## Design

### 1. Raw file format

For URL-based raw sources, the pipeline will append a stable fetched-content block to the markdown body after a successful fetch. The block should be easy to find, easy to replace, and safe to parse on later runs.

The block should contain:

- the fetch timestamp,
- the resolved source URL if it differs from the original,
- the content type when available, and
- the normalized article body used for extraction.

The body should preserve meaningful structure where possible. Headings, lists, code blocks, and tables should survive normalization. Boilerplate, duplicate navigation text, and obvious scrape noise should not.

### 2. Update behavior

The write path should be deterministic:

- If the fetched-content block does not exist, add it.
- If it already exists, replace only that block.
- If the fetch fails, do not write an empty block.

This keeps re-runs idempotent and avoids raw-file growth from duplicate appended bodies.

### 3. Scope boundaries

This change applies to all future URL ingests. It does not change checkpoint handling. The immediate backfill remains limited to three selected URL pages so the evaluation stays cheap and readable.

### 4. Pilot selection

The pilot should cover three shapes of source material:

1. **Text-heavy**: a page whose value is mostly narrative explanation.
2. **Table-heavy**: a page with comparison tables, parameter grids, or structured feature summaries.
3. **Image- or chart-heavy**: a page where diagrams, charts, or images materially affect understanding.

Selection should favor pages already identified as thin under the current pipeline so the before-and-after comparison is meaningful.

### 5. Evaluation output

After the three-page backfill, write a short evaluation artifact that records:

- which pages were selected,
- what new source material was preserved in `raw/`,
- whether the regenerated wiki pages captured more technical detail,
- whether tables and image-linked explanations translated better, and
- what fidelity gaps still remain.

The evaluation should answer one decision clearly: whether this raw-preservation pattern is worth broader rollout.

## Error Handling

- If URL fetch fails, keep the raw file unchanged except for the existing failure reporting path.
- If normalization produces no meaningful body, treat that as a failed preservation and keep the raw file unchanged.
- If a raw file contains manual notes outside the fetched-content block, preserve them.

The system should fail explicitly, not silently produce an empty or misleading durable source.

## Validation

Validate the change in three ways:

1. Run the repository's existing ingest or script validation path on the modified pipeline.
2. Re-ingest only the three pilot pages.
3. Inspect the resulting raw and wiki outputs to confirm that:
   - the fetched-content block is written once,
   - re-running updates the block instead of duplicating it, and
   - the generated pages preserve more useful detail than before.

## Risks and Mitigations

### Risk: raw files become noisy

Mitigation: normalize aggressively enough to remove boilerplate and write only the content that supports downstream extraction.

### Risk: free-tier model usage grows

Mitigation: restrict the backfill to three pages and avoid broad reprocessing.

### Risk: large fetched bodies obscure manual notes

Mitigation: isolate the fetched-content block with clear delimiters and replace only that block on updates.

## Expected Outcome

After this pilot, URL-derived raw files should preserve the article body that the ingest pipeline actually used. That should make URL-derived wiki pages deeper, more reproducible, and easier to audit. The evaluation should show whether the improvement is strong enough to justify a broader rollout.
