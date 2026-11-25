"""Exercise the issue workflow's publication step in a disposable local remote."""

from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from auto_ingest import parse_frontmatter
from capture_issue import capture_issue


class IssueCaptureTests(unittest.TestCase):
    def test_stable_capture_is_published_once_and_preserves_the_issue_text(self):
        event = {
            "action": "labeled", "label": {"name": "ingest"},
            "issue": {
                "number": 31, "title": 'Notes --- "summer" and autumn',
                "body": "First paragraph.\n\n  Preserve the indentation.",
                "created_at": "2026-06-01T12:00:00Z", "updated_at": "2026-08-01T13:30:00Z",
            },
        }
        steps = yaml.safe_load((ROOT / ".github/workflows/ingest-from-issue.yml").read_text())["jobs"]["ingest"]["steps"]
        publish = next(s["run"] for s in steps if s.get("id") == "publish")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "runner"
            repo.mkdir()
            env = {
                **os.environ, "BRANCH": "main", "ISSUE_NUMBER": "31",
                "GITHUB_EVENT_PATH": str(root / "event.json"), "GITHUB_OUTPUT": str(root / "output"),
                "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1",
            }
            def run(*args):
                return subprocess.run(args, cwd=repo, env=env, capture_output=True, check=True, text=True).stdout
            run("git", "init", "-q", "--bare", "-b", "main", str(root / "remote.git"))
            run("git", "init", "-q", "-b", "main")
            (repo / "scripts").mkdir()
            (repo / "raw").mkdir()
            (repo / "raw/.gitkeep").touch()
            shutil.copy2(ROOT / "scripts/capture_issue.py", repo / "scripts")
            run("git", "add", "--", "raw/.gitkeep", "scripts/capture_issue.py")
            run("git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "fixture")
            run("git", "remote", "add", "origin", str(root / "remote.git"))
            run("git", "push", "-q", "origin", "main")
            (root / "event.json").write_text(json.dumps(event))
            (repo / "raw/unrelated.md").write_text("unrelated")
            run("git", "add", "--", "raw/unrelated.md")
            run("bash", "-eu", "-c", publish)
            head = run("git", "rev-parse", "HEAD")
            path = "raw/2026-06-01-github-issue-31.md"
            self.assertEqual(run("git", "show", "--format=", "--name-only", "HEAD").strip(), path)
            fm, body = parse_frontmatter(repo / path)
            self.assertEqual(fm["title"], event["issue"]["title"])
            self.assertEqual(body, event["issue"]["body"])
            self.assertEqual(fm["status"], "pending")
            self.assertEqual(run("git", "diff", "--cached", "--name-only").strip(), "raw/unrelated.md")
            run("bash", "-eu", "-c", publish)
            self.assertEqual(run("git", "rev-parse", "HEAD"), head)
            self.assertEqual((root / "output").read_text().splitlines(), [f"filename={path}"] * 2)
            # Two independent jobs can start at the same branch tip.
            peer = root / "peer"
            run("git", "clone", "-q", str(root / "remote.git"), str(peer))
            def publish_issue(worktree, number):
                payload = {**event, "issue": {**event["issue"], "number": number}}
                event_path = root / f"event-{number}.json"
                event_path.write_text(json.dumps(payload))
                subprocess.run(
                    ["bash", "-eu", "-c", publish], cwd=worktree,
                    env={**env, "ISSUE_NUMBER": str(number), "GITHUB_EVENT_PATH": str(event_path),
                         "GITHUB_OUTPUT": str(root / f"out-{number}")},
                    capture_output=True, check=True, timeout=25,
                )
            with ThreadPoolExecutor(max_workers=2) as pool:
                first = pool.submit(publish_issue, repo, 32)
                second = pool.submit(publish_issue, peer, 33)
                first.result()
                second.result()
            paths = run("git", "--git-dir", str(root / "remote.git"), "ls-tree", "-r", "--name-only", "main", "raw")
            self.assertTrue(all(f"github-issue-{number}.md" in paths for number in (31, 32, 33)))
            event["label"]["name"] = "Ingest"
            with self.assertRaisesRegex(ValueError, "label"):
                capture_issue(event, repo / "raw")
