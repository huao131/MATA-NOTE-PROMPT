#!/usr/bin/env python3
"""Always-on, single-consumer transport watcher for ChatGPT run requests."""
from __future__ import annotations
import argparse, atexit, json, os, subprocess, threading, time
from datetime import datetime, timezone
from pathlib import Path
from chatgpt_runner_bridge import Bridge
from github_api_transport import AuthRequired, GitHubApiTransport, TransportError

ROOT = Path(__file__).resolve().parents[1]

class LocalWatcher:
    def __init__(self, root: Path = ROOT, poll_seconds: float = 10, sync: bool = True) -> None:
        self.root, self.poll_seconds, self.sync = root.resolve(), poll_seconds, sync
        self.inbox = self.root / "control" / "transport" / "inbox"
        self.processing = self.root / "control" / "transport" / "processing"
        self.results = self.root / "control" / "transport" / "results"
        self.runtime = self.root / "control" / "runtime"
        self.pid_path = self.runtime / "local_watcher.pid"
        self.heartbeat_path = self.runtime / "local_watcher.heartbeat.json"
        self.log_path = self.runtime / "local_watcher.log"
        self.transport_mode = os.environ.get("TRANSPORT_MODE", "git").lower()
        self.git_lock = threading.Lock()

    def log(self, message: str) -> None:
        self.runtime.mkdir(parents=True, exist_ok=True)
        with self.log_path.open("a", encoding="utf-8") as output:
            output.write(f"{datetime.now(timezone.utc).isoformat()} {message}\n")

    def _pid_is_running(self, pid: int) -> bool:
        try:
            os.kill(pid, 0)
            return True
        except (OSError, ValueError):
            return False

    def acquire_lock(self) -> None:
        self.runtime.mkdir(parents=True, exist_ok=True)
        if self.pid_path.exists():
            try:
                existing = int(self.pid_path.read_text(encoding="utf-8").strip())
            except ValueError:
                existing = 0
            if existing and self._pid_is_running(existing):
                raise RuntimeError(f"WATCHER_ALREADY_RUNNING:{existing}")
            self.pid_path.unlink(missing_ok=True)
        try:
            descriptor = os.open(self.pid_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError as error:
            raise RuntimeError("WATCHER_ALREADY_RUNNING") from error
        with os.fdopen(descriptor, "w", encoding="utf-8") as output:
            output.write(str(os.getpid()))
        self.log(f"WATCHER_STARTED pid={os.getpid()}")
        atexit.register(lambda: self.pid_path.unlink(missing_ok=True))

    def heartbeat(self, status: str, error: str | None = None) -> None:
        self.runtime.mkdir(parents=True, exist_ok=True)
        self.heartbeat_path.write_text(json.dumps({"pid": os.getpid(), "status": status, "updated_at": datetime.now(timezone.utc).isoformat(), "error": error}, ensure_ascii=False, indent=2), encoding="utf-8")

    def sync_transport(self) -> None:
        if not self.sync or self.transport_mode in {"file_queue", "github_api"}: return
        environment = os.environ.copy()
        environment["GIT_TERMINAL_PROMPT"] = "0"
        environment["GCM_INTERACTIVE"] = "Never"
        environment["GIT_ASKPASS"] = ""
        environment["SSH_ASKPASS"] = ""
        commands = [["fetch", "--prune", "origin"], ["reset", "--hard", "origin/agent/issue-14-runner-bridge"]]
        with self.git_lock:
            for step in commands:
                try:
                    completed = subprocess.run(["git", "-c", f"safe.directory={self.root}"] + step, cwd=self.root, capture_output=True, text=True, check=False, timeout=30, env=environment)
                except subprocess.TimeoutExpired:
                    self.log("TRANSPORT_RETRY step=" + step[0] + " reason=timeout")
                    raise RuntimeError("TRANSPORT_RETRY: " + step[0] + " timeout")
                if completed.returncode:
                    self.log("TRANSPORT_RETRY step=" + step[0] + " exit=" + str(completed.returncode) + " error=" + completed.stderr.strip())
                    raise RuntimeError("TRANSPORT_RETRY: " + step[0] + " exit=" + str(completed.returncode))
                self.log("TRANSPORT_SYNC step=" + step[0] + " ok")

    def process_once(self) -> int:
        if self.transport_mode == "github_rest_api":
            return self.process_github_api()
        self.sync_transport()
        for folder in (self.inbox, self.processing, self.results): folder.mkdir(parents=True, exist_ok=True)
        count = 0
        for source in sorted(self.inbox.glob("*.json")):
            claimed = self.processing / source.name
            try: source.replace(claimed)  # atomic claim: a request has exactly one local consumer
            except FileNotFoundError: continue
            try:
                request = json.loads(claimed.read_text(encoding="utf-8")); outcome = Bridge(root=self.root).run(request)
            except Exception as error:
                outcome = {"result": "BLOCKED", "status": "BLOCKED", "error": str(error)}
            result = {"request_id": request.get("request_id", claimed.stem) if 'request' in locals() else claimed.stem, "transport_status": "COMPLETED", "outcome": outcome}
            (self.results / source.name).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
            claimed.unlink(missing_ok=True); count += 1
        if count and self.sync:
            git = ["git", "-c", f"safe.directory={self.root}"]
            completed = subprocess.run(git + ["add", "-A", "control/transport"], cwd=self.root, capture_output=True, text=True, check=False)
            completed = subprocess.run(git + ["commit", "-m", "chore(transport): publish watcher results"], cwd=self.root, capture_output=True, text=True, check=False)
            if completed.returncode:
                raise RuntimeError("TRANSPORT_RESULT_COMMIT_FAILED: " + completed.stderr.strip())
            completed = subprocess.run(git + ["push"], cwd=self.root, capture_output=True, text=True, check=False)
            if completed.returncode:
                raise RuntimeError("TRANSPORT_RESULT_PUSH_FAILED: " + completed.stderr.strip())
        return count

    def process_github_api(self) -> int:
        transport = GitHubApiTransport()
        count = 0
        for item in transport.inbox():
            if item.get("type") != "file" or not item["name"].endswith(".json"):
                continue
            request_value = transport.read(item["path"])
            result_path = self.results / (request_value["request_id"] + ".json")
            if result_path.exists():
                continue
            try:
                outcome = Bridge(root=self.root).run(request_value)
            except Exception as exc:
                outcome = {"result":"BLOCKED","status":"BLOCKED","error":str(exc)}
            value = {"request_id":request_value["request_id"],"transport_status":"COMPLETED","outcome":outcome}
            transport.result(request_value["request_id"], value)
            result_path.parent.mkdir(parents=True, exist_ok=True); result_path.write_text(json.dumps(value), encoding="utf-8")
            count += 1
        return count

    def serve(self, once: bool = False) -> None:
        self.acquire_lock()
        try:
            while True:
                try:
                    count = self.process_once()
                    self.heartbeat("RUNNING", None)
                    if count:
                        self.log(f"REQUESTS_PROCESSED count={count}")
                except Exception as error:
                    self.heartbeat("AUTH_REQUIRED" if isinstance(error, AuthRequired) else "TRANSPORT_RETRY", str(error))
                    self.log(f"WATCHER_ERROR {error}")
                    if once: raise
                if once: return
                time.sleep(self.poll_seconds)
        finally:
            self.pid_path.unlink(missing_ok=True)
            self.log("WATCHER_STOPPED")

def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--once", action="store_true"); parser.add_argument("--poll-seconds", type=float, default=10); parser.add_argument("--no-sync", action="store_true")
    args = parser.parse_args(); LocalWatcher(poll_seconds=args.poll_seconds, sync=not args.no_sync).serve(args.once); return 0
if __name__ == "__main__": raise SystemExit(main())
