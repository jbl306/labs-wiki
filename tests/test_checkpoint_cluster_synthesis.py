import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import backfill_checkpoint_cluster_synthesis as backfill  # noqa: E402


class CheckpointClusterSynthesisTests(unittest.TestCase):
    def test_community_id_alone_does_not_match_existing_synthesis(self) -> None:
        page = {
            "path": Path("wiki/synthesis/old.md"),
            "community": 7,
            "signature": "different",
            "sources": ["raw/old.md"],
        }

        match = backfill.find_existing_cluster_synthesis(
            [page],
            community=7,
            raw_paths=["raw/new.md"],
        )

        self.assertIsNone(match)

    def test_cluster_signature_is_order_independent_and_versioned(self) -> None:
        first = backfill.build_cluster_signature(["raw/b.md", "raw/a.md"])
        second = backfill.build_cluster_signature(["raw/a.md", "raw/b.md"])
        legacy_unversioned = __import__("hashlib").sha256(
            "raw/a.md\nraw/b.md".encode()
        ).hexdigest()[:16]

        self.assertEqual(first, second)
        self.assertNotEqual(first, legacy_unversioned)

    def test_generated_title_truncates_at_word_boundary(self) -> None:
        title = backfill.build_synthesis_title(
            3,
            [
                "Caddy handle_path Directive and Its Impact on Upstream URL Construction",
                "Docker Container Resource Auditing and Optimization",
            ],
        )

        self.assertLessEqual(len(title), 100)
        self.assertFalse(title.endswith("Resourc"))
        self.assertNotIn("Recurring checkpoint patterns", title)

    def test_compare_packet_tracks_only_supplied_page_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            wiki = Path(tmp) / "wiki"
            concepts = wiki / "concepts"
            concepts.mkdir(parents=True)
            (concepts / "alpha.md").write_text(
                "---\ntitle: Alpha\ntype: concept\nsources:\n  - raw/a.md\n---\nAlpha body"
            )
            (concepts / "beta.md").write_text(
                "---\ntitle: Beta\ntype: concept\nsources:\n  - raw/b.md\n---\nBeta body"
            )

            pages, labels, evidence, provenance = backfill.resolve_compare_pages(
                wiki,
                Counter({"alpha": 3, "beta": 2}),
                {"Unselected checkpoint": ("body", ["raw/not-supplied.md"])},
            )

            self.assertEqual(labels, ["Alpha", "Beta"])
            self.assertEqual(set(pages), {"Alpha", "Beta"})
            self.assertEqual(evidence, ["raw/a.md", "raw/b.md"])
            self.assertEqual(provenance, {"Alpha": ["raw/a.md"], "Beta": ["raw/b.md"]})
            self.assertNotIn("raw/not-supplied.md", evidence)

    def test_strict_gate_rejects_weak_generated_page(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw = root / "raw" / "a.md"
            page = root / "wiki" / "synthesis" / "weak.md"
            raw.parent.mkdir(parents=True)
            page.parent.mkdir(parents=True)
            raw.write_text("---\nsource: test\n---\nevidence")
            page.write_text(
                "---\ntitle: Weak\ntype: synthesis\nsources: [raw/a.md]\n"
                "concepts: [a]\nrelated: ['[[A]]']\nevidence_scope: within-source\n"
                "evidence_source_count: 1\n---\n## Summary\nToo short.\n"
            )

            passed, reason = backfill.strict_synthesis_gate(page, root)

            self.assertFalse(passed)
            self.assertIn("strict audit failed", reason)


if __name__ == "__main__":
    unittest.main()
