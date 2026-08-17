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
import watch_raw  # noqa: E402


class AgentCliBackendTests(unittest.TestCase):
    def test_agent_failure_sends_ntfy_with_actionable_details(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_path = root / "raw" / "example.md"
            raw_path.parent.mkdir(parents=True)
            raw_path.write_text(
                "---\ntitle: Example\ntype: text\nstatus: pending\n---\nUseful source body"
            )
            failure = auto_ingest._failed_agent_proposal(
                "codex exec exited with code 1: 401 Unauthorized"
            )

            with (
                patch("auto_ingest._selected_backend", return_value="codex-cli"),
                patch("auto_ingest.call_codex_cli_ingest", return_value=failure),
                patch("auto_ingest.send_ntfy") as send_ntfy,
            ):
                success = auto_ingest.ingest_raw_source(raw_path, root, token="")

            self.assertFalse(success)
            send_ntfy.assert_called_once()
            title, message = send_ntfy.call_args.args[:2]
            self.assertIn(raw_path.name, title)
            self.assertIn("codex-cli", message)
            self.assertIn("401 Unauthorized", message)
            self.assertIn("status: pending", raw_path.read_text())

    def test_failure_detail_formatter_redacts_secrets_and_bounds_message(self) -> None:
        detail = (
            "Authorization: Bearer super-secret-token\n"
            "token=ghp_abcdefghijklmnopqrstuvwxyz\n"
            "AWS_SECRET_ACCESS_KEY=aws-secret-value\n"
            "client_secret=oauth-secret\n"
            "Cookie: session=browser-secret\n"
            "https://user:pass@example.test/path?token=query-secret\n"
            + ("🙂" * 5000)
            + "\n401 Unauthorized at final transport attempt"
        )

        message = auto_ingest.format_ingest_failure_message(
            Path("raw/example.md"),
            backend="codex-cli",
            detail=detail,
        )

        self.assertNotIn("super-secret-token", message)
        for secret in (
            "ghp_abcdefghijklmnopqrstuvwxyz",
            "aws-secret-value",
            "oauth-secret",
            "browser-secret",
            "user:pass",
            "query-secret",
        ):
            self.assertNotIn(secret, message)
        self.assertIn("Authorization: Bearer [REDACTED]", message)
        self.assertIn("401 Unauthorized at final transport attempt", message)
        self.assertLessEqual(
            len(message.encode("utf-8")),
            auto_ingest.NTFY_FAILURE_MESSAGE_MAX_CHARS,
        )

    def test_pending_loop_exception_notifies_with_exception_details(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_path = root / "raw" / "example.md"
            raw_path.parent.mkdir(parents=True)
            raw_path.write_text("---\ntitle: Example\ntype: text\nstatus: pending\n---\nBody")

            with (
                patch("auto_ingest.ingest_raw_source", side_effect=RuntimeError("disk exploded")),
                patch("auto_ingest.send_ntfy") as send_ntfy,
            ):
                count = auto_ingest.process_all_pending(root, token="")

            self.assertEqual(count, 0)
            send_ntfy.assert_called_once()
            _title, message = send_ntfy.call_args.args[:2]
            self.assertIn("RuntimeError: disk exploded", message)

    def test_pending_discovery_failure_notifies_and_preserves_retry_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_path = root / "raw" / "example.md"
            raw_path.parent.mkdir(parents=True)
            raw_path.write_text("---\ntitle: Example\ntype: text\nstatus: pending\n---\nBody")

            with (
                patch("auto_ingest.classify_ingest_route", side_effect=ValueError("bad route")),
                patch("auto_ingest.send_ntfy") as send_ntfy,
            ):
                count = auto_ingest.process_all_pending(root, token="")

            self.assertEqual(count, 0)
            send_ntfy.assert_called_once()
            self.assertIn("ValueError: bad route", send_ntfy.call_args.args[1])
            self.assertIn("status: pending", raw_path.read_text())

    def test_watcher_classification_failure_notifies(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_path = root / "raw" / "example.md"
            raw_path.parent.mkdir(parents=True)
            raw_path.write_text("---\ntitle: Example\ntype: text\nstatus: pending\n---\nBody")
            handler = watch_raw.RawFileHandler(root, token="", model_override=None)
            handler._pending[str(raw_path)] = 0

            with (
                patch("watch_raw.classify_ingest_route", side_effect=ValueError("bad route")),
                patch("watch_raw.notify_ingest_failure") as notify,
            ):
                handler._process_pending()

            notify.assert_called_once()
            self.assertIn("ValueError: bad route", notify.call_args.kwargs["detail"])

    def test_direct_cli_exception_notifies_and_exits_failed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_path = root / "raw" / "example.md"
            raw_path.parent.mkdir(parents=True)
            raw_path.write_text("---\ntitle: Example\ntype: text\nstatus: pending\n---\nBody")

            with (
                patch.object(sys, "argv", ["auto_ingest.py", str(raw_path), "--project-root", str(root)]),
                patch("auto_ingest.ingest_raw_source", side_effect=RuntimeError("publish exploded")),
                patch("auto_ingest.send_ntfy") as send_ntfy,
                self.assertRaises(SystemExit) as exit_error,
            ):
                auto_ingest.main()

            self.assertEqual(exit_error.exception.code, 1)
            send_ntfy.assert_called_once()
            self.assertIn("RuntimeError: publish exploded", send_ntfy.call_args.args[1])
            self.assertIn("status: pending", raw_path.read_text())

    def test_direct_cli_exception_validation_run_suppresses_notification(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_path = root / "raw" / "example.md"
            raw_path.parent.mkdir(parents=True)
            raw_path.write_text("---\ntitle: Example\ntype: text\nstatus: pending\n---\nBody")

            with (
                patch.object(
                    sys,
                    "argv",
                    [
                        "auto_ingest.py",
                        str(raw_path),
                        "--project-root",
                        str(root),
                        "--force",
                        "--validation-run",
                    ],
                ),
                patch("auto_ingest.ingest_raw_source", side_effect=RuntimeError("publish exploded")),
                patch("auto_ingest.send_ntfy") as send_ntfy,
                self.assertRaises(SystemExit) as exit_error,
            ):
                auto_ingest.main()

            self.assertEqual(exit_error.exception.code, 1)
            send_ntfy.assert_not_called()

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
                '"page_mutations":[],"duplicates_avoided":[],"kg_facts":[],'
                '"notes":"ok"}\n'
            ),
            stderr="",
        )
        with (
            patch.dict(os.environ, {"WIKI_CODEX_SANDBOX": "read-only"}),
            patch("auto_ingest.subprocess.run", return_value=completed) as run,
        ):
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
        self.assertEqual(cmd[cmd.index("-s") + 1], "read-only")
        self.assertNotEqual(Path(cmd[cmd.index("-C") + 1]), ROOT)
        self.assertNotEqual(Path(cmd[cmd.index("--add-dir") + 1]), ROOT)
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
        self.assertIn("propose only the source summary", prompt)
        self.assertIn("read-only", prompt.casefold())

    def test_agent_proposal_parser_rejects_incomplete_or_unknown_fields(self) -> None:
        missing = auto_ingest._parse_agent_status_output(
            '{"status":"success","source_path":"wiki/sources/example.md"}',
            "Codex CLI",
            ROOT / "raw" / "example.md",
        )
        unknown = auto_ingest._parse_agent_status_output(
            json.dumps(
                {
                    "status": "success",
                    "source_path": "wiki/sources/example.md",
                    "page_mutations": [],
                    "duplicates_avoided": [],
                    "kg_facts": [],
                    "notes": "ok",
                    "unexpected": True,
                }
            ),
            "Codex CLI",
            ROOT / "raw" / "example.md",
        )

        self.assertEqual(missing["status"], "failed")
        self.assertIn("schema", missing["notes"])
        self.assertEqual(unknown["status"], "failed")
        self.assertIn("schema", unknown["notes"])

    def test_all_backends_short_circuit_source_hash_before_backend_call(self) -> None:
        for backend in ("codex-cli", "copilot-cli", "github-models"):
            with self.subTest(backend=backend), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                raw_path = root / "raw" / "duplicate.md"
                source_path = root / "wiki" / "sources" / "existing.md"
                raw_path.parent.mkdir(parents=True)
                source_path.parent.mkdir(parents=True)
                body = "Deterministic duplicate body"
                source_hash = auto_ingest.compute_sha256(body)
                raw_path.write_text(
                    f"---\ntitle: Duplicate\ntype: text\nstatus: pending\n---\n{body}"
                )
                source_path.write_text(
                    f"---\ntitle: Existing\ntype: source\nsource_hash: sha256:{source_hash}\n---\n"
                )

                with (
                    patch("auto_ingest._selected_backend", return_value=backend),
                    patch("auto_ingest.call_codex_cli_ingest") as codex,
                    patch("auto_ingest.call_copilot_cli_ingest") as copilot,
                    patch("auto_ingest.commit_wiki_changes", return_value=True) as commit,
                    patch("auto_ingest.send_ntfy") as send_ntfy,
                ):
                    success = auto_ingest.ingest_raw_source(raw_path, root, token="")

                self.assertTrue(success)
                codex.assert_not_called()
                copilot.assert_not_called()
                self.assertIn("status: ingested", raw_path.read_text())
                commit.assert_called_once()
                committed_paths = commit.call_args.kwargs["paths"]
                self.assertIn("raw/duplicate.md", committed_paths)
                self.assertIn("wiki/log.md", committed_paths)
                send_ntfy.assert_called_once()
                self.assertIn("duplicate", (root / "wiki" / "log.md").read_text().lower())

    def test_validation_run_skips_log_notification_and_commit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_path = root / "raw" / "example.md"
            source_path = root / "wiki" / "sources" / "example.md"
            raw_path.parent.mkdir(parents=True)
            source_path.parent.mkdir(parents=True)
            raw_path.write_text(
                "---\ntitle: Example\ntype: text\nurl: https://example.com/source\n"
                "status: pending\n---\nUseful source body"
            )
            source_hash = auto_ingest.compute_sha256("Useful source body")
            existing_content = (
                "---\ntitle: Example\ntype: source\ncreated: 2026-08-01\n"
                "last_verified: 2026-08-01\nsource_hash: \"" + "b" * 64 + "\"\n"
                "sources:\n  - raw/example.md\nconcepts: []\nrelated: []\n"
                "tier: hot\ntags: [example]\n---\n\n# Example\n\n## Summary\n\nExisting summary.\n"
            )
            source_path.write_text(existing_content)
            proposed_content = existing_content.replace(
                "created: 2026-08-01\nlast_verified: 2026-08-01\nsource_hash: \"" + "b" * 64 + "\"",
                f"created: 2026-08-01\nlast_verified: 2026-08-02\nsource_hash: \"{source_hash}\"",
            )
            status = {
                "status": "success",
                "source_path": "wiki/sources/example.md",
                "page_mutations": [
                    {
                        "path": "wiki/sources/example.md",
                        "operation": "update",
                        "content": proposed_content,
                    }
                ],
                "duplicates_avoided": [],
                "kg_facts": [],
                "notes": "ok",
            }

            def fake_graph(stage_root, _runtime=None):
                graph = stage_root / "wiki" / "graph" / "graph.json"
                graph.parent.mkdir(parents=True, exist_ok=True)
                graph.write_text('{"node_count": 1, "nodes": []}\n')
                tracker = stage_root / "reports" / "checkpoint-graph-tracker.md"
                tracker.parent.mkdir(parents=True, exist_ok=True)
                tracker.write_text("# Tracker\n")

            with (
                patch("auto_ingest._selected_backend", return_value="codex-cli"),
                patch("auto_ingest.call_codex_cli_ingest", return_value=status),
                patch("ingest_transaction._build_graph", side_effect=fake_graph),
                patch("auto_ingest.send_ntfy") as send_ntfy,
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

    def test_git_publish_manifest_excludes_runtime_kg_outbox(self) -> None:
        self.assertEqual(
            auto_ingest.git_publish_manifest(
                ["wiki/sources/example.md", "wiki/.kg-pending.jsonl", "raw/example.md"]
            ),
            ["wiki/sources/example.md", "raw/example.md"],
        )

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
        self.assertIn("evidence_origin_family_count: 2", content)
        self.assertRegex(content, r'source_hash: "[0-9a-f]{64}"')
        self.assertIn("## Evidence Map", content)
        insight_one = next(line for line in content.splitlines() if line.startswith("| Insight 1 |"))
        insight_two = next(line for line in content.splitlines() if line.startswith("| Insight 2 |"))
        self.assertIn("`raw/a.md`", insight_one)
        self.assertNotIn("`raw/b.md`", insight_one)
        self.assertIn("`raw/b.md`", insight_two)
        self.assertNotIn("`raw/a.md`", insight_two)


if __name__ == "__main__":
    unittest.main()
