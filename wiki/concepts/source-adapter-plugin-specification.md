---
title: "Source Adapter Plugin Specification"
type: concept
created: 2026-04-21
last_verified: 2026-04-21
source_hash: "d08a3ffff055c78ea944afe2266f216cbdf096a7a4848a8aaca92dff7205ba1d"
sources:
  - raw/2026-04-11-httpsgithubcommilla-jovovichmempalace.md
quality_score: 56
concepts:
  - source-adapter-plugin-specification
related:
  - "[[MemPalace Memory System]]"
  - "[[milla-jovovich/mempalace]]"
tier: hot
tags: [plugin, adapter, ingest, extensibility, privacy, metadata]
---

# Source Adapter Plugin Specification

## Overview

The Source Adapter Plugin Specification (RFC 002) defines a formal contract for integrating new data sources into MemPalace. It enables third-party adapters to provide content for mining and retrieval, supporting extensibility, privacy, and structured metadata.

## How It Works

The specification formalizes how external data sources can be ingested into MemPalace via source adapters. Each adapter is a standalone Python package (e.g., `pip install mempalace-source-<name>`) that implements the `BaseSourceAdapter` interface. The core method is `ingest`, which receives a source reference and palace context, and yields a stream of `IngestResult` objects representing mined content.

Adapters declare the set of transformations they apply to source data, supporting both byte-preserving and transformed ingestion. This declaration is programmatically accessible, allowing users and enterprises to audit what happens to their data. Each adapter also declares a structured metadata schema, which can include domain-specific fields (e.g., `repo/PR/SHA` for code, `patient/encounter/CPT` for healthcare). The core system is agnostic to adapter-specific metadata beyond universal fields.

Incremental ingest is a key feature: re-running mining only touches items whose source-side version changed, using the palace itself as the cursor (no sidecar needed). Adapters are responsible for their own chunking strategies (e.g., tree-sitter for code, exchange-pair for chat, whole-record for PRs), and the system does not impose a chunk size.

Privacy is explicit: each adapter can declare a privacy class, ensuring that sensitive data (e.g., medical, legal, financial) is handled according to policy rather than implicit trust. The specification also covers entry-point registration, conformance tests, and the migration of existing miners into first-party adapters.

The adapter pattern generalizes to a wide range of sources, including knowledge work (Notion, Obsidian), communications (Slack, Discord, email), research (PDFs, Zotero), and creator workflows (YouTube captions, podcast transcripts).

## Key Properties

- **Pluggable Adapters:** Adapters are standalone Python packages that integrate new data sources into MemPalace.
- **Declared Transformations:** Each adapter advertises the transformations applied to source data, supporting auditability and trust.
- **Structured Metadata:** Adapters define their own metadata schemas, enabling domain-specific indexing and filtering.
- **Incremental Ingest:** Mining only processes changed items, using the palace as the cursor for efficient updates.
- **Privacy Classes:** Adapters can declare privacy classes for sensitive data, supporting explicit policy enforcement.

## Limitations

The specification does not define chunking strategies, live-stream/webhook shapes, LLM-based extraction, cross-adapter deduplication, or closet construction algorithms. These are left to adapters or core system features. Live-streaming and deduplication are future work.

## Example

A source adapter implements:

```python
class BaseSourceAdapter(ABC):
    @abstractmethod
    def ingest(
        *,
        source: SourceRef,
        palace: PalaceContext,
    ) -> Iterator[IngestResult]:
        """Enumerate and extract content from a source."""
```

A user installs an adapter:
```bash
pip install mempalace-source-slack
mempalace mine --source slack
```

## Visual

No diagram, but the RFC provides tables of in-flight adapters and describes the adapter integration workflow.

## Relationship to Other Concepts

- **[[MemPalace Memory System]]** — Source adapters are the entry point for mining content into the MemPalace memory architecture.

## Practical Applications

Organizations and users can extend MemPalace to ingest data from diverse sources (code, chat, documents, email, etc.) without modifying core code. This supports regulated domains, research, and enterprise workflows requiring structured, privacy-aware memory ingestion.

## Sources

- [[milla-jovovich/mempalace]] — primary source for this concept
