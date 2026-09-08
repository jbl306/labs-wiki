# Lessons Learned — labs-wiki

<!--
Format:
## YYYY-MM-DD: Short title

- **Pattern**: What went wrong or what was learned
- **Root cause**: Why it happened
- **Prevention rule**: How to avoid it next time
- **Affected files**: Which files were involved
- **Category**: knowledge-curation | auto-ingest | infrastructure | agents
-->

## 2026-04-19: Quality score conflated structural completeness with execution posture

- **Pattern**: Copilot session checkpoints landed in the wiki with `quality_score: 100` regardless of whether they described **planned**, **executed**, or **validated** work. Downstream agents treated the score as a proxy for "this is settled knowledge" and pulled tentative plans into MemPalace as truth.
- **Root cause**: `compute_quality_score` only measured frontmatter completeness, cross-references, source attribution, and recency — none of which capture whether the underlying work actually shipped. The schema had no field to distinguish posture, so the rubric quietly absorbed the question.
- **Prevention rule**: Track execution posture as its own first-class field (`knowledge_state: planned | executed | validated`) and never read `quality_score` as confidence. When introducing a new posture-bearing schema, also update the lint rubric, the auto-ingest path, and the MemPalace export filter in the same change so the three views stay coherent.
- **Affected files**: `scripts/checkpoint_classifier.py`, `scripts/auto_ingest.py`, `scripts/wiki_to_mempalace.py`, `docs/memory-model.md`, `templates/source-summary.md`
- **Category**: knowledge-curation

## 2026-04-20: Second-curation report ran on stale checkpoint state because the audit script hadn't been re-run

- **Pattern**: The second-curation report (`reports/second-curation-report-2026-04-20.md`) was generated against a snapshot of `checkpoint_state` that predated several `retention_mode` flips. Recommendations in the report contradicted what was already on disk, and the agent acted on the stale rows.
- **Root cause**: The curation script defaulted to its cached state file instead of recomputing from the live wiki. There was no freshness assertion before producing recommendations, so a multi-day-old cache silently became the input.
- **Prevention rule**: Any script that produces editorial recommendations must either (a) recompute its inputs from the canonical source on every run, or (b) print a `state generated at: <timestamp>` banner and refuse to emit recommendations if that timestamp is older than the most recent `wiki/log.md` entry. Add the freshness check upstream, not downstream.
- **Affected files**: `scripts/backfill_checkpoint_curation.py`, `scripts/checkpoint_state.py`, `reports/second-curation-report-2026-04-20.md`
- **Category**: tooling

## 2026-04-21: quality_score saturated at 100 across the entire corpus

- **Pattern**: The full review (`reports/full-review-2026-04-21.md`) found 324 of 327 wiki pages pinned at `quality_score: 100`. The score had stopped differentiating thin entity stubs from six-source synthesis pages, breaking the signal that tier promotion (R7) and lint review depend on.
- **Root cause**: The four-bucket rubric (frontmatter complete / has any wikilink / sources non-empty / verified within 90 days) is satisfied by every page on day one of auto-ingest. The rubric measured presence, not quality.
- **Prevention rule**: Any "score" that produces a near-uniform distribution after >100 samples is broken — track the score distribution in CI and alarm when the IQR collapses. Replace presence-checks with continuous signals (graph degree, body length band, citable-claim regex, staleness curve, knowledge_state). R3 in the full review owns the rewrite of `compute_quality_score` and is the prevention.
- **Affected files**: `scripts/lint_wiki.py`, `docs/memory-model.md`, `reports/full-review-2026-04-21.md`
- **Category**: knowledge-curation

## 2026-08-13: Auto-ingest deployment exposed build-time permissions and strict-schema drift

- **Pattern**: The updated watcher reached Codex only after two unrelated runtime blockers were corrected: operator-private prompt files were unreadable to the non-root container user, and an optional object property was omitted from a strict structured-output schema's `required` array.
- **Root cause**: Image copies inherited source-tree modes without a runtime-readability assertion, while local schema validation did not enforce the OpenAI strict-mode rule that every declared object property must be required (nullable when semantically optional).
- **Prevention rule**: Auto-ingest image tests must read every shipped prompt/template as the configured runtime UID, and proposal-schema tests must recursively assert `required == properties.keys()` for closed objects before deployment.
- **Affected files**: `Dockerfile.auto-ingest`, `scripts/ingest_transaction.py`, `tests/test_ingest_transaction.py`
- **Category**: auto-ingest

## 2026-08-17: Same-document source captures must upsert the canonical page

- **Pattern**: An arXiv abstract capture created a canonical source page, then a second capture of the paper's PDF proposed `operation: create` for that same source path and the transaction failed instead of incorporating the richer raw capture.
- **Root cause**: The proposal validator treated every create-to-existing-path mismatch as terminal, even when the collision was the single required source mutation for the same normalized title. The model's operation label was trusted more than the deterministic path and page identity evidence.
- **Prevention rule**: Reconcile exact-path, same-type, same-title source/concept/entity creates from racing ingests only when the current raw capture's normalized upstream identity matches the canonical page; normalize both modern and legacy slash-style arXiv abstract/PDF IDs, and use equal source hashes as the fallback only when that raw has no URL identity. Require the deterministic current-raw preflight hash for every reconciliation, require every reconciled mutation to cite the current raw, and bind its `source_hash` to that deterministic hash rather than accepting inherited provenance or a model-proposed copied hash as identity proof; fail closed when the deterministic hash is absent or invalid. Compare titles case-insensitively with whitespace normalization only, retaining punctuation as identity-significant. Keep prior raw sources, accumulated list metadata, original creation date, quality metadata, and established tier. Use the richer proposed body for source pages; retain both racers' body content for concepts/entities. Continue rejecting existing-path creates for synthesis pages and identity, type, or title mismatches.
- **Affected files**: `scripts/ingest_transaction.py`, `tests/test_ingest_transaction.py`, `.github/skills/wiki-ingest/SKILL.md`
- **Category**: auto-ingest

