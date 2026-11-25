from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compile_index import compile_index
import lint_wiki  # noqa: E402  # pyright: ignore[reportMissingImports]


class WikiLinkParsingTests(unittest.TestCase):
    def test_fenced_toml_array_header_is_not_a_wikilink(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            page = Path(tmp) / "example.md"
            page.write_text(
                "See [[Actual Page]].\n\n"
                "```toml\n[[tool.mypy.overrides]]\nmodule = ['example']\n```\n"
            )

            self.assertEqual(lint_wiki.find_wikilinks(page), ["Actual Page"])

    def test_recursive_index_and_contained_raw_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw = root / "raw"
            raw.mkdir()
            (raw / "real.md").write_text("raw source")
            (root / "outside.md").write_text("outside")
            (raw / "alias.md").symlink_to(root / "outside.md")
            page = root / "wiki" / "sources" / "_archive" / "example.md"
            page.parent.mkdir(parents=True)
            header = "---\ntype: source\ntitle: Example\ncreated: 2026-01-01\nsources: "
            page.write_text(header + "[raw/real.md]\n---\n# Example\n")
            index = root / "wiki" / "index.md"
            index.write_text(compile_index(str(root)))
            errors, warnings, _ = lint_wiki.lint_wiki(str(root))
            self.assertFalse(errors)
            self.assertIn("- [[Example]]", index.read_text())
            self.assertFalse(any("orphan" in item for item in warnings))
            index.write_text("- [[Example Expanded]]\n")
            page.write_text(header + "[raw/missing.md, raw/../outside.md, raw/alias.md]\n---\n# Example\n")
            errors, warnings, _ = lint_wiki.lint_wiki(str(root))
            self.assertEqual(len(errors), 3)
            self.assertTrue(any("does not exist" in err and "missing.md" in err for err in errors))
            self.assertTrue(any("contained" in err and "outside.md" in err for err in errors))
            self.assertTrue(any("contained" in err and "alias.md" in err for err in errors))
            self.assertTrue(any("orphan" in item for item in warnings))


if __name__ == "__main__":
    unittest.main()