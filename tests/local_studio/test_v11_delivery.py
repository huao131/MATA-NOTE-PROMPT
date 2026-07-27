from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from mata_studio.app import StudioApp
from mata_studio.git_context import build_git_context


class GitBuildContextTests(unittest.TestCase):
    def setUp(self) -> None:
        self.git_executable = r"C:\Users\huao3\AppData\Local\GitHubDesktop\app-3.6.3\resources\app\git\cmd\git.exe"

    def _init_repo(self, repo_root: Path) -> None:
        subprocess.run([self.git_executable, "-C", str(repo_root), "init"], check=True, capture_output=True, text=True)
        subprocess.run([self.git_executable, "-C", str(repo_root), "config", "user.name", "Test User"], check=True, capture_output=True, text=True)
        subprocess.run([self.git_executable, "-C", str(repo_root), "config", "user.email", "test@example.com"], check=True, capture_output=True, text=True)
        (repo_root / "README.md").write_text("hello\n", encoding="utf-8")
        subprocess.run([self.git_executable, "-C", str(repo_root), "add", "README.md"], check=True, capture_output=True, text=True)
        subprocess.run([self.git_executable, "-C", str(repo_root), "commit", "-m", "initial"], check=True, capture_output=True, text=True)

    def test_git_build_context_returns_expected_values(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            self._init_repo(repo_root)
            subprocess.run([self.git_executable, "-C", str(repo_root), "remote", "add", "origin", "https://github.com/example/repo.git"], check=True, capture_output=True, text=True)

            context = build_git_context(repo_root=repo_root, git_executable=self.git_executable)

            self.assertEqual(context["status"], "OK")
            self.assertEqual(context["worktree_path"], str(repo_root.resolve()))
            self.assertTrue(context["branch"])
            self.assertTrue(context["commit_sha"])
            self.assertEqual(context["remote_repository"], "https://github.com/example/repo.git")

    def test_git_build_context_returns_unavailable_on_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            context = build_git_context(repo_root=Path(temp_dir) / "missing", git_executable=self.git_executable)
            self.assertEqual(context["status"], "GIT_BUILD_CONTEXT_UNAVAILABLE")

    def test_git_build_context_reports_dirty_state(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            self._init_repo(repo_root)
            (repo_root / "README.md").write_text("edited\n", encoding="utf-8")

            context = build_git_context(repo_root=repo_root, git_executable=self.git_executable)

            self.assertTrue(context["working_tree_dirty"])
            self.assertGreaterEqual(context["uncommitted_changes_count"], 1)


class DashboardDeliveryTests(unittest.TestCase):
    def test_v11_dashboard_copy_and_labels_are_present(self) -> None:
        root = Path(__file__).resolve().parents[2]
        app_js = (root / "src" / "mata_studio" / "web" / "app.js").read_text(encoding="utf-8")
        index_html = (root / "src" / "mata_studio" / "web" / "index.html").read_text(encoding="utf-8")

        self.assertIn("LOCAL STUDIO V1.1", index_html)
        self.assertIn("CHATGPT WORK PACKAGE BRIDGE", index_html)
        self.assertIn("建立新劇集", app_js)
        self.assertIn("故事、腳本與分鏡", app_js)
        self.assertIn("關鍵影格工作室", app_js)
        self.assertIn("Google Drive資產", app_js)
        self.assertIn("Google Drive：未連線", app_js)
        self.assertIn("生產交接", app_js)
        self.assertNotIn("最新一集", app_js)
        self.assertNotIn("Drive Asset Browser", app_js)
        self.assertNotIn("Production Handoff", app_js)

    def test_status_exposes_dashboard_build_context_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            app = StudioApp(temp_dir)
            status = app.status()
            self.assertIn("git_build_context", status)
            self.assertIn("specification_context", status)
            self.assertIn("google_drive_sync_status", status)
            self.assertIn("working_tree_dirty", status)
            self.assertIn("uncommitted_changes_count", status)
