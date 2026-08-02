import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import auto_ingest  # noqa: E402


class AgentCliBackendTests(unittest.TestCase):
    def test_codex_backend_is_default_and_tokenless(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(auto_ingest._selected_backend(), "codex-cli")
            self.assertFalse(auto_ingest._backend_requires_token("codex-cli"))
            self.assertEqual(auto_ingest.DEFAULT_CODEX_MODEL, "gpt-5.6-luna")
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

    def test_light_agent_route_uses_low_effort(self) -> None:
        route = auto_ingest.IngestRoute(
            lane="light",
            model="gpt-5.6-luna",
            priority=30,
            max_source_chars=18000,
            source_class="copilot-session-checkpoint",
            checkpoint_class="project-progress",
            retention_mode="compress",
        )
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(auto_ingest._compute_agent_effort({}, "body", route), "low")

    def test_codex_cli_invocation_uses_global_approval_flag_before_exec(self) -> None:
        completed = subprocess.CompletedProcess(
            args=[],
            returncode=0,
            stdout=(
                'progress\n{"status":"success","source_path":"wiki/sources/example.md",'
                '"entities_created":[],"concepts_created":[],"synthesis_created":[],'
                '"pages_updated":[],"duplicates_avoided":[],"kg_facts_added":0,'
                '"notes":"ok"}\n'
            ),
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
        self.assertIn("--ephemeral", cmd)
        self.assertIn("--ignore-user-config", cmd)
        self.assertIn("--output-schema", cmd)
        self.assertIn("--output-last-message", cmd)
        self.assertEqual(cmd[cmd.index("-s") + 1], "workspace-write")
        self.assertNotIn("-a", cmd[4:])

    def test_codex_sandbox_allows_container_outer_boundary_override(self) -> None:
        with patch.dict(os.environ, {"WIKI_CODEX_SANDBOX": "danger-full-access"}):
            self.assertEqual(auto_ingest._codex_sandbox_mode(), "danger-full-access")
        with patch.dict(os.environ, {"WIKI_CODEX_SANDBOX": "invalid"}):
            with self.assertRaises(ValueError):
                auto_ingest._codex_sandbox_mode()

    def test_missing_status_json_is_a_failure(self) -> None:
        result = auto_ingest._parse_agent_status_output(
            "finished without a status object",
            "Codex CLI",
            ROOT / "raw" / "example.md",
        )
        self.assertEqual(result["status"], "failed")

    def test_status_parser_prefers_outer_result_over_nested_duplicate(self) -> None:
        output = json.dumps(
            {
                "status": "success",
                "source_path": "wiki/sources/example.md",
                "entities_created": [],
                "concepts_created": [],
                "synthesis_created": [],
                "pages_updated": [],
                "duplicates_avoided": [
                    {"candidate": "Example", "linked_to": "Existing Example"}
                ],
                "kg_facts_added": 0,
                "notes": "ok",
            }
        )

        result = auto_ingest._extract_last_json_object(output)

        self.assertIsNotNone(result)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["duplicates_avoided"][0]["candidate"], "Example")

    def test_agent_prompt_carries_deterministic_checkpoint_policy(self) -> None:
        prompt = auto_ingest._build_agent_ingest_prompt(
            raw_path=ROOT / "raw" / "example.md",
            project_root=ROOT,
            model="gpt-5.6-luna",
            backend="codex-cli",
            checkpoint_class="project-progress",
            retention_mode="compress",
            planning_only=True,
        )

        self.assertIn("CHECKPOINT_CLASS**: `project-progress`", prompt)
        self.assertIn("RETENTION_MODE**: `compress`", prompt)
        self.assertIn("PLANNING_ONLY**: `true`", prompt)
        self.assertIn("create or update only the source", prompt)

    def test_agent_result_requires_existing_source_page(self) -> None:
        with self.subTest("missing source_path"):
            result = auto_ingest._validate_agent_ingest_result(
                {"status": "success", "source_path": ""},
                ROOT / "raw" / "example.md",
                ROOT,
            )
            self.assertEqual(result["status"], "failed")
            self.assertTrue(result["validation_errors"])

    def test_agent_result_accepts_existing_source_with_raw_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_path = root / "raw" / "example.md"
            source_path = root / "wiki" / "sources" / "example.md"
            raw_path.parent.mkdir(parents=True)
            source_path.parent.mkdir(parents=True)
            raw_path.write_text("---\nstatus: pending\n---\nsource")
            source_path.write_text(
                "---\ntitle: Example\ntype: source\ncreated: 2026-08-02\n"
                "sources:\n  - raw/example.md\n---\n\n# Example\n"
            )

            result = auto_ingest._validate_agent_ingest_result(
                {
                    "status": "success",
                    "source_path": "wiki/sources/example.md",
                    "entities_created": [],
                    "concepts_created": [],
                    "synthesis_created": [],
                    "pages_updated": [],
                    "duplicates_avoided": [],
                    "kg_facts_added": 0,
                    "notes": "ok",
                },
                raw_path,
                root,
            )

            self.assertEqual(result["status"], "success")
            self.assertNotIn("validation_errors", result)

    def test_agent_result_requires_complete_schema_and_rejects_unknown_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_path = root / "raw" / "example.md"
            source_path = root / "wiki" / "sources" / "example.md"
            raw_path.parent.mkdir(parents=True)
            source_path.parent.mkdir(parents=True)
            raw_path.write_text("---\nstatus: pending\n---\nsource")
            source_path.write_text(
                "---\ntitle: Example\ntype: source\nsources:\n  - raw/example.md\n---\n# Example\n"
            )

            missing = auto_ingest._validate_agent_ingest_result(
                {"status": "success", "source_path": "wiki/sources/example.md"},
                raw_path,
                root,
            )
            unknown = auto_ingest._validate_agent_ingest_result(
                {
                    "status": "success",
                    "source_path": "wiki/sources/example.md",
                    "entities_created": [],
                    "concepts_created": [],
                    "synthesis_created": [],
                    "pages_updated": [],
                    "duplicates_avoided": [],
                    "kg_facts_added": 0,
                    "notes": "ok",
                    "unexpected": True,
                },
                raw_path,
                root,
            )

            self.assertEqual(missing["status"], "failed")
            self.assertTrue(any("schema" in error for error in missing["validation_errors"]))
            self.assertEqual(unknown["status"], "failed")
            self.assertTrue(any("schema" in error for error in unknown["validation_errors"]))

    def test_checkout_manifest_rejects_unreported_agent_writes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "wiki" / "sources" / "example.md"
            script = root / "scripts" / "unexpected.py"
            source.parent.mkdir(parents=True)
            script.parent.mkdir(parents=True)
            source.write_text("before")
            script.write_text("before")
            before = auto_ingest._snapshot_agent_write_scope(root)

            source.write_text("declared update")
            script.write_text("unexpected update")
            after = auto_ingest._snapshot_agent_write_scope(root)
            unexpected = auto_ingest._unexpected_agent_changes(
                before,
                after,
                {
                    "source_path": str(source),
                    "entities_created": [],
                    "concepts_created": [],
                    "synthesis_created": [],
                    "pages_updated": [],
                },
                root,
            )

            self.assertEqual(unexpected, ["scripts/unexpected.py"])

    def test_validation_run_skips_log_notification_and_commit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_path = root / "raw" / "example.md"
            source_path = root / "wiki" / "sources" / "example.md"
            raw_path.parent.mkdir(parents=True)
            source_path.parent.mkdir(parents=True)
            raw_path.write_text(
                "---\ntitle: Example\ntype: text\nsource: test\nstatus: pending\n---\nUseful source body"
            )
            source_path.write_text(
                "---\ntitle: Example\ntype: source\ncreated: 2026-08-02\n"
                "sources:\n  - raw/example.md\n---\n\n# Example\n"
            )
            status = {
                "status": "success",
                "source_path": "wiki/sources/example.md",
                "entities_created": [],
                "concepts_created": [],
                "synthesis_created": [],
                "pages_updated": [],
                "duplicates_avoided": [],
                "kg_facts_added": 0,
                "notes": "ok",
            }

            with (
                patch("auto_ingest._selected_backend", return_value="codex-cli"),
                patch("auto_ingest.call_codex_cli_ingest", return_value=status),
                patch("auto_ingest.append_log") as append_log,
                patch("auto_ingest.send_ntfy") as send_ntfy,
                patch("auto_ingest.rebuild_index"),
                patch("auto_ingest.replay_pending_kg_facts"),
                patch("auto_ingest.commit_wiki_changes") as commit,
            ):
                success = auto_ingest.ingest_raw_source(
                    raw_path,
                    root,
                    token="",
                    validation_run=True,
                )

            self.assertTrue(success)
            append_log.assert_not_called()
            send_ntfy.assert_not_called()
            commit.assert_not_called()
            self.assertIn("status: ingested", raw_path.read_text())

    def test_commit_stages_only_manifest_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            page = root / "wiki" / "sources" / "example.md"
            raw = root / "raw" / "example.md"
            page.parent.mkdir(parents=True)
            raw.parent.mkdir(parents=True)
            page.write_text("page")
            raw.write_text("raw")
            completed = subprocess.CompletedProcess(args=[], returncode=0)
            with patch(
                "auto_ingest.subprocess.run",
                side_effect=[completed, completed, completed],
            ) as run:
                committed = auto_ingest.commit_wiki_changes(
                    root,
                    title="Example",
                    notes="ok",
                    paths=[
                        "wiki/sources/example.md",
                        "raw/example.md",
                        "../outside.md",
                    ],
                )

            self.assertFalse(committed)
            add_command = run.call_args_list[1].args[0]
            self.assertEqual(
                add_command[-3:],
                ["--", "wiki/sources/example.md", "raw/example.md"],
            )
            self.assertNotIn("wiki/", add_command)

    def test_commit_excludes_unrelated_pre_staged_changes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            subprocess.run(["git", "-C", str(root), "config", "user.name", "Test"], check=True)
            subprocess.run(["git", "-C", str(root), "config", "user.email", "test@example.invalid"], check=True)
            page = root / "wiki" / "sources" / "example.md"
            raw = root / "raw" / "example.md"
            unrelated = root / "unrelated.txt"
            page.parent.mkdir(parents=True)
            raw.parent.mkdir(parents=True)
            page.write_text("baseline page")
            raw.write_text("baseline raw")
            unrelated.write_text("baseline unrelated")
            subprocess.run(["git", "-C", str(root), "add", "."], check=True)
            subprocess.run(["git", "-C", str(root), "commit", "-qm", "baseline"], check=True)

            unrelated.write_text("staged unrelated")
            subprocess.run(["git", "-C", str(root), "add", "unrelated.txt"], check=True)
            page.write_text("manifest page")
            raw.write_text("manifest raw")

            committed = auto_ingest.commit_wiki_changes(
                root,
                title="Example",
                notes="ok",
                paths=["wiki/sources/example.md", "raw/example.md"],
            )

            self.assertTrue(committed)
            committed_paths = subprocess.check_output(
                ["git", "-C", str(root), "show", "--pretty=format:", "--name-only", "HEAD"],
                text=True,
            ).split()
            self.assertEqual(set(committed_paths), {"wiki/sources/example.md", "raw/example.md"})
            staged_paths = subprocess.check_output(
                ["git", "-C", str(root), "diff", "--cached", "--name-only"],
                text=True,
            ).split()
            self.assertEqual(staged_paths, ["unrelated.txt"])

    def test_index_failure_does_not_finalize_agent_success(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_path = root / "raw" / "example.md"
            source_path = root / "wiki" / "sources" / "example.md"
            raw_path.parent.mkdir(parents=True)
            source_path.parent.mkdir(parents=True)
            raw_path.write_text(
                "---\ntitle: Example\ntype: text\nsource: test\nstatus: pending\n---\nUseful source body"
            )
            source_path.write_text(
                "---\ntitle: Example\ntype: source\nsources:\n  - raw/example.md\n---\n# Example\n"
            )
            status = {
                "status": "success",
                "source_path": "wiki/sources/example.md",
                "entities_created": [],
                "concepts_created": [],
                "synthesis_created": [],
                "pages_updated": [],
                "duplicates_avoided": [],
                "kg_facts_added": 0,
                "notes": "ok",
            }
            with (
                patch("auto_ingest._selected_backend", return_value="codex-cli"),
                patch("auto_ingest.call_codex_cli_ingest", return_value=status),
                patch("auto_ingest.rebuild_index", side_effect=RuntimeError("index failed")),
                patch("auto_ingest.append_log") as append_log,
                patch("auto_ingest.send_ntfy") as send_ntfy,
                patch("auto_ingest.commit_wiki_changes") as commit,
            ):
                success = auto_ingest.ingest_raw_source(raw_path, root, token="")

            self.assertFalse(success)
            self.assertIn("status: pending", raw_path.read_text())
            append_log.assert_not_called()
            send_ntfy.assert_not_called()
            commit.assert_not_called()

    def test_synthesis_generator_emits_evidence_contract(self) -> None:
        synthesis = {
            "title": "Choosing A or B",
            "question": "When should A or B be selected?",
            "summary": (
                "A is appropriate for stable conditions, while B is appropriate for changing "
                "conditions. The choice depends on observability, cost, and failure tolerance."
            ),
            "comparison": [
                {
                    "dimension": "Reliability",
                    "entries": [
                        {"concept": "Concept A", "description": "Explicit gates"},
                        {"concept": "Concept B", "description": "Adaptive fallback"},
                    ],
                }
            ],
            "analysis": "Evidence supports a conditional choice. " * 60,
            "key_insights": [
                {"insight": "Insight 1", "supporting_pages": ["Concept A"]},
                {"insight": "Insight 2", "supporting_pages": ["Concept B"]},
                {"insight": "Insight 3", "supporting_pages": ["Concept A", "Concept B"]},
            ],
            "open_questions": ["How does scale change the decision?"],
            "tags": ["decision"],
        }

        _filename, content = auto_ingest.generate_synthesis_page(
            synthesis,
            ["raw/a.md", "raw/b.md"],
            ["Source A", "Source B"],
            "2026-08-02",
            source_provenance={
                "Concept A": ["raw/a.md"],
                "Concept B": ["raw/b.md"],
            },
        )

        self.assertIn("evidence_scope: cross-source", content)
        self.assertIn("evidence_source_count: 2", content)
        self.assertIn("## Evidence Map", content)
        insight_one = next(line for line in content.splitlines() if line.startswith("| Insight 1 |"))
        insight_two = next(line for line in content.splitlines() if line.startswith("| Insight 2 |"))
        self.assertIn("`raw/a.md`", insight_one)
        self.assertNotIn("`raw/b.md`", insight_one)
        self.assertIn("`raw/b.md`", insight_two)
        self.assertNotIn("`raw/a.md`", insight_two)


if __name__ == "__main__":
    unittest.main()
