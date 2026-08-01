from __future__ import annotations
import hashlib, json, shutil, sys, tempfile, threading, time, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "control"))
from chatgpt_runner_bridge import Bridge, release_sha256
from local_watcher import LocalWatcher

class BridgeSmokeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(); self.root = Path(self.tmp.name) / "repo"
        for name in ("control", "runners"): shutil.copytree(ROOT / name, self.root / name, ignore=shutil.ignore_patterns("logs", "state", "transport", "__pycache__"))
        (self.root / "control" / "logs").mkdir(); (self.root / "control" / "state").mkdir()
        self.release = self.root / "runners" / "CURRENT_RELEASE.json"

    def tearDown(self) -> None: self.tmp.cleanup()
    def request(self, **overrides):
        value = {"request_id": "test-001", "request_type": "connection_test", "episode_id": "CONNECTION_TEST", "payload": {}}
        value.update(overrides); return value
    def bridge(self): return Bridge(root=self.root, release_path=self.release)

    def test_connection_test_succeeds(self):
        outcome = self.bridge().run(self.request())
        self.assertEqual(outcome["result"], "CONNECTION_TEST_SUCCESS"); self.assertEqual(outcome["status"], "SUCCESS")
        self.assertTrue((self.root / outcome["output_manifest"]).is_file())

    def test_unapproved_and_tampered_temp_release_are_rejected(self):
        release = json.loads(self.release.read_text()); release["status"] = "CANDIDATE"; self.release.write_text(json.dumps(release))
        with self.assertRaisesRegex(Exception, "CURRENT_RELEASE_NOT_APPROVED"): self.bridge().run(self.request())
        release["status"] = "APPROVED"; release["sha256"] = "0" * 64; self.release.write_text(json.dumps(release))
        with self.assertRaisesRegex(Exception, "RUNNER_SHA256_MISMATCH"): self.bridge().run(self.request())
        self.assertEqual(json.loads((ROOT / "runners" / "CURRENT_RELEASE.json").read_text())["status"], "APPROVED")

    def test_unknown_manifest_with_zero_exit_is_blocked(self):
        runner = self.root / "runners" / "releases" / "1.0.0" / "runner.py"
        runner.write_text("import argparse,json\np=argparse.ArgumentParser();p.add_argument('--request');p.add_argument('--output-manifest');a=p.parse_args();open(a.output_manifest,'w').write(json.dumps({'status':'RUNNER_READY','runner_version':'1.0.0'}))")
        release = json.loads(self.release.read_text()); release["sha256"] = release_sha256(runner); self.release.write_text(json.dumps(release))
        outcome = self.bridge().run(self.request(request_type="episode", episode_id="EP-1")); self.assertEqual(outcome["status"], "BLOCKED")

    def test_running_manifest_is_not_promoted_to_success(self):
        runner = self.root / "runners" / "releases" / "1.0.0" / "runner.py"
        runner.write_text("import argparse,json\np=argparse.ArgumentParser();p.add_argument('--request');p.add_argument('--output-manifest');a=p.parse_args();open(a.output_manifest,'w').write(json.dumps({'status':'RUNNING','runner_version':'1.0.0'}))")
        release = json.loads(self.release.read_text()); release["sha256"] = release_sha256(runner); self.release.write_text(json.dumps(release))
        self.assertEqual(self.bridge().run(self.request(request_type="episode", episode_id="EP-1"))["status"], "RUNNING")

    def test_waiting_resume_keeps_completed_stages_and_locked_runner(self):
        waiting = self.bridge().run(self.request(request_type="episode", episode_id="EP-1", payload={"flow_asset_ready": False}))
        self.assertEqual(waiting["status"], "WAITING_FOR_FLOW_ASSET")
        resumed = self.bridge().run(self.request(request_id="test-002", request_type="episode", episode_id="EP-1", payload={"flow_asset_ready": True}, resume_run_id=Path(waiting["state_path"]).stem.replace(".state", "")))
        manifest = json.loads((self.root / resumed["output_manifest"]).read_text())
        self.assertEqual(resumed["status"], "SUCCESS"); self.assertEqual(manifest["completed_stages"].count("preflight"), 1)
        self.assertEqual(resumed["locked_release"]["runner_version"], "1.0.0")

    def test_inflight_episode_uses_old_runner_after_release_update(self):
        runner = self.root / "runners" / "releases" / "1.0.0" / "runner.py"; signal = self.root / "started"; gate = self.root / "continue"
        runner.write_text(f"import argparse,json,time\np=argparse.ArgumentParser();p.add_argument('--request');p.add_argument('--output-manifest');a=p.parse_args();open(r'{signal}','w').write('x')\nwhile not __import__('pathlib').Path(r'{gate}').exists(): time.sleep(.01)\nopen(a.output_manifest,'w').write(json.dumps({{'status':'SUCCESS','runner_version':'1.0.0','completed_stages':['render']}}))")
        release = json.loads(self.release.read_text()); release["sha256"] = release_sha256(runner); self.release.write_text(json.dumps(release))
        result = {}; thread = threading.Thread(target=lambda: result.setdefault("outcome", self.bridge().run(self.request(request_type="episode", episode_id="EP-2")))); thread.start()
        while not signal.exists(): time.sleep(.01)
        release["runner_version"] = "1.0.1"; self.release.write_text(json.dumps(release)); gate.write_text("go"); thread.join(3)
        self.assertEqual(result["outcome"]["locked_release"]["runner_version"], "1.0.0")

    def test_watcher_processes_transport_request_without_manual_bridge_command(self):
        inbox = self.root / "control" / "transport" / "inbox"; inbox.mkdir(parents=True); (inbox / "watch-001.json").write_text(json.dumps(self.request(request_id="watch-001")))
        self.assertEqual(LocalWatcher(root=self.root, sync=False).process_once(), 1)
        outcome = json.loads((self.root / "control" / "transport" / "results" / "watch-001.json").read_text())
        self.assertEqual(outcome["outcome"]["status"], "SUCCESS")

if __name__ == "__main__": unittest.main()
