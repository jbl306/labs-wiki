import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import audit_synthesis  # noqa: E402
import migrate_synthesis_contract  # noqa: E402


class SynthesisMigrationTests(unittest.TestCase):
    def test_migration_is_idempotent_and_does_not_promote_unmapped_claims(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw = root / "raw" / "source.md"
            raw.parent.mkdir(parents=True)
            raw.write_text("---\ntitle: Raw\ntype: copilot-session\n---\nEvidence\n")
            concept = root / "wiki" / "concepts" / "grounded.md"
            concept.parent.mkdir(parents=True)
            concept.write_text(
                "---\ntitle: Grounded\ntype: concept\nsources: [raw/source.md]\n---\n# Grounded\n"
            )
            page = root / "wiki" / "synthesis" / "legacy.md"
            page.parent.mkdir(parents=True)
            page.write_text(
                """---
title: Legacy
type: synthesis
created: 2026-08-02
last_verified: 2026-08-02
source_hash: synthesis-generated
sources: [raw/source.md]
concepts: [grounded, other]
related: ["[[Grounded]]"]
tier: hot
tags: [legacy]
---
# Legacy
## Question
What follows?
## Summary
A summary long enough to describe the comparison and why it matters for this deterministic migration fixture.
## Comparison
| Dimension | [[Grounded]] | Other |
|---|---|---|
| Result | Known | Unknown |
## Analysis
Detailed analysis of the grounded comparison. Detailed analysis of the grounded comparison. Detailed analysis of the grounded comparison.
## Key Insights
1. **Grounded claim.** — described by [[Grounded]].
2. **Unsupported legacy claim.**
## Open Questions
- What remains unknown?
## Sources
- [[Grounded]]
"""
            )
            provenance, titles = migrate_synthesis_contract._page_provenance(root)

            changed = migrate_synthesis_contract.migrate_page(page, root, provenance, titles)
            first = page.read_text()
            changed_again = migrate_synthesis_contract.migrate_page(page, root, provenance, titles)

            self.assertTrue(changed)
            self.assertFalse(changed_again)
            self.assertEqual(page.read_text(), first)
            self.assertIn("evidence_scope: within-source", first)
            self.assertIn("evidence_origin_family_count: 1", first)
            self.assertIn("— supported by [[Grounded]]", first)
            self.assertIn("## Evidence Map", first)
            key_insights = audit_synthesis.section_body(
                audit_synthesis.parse_frontmatter_text(first)[1], "Key Insights"
            )
            self.assertNotIn("Unsupported legacy claim", key_insights)
            self.assertIn("## Legacy Claims Pending Evidence", first)
            self.assertIn("Unsupported legacy claim", first)


if __name__ == "__main__":
    unittest.main()
