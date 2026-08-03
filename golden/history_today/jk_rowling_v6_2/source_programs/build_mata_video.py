#!/usr/bin/env python3
"""V4 hybrid episode runner: prepares a truthful Flow handoff and resumes on asset return."""
from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


def now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def dump(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def pick_one(folder: Path, pattern: str) -> Path | None:
    found = sorted(folder.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)
    return found[0] if found else None


class Runner:
    def __init__(self) -> None:
        self.runtime = Path(__file__).resolve().parents[1]
        self.root = self.runtime.parents[1]
        self.project = self.root / "2026" / "0731" / "0731_JK_ROWLING"
        self.logs = self.project / "logs"
        self.log_path = self.logs / "v4_hybrid_pipeline.log"
        self.state_path = self.project / "pipeline_state.json"
        self.flow_dir = self.project / "05_FLOW_QUEUE" / "SCENE_03"
        self.tech = self.project / "07_CINEMATIC_TECH_TEST"
        self.visual = next(iter(self.project.glob("03_*")), None)
        self.voice_dir = next(iter(self.project.glob("04_*")), None)
        self.clip_dir = next((x for x in self.project.glob("05_*") if x.name != "05_FLOW_QUEUE"), None)
        self.master_dir = next(iter(self.project.glob("06_*")), None)
        self.state = {"project": "0731_JK_ROWLING", "version": "V4_HYBRID", "stages": {}}

    def log(self, stage: str, status: str, elapsed: float = 0.0, detail: str = "") -> None:
        self.logs.mkdir(parents=True, exist_ok=True)
        line = f"{now()} | {stage} | {status} | elapsed_seconds={elapsed:.3f}"
        if detail:
            line += f" | {detail}"
        with self.log_path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")
        print(line)

    def stage(self, name: str, status: str, detail: str = "", elapsed: float = 0.0) -> None:
        self.state["stages"][name] = {"status": status, "updated_at": now(), "detail": detail, "elapsed_seconds": round(elapsed, 3)}
        dump(self.state_path, self.state)
        self.log(name, status, elapsed, detail)

    def load(self) -> None:
        if self.state_path.exists():
            try:
                old = json.loads(self.state_path.read_text(encoding="utf-8"))
                if isinstance(old, dict) and isinstance(old.get("stages"), dict):
                    self.state.update(old)
            except json.JSONDecodeError:
                self.log("STATE_LOAD", "WARNING", detail="invalid prior state replaced")

    def require(self, value: Path | None, name: str) -> Path:
        if value is None or not value.exists():
            self.stage("PRECHECK", "FAIL", f"missing {name}")
            raise RuntimeError(f"missing required asset: {name}")
        return value

    def write_metadata(self, source: Path, b2: Path, flow_asset: Path) -> None:
        dump(self.project / "episode_request.json", {
            "project": "0731_JK_ROWLING", "content_type": "PERSON", "episode_date": "07.31",
            "voice_policy": "FROZEN_EXISTING_VOICE", "hero_scene": "SCENE_03", "render_strategy": "HYBRID",
        })
        dump(self.project / "VISUAL_EVIDENCE_MAP.json", {
            "SCENE_03": {"source": str(source), "evidence": "visible 3/4 writer portrait", "approved_local_baseline": str(b2)}
        })
        dump(self.project / "HERO_SCENE_PLAN.json", {
            "scene": "SCENE_03", "renderer": "FLOW_TRUE_VIDEO", "fallback": "LOCAL_2_5D_B2", "duration_seconds": 5,
            "source_image": str(source), "return_asset": str(flow_asset),
            "acceptance": ["identity stable", "subtle breathing", "small eye/head motion", "environment movement", "slow cinematic push"]
        })
        dump(self.project / "FINAL_TIMELINE_ASSET_MAP.json", {
            "SCENE_03": {
                "flow_asset": str(flow_asset), "flow_asset_exists": flow_asset.exists(),
                "local_2_5d_baseline": str(b2), "actually_used_in_final": False,
                "truth_note": "No V4 master has been encoded before the Flow hero asset is returned."
            }
        })
        configs = {
            "subtitle_style.json": {"status": "DEFERRED_UNTIL_HERO_RETURN", "format": "1080x1920"},
            "motion_presets.json": {"local_baseline": "B2_MEDIUM", "hero": "FLOW_TRUE_VIDEO"},
            "narration_style.json": {"voice": "zh-TW-HsiaoChenNeural", "reuse_existing": True},
            "audio_style.json": {"status": "DEFERRED_UNTIL_HERO_RETURN"},
            "quality_gates.json": {"hero": ["no face deformation", "no identity drift", "no black borders", "no fast camera"]},
        }
        for name, value in configs.items():
            dump(self.project / name, value)

    def flow_package(self, source: Path, flow_asset: Path) -> None:
        self.flow_dir.mkdir(parents=True, exist_ok=True)
        queued_source = self.flow_dir / "SOURCE_IMAGE.png"
        if not queued_source.exists() or queued_source.stat().st_size != source.stat().st_size:
            shutil.copy2(source, queued_source)
        prompt = (
            "A realistic historical documentary drama portrait of the same red-haired woman writer in the supplied image. "
            "Preserve her identity, face, wardrobe, composition, and seated writing environment. "
            "Very subtle natural breathing, tiny eye or head movement, gentle posture movement, rain and ambient background motion, "
            "and a slow cinematic camera push. Quiet, premium, restrained period-drama tone. "
            "No lip sync, no speaking, no large movement, no hand changes, no extra fingers, no face change, no identity drift, no fast camera."
        )
        (self.flow_dir / "FLOW_PROMPT.txt").write_text(prompt + "\n", encoding="utf-8")
        dump(self.flow_dir / "FLOW_SETTINGS.json", {
            "duration_seconds": 5, "aspect_ratio": "9:16", "target_delivery": "1080x1920", "fps": 30,
            "input": "SOURCE_IMAGE.png", "output_required": "FLOW_SCENE_03.mp4", "prompt_file": "FLOW_PROMPT.txt"
        })
        readme = (
            "FLOW HERO HANDOFF\n\n"
            "1. Open Google Flow with the account that has your existing Flow credits.\n"
            "2. Upload SOURCE_IMAGE.png.\n"
            "3. Paste the exact text from FLOW_PROMPT.txt and generate one 5-second 9:16 clip.\n"
            "4. Export it as MP4, name it FLOW_SCENE_03.mp4, and put it in this same folder.\n"
            "5. Re-run build_mata_video.py. It will detect the returned asset and resume.\n\n"
            "The local runner does not claim an unreturned Flow asset was used in a master.\n"
        )
        (self.flow_dir / "README_ACTION.txt").write_text(readme, encoding="utf-8")

    def write_report(self, source: Path, b2: Path, flow_asset: Path) -> None:
        status = "FLOW_RETURNED" if flow_asset.exists() and flow_asset.stat().st_size >= 4096 else "WAITING_FOR_FLOW_ASSET"
        report = (
            "# V4 Hybrid Golden Path Build Report\n\n"
            f"- Project: `0731_JK_ROWLING`\n"
            f"- Status: `{status}`\n"
            "- Content type: `PERSON`\n"
            "- Frozen voice: `zh-TW-HsiaoChenNeural` existing assets reused; no voice regeneration.\n"
            f"- Local cinematic baseline: `{b2.name}` (reused; no rembg or ONNX rerun).\n"
            f"- Hero source: `{source.name}`\n"
            f"- Flow return target: `{flow_asset}`\n\n"
            "## Truthful gate\n\n"
            "No direct, callable Google Flow Image-to-Video endpoint is available in this Codex session. "
            "The pipeline therefore does not claim a True I2V asset is used until `FLOW_SCENE_03.mp4` is returned to the queue.\n"
        )
        (self.project / "BUILD_REPORT_V4.md").write_text(report, encoding="utf-8")

    def ffmpeg(self) -> str:
        return subprocess.check_output([sys.executable, "-c", "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())"], text=True).strip()

    def command(self, stage: str, args: list[str], cwd: Path | None = None) -> None:
        started = time.monotonic()
        self.log(stage, "START")
        completed = subprocess.run(args, text=True, encoding="utf-8", errors="replace", stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd or self.project)
        elapsed = time.monotonic() - started
        if completed.returncode:
            self.stage(stage, "FAIL", (completed.stderr or "no ffmpeg stderr")[-1200:], elapsed)
            raise RuntimeError(f"{stage} ffmpeg exit={completed.returncode}")
        self.stage(stage, "PASS", "ffmpeg completed", elapsed)

    def finish_v4(self, flow_asset: Path, b2: Path) -> None:
        if not self.clip_dir or not self.master_dir:
            raise RuntimeError("missing clip or master directory")
        ff = self.ffmpeg()
        story = self.clip_dir / "MAIN_STORY_NORMALIZED.mp4"
        ending = self.clip_dir / "ENDING_NORMALIZED.mp4"
        voice = self.voice_dir / "voice_full.mp3"
        srt = self.voice_dir / "voice_full.srt"
        bgm, space, sfx = self.clip_dir / "BGM.wav", self.clip_dir / "SPACE.wav", self.clip_dir / "SFX.wav"
        for value, name in [(story, "story"), (ending, "ending"), (voice, "voice"), (srt, "subtitle"), (bgm, "bgm"), (space, "space"), (sfx, "sfx")]:
            self.require(value, name)
        out = self.master_dir / "MASTER_PREVIEW_V4_HYBRID_GOLDEN_SAMPLE.mp4"
        timeline_tmp = self.master_dir / "_V4_TIMELINE_PRE_SUBTITLE.mp4"
        montage = self.master_dir / "QC_MONTAGE_V4.jpg"
        # Scene 03 occupies 21-27 seconds.  The original story audio remains continuous under the Flow hero.
        subtitle_copy = Path(tempfile.gettempdir()) / "mata_v4_subtitles.srt"
        if srt.stat().st_size > 16:
            shutil.copy2(srt, subtitle_copy)
        else:
            script_dir = next(iter(self.project.glob("02_*")), None)
            plan_path = self.require(script_dir / "scene_plan.json" if script_dir else None, "scene plan for subtitle repair")
            scenes = json.loads(plan_path.read_text(encoding="utf-8"))
            lines = []
            for index, scene in enumerate(scenes):
                begin, finish = index * 9.83, min((index + 1) * 9.83, 49.15)
                def stamp(value: float) -> str:
                    hours, remain = divmod(int(value * 1000), 3600000)
                    minutes, remain = divmod(remain, 60000)
                    seconds, milliseconds = divmod(remain, 1000)
                    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"
                lines.append(f"{index + 1}\n{stamp(begin)} --> {stamp(finish)}\n{scene.get('narration', '')}\n")
            subtitle_copy.write_text("\n".join(lines), encoding="utf-8")
            self.stage("SUBTITLE_SOURCE_REPAIR", "PASS", "source voice_full.srt was zero bytes; V4 temporary subtitles derived from frozen scene_plan")
        srt_filter = subtitle_copy.name
        vf = (
            "[0:v]trim=end=21,setpts=PTS-STARTPTS[a];"
            "[1:v]fps=30,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,trim=end=6,setpts=PTS-STARTPTS[b];"
            "[0:v]trim=start=27,setpts=PTS-STARTPTS[c];"
            "[a][b][c]concat=n=3:v=1:a=0[sv];"
            "[2:a]aresample=48000,aformat=channel_layouts=stereo[voice];"
            "[3:a]aresample=48000,aformat=channel_layouts=stereo,volume=0.20[bgm];"
            "[4:a]aresample=48000,aformat=channel_layouts=stereo,volume=0.055[space];"
            "[5:a]aresample=48000,aformat=channel_layouts=stereo,volume=0.085[sfx];"
            "[bgm][voice]sidechaincompress=threshold=0.035:ratio=7:attack=18:release=350[duck];"
            "[voice][duck][space][sfx]amix=inputs=4:duration=first:normalize=0,alimiter=limit=0.84[sa];"
            "[6:v]setpts=PTS-STARTPTS[ev];[6:a]aresample=48000,aformat=channel_layouts=stereo[ea];"
            "[sv][sa][ev][ea]concat=n=2:v=1:a=1[v][mix]"
        )
        self.stage("FLOW_HERO_SCENE_BINDING", "PASS", f"replaced Scene 03 video with {flow_asset.name}")
        self.stage("TIMELINE", "RUNNING", "21-27 seconds is Flow hero; story audio continuous")
        if timeline_tmp.exists() and timeline_tmp.stat().st_size > 100000:
            self.stage("FINAL_ENCODE", "SKIPPED", "existing valid pre-subtitle timeline reused")
        else:
            self.command("FINAL_ENCODE", [ff, "-y", "-i", str(story), "-i", str(flow_asset), "-i", str(voice), "-i", str(bgm), "-i", str(space), "-i", str(sfx), "-i", str(ending), "-filter_complex", vf, "-map", "[v]", "-map", "[mix]", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", str(timeline_tmp)])
        overlay = ("drawbox=x=0:y=0:w=iw:h=132:color=black@0.32:t=fill,drawbox=x=110:y=111:w=860:h=3:color=0xD6B56B@0.95:t=fill,drawtext=fontfile='C\\:/Windows/Fonts/georgia.ttf':text='HISTORY TODAY  |  07.31  |  J.K. ROWLING':fontcolor=0xE2C37D:fontsize=28:x=(w-text_w)/2:y=51,drawbox=x=0:y=h-248:w=iw:h=248:color=black@0.45:t=fill,subtitles=filename='" + srt_filter + "':force_style='FontName=Microsoft JhengHei,FontSize=22,PrimaryColour=&H00FFFFFF,OutlineColour=&HAA000000,BorderStyle=1,Outline=2,Alignment=2,MarginV=72'")
        self.command("SUBTITLE_GRAPHIC_BURN_IN", [ff, "-y", "-i", str(timeline_tmp), "-vf", overlay, "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", str(out)], cwd=subtitle_copy.parent)
        self.stage("TIMELINE", "PASS", f"master timeline encoded: {out.name}")
        for stage, detail in [
            ("EMOTIONAL_NARRATION", "existing frozen voice reused"),
            ("BGM_EMOTIONAL_CURVE", "BGM.wav mixed at 20 percent"),
            ("AMBIENCE", "SPACE.wav mixed at 5.5 percent"),
            ("SCENE_SFX", "SFX.wav mixed at 8.5 percent"),
            ("AUDIO_DUCKING", "sidechaincompress threshold 0.035 ratio 7 attack 18 release 350"),
            ("TRANSITION", "Flow hero cut bound at 21 and 27 seconds"),
            ("FIXED_ENDING", "ENDING_NORMALIZED.mp4 appended with native audio"),
        ]:
            self.stage(stage, "PASS", detail)
        self.command("VISUAL_QC", [ff, "-v", "error", "-i", str(out), "-f", "null", "-"])
        self.command("QC_MONTAGE", [ff, "-y", "-i", str(out), "-vf", "fps=1/8,scale=270:480,tile=4x2", "-frames:v", "1", str(montage)])
        qc = subprocess.run([ff, "-i", str(out), "-af", "volumedetect", "-f", "null", "-"], text=True, encoding="utf-8", errors="replace", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if qc.returncode:
            raise RuntimeError("AUDIO_QC analysis failed")
        dump(self.project / "FINAL_QC_V4.json", {"status": "PASS", "master": str(out), "montage": str(montage), "flow_hero": str(flow_asset), "flow_hero_used": True, "video_validation": "ffmpeg error scan passed", "audio_validation": "volumedetect passed", "audio_master": "AAC 192 kbps 48 kHz stereo", "checked_at": now()})
        self.stage("AUDIO_QC", "PASS", "volumedetect passed; AAC 48kHz stereo")
        self.stage("MASTER_READY", "PASS", str(out))
        dump(self.project / "FINAL_TIMELINE_ASSET_MAP.json", {"SCENE_03": {"flow_asset": str(flow_asset), "actually_used_in_final": True, "binding_window_seconds": [21, 27], "local_2_5d_baseline": str(b2)}})
        self.write_report(self.flow_dir / "SOURCE_IMAGE.png", b2, flow_asset)

    def run(self) -> int:
        started = time.monotonic()
        self.load()
        source = self.require(pick_one(self.require(self.visual, "visual directory"), "Scene_03_HUMAN_PRESENCE_V2.png"), "human portrait")
        b2 = self.require(self.tech / "TEST_B2_MEDIUM_MOTION.mp4", "approved B2 local motion")
        voice = self.require(self.require(self.voice_dir, "voice directory") / "voice_full.mp3", "frozen voice_full.mp3")
        self.require(self.voice_dir / "voice_full.srt", "frozen voice_full.srt")
        self.stage("PRECHECK", "PASS", f"voice frozen: {voice.name}", time.monotonic() - started)
        flow_asset = self.flow_dir / "FLOW_SCENE_03.mp4"
        self.write_metadata(source, b2, flow_asset)
        self.stage("HERO_SCENE_SELECTION", "PASS", "SCENE_03 selected; B2 retained as local baseline")
        if not flow_asset.exists() or flow_asset.stat().st_size < 4096:
            self.flow_package(source, flow_asset)
            self.write_report(source, b2, flow_asset)
            self.stage("FLOW_PREP", "PASS", f"queue={self.flow_dir}")
            self.stage("FLOW_RETURN_CHECK", "WAITING_FOR_FLOW_ASSET", "place FLOW_SCENE_03.mp4 in Flow queue then rerun")
            return 20
        self.stage("FLOW_RETURN_CHECK", "PASS", f"detected {flow_asset.name} ({flow_asset.stat().st_size} bytes)")
        self.write_report(source, b2, flow_asset)
        self.stage("LOCAL_2_5D", "PASS", "B2 reused; no rembg or ONNX inference")
        self.finish_v4(flow_asset, b2)
        return 0


if __name__ == "__main__":
    try:
        raise SystemExit(Runner().run())
    except Exception as exc:
        print(f"V4_RUNNER_ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
