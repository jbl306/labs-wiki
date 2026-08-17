import asyncio
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
GRAPH_API = ROOT / "wiki-graph-api"
sys.path.insert(0, str(GRAPH_API))

HAS_FASTAPI = importlib.util.find_spec("fastapi") is not None
if HAS_FASTAPI:
    spec = importlib.util.spec_from_file_location("graph_api_main", GRAPH_API / "main.py")
    assert spec is not None and spec.loader is not None
    graph_api_main = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(graph_api_main)
else:
    graph_api_main = None


@unittest.skipUnless(HAS_FASTAPI, "wiki-graph-api requirements are not installed")
class GraphApiRebuildTests(unittest.TestCase):
    def test_rebuild_uses_configured_tracker_and_restores_runtime_embeddings(self) -> None:
        assert graph_api_main is not None
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wiki = root / "wiki"
            wiki.mkdir()
            (wiki / "concept.md").write_text("# Concept\n")
            graph_path = root / "graph.json"
            tracker_path = root / "reports" / "tracker.md"
            cache = root / "cache"
            payload = {
                "source_signature": "new-signature",
                "generated_at": 0,
                "build_seconds": 0.0,
                "node_count": 0,
                "edge_count": 0,
                "community_count": 0,
                "nodes": [],
                "edges": [],
            }
            state = graph_api_main.GraphState()

            with (
                patch.object(graph_api_main, "WIKI_PATH", wiki),
                patch.object(graph_api_main, "CACHE_DIR", cache),
                patch.object(graph_api_main, "GRAPH_PATH", graph_path),
                patch.object(graph_api_main, "TRACKER_PATH", tracker_path),
                patch.object(
                    graph_api_main,
                    "build_graph_artifact",
                    return_value=payload,
                ) as build,
                patch.object(state, "_refresh_query_embeddings") as refresh,
            ):
                result = asyncio.run(state.rebuild())

            self.assertIs(result, payload)
            build.assert_called_once_with(
                wiki,
                cache,
                graph_path,
                tracker_path=tracker_path,
            )
            refresh.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
