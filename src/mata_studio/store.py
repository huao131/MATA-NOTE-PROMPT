"""SQLite project index; Google Drive remains the formal media source."""

from __future__ import annotations

import json
import shutil
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

from .constants import GATES
from .errors import StudioError

DDL = """
PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS migrations(version INTEGER PRIMARY KEY, applied_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS series(series_id TEXT PRIMARY KEY,name TEXT NOT NULL,drive_folder_id TEXT UNIQUE,created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS episodes(episode_id TEXT PRIMARY KEY,series_id TEXT NOT NULL REFERENCES series(series_id),title TEXT NOT NULL,brief_json TEXT NOT NULL,production_state TEXT NOT NULL,drive_folder_id TEXT UNIQUE,created_at TEXT NOT NULL,updated_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS artifacts(artifact_id TEXT PRIMARY KEY,episode_id TEXT NOT NULL REFERENCES episodes(episode_id),artifact_type TEXT NOT NULL,version TEXT NOT NULL,lifecycle_status TEXT NOT NULL,approval_status TEXT NOT NULL,lock_status TEXT NOT NULL,payload_json TEXT NOT NULL,drive_file_id TEXT,created_at TEXT NOT NULL,UNIQUE(episode_id,artifact_type,version));
CREATE TABLE IF NOT EXISTS gates(episode_id TEXT NOT NULL REFERENCES episodes(episode_id),gate_id TEXT NOT NULL,gate_status TEXT NOT NULL,submitted_version TEXT,PRIMARY KEY(episode_id,gate_id));
CREATE TABLE IF NOT EXISTS approval_events(event_id INTEGER PRIMARY KEY AUTOINCREMENT,episode_id TEXT NOT NULL,gate_id TEXT NOT NULL,decision TEXT NOT NULL,approver TEXT NOT NULL,approved_at TEXT NOT NULL,artifact_version TEXT NOT NULL,evidence TEXT NOT NULL,comment TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS assets(asset_id TEXT PRIMARY KEY,episode_id TEXT NOT NULL REFERENCES episodes(episode_id),version TEXT NOT NULL,lifecycle_status TEXT NOT NULL,exact_asset INTEGER NOT NULL,rejected INTEGER NOT NULL,drive_file_id TEXT,drive_folder_id TEXT,mime_type TEXT,file_size INTEGER,web_view_link TEXT,metadata_json TEXT NOT NULL,UNIQUE(episode_id,asset_id,version));
CREATE TABLE IF NOT EXISTS events(event_id INTEGER PRIMARY KEY AUTOINCREMENT,kind TEXT NOT NULL,payload_json TEXT NOT NULL,created_at TEXT NOT NULL);
"""


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


