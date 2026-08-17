import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import wiki_schema  # noqa: E402


class WikiSchemaTests(unittest.TestCase):
    def _raw(self, root: Path, name: str = "source") -> str:
        rel = f"raw/{name}.md"
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("---\ntitle: Source\ntype: text\nstatus: pending\n---\nEvidence\n")
        return rel

    def test_complete_concept_page_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw = self._raw(root)
            page = root / "wiki" / "concepts" / "example.md"
            page.parent.mkdir(parents=True)
            page.write_text(
                f"""---
title: Example Concept
type: concept
created: 2026-08-02
last_verified: 2026-08-02
source_hash: {'a' * 64}
sources:
  - {raw}
concepts: [example]
related: []
tier: hot
tags: [example]
---
# Example Concept

## Overview

Grounded overview.
"""
            )

            self.assertEqual(wiki_schema.validate_page(page, root), [])

    def test_missing_or_wrong_typed_fields_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw = self._raw(root)
            page = root / "wiki" / "entities" / "broken.md"
            page.parent.mkdir(parents=True)
            page.write_text(
                f"""---
title: Broken
type: entity
created: yesterday
sources: {raw}
concepts: not-a-list
related: []
tags: []
---
# Broken
"""
            )

            errors = wiki_schema.validate_page(page, root)

            self.assertTrue(any("last_verified" in error for error in errors))
            self.assertTrue(any("source_hash" in error for error in errors))
            self.assertTrue(any("created" in error for error in errors))
            self.assertTrue(any("sources" in error for error in errors))
            self.assertTrue(any("concepts" in error for error in errors))
            self.assertTrue(any("tier" in error for error in errors))

    def test_provenance_must_resolve_under_raw(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            outside = root.parent / "outside.md"
            outside.write_text("outside")
            page = root / "wiki" / "sources" / "outside.md"
            page.parent.mkdir(parents=True)
            page.write_text(
                f"""---
title: Outside
type: source
created: 2026-08-02
last_verified: 2026-08-02
source_hash: {'b' * 64}
sources: [{outside}]
concepts: []
related: []
tier: hot
tags: []
---
# Outside
"""
            )

            errors = wiki_schema.validate_page(page, root)

            self.assertTrue(any("raw/*.md" in error for error in errors))

    def test_page_type_requires_its_primary_body_section(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw = self._raw(root)
            page = root / "wiki" / "sources" / "missing-summary.md"
            page.parent.mkdir(parents=True)
            page.write_text(
                f"""---
title: Missing Summary
type: source
created: 2026-08-02
last_verified: 2026-08-02
source_hash: sha256:{'c' * 64}
sources: [{raw}]
concepts: []
related: []
tier: hot
tags: []
---
# Missing Summary

Body without the required primary section.
"""
            )

            errors = wiki_schema.validate_page(page, root)

            self.assertTrue(any("## Summary" in error for error in errors))
            self.assertTrue(any("source_hash" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
