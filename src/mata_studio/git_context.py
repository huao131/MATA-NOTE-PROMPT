"""Git build context helpers for the local studio dashboard."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any


def build_git_context(*, repo_root: str | Path, git_executable: str | None = None) -> dict[str, Any]:
    repo_path = Path(repo_root).resolve()
    git_cmd = git_executable or r"C:\Users\huao3\AppData\Local\GitHubDesktop\app-3.6.3\resources\app\git\cmd\git.exe"
    try:
        branch = subprocess.run([git_cmd, "-C", str(repo_path), "branch", "--show-current"], check=False, capture_output=True, text=True).stdout.strip()
        commit_sha = subprocess.run([git_cmd, "-C", str(repo_path), "rev-parse", "HEAD"], check=False, capture_output=True, text=True).stdout.strip()
        remote = subprocess.run([git_cmd, "-C", str(repo_path), "config", "--get", "remote.origin.url"], check=False, capture_output=True, text=True).stdout.strip()
        status = subprocess.run([git_cmd, "-C", str(repo_path), "status", "--porcelain"], check=False, capture_output=True, text=True).stdout.splitlines()
        if not branch or not commit_sha:
            raise RuntimeError("Git context unavailable")
        return {
            "status": "OK",
            "worktree_path": str(repo_path),
            "branch": branch,
            "commit_sha": commit_sha,
            "remote_repository": remote or "",
            "working_tree_dirty": bool(status),
            "uncommitted_changes_count": len(status),
        }
    except Exception:
        return {
            "status": "GIT_BUILD_CONTEXT_UNAVAILABLE",
            "worktree_path": str(repo_path),
            "branch": "",
            "commit_sha": "",
            "remote_repository": "",
            "working_tree_dirty": False,
            "uncommitted_changes_count": 0,
        }
