import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import audit_synthesis  # noqa: E402  # pyright: ignore[reportMissingImports]


class SynthesisAuditTests(unittest.TestCase):
    def _write_raw(self, root: Path, name: str, source: str) -> str:
        relative = f"raw/{name}.md"
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"---\ntitle: {name}\nsource: {source}\n---\nEvidence.\n")
        return relative

    def _write_wiki_page(
        self, root: Path, title: str, slug: str, sources: list[str]
    ) -> None:
        path = root / "wiki" / "concepts" / f"{slug}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        source_lines = "\n".join(f"  - {source}" for source in sources)
        path.write_text(
            f"---\ntitle: \"{title}\"\ntype: concept\nsources:\n{source_lines}\n---\n# {title}\n"
        )

    def test_strict_cross_source_page_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_a = self._write_raw(root, "paper-a", "arxiv")
            source_b = self._write_raw(root, "incident-b", "homelab")
            self._write_wiki_page(root, "Concept A", "concept-a", [source_a])
            self._write_wiki_page(root, "Source A", "source-a", [source_a])
            self._write_wiki_page(root, "Concept B", "concept-b", [source_b])
            self._write_wiki_page(root, "Source B", "source-b", [source_b])
            page = root / "wiki" / "synthesis" / "choice.md"
            page.parent.mkdir(parents=True)
            page.write_text(
                f"""---
title: "Choosing Between A and B"
type: synthesis
sources: [{source_a}, {source_b}]
concepts: [concept-a, concept-b]
related: ["[[Concept A]]", "[[Concept B]]"]
evidence_scope: cross-source
evidence_source_count: 2
evidence_origin_family_count: 2
---
# Choosing Between A and B
## Question
When should each approach be used?
## Summary
Approach A favors predictable operation while Approach B favors flexibility. The evidence indicates that the choice depends on failure tolerance, observability, and maintenance constraints.
## Comparison
| Dimension | [[Concept A]] | [[Concept B]] |
|---|---|---|
| Reliability | Explicit gates | Adaptive fallback |
| Cost | Lower runtime cost | Higher runtime cost |
## Analysis
{"The evidence supports a conditional choice rather than a universal winner. " * 45}
## Key Insights
1. **Use A for predictable workloads.** — supported by [[Concept A]], [[Source A]]
2. **Use B when inputs drift.** — supported by [[Concept B]], [[Source B]]
3. **Observability is the deciding constraint.** — supported by [[Concept A]], [[Concept B]]
## Evidence Map
| Insight | Supporting pages | Raw provenance | Confidence / limits |
|---|---|---|---|
| Use A for predictable workloads. | [[Concept A]], [[Source A]] | `{source_a}` | High |
| Use B when inputs drift. | [[Concept B]], [[Source B]] | `{source_b}` | Medium |
| Observability is the deciding constraint. | [[Concept A]], [[Concept B]] | `{source_a}`, `{source_b}` | Medium |
## Open Questions
- How does the choice change at larger scale?
## Sources
- [[Source A]]
- [[Source B]]
"""
            )

            result = audit_synthesis.audit_page(page, root, strict=True)

            self.assertTrue(result.passed, result.to_dict())
            self.assertGreaterEqual(result.score, 80)
            self.assertEqual(result.evidence_scope, "cross-source")

    def test_strict_cross_source_page_requires_independent_origin_families(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_a = self._write_raw(root, "checkpoint-a", "copilot-session")
            source_b = self._write_raw(root, "checkpoint-b", "copilot-session")
            self._write_wiki_page(root, "A", "a", [source_a])
            self._write_wiki_page(root, "B", "b", [source_b])
            page = root / "wiki" / "synthesis" / "same-family.md"
            page.parent.mkdir(parents=True)
            page.write_text(
                f"""---
title: Same Family Comparison
type: synthesis
sources: [{source_a}, {source_b}]
concepts: [a, b]
related: ["[[A]]", "[[B]]"]
evidence_scope: cross-source
evidence_source_count: 2
evidence_origin_family_count: 1
---
## Question
What can these checkpoints establish?
## Summary
This comparison is deliberately well structured, but both raw files originate from the same agent-session family and therefore are not independent evidence.
## Comparison
| Dimension | [[A]] | [[B]] |
|---|---|---|
| Evidence | First checkpoint | Second checkpoint |
## Analysis
{"Detailed analysis of the comparison and its source-independence limits. " * 45}
## Key Insights
1. **The checkpoints describe related behavior.** — supported by [[A]], [[B]]
## Evidence Map
| Insight | Supporting pages | Raw provenance | Confidence / limits |
|---|---|---|---|
| The checkpoints describe related behavior. | [[A]], [[B]] | `{source_a}`, `{source_b}` | Same origin family |
## Open Questions
- What does an independent source report?
## Sources
- [[A]]
- [[B]]
"""
            )

            result = audit_synthesis.audit_page(page, root, strict=True)

            self.assertFalse(result.passed)
            self.assertIn(
                "cross-source-not-independent",
                {finding.code for finding in result.findings},
            )

    def test_weak_mechanism_shaped_page_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = self._write_raw(root, "checkpoint", "copilot-session")
            page = root / "wiki" / "synthesis" / "weak.md"
            page.parent.mkdir(parents=True)
            page.write_text(
                f"""---
title: "Recurring checkpoint patterns: everything"
type: synthesis
sources: [{source}]
concepts: [one]
related: ["[[One]]"]
---
# Weak
## Summary
Short summary.
## Key Insights
1. Unsupported claim.
"""
            )

            result = audit_synthesis.audit_page(page, root, strict=True)

            self.assertFalse(result.passed)
            codes = {finding.code for finding in result.findings}
            self.assertIn("missing-evidence-map", codes)
            self.assertIn("mechanism-shaped-title", codes)
            self.assertIn("ungrounded-insights", codes)

    def test_strict_page_rejects_out_of_tree_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            root = base / "repo"
            root.mkdir()
            outside = base / "outside-evidence.md"
            outside.write_text("outside")
            page = root / "wiki" / "synthesis" / "outside.md"
            page.parent.mkdir(parents=True)
            page.write_text(
                f"""---
title: Outside Evidence
type: synthesis
sources: [{outside}]
concepts: [a, b]
related: ["[[A]]", "[[B]]"]
evidence_scope: within-source
evidence_source_count: 1
evidence_origin_family_count: 0
---
## Question
What should be chosen?
## Summary
This summary contains enough words to satisfy the editorial shape while deliberately using invalid provenance outside the repository raw directory.
## Comparison
| Dimension | [[A]] | [[B]] |
|---|---|---|
| Fit | A | B |
## Analysis
{"Detailed analysis of the choice and its operational constraints. " * 45}
## Key Insights
1. **Choose A for stable inputs.** — supported by [[A]]
## Evidence Map
| Insight | Supporting pages | Raw provenance | Confidence / limits |
|---|---|---|---|
| Choose A for stable inputs. | [[A]] | `{outside}` | High |
## Open Questions
- What changes later?
## Sources
- [[A]]
"""
            )

            result = audit_synthesis.audit_page(page, root, strict=True)

            self.assertFalse(result.passed)
            self.assertIn("invalid-provenance-path", {finding.code for finding in result.findings})

    def test_strict_page_requires_one_valid_evidence_row_per_insight(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_a = self._write_raw(root, "a", "arxiv")
            source_b = self._write_raw(root, "b", "homelab")
            self._write_wiki_page(root, "A", "a", [source_a])
            self._write_wiki_page(root, "B", "b", [source_b])
            page = root / "wiki" / "synthesis" / "incomplete-map.md"
            page.parent.mkdir(parents=True)
            page.write_text(
                f"""---
title: Incomplete Evidence Map
type: synthesis
sources: [{source_a}, {source_b}]
concepts: [a, b]
related: ["[[A]]", "[[B]]"]
evidence_scope: cross-source
evidence_source_count: 2
evidence_origin_family_count: 2
---
## Question
What should be chosen?
## Summary
This summary contains enough words to satisfy the editorial shape while deliberately omitting one claim-level Evidence Map row from the synthesis.
## Comparison
| Dimension | [[A]] | [[B]] |
|---|---|---|
| Fit | A | B |
## Analysis
{"Detailed analysis of the choice and its operational constraints. " * 45}
## Key Insights
1. **Choose A for stable inputs.** — supported by [[A]]
2. **Choose B for changing inputs.** — supported by [[B]]
## Evidence Map
| Insight | Supporting pages | Raw provenance | Confidence / limits |
|---|---|---|---|
| Choose A for stable inputs. | [[A]] | `{source_a}` | High |
## Open Questions
- What changes later?
## Sources
- [[A]]
"""
            )

            result = audit_synthesis.audit_page(page, root, strict=True)

            self.assertFalse(result.passed)
            self.assertIn("evidence-map-coverage", {finding.code for finding in result.findings})

    def test_strict_page_rejects_invented_pages_and_swapped_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_a = self._write_raw(root, "a", "arxiv")
            source_b = self._write_raw(root, "b", "homelab")
            self._write_wiki_page(root, "A", "a", [source_a])
            self._write_wiki_page(root, "B", "b", [source_b])
            page = root / "wiki" / "synthesis" / "fabricated-map.md"
            page.parent.mkdir(parents=True, exist_ok=True)
            page.write_text(
                f"""---
title: Fabricated Evidence Map
type: synthesis
sources: [{source_a}, {source_b}]
concepts: [a, b]
related: ["[[A]]", "[[B]]"]
evidence_scope: cross-source
evidence_source_count: 2
evidence_origin_family_count: 2
---
## Question
What should be chosen?
## Summary
This summary has enough editorial context to isolate the fabricated claim-level support mapping from unrelated structural audit failures.
## Comparison
| Dimension | [[A]] | [[B]] |
|---|---|---|
| Fit | A | B |
## Analysis
{"Detailed analysis of the choice, trade-offs, limits, and operational constraints. " * 45}
## Key Insights
1. **Choose A for stable inputs.** — supported by [[A]]
2. **Choose B for changing inputs.** — supported by [[B]]
## Evidence Map
| Insight | Supporting pages | Raw provenance | Confidence / limits |
|---|---|---|---|
| Choose A for stable inputs. | [[Invented A]] | `{source_b}` | High |
| Choose B for changing inputs. | [[B]] | `{source_a}` | High |
## Open Questions
- What changes later?
## Sources
- [[A]]
- [[B]]
"""
            )

            result = audit_synthesis.audit_page(page, root, strict=True)

            self.assertFalse(result.passed)
            self.assertIn(
                "invalid-evidence-map-provenance",
                {finding.code for finding in result.findings},
            )


if __name__ == "__main__":
    unittest.main()