class ProjectStore:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.initialize()

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys=ON")
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def initialize(self) -> None:
        with self.connect() as db:
            db.executescript(DDL)
            db.execute("INSERT OR IGNORE INTO migrations VALUES(1,?)", (now(),))

    def backup(self, destination: str | Path) -> Path:
        target = Path(destination)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(self.path, target)
        return target

    def export_manifest(self) -> dict[str, Any]:
        return {"schema_version": 1, "series": self.list_series(), "episodes": self.list_episodes()}

    def create_series(self, series_id: str, name: str) -> dict[str, Any]:
        if not series_id.strip() or not name.strip():
            raise StudioError("INVALID_SERIES", "series_id 與名稱不得為空。")
        try:
            with self.connect() as db:
                db.execute("INSERT INTO series(series_id,name,created_at) VALUES(?,?,?)", (series_id, name, now()))
        except sqlite3.IntegrityError as error:
            raise StudioError("DUPLICATE_SERIES", "Series 已存在。", status=409) from error
        return self.get_series(series_id)

    def list_series(self) -> list[dict[str, Any]]:
        with self.connect() as db:
            return [dict(row) for row in db.execute("SELECT * FROM series ORDER BY created_at DESC")]

    def get_series(self, series_id: str) -> dict[str, Any]:
        with self.connect() as db:
            row = db.execute("SELECT * FROM series WHERE series_id=?", (series_id,)).fetchone()
        if row is None:
            raise StudioError("SERIES_NOT_FOUND", "找不到 Series。", status=404)
        return dict(row)

    def create_episode(self, brief: dict[str, Any]) -> dict[str, Any]:
        stamp = now()
        try:
            with self.connect() as db:
                db.execute(
                    "INSERT INTO episodes(episode_id,series_id,title,brief_json,production_state,created_at,updated_at) VALUES(?,?,?,?,?,?,?)",
                    (brief["episode_id"], brief["series_id"], brief["title"], json.dumps(brief, ensure_ascii=False), "AWAITING_CREATIVE_INPUT", stamp, stamp),
                )
                for gate_id in GATES:
                    db.execute("INSERT INTO gates VALUES(?,?,?,NULL)", (brief["episode_id"], gate_id, "PENDING"))
        except sqlite3.IntegrityError as error:
            raise StudioError("EPISODE_CREATE_CONFLICT", str(error), status=409) from error
        return self.get_episode(brief["episode_id"])

    def list_episodes(self) -> list[dict[str, Any]]:
        with self.connect() as db:
            return [self._episode(row) for row in db.execute("SELECT * FROM episodes ORDER BY created_at DESC")]

    def get_episode(self, episode_id: str) -> dict[str, Any]:
        with self.connect() as db:
            row = db.execute("SELECT * FROM episodes WHERE episode_id=?", (episode_id,)).fetchone()
        if row is None:
            raise StudioError("EPISODE_NOT_FOUND", "找不到 Episode。", status=404)
        return self._episode(row)

    @staticmethod
    def _episode(row: sqlite3.Row) -> dict[str, Any]:
        item = dict(row)
        item["brief"] = json.loads(item.pop("brief_json"))
        return item

    def update_episode(self, episode_id: str, values: dict[str, Any]) -> dict[str, Any]:
        allowed = {"title", "production_state", "drive_folder_id"}
        updates = {key: value for key, value in values.items() if key in allowed}
        if not updates:
            raise StudioError("NO_VALID_EPISODE_FIELDS", "沒有可更新欄位。")
        updates["updated_at"] = now()
        clause = ", ".join(f"{key}=?" for key in updates)
        with self.connect() as db:
            cursor = db.execute(f"UPDATE episodes SET {clause} WHERE episode_id=?", (*updates.values(), episode_id))
        if cursor.rowcount != 1:
            raise StudioError("EPISODE_NOT_FOUND", "找不到 Episode。", status=404)
        return self.get_episode(episode_id)

    def gates(self, episode_id: str) -> list[dict[str, Any]]:
        with self.connect() as db:
            return [dict(row) for row in db.execute("SELECT * FROM gates WHERE episode_id=? ORDER BY rowid", (episode_id,))]

    def artifacts(self, episode_id: str) -> list[dict[str, Any]]:
        with self.connect() as db:
            rows = db.execute("SELECT * FROM artifacts WHERE episode_id=? ORDER BY created_at", (episode_id,))
            return [self._artifact(row) for row in rows]

    def artifact(self, artifact_id: str) -> dict[str, Any]:
        with self.connect() as db:
            row = db.execute("SELECT * FROM artifacts WHERE artifact_id=?", (artifact_id,)).fetchone()
        if row is None:
            raise StudioError("ARTIFACT_NOT_FOUND", "找不到 Artifact。", status=404)
        return self._artifact(row)

    @staticmethod
    def _artifact(row: sqlite3.Row) -> dict[str, Any]:
        item = dict(row)
        item["payload"] = json.loads(item.pop("payload_json"))
        return item

    def insert_artifact(self, record: dict[str, Any]) -> dict[str, Any]:
        try:
            with self.connect() as db:
                db.execute(
                    "INSERT INTO artifacts VALUES(?,?,?,?,?,?,?,?,?,?)",
                    (record["artifact_id"], record["episode_id"], record["artifact_type"], record["version"], record["lifecycle_status"], record["approval_status"], record["lock_status"], json.dumps(record["payload"], ensure_ascii=False), record.get("drive_file_id"), now()),
                )
        except sqlite3.IntegrityError as error:
            raise StudioError("ARTIFACT_VERSION_CONFLICT", str(error), status=409) from error
        return self.artifact(record["artifact_id"])

    def submit_gate(self, episode_id: str, gate_id: str, version: str) -> None:
        with self.connect() as db:
            db.execute("UPDATE gates SET gate_status='SUBMITTED',submitted_version=? WHERE episode_id=? AND gate_id=?", (version, episode_id, gate_id))

    def decide_gate(self, episode_id: str, gate_id: str, decision: str, event: dict[str, str]) -> None:
        with self.connect() as db:
            db.execute("UPDATE gates SET gate_status=? WHERE episode_id=? AND gate_id=?", (decision, episode_id, gate_id))
            db.execute(
                "INSERT INTO approval_events(episode_id,gate_id,decision,approver,approved_at,artifact_version,evidence,comment) VALUES(?,?,?,?,?,?,?,?)",
                (episode_id, gate_id, decision, event["approver"], event["approved_at"], event["artifact_version"], event["evidence"], event["comment"]),
            )

    def assets(self, episode_id: str) -> list[dict[str, Any]]:
        with self.connect() as db:
            return [dict(row) for row in db.execute("SELECT * FROM assets WHERE episode_id=?", (episode_id,))]

    def asset(self, asset_id: str) -> dict[str, Any]:
        with self.connect() as db:
            row = db.execute("SELECT * FROM assets WHERE asset_id=?", (asset_id,)).fetchone()
        if row is None:
            raise StudioError("ASSET_NOT_FOUND", "找不到 Asset。", status=404)
        return dict(row)

    def insert_asset(self, item: dict[str, Any]) -> dict[str, Any]:
        try:
            with self.connect() as db:
                db.execute(
                    "INSERT INTO assets VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                    (item["asset_id"], item["episode_id"], item["version"], item.get("lifecycle_status", "DRAFT"), int(bool(item.get("exact_asset"))), int(item.get("lifecycle_status") == "REJECTED"), item.get("drive_file_id"), item.get("drive_folder_id"), item.get("mime_type"), item.get("file_size"), item.get("web_view_link"), json.dumps(item, ensure_ascii=False)),
                )
        except sqlite3.IntegrityError as error:
            raise StudioError("ASSET_CONFLICT", str(error), status=409) from error
        return self.asset(item["asset_id"])
