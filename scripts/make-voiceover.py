#!/usr/bin/env python3
"""Generate the 90-second KillSwitch AI narration track.

Primary: edge-tts (natural US voice, needs internet):
    python -m edge_tts --voice en-US-ChristopherNeural -f demo-voice.txt --write-media narration.mp3

Fallback (Windows, offline): PowerShell System.Speech → narration.wav.
Usage:
    python scripts/make-voiceover.py [--voice NAME] [--out PATH]
"""
import argparse
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "DEMO_SCRIPT.md"

FULL_SCRIPT = """Coding agents now run with full shell access. They deploy, they query databases, they scale infrastructure — and one hallucinated command can wipe production in milliseconds. The problem is not the agent. It is the missing remote control.

KillSwitch AI is that remote control. It sits between every autonomous agent and the terminal, scoring each command in about twelve milliseconds. Safe work flows through. Dangerous work pauses — before it ever executes.

Watch the live stream. Liam Agent scales down AWS EC2, risk eighteen, approved. Then AutoDev issues DROP TABLE users. At risk ninety-four, KillSwitch intercepts it instantly — nothing runs without your say-so.

Now I fire a rogue command: rm minus rf slash database slash backups. Risk ninety-eight. Critical. The gateway freezes it, shows the blast radius and the reason, and puts two choices in front of me. Kill Session terminates the agent on the spot — score counter updates, audit signed. Approve would authorize it — under my name.

That is remote control for autonomous agents: intercept, score, and steer from anywhere — with a tamper-evident audit trail for every decision. One file, zero backend, double-click to run. KillSwitch AI: your safety bridge to autonomous agents.
"""

def write_voice_text(path: pathlib.Path):
    path.write_text(FULL_SCRIPT, encoding="utf-8")

def try_edge_tts(voice: str, text_file: pathlib.Path, out_file: pathlib.Path) -> bool:
    cmd = [sys.executable, "-m", "edge_tts", "--voice", voice,
           "-f", str(text_file), "--write-media", str(out_file)]
    print("Running:", " ".join(cmd))
    try:
        subprocess.run(cmd, check=True, timeout=120)
        if out_file.exists() and out_file.stat().st_size > 10000:
            print(f"OK edge-tts -> {out_file} ({out_file.stat().st_size/1024:.0f} KB)")
            return True
    except Exception as e:
        print(f"edge-tts failed: {e}")
    return False

def fallback_ps_tts(text_file: pathlib.Path, out_file: pathlib.Path):
    """Windows System.Speech offline fallback → WAV (convert to MP3 with ffmpeg)."""
    wav = out_file.with_suffix(".wav")
    ps1 = ROOT / "scripts" / "make-voiceover.ps1"
    print("Falling back to Windows System.Speech ->", wav)
    subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", str(ps1),
                    str(text_file), str(wav)], check=True, timeout=180)
    # convert wav → mp3 via imageio-ffmpeg
    import imageio_ffmpeg
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    subprocess.run([ffmpeg, "-y", "-i", str(wav), "-codec:a", "libmp3lame",
                    "-q:a", "4", str(out_file)], check=True)
    print(f"OK System.Speech -> {out_file}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--voice", default="en-US-ChristopherNeural")
    ap.add_argument("--out", type=pathlib.Path, default=ROOT / "narration.mp3")
    args = ap.parse_args()

    text_file = ROOT / "demo-voice.txt"
    write_voice_text(text_file)
    print(f"Wrote {text_file} ({len(FULL_SCRIPT.split())} words)")

    if try_edge_tts(args.voice, text_file, args.out):
        return
    fallback_ps_tts(text_file, args.out)

if __name__ == "__main__":
    main()
