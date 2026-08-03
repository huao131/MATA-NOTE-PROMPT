import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "control"))
from chatgpt_runner_bridge import Bridge


class RenderFrameBridgeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        shutil.copytree(ROOT / "control" / "schemas", self.root / "control" / "schemas")
        self.episode = self.root / "episode"
        (self.episode / "03_視覺素材").mkdir(parents=True)
        self.generated = self.root / "generated.png"
        Image.new("RGB", (900, 1600), (40, 50, 60)).save(self.generated)

    def tearDown(self):
        self.tmp.cleanup()

    def request(self, role="START", action="prepare"):
        output = self.episode / "03_視覺素材" / f"20260803_SCENE_01_{role}_V1.png"
        payload = {
            "action": action, "episode_path": str(self.episode), "scene_id": "20260803_SCENE_01",
            "frame_role": role, "visual_prompt": "Historically accurate harbor departure scene with cinematic framing.",
            "negative_prompt": "text, tables, collage, watermark", "output_path": str(output),
            "width": 1080, "height": 1920,
        }
        if action == "complete": payload["generated_path"] = str(self.generated)
        return {"request_id": f"render-{role.lower()}-{action}", "request_type": "render_frame", "episode_id": "0803_COLUMBUS", "payload": payload}

    def test_prepare_routes_to_codex_job(self):
        result = Bridge(root=self.root).run(self.request())
        self.assertEqual(result["status"], "WAITING_FOR_CODEX_IMAGE")
        self.assertTrue((self.root / result["codex_job"]).is_file())

    def test_complete_copies_qc_and_updates_state(self):
        result = Bridge(root=self.root).run(self.request(action="complete"))
        self.assertEqual(result["status"], "SUCCESS")
        self.assertEqual(result["qc"]["status"], "PASS")
        self.assertTrue(Path(result["output_path"]).is_file())
        self.assertTrue(Path(result["asset_index"]).is_file())
        self.assertTrue(Path(result["production_state"]).is_file())

    def test_flow_prompt_after_start_and_end(self):
        Bridge(root=self.root).run(self.request("START", "complete"))
        result = Bridge(root=self.root).run(self.request("END", "complete"))
        self.assertTrue(Path(result["flow_prompt"]).is_file())


if __name__ == "__main__": unittest.main()
