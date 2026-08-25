import asyncio
import json
import os
import sys
import unittest
from unittest.mock import patch

import httpx

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import wiki_mcp_server as server  # noqa: E402


class WikiCaptureTests(unittest.TestCase):
    def setUp(self):
        self.config = {
            "WIKI_INGEST_API_BASE_URL": "https://wiki.example.test/",
            "WIKI_INGEST_API_TOKEN": "test-token-do-not-disclose",
        }

    @staticmethod
    def client(handler):
        return httpx.Client(transport=httpx.MockTransport(handler))

    @staticmethod
    def ok(request, path="raw/2026-08-25-capture.md"):
        return httpx.Response(200, json={"status": "ok", "path": path})

    def capture_with_handler(self, handler, *args, config=None, **kwargs):
        client = self.client(handler)
        with patch.dict(os.environ, config or self.config, clear=True), patch.object(
            server.httpx, "Client", return_value=client
        ) as client_factory:
            result = server.wiki_capture(*args, **kwargs)
        client_factory.assert_called_once_with(timeout=server.CAPTURE_API_TIMEOUT)
        return result

    def test_success_forwards_json_and_bearer_auth_without_disclosure(self):
        requests = []

        def handler(request):
            requests.append(request)
            return self.ok(request)

        result = self.capture_with_handler(
            handler,
            "text",
            "A useful capture",
            title="Useful title",
            tags=["one", "two"],
            source="codex-mcp",
        )

        self.assertEqual(result, "wiki capture succeeded: raw/2026-08-25-capture.md")
        self.assertNotIn(self.config["WIKI_INGEST_API_TOKEN"], result)
        self.assertEqual(len(requests), 1)
        request = requests[0]
        self.assertEqual(str(request.url), "https://wiki.example.test/api/ingest")
        self.assertEqual(request.headers["Authorization"], "Bearer test-token-do-not-disclose")
        self.assertEqual(request.headers["Content-Type"], "application/json")
        self.assertEqual(
            json.loads(request.content),
            {
                "type": "text",
                "content": "A useful capture",
                "title": "Useful title",
                "tags": ["one", "two"],
                "source": "codex-mcp",
            },
        )

    def test_url_and_note_payloads_are_forwarded_without_reinterpretation(self):
        cases = [
            ("url", "https://example.com/article", "Article"),
            ("note", "Remember this exactly", None),
        ]
        for capture_type, content, title in cases:
            requests = []

            def handler(request):
                requests.append(request)
                return self.ok(request)

            with self.subTest(capture_type=capture_type):
                result = self.capture_with_handler(
                    handler,
                    capture_type,
                    content,
                    title=title,
                    tags=["contract"],
                )

            self.assertIn("succeeded", result)
            payload = json.loads(requests[0].content)
            self.assertEqual(payload["type"], capture_type)
            self.assertEqual(payload["content"], content)
            self.assertEqual(payload["tags"], ["contract"])
            if title is None:
                self.assertNotIn("title", payload)
            else:
                self.assertEqual(payload["title"], title)

    def test_missing_malformed_or_cleartext_remote_configuration_fails_closed(self):
        cases = [
            ({"WIKI_INGEST_API_TOKEN": "token"}, "WIKI_INGEST_API_BASE_URL"),
            ({"WIKI_INGEST_API_BASE_URL": "https://wiki.example.test"}, "WIKI_INGEST_API_TOKEN"),
            ({**self.config, "WIKI_INGEST_API_BASE_URL": "ftp://wiki.example.test"}, "base URL"),
            ({**self.config, "WIKI_INGEST_API_BASE_URL": "https://user:pass@wiki.example.test"}, "base URL"),
            ({**self.config, "WIKI_INGEST_API_TOKEN": "Bearer token with spaces"}, "token"),
            ({**self.config, "WIKI_INGEST_API_BASE_URL": "http://wiki.internal:8000"}, "HTTPS"),
            ({**self.config, "WIKI_INGEST_API_BASE_URL": "http://192.168.1.20:8000"}, "HTTPS"),
            ({**self.config, "WIKI_INGEST_API_BASE_URL": "http://example.com"}, "HTTPS"),
        ]
        for environment, expected in cases:
            with self.subTest(expected=expected), patch.dict(
                os.environ, environment, clear=True
            ), patch.object(server.httpx, "Client") as client_factory:
                result = server.wiki_capture("note", "capture")

            self.assertIn(expected, result)
            client_factory.assert_not_called()
            self.assertNotIn(self.config["WIKI_INGEST_API_TOKEN"], result)

    def test_cleartext_loopback_configuration_is_allowed(self):
        for base_url in (
            "http://localhost:8000",
            "http://127.0.0.9:8000",
            "http://[::1]:8000",
        ):
            with self.subTest(base_url=base_url):
                config = {**self.config, "WIKI_INGEST_API_BASE_URL": base_url}
                client = self.client(self.ok)
                with patch.dict(os.environ, config, clear=True), patch.object(
                    server.httpx, "Client", return_value=client
                ):
                    result = server.wiki_capture("note", "capture")
                self.assertIn("succeeded", result)

    def test_invalid_type_and_input_bounds_have_no_side_effect(self):
        invalid_calls = [
            {"type": "file", "content": "capture"},
            {"type": [], "content": "capture"},
            {"type": "url", "content": "x" * (server.CAPTURE_MAX_CONTENT + 1)},
            {"type": "text", "content": "capture", "title": "x" * (server.CAPTURE_MAX_TITLE + 1)},
            {"type": "text", "content": "capture", "tags": ["x"] * (server.CAPTURE_MAX_TAGS + 1)},
            {"type": "text", "content": "capture", "source": "x" * (server.CAPTURE_MAX_SOURCE + 1)},
        ]
        with patch.dict(os.environ, self.config, clear=True), patch.object(
            server.httpx, "Client"
        ) as client_factory:
            for arguments in invalid_calls:
                with self.subTest(arguments=list(arguments)):
                    result = server.wiki_capture(**arguments)
                    self.assertIn("invalid", result.lower())

        client_factory.assert_not_called()

    def test_http_auth_failures_do_not_return_secret_or_upstream_body(self):
        for status_code in (401, 403):
            def handler(request, status_code=status_code):
                return httpx.Response(
                    status_code,
                    json={"detail": "upstream body contains test-token-do-not-disclose"},
                )

            with self.subTest(status_code=status_code):
                result = self.capture_with_handler(handler, "note", "capture")

            self.assertIn(f"HTTP {status_code}", result)
            self.assertNotIn("test-token-do-not-disclose", result)
            self.assertNotIn("upstream body", result)

    def test_http_failure_does_not_return_secret_or_upstream_body(self):
        def handler(request):
            return httpx.Response(
                502,
                json={"detail": "upstream body contains test-token-do-not-disclose"},
            )

        result = self.capture_with_handler(handler, "note", "capture")

        self.assertIn("HTTP 502", result)
        self.assertNotIn("test-token-do-not-disclose", result)
        self.assertNotIn("upstream body", result)

    def test_network_failure_is_not_retried_and_is_redacted(self):
        calls = 0

        def handler(request):
            nonlocal calls
            calls += 1
            raise httpx.ReadTimeout(
                "failed with test-token-do-not-disclose",
                request=request,
            )

        result = self.capture_with_handler(handler, "note", "capture")

        self.assertEqual(calls, 1)
        self.assertIn("network", result.lower())
        self.assertNotIn("test-token-do-not-disclose", result)

    def test_only_normalized_relative_raw_markdown_response_paths_are_disclosed(self):
        malicious_paths = [
            "/etc/passwd",
            "../outside.md",
            "https://evil.example/leak.md",
            r"raw\outside.md",
            "raw/../outside.md",
            "raw//outside.md",
            "raw/not-markdown.txt",
        ]
        for path in malicious_paths:
            def handler(request, path=path):
                return self.ok(request, path)

            with self.subTest(path=path):
                result = self.capture_with_handler(handler, "note", "capture")

            self.assertEqual(result, "wiki capture failed: invalid response from ingest API")
            self.assertNotIn(self.config["WIKI_INGEST_API_TOKEN"], result)

    def test_valid_paths_containing_the_token_return_generic_success(self):
        secret_token = self.config["WIKI_INGEST_API_TOKEN"]
        cases = [
            ("raw", "raw/2026-08-25-note.md"),
            ("capture", "raw/2026-08-25-capture.md"),
            (secret_token, f"raw/2026-08-25-{secret_token}.md"),
        ]
        for token, path in cases:
            def handler(request, path=path):
                return self.ok(request, path)

            config = {**self.config, "WIKI_INGEST_API_TOKEN": token}
            with self.subTest(token=token):
                result = self.capture_with_handler(
                    handler, "note", "capture", config=config
                )

            self.assertEqual(result, "wiki ingest succeeded")
            self.assertLessEqual(len(result), server.CAPTURE_MAX_OUTPUT)
            self.assertNotIn(path, result)
            self.assertNotIn(token, result)

    def test_response_shape_is_validated_and_bounded(self):
        payloads = [
            {},
            [],
            {"status": "ok"},
            {"status": "error", "path": "raw/failure.md"},
            {"status": "ok", "path": 42},
            {"status": "ok", "path": "x" * (server.CAPTURE_MAX_OUTPUT + 1)},
        ]
        for payload in payloads:
            def handler(request, payload=payload):
                return httpx.Response(200, json=payload)

            with self.subTest(payload=payload):
                result = self.capture_with_handler(handler, "note", "capture")

            self.assertIn("invalid response", result.lower())
            self.assertLessEqual(len(result), server.CAPTURE_MAX_OUTPUT)

    def test_invalid_response_json_is_reported_without_body(self):
        def handler(request):
            return httpx.Response(200, content=b"secret body", request=request)

        result = self.capture_with_handler(handler, "note", "capture")

        self.assertIn("invalid response", result.lower())
        self.assertNotIn("secret body", result)


class FastMCPContractTests(unittest.TestCase):
    @staticmethod
    def tools():
        return asyncio.run(server.mcp.list_tools())

    def test_capture_type_schema_is_the_supported_enum(self):
        tools = {tool.name: tool for tool in self.tools()}
        self.assertEqual(
            tools["wiki_capture"].inputSchema["properties"]["type"]["enum"],
            ["url", "text", "note"],
        )

    def test_existing_tool_inventory_is_preserved(self):
        self.assertEqual(
            {tool.name for tool in self.tools()},
            {
                "wiki_capture",
                "wiki_list",
                "wiki_search",
                "wiki_read",
                "wiki_graph_neighbors",
                "wiki_graph_shortest_path",
                "wiki_graph_communities",
                "wiki_graph_god_nodes",
                "wiki_graph_surprises",
                "wiki_graph_query",
            },
        )


if __name__ == "__main__":
    unittest.main()
