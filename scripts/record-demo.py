#!/usr/bin/env python3
"""Record the KillSwitch AI live UI with headless Playwright and mux narration.

Steps:
  1. Open index.html via file:// in Chromium (1280x720), record_video.
  2. Timed interaction beats matching DEMO_SCRIPT.md (scroll, simulate rogue, kill).
  3. Convert webm -> demo.mp4 (libx264), then mux narration.mp3 -> demo_with_audio.mp4.

Run:
    python scripts/record-demo.py
"""
import pathlib
import subprocess
import sys
import time

from playwright.sync_api import sync_playwright
import imageio_ffmpeg

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = (ROOT / "index.html").resolve()
VIDEO_DIR = ROOT / "video-tmp"
DEMO_MP4 = ROOT / "demo.mp4"
NARR = ROOT / "narration.mp3"
FINAL = ROOT / "demo_with_audio.mp4"

def record():
    VIDEO_DIR.mkdir(exist_ok=True)
    url = INDEX.as_uri()
    print(f"Opening {url}")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            record_video_dir=str(VIDEO_DIR),
            record_video_size={"width": 1280, "height": 720},
        )
        page = context.new_page()
        page.goto(url, wait_until="networkidle")
        # Beats synced to the 90s narration (~95s w/ edge-tts at +0%).
        # Total in-page holds ~88s + load/settle ~= 95s video.
        page.wait_for_timeout(6000)
        # Beat 1 (0:00-0:14) — hero + ticket settle
        page.mouse.wheel(0, 120)
        page.wait_for_timeout(7000)
        # Beat 2 (0:14-0:28) — scroll the security engine into view
        try:
            page.locator("#engine").scroll_into_view_if_needed()
        except Exception:
            pass
        page.wait_for_timeout(9000)
        try:
            page.locator("#how").scroll_into_view_if_needed()
        except Exception:
            pass
        page.wait_for_timeout(5000)
        # Beat 3 (0:28-0:44) — back to ticket, fire the rogue command
        try:
            page.locator("#ticketWrap").scroll_into_view_if_needed()
        except Exception:
            pass
        page.wait_for_timeout(5000)
        page.get_by_text("Simulate Rogue Agent Command").first.click()
        page.wait_for_timeout(8000)
        # Beat 4 (0:44-1:02) — resolve: Kill Session (terminates, counter updates)
        try:
            page.get_by_text("Kill Session").first.click(timeout=5000)
        except Exception as e:
            print(f"Kill click issue: {e}")
        page.wait_for_timeout(9000)
        # Beat 5 (1:02-1:30) — scroll to simulator terminal, show counters
        try:
            page.locator("#simulator").scroll_into_view_if_needed()
        except Exception:
            pass
        page.wait_for_timeout(7000)
        try:
            page.get_by_text("Simulate Rogue Agent Command").last.click(timeout=5000)
        except Exception:
            pass
        page.wait_for_timeout(7000)
        page.mouse.wheel(0, 300)
        page.wait_for_timeout(5000)
        # End card hold
        page.goto(url, wait_until="networkidle")
        page.mouse.wheel(0, 400)
        page.wait_for_timeout(8000)
        context.close()
        browser.close()
    # Playwright writes a .webm into VIDEO_DIR
    webms = sorted(VIDEO_DIR.glob("*.webm"))
    if not webms:
        raise SystemExit(f"No video captured in {VIDEO_DIR}")
    src = webms[-1]
    print(f"Captured {src} ({src.stat().st_size/1024/1024:.2f} MB)")
    return src

def convert_and_mux(webm: pathlib.Path):
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    print(f"ffmpeg: {ffmpeg}")
    # webm -> demo.mp4 (H.264, yuv420p for max player support)
    cmd1 = [ffmpeg, "-y", "-i", str(webm), "-c:v", "libx264",
            "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "medium",
            "-af", "apad=pad_dur=2", str(DEMO_MP4)]
    print("Converting:", " ".join(cmd1))
    subprocess.run(cmd1, check=True)
    print(f"Wrote {DEMO_MP4} ({DEMO_MP4.stat().st_size/1024/1024:.2f} MB)")

    if NARR.exists() and NARR.stat().st_size > 10000:
        # Never truncate the narration: pad video with a cloned last frame
        # to the audio length, then mux (no -shortest on the raw inputs).
        padded = ROOT / "demo_padded.mp4"
        cmd_pad = [ffmpeg, "-y", "-i", str(DEMO_MP4),
                    "-vf", "tpad=stop_mode=clone:stop_duration=60",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
                    "-c:a", "copy", str(padded)]
        print("Padding video (freeze last frame):", " ".join(cmd_pad))
        subprocess.run(cmd_pad, check=True)
        cmd2 = [ffmpeg, "-y", "-i", str(padded), "-i", str(NARR),
                "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
                "-shortest", str(FINAL)]
        print("Muxing:", " ".join(cmd2))
        subprocess.run(cmd2, check=True)
        print(f"Wrote {FINAL} ({FINAL.stat().st_size/1024/1024:.2f} MB)")
    else:
        print(f"WARNING: narration not found at {NARR} — skipping mux. "
              f"Run: python scripts/make-voiceover.py then re-mux manually.")
        # Copy silent file as placeholder so the artifact exists
        import shutil
        shutil.copyfile(DEMO_MP4, FINAL)
        print(f"Copied silent demo to {FINAL}")

def main():
    webm = record()
    convert_and_mux(webm)
    print("Done. Artifacts:")
    for f in [DEMO_MP4, FINAL, NARR]:
        if f.exists():
            print(f"  {f.name}  {f.stat().st_size/1024/1024:.2f} MB")

if __name__ == "__main__":
    main()
