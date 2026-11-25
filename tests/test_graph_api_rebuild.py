import importlib.util
import json
import os
import sys
import tempfile
import time
import unittest
from contextlib import ExitStack
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
GRAPH_API = ROOT / "wiki-graph-api"
sys.path.insert(0, str(GRAPH_API))

HAS_HTTP = all(importlib.util.find_spec(dep) for dep in ("fastapi", "httpx"))
if HAS_HTTP:
    from fastapi.testclient import TestClient

    spec = importlib.util.spec_from_file_location("graph_api_main", GRAPH_API / "main.py")
    assert spec is not None and spec.loader is not None
    graph_api_main = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(graph_api_main)


@unittest.skipUnless(HAS_HTTP, "graph HTTP dependencies are not installed")
class GraphApiRebuildTests(unittest.TestCase):
    def setUp(self):
        stack = self.enterContext(ExitStack())
        root = Path(stack.enter_context(tempfile.TemporaryDirectory()))
        self.wiki = root / "wiki"
        self.wiki.mkdir()
        self.graph_path = root / "data" / "graph.json"
        self.tracker = root / "data" / "tracker.md"
        self.published = self.wiki / "graph" / "graph.json"
        stack.enter_context(patch.multiple(
            graph_api_main,
            WIKI_PATH=self.wiki, CACHE_DIR=root / "cache", GRAPH_PATH=self.graph_path,
            TRACKER_PATH=self.tracker, ADMIN_TOKEN="fixture", PUBLICATION_POLL_SECONDS=0.05,
        ))
        stack.enter_context(patch.dict(os.environ, {"WIKI_GRAPH_EMBEDDING_BACKEND": "tfidf"}))
        self.add_page("alpha", "Alpha", "Read [[Missing]].")

    def add_page(self, slug, title, body, *, metadata=""):
        path = self.wiki / "concepts" / (slug + ".md")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            f"---\ntitle: {title}\ntype: concept\nlast_verified: 2020-01-01\n{metadata}---\n\n{body}\n"
        )

    def client(self):
        graph_api_main.state = graph_api_main.GraphState()
        return TestClient(graph_api_main.app)

    def publish(self):
        graph_api_main.build_graph_artifact(
            self.wiki, None, self.published, tracker_path=self.wiki.parent / "reports" / "tracker.md",
        )

    def wait_for(self, client, check):
        deadline = time.monotonic() + 8
        while time.monotonic() < deadline:
            stats = client.get("/graph/stats").json()
            if check(stats):
                return stats
            time.sleep(0.03)
        self.fail(f"graph did not reach expected state: {stats}")

    def test_unreceipted_snapshot_restart_and_unchanged_rebuild(self):
        graph_api_main.build_graph_artifact(self.wiki, None, self.graph_path, tracker_path=self.tracker)
        canonical = self.graph_path.read_bytes()
        graph_api_main.state = graph_api_main.GraphState()
        self.assertTrue(graph_api_main.state.load_from_disk())
        self.assertIsNone(graph_api_main.graph_stats()["last_rebuild"])

        with self.client() as client:
            stats = client.get("/graph/stats").json()
            receipt = stats["build_receipt"]
            self.assertEqual(stats["sync_status"], "current")
            self.assertTrue(stats["content_as_of"].startswith("2020-01-01"))
            self.assertNotEqual(stats["last_rebuild"][:10], "2020-01-01")
            self.assertGreater(receipt["build_seconds"], 0)
            self.assertEqual(receipt["source_counts"], {"wiki_pages": 1, "by_page_type": {"concept": 1}})
            self.assertEqual(receipt["source_signature"], stats["observed_source_signature"])
            self.assertTrue(client.get("/graph/checkpoint-tracker").json()["available"])
            response = client.post("/internal/rebuild", headers={"X-Admin-Token": "fixture"})
            self.assertTrue(response.json()["rebuild_skipped"])
            self.assertEqual(client.get("/graph/stats").json()["build_receipt"], receipt)
            self.assertEqual(canonical, self.graph_path.read_bytes())
        with self.client() as client:
            self.assertEqual(client.get("/graph/stats").json()["build_receipt"], receipt)

        self.add_page("beta", "Beta", "Read [[Alpha]].")
        self.publish()
        with self.client() as client:
            stats = client.get("/graph/stats").json()
            self.assertEqual(stats["node_count"], 2)
            self.assertEqual(stats["source_signature"], json.loads(self.published.read_text())["source_signature"])
            self.assertNotEqual(stats["source_signature"], receipt["source_signature"])

    def test_publication_failure_is_visible_then_retried(self):
        with self.client() as client:
            initial = client.get("/graph/stats").json()
            self.add_page("beta", "Beta", "[[Alpha]]")
            self.publish()
            with patch.object(graph_api_main, "build_graph_artifact", side_effect=OSError("fixture write error")):
                # A fresh atomic publication guarantees a poll even if the first
                # one happened while the canonical artifact was being produced.
                self.add_page("gamma", "Gamma", "[[Beta]]")
                self.published.touch()
                failed = self.wait_for(client, lambda stats: stats["sync_status"] == "error")
                self.assertEqual(failed["sync_error"], "fixture write error")
                self.assertLess(failed["node_count"], 3)
            refreshed = self.wait_for(client, lambda stats: stats["sync_status"] == "current" and stats["node_count"] == 3)
            self.assertNotEqual(initial["source_signature"], refreshed["source_signature"])
            self.assertIsNone(refreshed["sync_error"])

    @unittest.skipUnless(importlib.util.find_spec("sklearn"), "scikit-learn is not installed")
    def test_queries_neighbors_and_health_measure_actual_evidence(self):
        self.add_page("_archive/beta", "Beta", "Telescope. [[Alpha]]")
        self.add_page("gamma", "Gamma", "Telescope. [[Beta]] [[Delta]]", metadata="tier: warm\n")
        self.add_page("delta", "Delta", "Telescope.", metadata="tier: archive\nretention_mode: compress\n")
        with self.client() as client:
            def query(**body):
                return client.post("/graph/query", json=body).json()

            absent = query(q="zzzznotinthecorpus")
            self.assertNotIn("error", absent)
            self.assertEqual(absent["nodes"], [])
            self.assertEqual(absent["subgraph"], {"nodes": [], "edges": []})
            self.assertEqual({n["title"] for n in query(q="telescope")["nodes"]}, {"Beta", "Gamma", "Delta"})
            active = query(q="telescope", include_archived=False)
            self.assertEqual([n["title"] for n in active["nodes"]], ["Gamma"])
            self.assertEqual([n["title"] for n in active["subgraph"]["nodes"]], ["Gamma"])
            self.assertEqual(active["subgraph"]["edges"], [])
            self.assertEqual(query(q="telescope", include_archived=False, k=1)["nodes"], active["nodes"])

            # A bounded TF-IDF vocabulary can omit a real page's entire title.
            with patch.object(graph_api_main, "embed_query", return_value=[0.0]):
                exact = query(q="  gAmMa  ", include_archived=False)["nodes"]
                self.assertEqual([(n["title"], n["score"], n["match_type"]) for n in exact],
                                 [("Gamma", 0.0, "exact_title")])
                self.assertEqual(query(q="Delta", include_archived=False)["nodes"], [])
                self.assertEqual(query(q="unrelated", include_archived=False)["nodes"], [])

            neighbors = client.get("/graph/neighbors/concepts/alpha?depth=2").json()
            self.assertEqual([n["depth"] for n in neighbors["nodes"]], [0, 1, 2])
            self.assertEqual(len(neighbors["edges"]), 2)
            self.assertTrue(all("embedding" not in n and "content_hash" not in n for n in neighbors["nodes"]))
            health = client.get("/graph/health").json()
            self.assertEqual(health["tier_distribution"]["warm"], 1)
            self.assertEqual(health["tier_distribution"]["archive"], 1)
            self.assertEqual(health["broken_link_count"], 1)
            self.assertIsNone(health["dedupe_candidate_count"])
            report = self.wiki.parent / "reports" / "dedupe-candidates-latest.json"
            report.parent.mkdir(exist_ok=True)
            report.write_text("{}")
            self.assertIsNone(client.get("/graph/health").json()["dedupe_candidate_count"])
            report.write_text("[]")
            self.assertEqual(client.get("/graph/health").json()["dedupe_candidate_count"], 0)


if __name__ == "__main__":
    unittest.main()
