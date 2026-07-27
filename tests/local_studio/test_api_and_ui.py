from __future__ import annotations

import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

from mata_studio.api import handler_factory
from mata_studio.app import StudioApp


class ApiUiTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        app = StudioApp(self.temp.name)
        web = Path(__file__).parents[2] / "src" / "mata_studio" / "web"
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), handler_factory(app, web))
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base = f"http://127.0.0.1:{self.server.server_port}"

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.temp.cleanup()

    def get(self, path):
        with urllib.request.urlopen(self.base + path) as response:
            return response.status, response.read().decode()

    def test_ui_starts(self):
        status, body = self.get("/")
        self.assertEqual(status, 200)
        self.assertIn("MATA AI VIDEO STUDIO", body)

    def test_status_api(self):
        status, body = self.get("/api/system/status")
        self.assertEqual(status, 200)
        self.assertIn("localhost-only", body)

    def test_drive_status_api(self):
        _, body = self.get("/api/system/drive-status")
        self.assertIn("NOT_CONNECTED", body)

    def test_openapi_document(self):
        _, body = self.get("/api/openapi.json")
        self.assertIn('"openapi": "3.1.0"', body)

    def test_pages_exist(self):
        _, body = self.get("/")
        for title in ("Dashboard", "New Episode", "Creative Studio", "Story & Storyboard", "Visual Bible", "Keyframe Studio", "Drive Asset Browser", "Production Handoff", "Settings"):
            self.assertIn(title, body)

    def test_missing_route_structured(self):
        with self.assertRaises(urllib.error.HTTPError) as caught:
            self.get("/api/not-found")
        self.assertEqual(caught.exception.code, 404)
        self.assertIn("ROUTE_NOT_FOUND", caught.exception.read().decode())
        caught.exception.close()
