#!/usr/bin/env python3
"""Always-on, single-consumer transport watcher for ChatGPT run requests."""
from __future__ import annotations
import argparse, json, shutil, subprocess, time
from pathlib import Path
from chatgpt_runner_bridge import Bridge

ROOT = Path(__file__).resolve().parents[1]

class LocalWatcher:
    def __init__(self, root: Path = ROOT, poll_seconds: float = 10, sync: bool = True) -> None:
        self.root, self.poll_seconds, self.sync = root.resolve(), poll_seconds, sync
        self.inbox = self.root / "control" / "transport" / "inbox"
        self.processing = self.root / "control" / "transport" / "processing"
        self.results = self.root / "control" / "transport" / "results"

    def sync_transport(self) -> None:
        if not self.sync: return
        completed = subprocess.run(["git", "pull", "--ff-only"], cwd=self.root, capture_output=True, text=True, check=False)
        if completed.returncode: raise RuntimeError("TRANSPORT_SYNC_FAILED: " + completed.stderr.strip())

    def process_once(self) -> int:
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
            completed = subprocess.run(["git", "add", "control/transport/results"], cwd=self.root, capture_output=True, text=True, check=False)
            completed = subprocess.run(["git", "commit", "-m", "chore(transport): publish watcher results"], cwd=self.root, capture_output=True, text=True, check=False)
            if completed.returncode:
                raise RuntimeError("TRANSPORT_RESULT_COMMIT_FAILED: " + completed.stderr.strip())
            completed = subprocess.run(["git", "push"], cwd=self.root, capture_output=True, text=True, check=False)
            if completed.returncode:
                raise RuntimeError("TRANSPORT_RESULT_PUSH_FAILED: " + completed.stderr.strip())
        return count

    def serve(self, once: bool = False) -> None:
        while True:
            self.process_once()
            if once: return
            time.sleep(self.poll_seconds)

def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--once", action="store_true"); parser.add_argument("--poll-seconds", type=float, default=10); parser.add_argument("--no-sync", action="store_true")
    args = parser.parse_args(); LocalWatcher(poll_seconds=args.poll_seconds, sync=not args.no_sync).serve(args.once); return 0
if __name__ == "__main__": raise SystemExit(main())
