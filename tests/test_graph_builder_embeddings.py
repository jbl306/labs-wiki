import importlib.util
import os
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GRAPH_BUILDER_PATH = ROOT / "wiki-graph-api" / "graph_builder.py"

spec = importlib.util.spec_from_file_location("graph_builder", GRAPH_BUILDER_PATH)
graph_builder = importlib.util.module_from_spec(spec)
sys.modules["graph_builder"] = graph_builder
assert spec.loader is not None
spec.loader.exec_module(graph_builder)


class GraphBuilderEmbeddingTests(unittest.TestCase):
    def setUp(self) -> None:
        self._old_backend = os.environ.get("WIKI_GRAPH_EMBEDDING_BACKEND")
        self._old_features = os.environ.get("WIKI_GRAPH_TFIDF_MAX_FEATURES")
        os.environ["WIKI_GRAPH_EMBEDDING_BACKEND"] = "tfidf"
        os.environ["WIKI_GRAPH_TFIDF_MAX_FEATURES"] = "64"
        graph_builder._tfidf_state.clear()
        graph_builder._st_model = None

    def tearDown(self) -> None:
        if self._old_backend is None:
            os.environ.pop("WIKI_GRAPH_EMBEDDING_BACKEND", None)
        else:
            os.environ["WIKI_GRAPH_EMBEDDING_BACKEND"] = self._old_backend
        if self._old_features is None:
            os.environ.pop("WIKI_GRAPH_TFIDF_MAX_FEATURES", None)
        else:
            os.environ["WIKI_GRAPH_TFIDF_MAX_FEATURES"] = self._old_features
        graph_builder._tfidf_state.clear()
        graph_builder._st_model = None

    def test_default_tfidf_backend_keeps_query_embedding_available(self) -> None:
        try:
            import sklearn  # noqa: F401
        except ImportError:
            self.skipTest("scikit-learn is not installed in this Python environment")

        nodes = [
            {
                "id": "concepts/player-projection",
                "title": "Player Projection",
                "summary": "basketball player projections and fantasy scoring",
                "content_hash": "hash-a",
            },
            {
                "id": "concepts/docker-memory",
                "title": "Docker Memory",
                "summary": "container memory limits and runtime resources",
                "content_hash": "hash-b",
            },
        ]

        with tempfile.TemporaryDirectory() as tmp:
            embeddings, backend = graph_builder.compute_node_embeddings(nodes, Path(tmp))

        self.assertEqual(backend, "tfidf")
        self.assertEqual(set(embeddings), {node["id"] for node in nodes})
        self.assertIsNotNone(graph_builder.embed_query("fantasy basketball projection"))
        self.assertIsNone(graph_builder._st_model)

    def test_wiki_signature_changes_only_when_content_changes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            wiki = Path(tmp)
            page = wiki / "concepts" / "memory.md"
            page.parent.mkdir()
            page.write_text("---\ntitle: Memory\n---\n\nFirst version\n")

            first = graph_builder.compute_wiki_signature(wiki)
            second = graph_builder.compute_wiki_signature(wiki)
            page.write_text("---\ntitle: Memory\n---\n\nSecond version\n")
            third = graph_builder.compute_wiki_signature(wiki)

        self.assertEqual(first, second)
        self.assertNotEqual(first, third)


if __name__ == "__main__":
    unittest.main()
