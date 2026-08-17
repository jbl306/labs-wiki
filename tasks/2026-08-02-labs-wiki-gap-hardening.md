# Labs Wiki gap hardening

## Goal

Close the six production gaps identified by the independent `llm-wiki` comparison while retaining Labs Wiki as the executable engine:

1. enforce source-origin-family independence for `cross-source` synthesis;
2. replace checkout-mutating agent execution with read-only typed proposals and orchestrator-owned publication;
3. validate every proposed wiki page against a shared strict schema, not only synthesis pages;
4. migrate the legacy synthesis corpus to the strict evidence contract without inventing support;
5. perform source-hash deduplication before every model/backend invocation;
6. make graph generation a deterministic ingest-finalization gate.

## Constraints

- Keep the repository/homelab boundary: no live service restart, compose edit, credential movement, or deployment.
- Preserve raw-source immutability except deterministic fetched/extracted blocks and orchestrator-owned status.
- Preserve unrelated work and manifest-limit any ingest publication/commit.
- Failed agent proposal, schema validation, index generation, or graph generation must leave canonical wiki pages, log, and raw status unchanged.
- Corpus migration must never fabricate supporting pages or raw provenance. Unsupported legacy claims are retained as explicitly pending evidence, not accepted as grounded insights.

## Plan

- [x] Add RED tests for origin-family enforcement, shared page schema, read-only proposal output, transaction rollback, all-backend preflight hash dedup, and graph-gated finalization.
- [x] Add a shared strict wiki-page contract and use it to gate every touched canonical page.
- [x] Change agent CLI output to a typed proposal containing page mutations and KG facts; run Codex read-only.
- [x] Stage proposals in an isolated temporary wiki, validate all pages, rebuild index and graph, then publish with rollback-on-failure semantics.
- [x] Run the same pre-backend content-hash check and deterministic index/graph finalization gates for compatibility/legacy backends.
- [x] Enforce independent origin families for `cross-source` synthesis and record deterministic family count.
- [x] Add and run an idempotent legacy synthesis migration that backfills the strict frontmatter/Evidence Map contract from existing wikilinks/provenance only.
- [x] Update prompt/templates/docs/container dependencies and runtime script packaging.
- [x] Run focused tests, full tests, strict corpus audit, wiki lint, graph rebuild, Python compilation, `git diff --check`, and independent diff review.

## Acceptance criteria

- Agent CLIs use a read-only sandbox and cannot write canonical files directly.
- A malformed/failed/timed-out proposal leaves no wiki page artifacts.
- Every proposed source/concept/entity/synthesis page is schema-validated before publication.
- Duplicate source content returns before the backend call for every backend.
- `cross-source` synthesis fails strict audit unless at least two deterministic origin families are present.
- Every synthesis page carries `evidence_scope`, `evidence_source_count`, `evidence_origin_family_count`, and an `## Evidence Map`; unsupported legacy claims are not represented as grounded Key Insights.
- Index and graph artifacts are produced before log/status/notification finalization; either failure leaves raw status pending and canonical state unchanged.
- No live homelab runtime/config is changed.

## Review / results

- Full Python suite: 43 tests passed; a real staged ingest rebuilt and validated index/graph/tracker before atomic publication.
- Auto-ingest Docker image built successfully and imported all packaged runtime modules.
- Wiki lint: 967 pages, 0 errors (existing freshness/quality warnings remain advisory).
- Strict synthesis audit: 83/83 passed, all fully grounded; migration check is idempotent with 0 pages pending.
- Canonical graph: 967 nodes / 3,309 edges with source-signature, endpoint, count, and cold/warm byte-determinism checks passing.
- Agent proposals publish under an ingest lock through staged index/graph generation and rollback-capable atomic replacement.
- Independent audit findings were incorporated: normalized historical hash prefixes, cache-independent graph bytes, runtime-only embeddings, configured tracker refresh, and commit-before-notification ordering.
