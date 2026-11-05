# KillSwitch AI — 90-second demo voiceover

**Video:** [`demo_with_audio.mp4`](demo_with_audio.mp4) · 1280×720 · 95 seconds (1:35, muxed narration + live UI recording)
**Silent screen-only capture:** [`demo.mp4`](demo.mp4) · 80 s
**Script length:** ~218 words · ~138 words per minute (edge-tts `en-US-ChristopherNeural`, +0%)
**Visual flow:** hero + live ticket → agent stream → rogue alert → kill session → score counter → remote control close

---

## Timed script

| Time | Voiceover | On screen |
| --- | --- | --- |
| 0:00–0:14 | Coding agents now run with full shell access. They deploy, they query databases, they scale infrastructure — and one hallucinated command can wipe production in milliseconds. The problem is not the agent. It is the missing remote control. | Hero headline + live ticket, `99.4%` metric, `Gateway Online` pill |
| 0:14–0:28 | KillSwitch AI is that remote control. It sits between every autonomous agent and the terminal, scoring each command in about twelve milliseconds. Safe work flows through. Dangerous work pauses — before it ever executes. | Scroll to `How it works` / `Security Engine`, Safe / Verify / Block lanes |
| 0:28–0:44 | Watch the live stream. Liam Agent scales down AWS EC2, risk eighteen, approved. Then AutoDev issues `DROP TABLE users`. At risk ninety-four, KillSwitch intercepts it instantly — nothing runs without your say-so. | Live Agent Stream: Approved → INTERCEPTED → KILLED BY OPERATOR |
| 0:44–1:02 | Now I fire a rogue command: `rm -rf /database/backups`. Risk ninety-eight. Critical. The gateway freezes it, shows the blast radius and the reason, and puts two choices in front of me. Kill Session terminates the agent on the spot — score counter updates, audit signed. Approve would authorize it — under my name. | Click `⚡ Simulate Rogue Agent Command`, CRITICAL card appears with pulsing alert, click `⛔ Kill Session` → `Agent Terminated` |
| 1:02–1:30 | That is remote control for autonomous agents: intercept, score, and steer from anywhere — with a tamper-evident audit trail for every decision. One file, zero backend, double-click to run. KillSwitch AI: your safety bridge to autonomous agents. | Terminal + operator counters update, `99.4%` ticks up, end card `Your safety bridge…` |

---

## Full script — copy and paste

```text
Coding agents now run with full shell access. They deploy, they query databases, they scale infrastructure — and one hallucinated command can wipe production in milliseconds. The problem is not the agent. It is the missing remote control.

KillSwitch AI is that remote control. It sits between every autonomous agent and the terminal, scoring each command in about twelve milliseconds. Safe work flows through. Dangerous work pauses — before it ever executes.

Watch the live stream. Liam Agent scales down AWS EC2, risk eighteen, approved. Then AutoDev issues DROP TABLE users. At risk ninety-four, KillSwitch intercepts it instantly — nothing runs without your say-so.

Now I fire a rogue command: rm -rf slash database slash backups. Risk ninety-eight. Critical. The gateway freezes it, shows the blast radius and the reason, and puts two choices in front of me. Kill Session terminates the agent on the spot — score counter updates, audit signed. Approve would authorize it — under my name.

That is remote control for autonomous agents: intercept, score, and steer from anywhere — with a tamper-evident audit trail for every decision. One file, zero backend, double-click to run. KillSwitch AI: your safety bridge to autonomous agents.
```

---

## Delivery notes

- Voice: calm, confident US male (`en-US-ChristopherNeural`) at ~145 wpm. Pause briefly after `Critical`, `Kill Session`, and the final tagline.
- Emphasize the numbers: **twelve milliseconds**, **risk eighteen**, **risk ninety-four**, **risk ninety-eight**, **ninety-nine point four percent**.
- Align `rm -rf /database/backups` with the CRITICAL card appearing; align `Kill Session terminates…` with the `Agent Terminated` state and the kills counter incrementing.
- Synthesis commands:

```bash
# Edge TTS (natural voice, needs internet)
python -m edge_tts --voice en-US-ChristopherNeural --rate=+0% -f demo-voice.txt --write-media narration.mp3

# Fallback offline TTS (Windows System.Speech, no internet)
powershell -ExecutionPolicy Bypass -File scripts/make-voiceover.ps1
```

- Mux:

```bash
python scripts/record-demo.py        # → demo_silent.webm / demo.mp4
ffmpeg -i demo.mp4 -i narration.mp3 -c:v libx264 -pix_fmt yuv420p -c:a aac -b:a 160k -shortest demo_with_audio.mp4
```