## 2026-08-17: Explicit updates and deterministic skips share the publication trust boundary

- **Pattern**: A schema-valid model proposal could declare `operation: update` and replace an unrelated canonical source page, while duplicate/retention short-circuits changed raw status without log, commit, or notification evidence.
- **Root cause**: Transaction guards covered racing stale creates but treated explicit updates as trusted full replacements; pre-backend success branches bypassed normal publication finalization.
- **Prevention rule**: Bind every update to matching type/title plus deterministic current-raw hash and provenance, require current upstream identity for source-page updates, and preserve accumulated canonical metadata/provenance/body. Finalize deterministic skips through status, audit log, manifest-scoped commit, and notification outside validation mode.
- **Follow-up hardening**: Source provenance must remain identity-closed: validate every newly proposed raw path before merging so an untrusted proposal cannot seed a second upstream identity that authorizes future updates. Treat the manifest commit as the success boundary for duplicate/retention finalization; if it returns false or raises, restore raw/log state, suppress success notification, and fail for retry.
- **Affected files**: `scripts/ingest_transaction.py`, `scripts/auto_ingest.py`, `tests/test_ingest_transaction.py`, `tests/test_auto_ingest_agent_cli.py`, `.github/skills/wiki-ingest/SKILL.md`
- **Category**: auto-ingest

## 2026-08-25: Shared API and MCP boundaries need executable contract tests

- **Pattern**: The MCP capture wrapper advertised a narrower, authenticated contract than the ingest API and generated tool schema actually enforced; tags changed shape, authentication could disappear, unsafe response paths were echoed, and retry behavior was ambiguous.
- **Root cause**: The wrapper was tested with hand-built response doubles and in isolation from the FastMCP schema and ASGI endpoint, so cross-boundary drift and transport behavior were not exercised.
- **Prevention rule**: Test shared capture contracts with real `httpx` responses/transports, the generated FastMCP schema, and the ASGI app. Cover authentication, transport restrictions, input shape, safe output paths, existing tool inventory, and explicit duplicate/retry semantics without claiming unsupported idempotency.
- **Affected files**: `scripts/wiki_mcp_server.py`, `wiki-ingest-api/app.py`, `tests/test_wiki_mcp_server.py`, `tests/test_wiki_ingest_api_contract.py`, `docs/tool-setup.md`, `wiki-ingest-api/README.md`
- **Category**: api

## 2026-08-25: Keep frontmatter serialization and response disclosure separate

- **Pattern**: Punctuation-bearing tags did not round-trip through raw frontmatter, and a valid post-write response path was rejected whenever an ordinary authentication token appeared in the path.
- **Root cause**: Tags used display-oriented comma joining instead of a data serializer, while one predicate combined structural path validation with secret-disclosure policy.
- **Prevention rule**: Serialize frontmatter collections with JSON-valid YAML and round-trip punctuation-heavy cases; validate response structure independently, then suppress only the sensitive value while still reporting bounded success.
- **Affected files**: `wiki-ingest-api/app.py`, `scripts/wiki_mcp_server.py`, `tests/test_wiki_ingest_api_contract.py`, `tests/test_wiki_mcp_server.py`
- **Category**: api

## 2026-08-25: Validate transport shapes before coercion and serialize YAML scalars

- **Pattern**: User-controlled title, source, and URL values could break raw-source YAML, while JSON tags outside `list[str]` were coerced or ignored instead of rejected.
- **Root cause**: The flexible request parser coerced JSON values before enforcing the JSON contract, and the frontmatter writer used hand-built quoting instead of a scalar serializer.
- **Prevention rule**: Validate JSON collection shapes before generic transport coercion, keep form/query string parsing separate, serialize user-controlled YAML scalars with JSON-valid YAML, and round-trip quotes, backslashes, colons, and hashes through PyYAML tests.
- **Affected files**: `wiki-ingest-api/app.py`, `tests/test_wiki_ingest_api_contract.py`
- **Category**: api


## 2026-09-07: Match paper captures by verified upstream identity

- **Pattern**: An arXiv PDF could not enrich the source page created from the same paper's Hugging Face listing.
- **Root cause**: URL normalization recognized arXiv abstract/PDF aliases but treated the listing and HTML URL as different documents.
- **Prevention rule**: Normalize supported paper URLs by validated arXiv ID; retain exact-host, provenance, hash, and title checks, and test both create reconciliation and updates.
- **Affected files**: `scripts/ingest_transaction.py`, `tests/test_ingest_transaction.py`
- **Category**: auto-ingest


## 2026-09-07: Keep proposal hash instructions aligned with validation

- **Pattern**: After paper identity was fixed, the live proposal failed because an updated concept retained its earlier source hash.
- **Root cause**: The proposal prompt told the model to preserve valid canonical-page hashes, while the transaction validator requires the current deterministic raw-source hash for every mutation.
- **Prevention rule**: Apply the supplied SOURCE_HASH to every created or updated page; preserve historical provenance through sources. Keep the strict hash check and align prompt instructions with it.
- **Affected files**: `scripts/prompts/wiki_ingest_proposal_prompt.md`, `scripts/ingest_transaction.py`
- **Category**: auto-ingest
