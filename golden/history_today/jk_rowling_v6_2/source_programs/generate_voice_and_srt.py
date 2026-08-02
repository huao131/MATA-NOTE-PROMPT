from pathlib import Path
import argparse, asyncio, sys, importlib.util

VOICE = "zh-TW-HsiaoChenNeural"
RATE = "-4%"
PITCH = "-2Hz"
VOLUME = "+0%"

def die(msg, code=20):
    print(msg, file=sys.stderr)
    raise SystemExit(code)

if importlib.util.find_spec("edge_tts") is None:
    die("BLOCKED_BY_TTS_RUNTIME: edge-tts missing; fallback voice prohibited.")

import edge_tts

ap = argparse.ArgumentParser()
ap.add_argument("narration_txt")
ap.add_argument("voice_mp3")
ap.add_argument("voice_srt")
args = ap.parse_args()

text = Path(args.narration_txt).read_text(encoding="utf-8").strip()
if not text:
    die("Narration text is empty.", 2)

async def main():
    media = Path(args.voice_mp3)
    srt = Path(args.voice_srt)
    media.parent.mkdir(parents=True, exist_ok=True)
    srt.parent.mkdir(parents=True, exist_ok=True)

    communicate = edge_tts.Communicate(
        text=text, voice=VOICE, rate=RATE, pitch=PITCH, volume=VOLUME
    )
    submaker = edge_tts.SubMaker()

    with media.open("wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                submaker.feed(chunk)

    srt.write_text(submaker.get_srt(), encoding="utf-8")
    print(f"VOICE_OK={media}")
    print(f"SRT_OK={srt}")
    print(f"VOICE={VOICE};RATE={RATE};PITCH={PITCH}")

asyncio.run(main())
