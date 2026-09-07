import asyncio
import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch
from concurrent.futures import ThreadPoolExecutor

import httpx
import yaml


MODULE_PATH = Path(__file__).parents[1] / "wiki-ingest-api" / "app.py"
SPEC = importlib.util.spec_from_file_location("wiki_ingest_api_app", MODULE_PATH)
assert SPEC and SPEC.loader
api = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(api)


class WikiIngestAPIContractTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.raw_dir = self.root / "raw"
        self.patches = [
            patch.object(api, "RAW_DIR", self.raw_dir),
            patch.object(api, "ASSETS_DIR", self.raw_dir / "assets"),
            patch.object(api, "API_TOKEN", "server-token"),
            patch.object(api, "notify", new=AsyncMock()),
        ]
        for item in self.patches:
            item.start()

    def tearDown(self):
        for item in reversed(self.patches):
            item.stop()
        self.temp_dir.cleanup()

    @staticmethod
    def request(path="/api/ingest", **kwargs):
        async def send():
            transport = httpx.ASGITransport(app=api.app)
            async with httpx.AsyncClient(
                transport=transport,
                base_url="http://testserver",
            ) as client:
                return await client.post(path, **kwargs)

        return asyncio.run(send())

    @staticmethod
    def auth(token="server-token"):
        return {"Authorization": f"Bearer {token}"}

    def frontmatter(self, response):
        raw_text = (self.root / response.json()["path"]).read_text()
        return yaml.safe_load(raw_text.split("---", 2)[1])

    def test_server_authentication_fails_closed(self):
        with patch.object(api, "API_TOKEN", ""):
            response = self.request(json={"type": "note", "content": "capture"})

        self.assertEqual(response.status_code, 503)
        self.assertFalse(self.raw_dir.exists())

    def test_missing_and_invalid_credentials_are_rejected(self):
        missing = self.request(json={"type": "note", "content": "capture"})
        invalid = self.request(
            json={"type": "note", "content": "capture"},
            headers=self.auth("wrong-token"),
        )

        self.assertEqual(missing.status_code, 401)
        self.assertEqual(invalid.status_code, 403)
        self.assertFalse(self.raw_dir.exists())

    def test_debug_requires_auth_and_returns_only_bounded_metadata(self):
        self.assertEqual(self.request('/api/debug').status_code, 401)
        response = self.request(
            '/api/debug?secret=query-secret',
            content='private capture',
            headers={**self.auth(), 'Cookie': 'session=cookie-secret'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'method': 'POST', 'body_length': 15})

    def test_ingest_logs_do_not_contain_request_values(self):
        with self.assertLogs(api.logger, level='DEBUG') as logs:
            response = self.request(
                '/api/ingest?private=query-secret',
                json={'type': 'note', 'content': 'body-secret', 'title': 'title-secret'},
                headers={**self.auth(), 'Cookie': 'session=cookie-secret'},
            )
        self.assertEqual(response.status_code, 200)
        for value in ('query-secret', 'body-secret', 'title-secret', 'cookie-secret', 'server-token'):
            self.assertNotIn(value, '\n'.join(logs.output))

    def test_repeated_file_uploads_preserve_both_raw_records_and_assets(self):
        first = self.request(
            '/api/ingest/file', files={'file': ('paper.txt', b'first version')},
            headers=self.auth(),
        )
        first_path = self.root / first.json()['path']
        first_bytes = first_path.read_bytes()
        second = self.request(
            '/api/ingest/file', files={'file': ('paper.txt', b'second version')},
            headers=self.auth(),
        )
        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 200)
        self.assertNotEqual(first.json()['path'], second.json()['path'])
        self.assertEqual(first_path.read_bytes(), first_bytes)
        assets = list((self.raw_dir / 'assets').iterdir())
        self.assertEqual({p.read_bytes() for p in assets}, {b'first version', b'second version'})
        second_text = (self.root / second.json()['path']).read_text()
        for asset in assets:
            self.assertIn(asset.name, first_bytes.decode() if asset.read_bytes() == b'first version' else second_text)

    def test_concurrent_captures_do_not_overwrite_existing_sources(self):
        def capture(index):
            return api._do_ingest('note', f'capture {index}', 'Same title', [], 'test')

        with ThreadPoolExecutor(max_workers=8) as pool:
            paths = list(pool.map(capture, range(16)))

        self.assertEqual(len(set(paths)), 16)
        for index, path in enumerate(paths):
            self.assertTrue(path.read_text().endswith(f'\ncapture {index}\n'))

    def test_json_tag_lists_round_trip_through_frontmatter(self):
        cases = [
            [],
            ["one", "two"],
            ["one,two", "key: value", '"quoted"', "[brackets]"],
        ]
        for tags in cases:
            with self.subTest(tags=tags):
                response = self.request(
                    json={
                        "type": "text",
                        "content": "Captured text",
                        "title": f"Tags {len(tags)}",
                        "tags": tags,
                        "source": "codex-mcp",
                    },
                    headers=self.auth(),
                )

            self.assertEqual(response.status_code, 200, response.text)
            self.assertEqual(self.frontmatter(response)["tags"], tags)

    def test_scalar_frontmatter_values_round_trip_through_yaml(self):
        title = 'Quoted "title" \\ path: # marker'
        source = 'source "channel" \\ path: # marker'
        url = 'https://example.test/"quoted"\\path:part#fragment'

        response = self.request(
            json={
                "type": "url",
                "content": url,
                "title": title,
                "tags": ["yaml"],
                "source": source,
            },
            headers=self.auth(),
        )

        self.assertEqual(response.status_code, 200, response.text)
        frontmatter = self.frontmatter(response)
        self.assertEqual(frontmatter["title"], title)
        self.assertEqual(frontmatter["source"], source)
        self.assertEqual(frontmatter["url"], url)

    def test_url_and_note_types_reach_the_raw_contract(self):
        cases = [
            (
                {"type": "url", "content": "https://example.com/article", "title": "URL"},
                ['type: url', 'url: "https://example.com/article"'],
            ),
            (
                {"type": "note", "content": "Remember this", "title": "Note"},
                ["type: note", "Remember this"],
            ),
        ]
        for payload, expected_lines in cases:
            with self.subTest(capture_type=payload["type"]):
                response = self.request(
                    json={**payload, "tags": ["contract"], "source": "codex-mcp"},
                    headers=self.auth(),
                )

            self.assertEqual(response.status_code, 200, response.text)
            raw_text = (self.root / response.json()["path"]).read_text()
            for expected in expected_lines:
                self.assertIn(expected, raw_text)
            if payload["type"] == "note":
                self.assertNotIn("\nurl:", raw_text)

    def test_identical_requests_are_explicitly_non_idempotent(self):
        payload = {
            "type": "note",
            "content": "Same capture",
            "title": "Duplicate contract",
            "tags": ["contract"],
            "source": "codex-mcp",
        }

        first = self.request(json=payload, headers=self.auth())
        second = self.request(json=payload, headers=self.auth())

        self.assertEqual(first.status_code, 200, first.text)
        self.assertEqual(second.status_code, 200, second.text)
        self.assertNotEqual(first.json()["path"], second.json()["path"])
        self.assertTrue((self.root / first.json()["path"]).is_file())
        self.assertTrue((self.root / second.json()["path"]).is_file())
        self.assertEqual(len(list(self.raw_dir.glob("*.md"))), 2)

    def test_json_tags_require_a_list_of_strings(self):
        invalid_tags = [
            "scalar",
            42,
            {"not": "a tag"},
            None,
            ["valid", 42],
            ["valid", None],
            ["valid", {"not": "a tag"}],
        ]
        for tags in invalid_tags:
            with self.subTest(tags=tags):
                before = set(self.raw_dir.glob("*.md"))
                response = self.request(
                    json={"type": "note", "content": "capture", "tags": tags},
                    headers=self.auth(),
                )

                self.assertEqual(response.status_code, 400)
                self.assertEqual(set(self.raw_dir.glob("*.md")), before)

    def test_form_and_query_string_tags_remain_supported(self):
        expected = ["one", "key: value", "#hash"]
        requests = [
            {"data": {"type": "note", "content": "form", "tags": ",".join(expected)}},
            {"params": {"type": "note", "content": "query", "tags": ",".join(expected)}},
        ]
        for request_data in requests:
            with self.subTest(transport=next(iter(request_data))):
                response = self.request(**request_data, headers=self.auth())

                self.assertEqual(response.status_code, 200, response.text)
                self.assertEqual(self.frontmatter(response)["tags"], expected)


if __name__ == "__main__":
    unittest.main()
