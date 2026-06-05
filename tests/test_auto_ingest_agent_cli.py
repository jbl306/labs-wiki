import os
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import auto_ingest  # noqa: E402


class AgentCliBackendTests(unittest.TestCase):
    def test_codex_backend_is_default_and_tokenless(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(auto_ingest._selected_backend(), "codex-cli")
        self.assertFalse(auto_ingest._backend_requires_token("codex-cli"))
        self.assertTrue(auto_ingest._backend_requires_token("copilot-cli"))
        self.assertTrue(auto_ingest._backend_requires_token("github-models"))

    def test_pdf_file_body_routes_to_high_effort(self) -> None:
        body = """
See uploaded file:
raw/assets/paper.pdf
Original filename: paper.pdf
"""
        self.assertEqual(
            auto_ingest._compute_effort_for_raw({"type": "file", "source": "manual"}, body),
            "high",
        )

    def test_non_pdf_file_body_uses_medium_effort(self) -> None:
        body = """
See uploaded file:
raw/assets/notes.docx
Original filename: notes.docx
"""
        self.assertEqual(
            auto_ingest._compute_effort_for_raw({"type": "file", "source": "manual"}, body),
            "medium",
        )

    def test_codex_cli_invocation_uses_global_approval_flag_before_exec(self) -> None:
        completed = subprocess.CompletedProcess(
            args=[],
            returncode=0,
            stdout='progress\n{"status":"success","notes":"ok"}\n',
            stderr="",
        )
        with patch("auto_ingest.subprocess.run", return_value=completed) as run:
            result = auto_ingest.call_codex_cli_ingest(
                raw_path=ROOT / "raw" / "example.md",
                project_root=ROOT,
                model="gpt-5.5",
                effort="medium",
            )

        self.assertEqual(result["status"], "success")
        cmd = run.call_args.args[0]
        self.assertEqual(cmd[:4], ["codex", "-a", "never", "exec"])
        self.assertIn("--output-last-message", cmd)
        self.assertNotIn("-a", cmd[4:])


if __name__ == "__main__":
    unittest.main()
