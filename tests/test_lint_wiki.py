from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

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


if __name__ == "__main__":
    unittest.main()