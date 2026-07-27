"""Specification context resolver for V1.1."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


class SpecificationResolver:
    """Resolve a minimal specification context from a Git ref or local worktree."""

    def __init__(self, repo_root: str | Path, ref: str | None = None):
        self.repo_root = Path(repo_root)
        self.ref = ref or 'HEAD'

    def _git(self, *args: str) -> str:
        result = subprocess.run(
            ['git', '-C', str(self.repo_root), *args],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or result.stdout.strip() or 'git command failed')
        return result.stdout.strip()

    def resolve(self, files: list[str]) -> dict[str, Any]:
        try:
            commit = self._git('rev-parse', self.ref)
            source_ref = self.ref
        except Exception:
            return {'status': 'SPECIFICATION_CONTEXT_UNAVAILABLE', 'reason': 'Git ref unavailable'}

        documents: list[dict[str, Any]] = []
        for relative_path in files:
            path = self.repo_root / relative_path
            if not path.exists():
                return {'status': 'SPECIFICATION_CONTEXT_UNAVAILABLE', 'reason': f'missing file {relative_path}'}
            content = path.read_bytes()
            documents.append({
                'path': relative_path,
                'sha256': hashlib.sha256(content).hexdigest(),
                'size': len(content),
            })

        return {
            'status': 'OK',
            'source_ref': source_ref,
            'source_commit_sha': commit,
            'documents': documents,
            'sop_version': 'V2.0',
            'cached': False,
        }
