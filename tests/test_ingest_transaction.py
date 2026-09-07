import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import ingest_transaction  # noqa: E402


class IngestTransactionTests(unittest.TestCase):
    def test_paper_urls_share_identity_only_for_recognized_hosts_and_ids(self) -> None:
        for url in (
            "https://huggingface.co/papers/2608.28122",
            "https://huggingface.co/papers/2608.28122/?source=daily#discussion",
            "https://arxiv.org/abs/2608.28122",
            "https://arxiv.org:443/abs/2608.28122/",
            "http://huggingface.co:80/papers/2608.28122",
            "https://arxiv.org/pdf/2608.28122v1.pdf",
            "https://arxiv.org/html/2608.28122v1",
        ):
            with self.subTest(url=url):
                self.assertEqual(ingest_transaction._normalized_upstream_identity(url), "arxiv:2608.28122")
        for url in (
            "https://huggingface.co/papers/2608.28123",
            "https://huggingface.co/papers/trending",
            "https://huggingface.co/papers/2608.28122/discussion",
            "https://huggingface.co.example.org/papers/2608.28122",
            "https://arxiv.org.example.org/pdf/2608.28122",
            "file://huggingface.co/papers/2608.28122",
            "https://huggingface.co:bad/papers/2608.28122",
            "https://huggingface.co:444/papers/2608.28122",
            "https://arxiv.org:bad/abs/2608.28122",
            "https://arxiv.org:444/pdf/2608.28122",
            "https://arxiv.org:0/abs/2608.28122",
            "https://arxiv.org/abs/2608.28122//",
        ):
            with self.subTest(url=url):
                self.assertNotEqual(ingest_transaction._normalized_upstream_identity(url), "arxiv:2608.28122")
        self.assertEqual(
            ingest_transaction._normalized_upstream_identity("https://arxiv.org:0/abs/2608.28122"),
            "https://arxiv.org:0/abs/2608.28122",
        )

    def test_huggingface_paper_can_be_enriched_from_arxiv_preserving_provenance(self) -> None:
        for operation in ("create", "update"):
            with self.subTest(operation=operation), tempfile.TemporaryDirectory() as tmp:
                root, raw = self._root(tmp)
                raw.write_text("---\ntitle: Example\ntype: url\nurl: https://arxiv.org/pdf/2608.28122\nstatus: pending\n---\nFull paper\n")
                (root / "raw/prior.md").write_text("---\ntitle: Prior\ntype: url\nurl: https://huggingface.co/papers/2608.28122\nstatus: ingested\n---\nPaper listing\n")
                existing = root / "wiki/sources/example.md"
                existing.write_text(self._proposal("raw/prior.md")["page_mutations"][0]["content"])
                proposal = self._proposal()
                proposal["page_mutations"][0]["operation"] = operation
                stage = root / "stage"
                ingest_transaction._copy_transaction_inputs(root, stage)
                ingest_transaction._write_mutations(proposal, root, stage, raw, expected_source_hash="a" * 64)
                frontmatter, _, error = ingest_transaction.parse_page_text((stage / "wiki/sources/example.md").read_text())
                self.assertIsNone(error)
                self.assertEqual(frontmatter["sources"], ["raw/prior.md", "raw/example.md"])

    def test_legacy_arxiv_abstract_and_pdf_urls_share_identity(self) -> None:
        self.assertEqual(
            ingest_transaction._normalized_upstream_identity(
                "https://arxiv.org/abs/hep-th/9901001v2"
            ),
            "arxiv:hep-th/9901001",
        )
        self.assertEqual(
            ingest_transaction._normalized_upstream_identity(
                "https://arxiv.org/pdf/hep-th/9901001v2.pdf"
            ),
            "arxiv:hep-th/9901001",
        )

    def test_proposal_schema_requires_every_declared_object_property(self) -> None:
        """Keep Codex structured-output schemas compatible with OpenAI strict mode."""
        def assert_closed_objects_require_all_properties(schema: object) -> None:
            if isinstance(schema, dict):
                properties = schema.get("properties")
                if schema.get("type") == "object" and isinstance(properties, dict):
                    self.assertEqual(set(schema.get("required", [])), set(properties))
                for value in schema.values():
                    assert_closed_objects_require_all_properties(value)
            elif isinstance(schema, list):
                for value in schema:
                    assert_closed_objects_require_all_properties(value)

        assert_closed_objects_require_all_properties(ingest_transaction.PROPOSAL_SCHEMA)

    def _root(self, tmp: str) -> tuple[Path, Path]:
        root = Path(tmp)
        for directory in ("raw", "wiki/sources", "wiki/concepts", "wiki/entities", "wiki/synthesis", "wiki/graph", "reports"):
            (root / directory).mkdir(parents=True, exist_ok=True)
        raw = root / "raw" / "example.md"
        raw.write_text("---\ntitle: Example\ntype: text\nstatus: pending\n---\nEvidence\n")
        (root / "wiki" / "index.md").write_text("# Old Index\n")
        (root / "wiki" / "log.md").write_text("# Log\n\n```yaml\n```\n")
        (root / "wiki" / "graph" / "graph.json").write_text('{"old": true}\n')
        return root, raw

    def _proposal(self, raw_rel: str = "raw/example.md") -> dict:
        page = f"""---
title: Example
type: source
created: 2026-08-02
last_verified: 2026-08-02
source_hash: {'a' * 64}
sources:
  - {raw_rel}
concepts: []
related: []
tier: hot
tags: [example]
---
# Example

## Summary

A source summary grounded in the raw evidence.
"""
        return {
            "status": "success",
            "source_path": "wiki/sources/example.md",
            "page_mutations": [
                {"path": "wiki/sources/example.md", "operation": "create", "content": page}
            ],
            "duplicates_avoided": [],
            "kg_facts": [],
            "notes": "created source",
        }

    def test_graph_failure_leaves_canonical_state_unchanged(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root, raw = self._root(tmp)
            before = {
                "raw": raw.read_text(),
                "index": (root / "wiki/index.md").read_text(),
                "graph": (root / "wiki/graph/graph.json").read_text(),
                "log": (root / "wiki/log.md").read_text(),
            }

            with patch("ingest_transaction._build_graph", side_effect=RuntimeError("graph failed")):
                with self.assertRaisesRegex(RuntimeError, "graph failed"):
                    ingest_transaction.prepare_and_publish(
                        self._proposal(),
                        root,
                        raw,
                        backend="codex-cli",
                        validation_run=False,
                    )

            self.assertFalse((root / "wiki/sources/example.md").exists())
            self.assertEqual(raw.read_text(), before["raw"])
            self.assertEqual((root / "wiki/index.md").read_text(), before["index"])
            self.assertEqual((root / "wiki/graph/graph.json").read_text(), before["graph"])
            self.assertEqual((root / "wiki/log.md").read_text(), before["log"])

    def test_success_publishes_pages_index_graph_log_and_status_together(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root, raw = self._root(tmp)

            def fake_graph(stage_root: Path, _runtime: Path | None = None) -> None:
                graph_path = stage_root / "wiki/graph/graph.json"
                graph_path.parent.mkdir(parents=True, exist_ok=True)
                graph_path.write_text(json.dumps({"node_count": 1, "nodes": [{"id": "example"}]}) + "\n")
                tracker = stage_root / "reports/checkpoint-graph-tracker.md"
                tracker.parent.mkdir(parents=True, exist_ok=True)
                tracker.write_text("# Tracker\n")

            with patch("ingest_transaction._build_graph", side_effect=fake_graph):
                manifest = ingest_transaction.prepare_and_publish(
                    self._proposal(),
                    root,
                    raw,
                    backend="codex-cli",
                    validation_run=False,
                )

            self.assertIn("wiki/sources/example.md", manifest)
            self.assertIn("wiki/index.md", manifest)
            self.assertIn("wiki/graph/graph.json", manifest)
            self.assertIn("reports/checkpoint-graph-tracker.md", manifest)
            self.assertIn("wiki/log.md", manifest)
            self.assertIn("raw/example.md", manifest)
            self.assertIn("status: ingested", raw.read_text())
            self.assertIn("[[Example]]", (root / "wiki/index.md").read_text())
            self.assertIn("codex-cli", (root / "wiki/log.md").read_text())

    def test_invalid_page_schema_is_rejected_before_publish(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root, raw = self._root(tmp)
            proposal = self._proposal()
            proposal["page_mutations"][0]["content"] = "---\ntitle: Broken\ntype: source\n---\n"

            with self.assertRaises(ingest_transaction.ProposalError):
                ingest_transaction.prepare_and_publish(
                    proposal,
                    root,
                    raw,
                    backend="codex-cli",
                    validation_run=False,
                )

            self.assertFalse((root / "wiki/sources/example.md").exists())
            self.assertIn("status: pending", raw.read_text())

    def test_existing_source_create_is_reconciled_as_an_update(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root, raw = self._root(tmp)
            raw.write_text(
                "---\ntitle: Example\ntype: url\nurl: https://arxiv.org/pdf/2608.14071\n"
                "status: pending\n---\nEvidence\n"
            )
            prior_raw = root / "raw" / "prior.md"
            prior_raw.write_text(
                "---\ntitle: Prior\ntype: url\nurl: https://arxiv.org/abs/2608.14071\n"
                "status: ingested\n---\nPrior evidence\n"
            )
            existing = root / "wiki" / "sources" / "example.md"
            existing.write_text(
                f"""---
title: Example
type: source
created: 2026-08-01
last_verified: 2026-08-01
source_hash: {'b' * 64}
sources:
  - raw/prior.md
concepts:
  - prior-concept
related:
  - "[[Prior Concept]]"
tier: established
tags: [prior]
quality_score: 91
---
# Example

## Summary

Existing summary.
"""
            )
            proposal = self._proposal()
            proposal["page_mutations"][0]["content"] = (
                proposal["page_mutations"][0]["content"]
                .replace(
                    "A source summary grounded in the raw evidence.",
                    "Updated summary grounded in the raw PDF.",
                )
                .replace("tags: [example]\n---", "tags: [example]\nquality_score: 0\n---")
            )
            stage = root / "stage"
            ingest_transaction._copy_transaction_inputs(root, stage)

            with self.assertRaisesRegex(
                ingest_transaction.ProposalError,
                "requires the deterministic current-raw hash",
            ):
                ingest_transaction._write_mutations(proposal, root, stage, raw)

            paths = ingest_transaction._write_mutations(
                proposal,
                root,
                stage,
                raw,
                expected_source_hash="a" * 64,
            )

            self.assertEqual(paths, ["wiki/sources/example.md"])
            frontmatter, body, error = ingest_transaction.parse_page_text(
                (stage / "wiki" / "sources" / "example.md").read_text()
            )
            self.assertIsNone(error)
            self.assertEqual(frontmatter["created"].isoformat(), "2026-08-01")
            self.assertEqual(frontmatter["source_hash"], "a" * 64)
            self.assertEqual(frontmatter["sources"], ["raw/prior.md", "raw/example.md"])
            self.assertEqual(frontmatter["concepts"], ["prior-concept"])
            self.assertEqual(frontmatter["related"], ["[[Prior Concept]]"])
            self.assertEqual(frontmatter["tags"], ["prior", "example"])
            self.assertEqual(frontmatter["tier"], "established")
            self.assertEqual(frontmatter["quality_score"], 91)
            self.assertIn("Updated summary grounded in the raw PDF.", body)
            self.assertNotIn("Existing summary.", body)

    def test_source_update_with_different_upstream_identity_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root, raw = self._root(tmp)
            raw.write_text(
                "---\ntitle: Example\ntype: url\nurl: https://arxiv.org/pdf/2608.22222\n"
                "status: pending\n---\nEvidence\n"
            )
            prior_raw = root / "raw" / "prior.md"
            prior_raw.write_text(
                "---\ntitle: Prior\ntype: url\nurl: https://arxiv.org/abs/2608.11111\n"
                "status: ingested\n---\nPrior evidence\n"
            )
            existing = root / "wiki" / "sources" / "example.md"
            existing.write_text(
                f"""---
title: Example
type: source
created: 2026-08-01
last_verified: 2026-08-01
source_hash: {'b' * 64}
sources: [raw/prior.md]
concepts: []
related: []
tier: established
tags: []
---
# Example

## Summary

Existing unrelated source.
"""
            )
            proposal = self._proposal()
            proposal["page_mutations"][0]["operation"] = "update"
            stage = root / "stage"
            ingest_transaction._copy_transaction_inputs(root, stage)

            with self.assertRaisesRegex(
                ingest_transaction.ProposalError,
                "different upstream identity",
            ):
                ingest_transaction._write_mutations(
                    proposal,
                    root,
                    stage,
                    raw,
                    expected_source_hash="a" * 64,
                )

    def test_source_reconciliation_cannot_add_unrelated_provenance(self) -> None:
        for operation in ("create", "update"):
            with self.subTest(operation=operation), tempfile.TemporaryDirectory() as tmp:
                root, raw = self._root(tmp)
                raw.write_text(
                    "---\ntitle: Current\ntype: url\nurl: https://arxiv.org/pdf/2608.11111\n"
                    "status: pending\n---\nEvidence\n"
                )
                (root / "raw" / "prior.md").write_text(
                    "---\ntitle: Prior\ntype: url\nurl: https://arxiv.org/abs/2608.11111\n"
                    "status: ingested\n---\nPrior evidence\n"
                )
                (root / "raw" / "unrelated.md").write_text(
                    "---\ntitle: Unrelated\ntype: url\nurl: https://arxiv.org/abs/2608.22222\n"
                    "status: ingested\n---\nUnrelated evidence\n"
                )
                existing = root / "wiki" / "sources" / "example.md"
                existing.write_text(
                    f"""---
title: Example
type: source
created: 2026-08-01
last_verified: 2026-08-01
source_hash: {'b' * 64}
sources: [raw/prior.md]
concepts: []
related: []
tier: established
tags: []
---
# Example

## Summary

Existing source.
"""
                )
                proposal = self._proposal()
                proposal["page_mutations"][0] = {
                    "path": "wiki/sources/example.md",
                    "operation": operation,
                    "content": f"""---
title: Example
type: source
created: 2026-08-02
last_verified: 2026-08-02
source_hash: {'a' * 64}
sources: [raw/prior.md, raw/example.md, raw/unrelated.md]
concepts: []
related: []
tier: hot
tags: []
---
# Example

## Summary

Proposed source.
""",
                }
                stage = root / "stage"
                ingest_transaction._copy_transaction_inputs(root, stage)

                with self.assertRaisesRegex(
                    ingest_transaction.ProposalError,
                    "unrelated provenance",
                ):
                    ingest_transaction._write_mutations(
                        proposal,
                        root,
                        stage,
                        raw,
                        expected_source_hash="a" * 64,
                    )

    def test_new_source_create_cannot_add_unrelated_provenance(self) -> None:
        for current_url in ("https://arxiv.org/pdf/2608.11111", None):
            with self.subTest(current_url=current_url), tempfile.TemporaryDirectory() as tmp:
                root, raw = self._root(tmp)
                url_line = f"url: {current_url}\n" if current_url else ""
                raw.write_text(
                    f"---\ntitle: Current\ntype: {'url' if current_url else 'text'}\n"
                    f"{url_line}status: pending\n---\nEvidence\n"
                )
                (root / "raw" / "unrelated.md").write_text(
                    "---\ntitle: Unrelated\ntype: url\nurl: https://arxiv.org/abs/2608.22222\n"
                    "status: ingested\n---\nUnrelated evidence\n"
                )
                proposal = self._proposal()
                proposal["page_mutations"][0]["content"] = proposal["page_mutations"][0][
                    "content"
                ].replace(
                    "sources:\n  - raw/example.md",
                    "sources:\n  - raw/example.md\n  - raw/unrelated.md",
                )
                stage = root / "stage"
                ingest_transaction._copy_transaction_inputs(root, stage)

                with self.assertRaisesRegex(
                    ingest_transaction.ProposalError,
                    "unrelated provenance",
                ):
                    ingest_transaction._write_mutations(
                        proposal,
                        root,
                        stage,
                        raw,
                        expected_source_hash="a" * 64,
                    )

    def test_concept_update_preserves_accumulated_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root, raw = self._root(tmp)
            existing = root / "wiki" / "concepts" / "example.md"
            existing.write_text(
                f"""---
title: Example Concept
type: concept
created: 2026-08-01
last_verified: 2026-08-01
source_hash: {'b' * 64}
sources: [raw/prior.md]
concepts: [prior-concept]
related: []
tier: established
tags: [prior]
quality_score: 91
---
# Example Concept

## Overview

Existing overview.
"""
            )
            (root / "raw" / "prior.md").write_text(
                "---\ntitle: Prior\ntype: text\nstatus: ingested\n---\nPrior evidence\n"
            )
            proposal = self._proposal()
            proposal["page_mutations"].append(
                {
                    "path": "wiki/concepts/example.md",
                    "operation": "update",
                    "content": f"""---
title: Example Concept
type: concept
created: 2026-08-02
last_verified: 2026-08-02
source_hash: {'a' * 64}
sources: [raw/example.md]
concepts: [new-concept]
related: []
tier: hot
tags: [new]
quality_score: 0
---
# Example Concept

## Overview

New overview.
""",
                }
            )
            stage = root / "stage"
            ingest_transaction._copy_transaction_inputs(root, stage)

            paths = ingest_transaction._write_mutations(
                proposal,
                root,
                stage,
                raw,
                expected_source_hash="a" * 64,
            )

            self.assertIn("wiki/concepts/example.md", paths)
            frontmatter, body, error = ingest_transaction.parse_page_text(
                (stage / "wiki" / "concepts" / "example.md").read_text()
            )
            self.assertIsNone(error)
            self.assertEqual(frontmatter["created"].isoformat(), "2026-08-01")
            self.assertEqual(frontmatter["tier"], "established")
            self.assertEqual(frontmatter["quality_score"], 91)
            self.assertEqual(frontmatter["sources"], ["raw/prior.md", "raw/example.md"])
            self.assertEqual(frontmatter["concepts"], ["prior-concept", "new-concept"])
            self.assertEqual(frontmatter["tags"], ["prior", "new"])
            self.assertIn("Existing overview.", body)
            self.assertIn("New overview.", body)

    def test_same_titled_source_create_cannot_borrow_prior_identity(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root, raw = self._root(tmp)
            raw.write_text(
                "---\ntitle: Example\ntype: url\nurl: https://arxiv.org/pdf/2608.22222\n"
                "status: pending\n---\nEvidence\n"
            )
            prior_raw = root / "raw" / "prior.md"
            prior_raw.write_text(
                "---\ntitle: Prior\ntype: url\nurl: https://arxiv.org/abs/2608.11111\n"
                "status: ingested\n---\nPrior evidence\n"
            )
            existing = root / "wiki" / "sources" / "example.md"
            existing.write_text(
                f"""---
title: Example
type: source
created: 2026-08-01
last_verified: 2026-08-01
source_hash: {'b' * 64}
sources: [raw/prior.md]
concepts: []
related: []
tier: hot
tags: []
---
# Example

## Summary

Unrelated source with the same title.
"""
            )
            proposal = self._proposal()
            proposal["page_mutations"][0]["content"] = proposal["page_mutations"][0][
                "content"
            ].replace(
                "sources:\n  - raw/example.md",
                "sources:\n  - raw/prior.md\n  - raw/example.md",
            )
            stage = root / "stage"
            ingest_transaction._copy_transaction_inputs(root, stage)

            with self.assertRaisesRegex(
                ingest_transaction.ProposalError,
                "upstream identity",
            ):
                ingest_transaction._write_mutations(
                    proposal,
                    root,
                    stage,
                    raw,
                    expected_source_hash="a" * 64,
                )

    def test_existing_concept_create_is_reconciled_after_racing_source_ingests(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root, raw = self._root(tmp)
            raw.write_text(
                "---\ntitle: Example\ntype: url\nurl: https://arxiv.org/pdf/2608.14071\n"
                "status: pending\n---\nEvidence\n"
            )
            prior_raw = root / "raw" / "prior.md"
            prior_raw.write_text(
                "---\ntitle: Prior\ntype: url\nurl: https://arxiv.org/abs/2608.14071\n"
                "status: ingested\n---\nPrior evidence\n"
            )
            existing = root / "wiki" / "concepts" / "example.md"
            existing.write_text(
                f"""---
title: Example Concept
type: concept
created: 2026-08-01
last_verified: 2026-08-01
source_hash: {'b' * 64}
sources: [raw/prior.md]
concepts: [prior-concept]
related: []
tier: established
tags: [prior]
---
# Example Concept

## Overview

Existing overview.
"""
            )
            proposal = self._proposal()
            proposal["page_mutations"].append(
                {
                    "path": "wiki/concepts/example.md",
                    "operation": "create",
                    "content": f"""---
title: Example Concept
type: concept
created: 2026-08-02
last_verified: 2026-08-02
source_hash: {'a' * 64}
sources: [raw/example.md]
concepts: [new-concept]
related: []
tier: hot
tags: [new]
---
# Example Concept

## Overview

Updated overview from the racing ingest.
""",
                }
            )
            stage = root / "stage"
            ingest_transaction._copy_transaction_inputs(root, stage)

            paths = ingest_transaction._write_mutations(
                proposal,
                root,
                stage,
                raw,
                expected_source_hash="a" * 64,
            )

            self.assertIn("wiki/concepts/example.md", paths)
            frontmatter, body, error = ingest_transaction.parse_page_text(
                (stage / "wiki" / "concepts" / "example.md").read_text()
            )
            self.assertIsNone(error)
            self.assertEqual(frontmatter["sources"], ["raw/prior.md", "raw/example.md"])
            self.assertEqual(frontmatter["concepts"], ["prior-concept", "new-concept"])
            self.assertEqual(frontmatter["created"].isoformat(), "2026-08-01")
            self.assertEqual(frontmatter["tier"], "established")
            self.assertIn("Existing overview.", body)
            self.assertIn("Updated overview from the racing ingest.", body)

    def test_existing_concept_create_with_different_upstream_identity_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root, raw = self._root(tmp)
            raw.write_text(
                "---\ntitle: Example\ntype: url\nurl: https://arxiv.org/pdf/2608.22222\n"
                "status: pending\n---\nEvidence\n"
            )
            prior_raw = root / "raw" / "prior.md"
            prior_raw.write_text(
                "---\ntitle: Prior\ntype: url\nurl: https://arxiv.org/abs/2608.11111\n"
                "status: ingested\n---\nPrior evidence\n"
            )
            existing = root / "wiki" / "concepts" / "example.md"
            existing.write_text(
                f"""---
title: Example Concept
type: concept
created: 2026-08-01
last_verified: 2026-08-01
source_hash: {'b' * 64}
sources: [raw/prior.md]
concepts: []
related: []
tier: established
tags: []
---
# Example Concept

## Overview

Existing overview from different evidence.
"""
            )
            proposal = self._proposal()
            proposal["page_mutations"].append(
                {
                    "path": "wiki/concepts/example.md",
                    "operation": "create",
                    "content": f"""---
title: Example Concept
type: concept
created: 2026-08-02
last_verified: 2026-08-02
source_hash: {'a' * 64}
sources: [raw/example.md]
concepts: []
related: []
tier: hot
tags: []
---
# Example Concept

## Overview

Conflicting replacement body.
""",
                }
            )
            stage = root / "stage"
            ingest_transaction._copy_transaction_inputs(root, stage)

            with self.assertRaisesRegex(
                ingest_transaction.ProposalError,
                "different upstream identity",
            ):
                ingest_transaction._write_mutations(
                    proposal,
                    root,
                    stage,
                    raw,
                    expected_source_hash="a" * 64,
                )

    def test_non_url_concept_create_cannot_copy_existing_hash(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root, raw = self._root(tmp)
            prior_raw = root / "raw" / "prior.md"
            prior_raw.write_text(
                "---\ntitle: Prior\ntype: text\nstatus: ingested\n---\nPrior evidence\n"
            )
            existing = root / "wiki" / "concepts" / "example.md"
            existing.write_text(
                f"""---
title: Example Concept
type: concept
created: 2026-08-01
last_verified: 2026-08-01
source_hash: {'b' * 64}
sources: [raw/prior.md]
concepts: []
related: []
tier: established
tags: []
---
# Example Concept

## Overview

Existing unrelated text-source concept.
"""
            )
            proposal = self._proposal()
            proposal["page_mutations"].append(
                {
                    "path": "wiki/concepts/example.md",
                    "operation": "create",
                    "content": f"""---
title: Example Concept
type: concept
created: 2026-08-02
last_verified: 2026-08-02
source_hash: {'b' * 64}
sources: [raw/example.md]
concepts: []
related: []
tier: hot
tags: []
---
# Example Concept

## Overview

Unrelated current text-source concept.
""",
                }
            )
            stage = root / "stage"
            ingest_transaction._copy_transaction_inputs(root, stage)

            with self.assertRaisesRegex(
                ingest_transaction.ProposalError,
                "requires the deterministic current-raw hash",
            ):
                ingest_transaction._write_mutations(proposal, root, stage, raw)

            with self.assertRaisesRegex(
                ingest_transaction.ProposalError,
                "deterministic current-raw hash",
            ):
                ingest_transaction._write_mutations(
                    proposal,
                    root,
                    stage,
                    raw,
                    expected_source_hash="a" * 64,
                )

    def test_existing_synthesis_create_remains_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root, raw = self._root(tmp)
            existing = root / "wiki" / "synthesis" / "example.md"
            existing.write_text("already exists\n")
            proposal = self._proposal()
            proposal["page_mutations"].append(
                {
                    "path": "wiki/synthesis/example.md",
                    "operation": "create",
                    "content": "not relevant because the operation must be rejected first",
                }
            )
            stage = root / "stage"
            ingest_transaction._copy_transaction_inputs(root, stage)

            with self.assertRaisesRegex(
                ingest_transaction.ProposalError,
                "create mutation targets an existing page: wiki/synthesis/example.md",
            ):
                ingest_transaction._write_mutations(proposal, root, stage, raw)

    def test_differently_titled_source_create_remains_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root, raw = self._root(tmp)
            existing = root / "wiki" / "sources" / "example.md"
            existing.write_text(
                f"""---
title: Unrelated Existing Source
type: source
created: 2026-08-01
last_verified: 2026-08-01
source_hash: {'b' * 64}
sources: [raw/example.md]
concepts: []
related: []
tier: hot
tags: []
---
# Unrelated Existing Source

## Summary

Different source.
"""
            )
            proposal = self._proposal()
            stage = root / "stage"
            ingest_transaction._copy_transaction_inputs(root, stage)

            with self.assertRaisesRegex(
                ingest_transaction.ProposalError,
                "conflicts with a differently titled existing page",
            ):
                ingest_transaction._write_mutations(proposal, root, stage, raw)

    def test_punctuation_significant_title_collision_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root, raw = self._root(tmp)
            raw.write_text(
                "---\ntitle: C\ntype: url\nurl: https://arxiv.org/pdf/2608.14071\n"
                "status: pending\n---\nEvidence\n"
            )
            prior_raw = root / "raw" / "prior.md"
            prior_raw.write_text(
                "---\ntitle: C++\ntype: url\nurl: https://arxiv.org/abs/2608.14071\n"
                "status: ingested\n---\nPrior evidence\n"
            )
            existing = root / "wiki" / "sources" / "example.md"
            existing.write_text(
                f"""---
title: C++
type: source
created: 2026-08-01
last_verified: 2026-08-01
source_hash: {'b' * 64}
sources: [raw/prior.md]
concepts: []
related: []
tier: hot
tags: []
---
# C++

## Summary

Existing C++ source.
"""
            )
            proposal = self._proposal()
            proposal["page_mutations"][0]["content"] = proposal["page_mutations"][0][
                "content"
            ].replace("title: Example", "title: C").replace("# Example", "# C")
            stage = root / "stage"
            ingest_transaction._copy_transaction_inputs(root, stage)

            with self.assertRaisesRegex(
                ingest_transaction.ProposalError,
                "conflicts with a differently titled existing page",
            ):
                ingest_transaction._write_mutations(
                    proposal,
                    root,
                    stage,
                    raw,
                    expected_source_hash="a" * 64,
                )

    def test_unsafe_mutation_path_is_rejected_before_candidate_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root, raw = self._root(tmp)
            proposal = self._proposal()
            proposal["source_path"] = "../outside.md"
            proposal["page_mutations"][0]["path"] = "../outside.md"

            with patch("ingest_transaction._digest_or_none") as digest:
                with self.assertRaisesRegex(ingest_transaction.ProposalError, "invalid canonical"):
                    ingest_transaction.prepare_and_publish(
                        proposal,
                        root,
                        raw,
                        backend="codex-cli",
                        validation_run=False,
                    )
            digest.assert_not_called()

    def test_graph_signature_mismatch_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            stage = Path(tmp) / "stage"
            (stage / "wiki" / "concepts").mkdir(parents=True)
            (stage / "wiki" / "concepts" / "example.md").write_text("# Example\n")
            runtime = Path(tmp) / "scripts"
            runtime.mkdir()
            builder = Path(tmp) / "wiki-graph-api" / "graph_builder.py"
            builder.parent.mkdir()
            builder.write_text("# test stub\n")

            def fake_run(*_args, **_kwargs):
                graph = stage / "wiki" / "graph" / "graph.json"
                graph.parent.mkdir(parents=True, exist_ok=True)
                graph.write_text(
                    json.dumps(
                        {
                            "source_signature": "0" * 64,
                            "node_count": 0,
                            "edge_count": 0,
                            "nodes": [],
                            "edges": [],
                        }
                    )
                )
                tracker = stage / "reports" / "checkpoint-graph-tracker.md"
                tracker.parent.mkdir(parents=True, exist_ok=True)
                tracker.write_text("# Tracker\n")

            with patch("ingest_transaction.subprocess.run", side_effect=fake_run) as run:
                with self.assertRaisesRegex(RuntimeError, "source_signature"):
                    ingest_transaction._build_graph(stage, runtime)
            self.assertEqual(Path(run.call_args.args[0][1]), builder)


if __name__ == "__main__":
    unittest.main()
