#!/usr/bin/env python3
"""Generate the TransBench narration VO v2 (8 beats) with edge-tts + per-word timings.
Run: /usr/bin/python3 build/vo/generate_vo.py
"""
import asyncio, json, os, subprocess
import edge_tts

BUILD = os.path.dirname(os.path.abspath(__file__))
VOICE = "en-US-AndrewNeural"
RATE  = "+5%"          # v3 grew past 3:00; +5% brings it to ~2:55 (imperceptible)
GAP   = 0.38

# Approved v2 narration. Name = "Kaeyomerz".
BEATS = [
    {"id": "intro", "label": "INTRO + PROBLEM",
     "text": "Medical doctor. AI engineer. …Same person — so now I get annoyed by two industries instead of one. I'm Kaeyomerz. Every clinic day throws up a puzzle — a patient who won't respond to a first-line drug, a lab value that doesn't fit. Turning that spark into a testable experiment takes weeks of reading — and a favour from a computational biologist. So most sparks just… die on the whiteboard. And this is where TransBench comes in."},
    {"id": "tech", "label": "HOW IT WORKS (technical)",
     "text": "Here's what it actually does. It takes that one plain sentence and breaks it into biological angles. It writes hypotheses you could prove wrong — then goes to the real literature, PubMed and Europe PMC, and grounds every one in papers you can actually open. If a citation won't resolve, it's dropped. Eight agents and three rigor gates, wired together with LangGraph — it demotes textbook facts, and when nothing clears the bar, it ships nothing. Opus writes the hypotheses and designs the experiment; Sonnet decomposes and checks novelty; Haiku grades, and assembles the brief."},
    {"id": "built", "label": "HOW I BUILT IT",
     "text": "Here's the fun part — I barely wrote a line of it by hand. I tunnelled into a bare Linux server from VS Code, and let the Claude command line do the building — agents that read the real docs, a scanner that guards every push, hooks that won't let me ship a mess. And when I was stuck on the ward, I kept it going from my phone, on breaks. Things that would've meant days of learning and hours of building — I did in minutes."},
    {"id": "onepaste", "label": "ONE PASTE / REPRODUCIBLE",
     "text": "And any scientist or doctor can run it too — one copy-paste into Claude Code, no engineering. It even replays byte-identical — so the results are yours to reproduce."},
    {"id": "demo", "label": "HOW IT WORKS (demo)",
     "text": "Watch. I paste a plain observation. It breaks the case into angles, proposes hypotheses tied to real, clickable papers — and when the evidence isn't there, it says so, and ships nothing. The guardrails I set up wouldn't budge."},
    {"id": "science", "label": "CLAUDE SCIENCE",
     "text": "The brief hands me a ready-made prompt. I drop it into Claude Science — it pulls a real, public single-cell dataset, like the Gladstone T-cell data — and it can pull others whenever the question calls for it. It runs the analysis, and draws the figures. A sentence at the bedside, to a grounded hypothesis, to a figure — the next step is a pipette, not another meeting. And you can run it yourself — same inputs, same figure, every time."},
    {"id": "future", "label": "WHERE IT'S GOING",
     "text": "Today it's one run at a time. Next — text it an observation from WhatsApp, like you'd text a colleague. It strips patient identifiers before a word is stored. It remembers every brief — so when new evidence lands, it pings you: that hunch you had? It's grounded now."},
    {"id": "outro", "label": "OUTRO + CREDITS",
     "text": "One confession: this video was planned and edited by Claude Code too. I mostly just told Claude how I was feeling. None of this fits into a weekend without the Max plan — so, thank you. One clinician, one command line, and a model that kept me honest. This is just a preview — the whole thing's documented on GitHub. If you're wondering what I'd build with a team around me instead of a terminal… so am I."},
]


def dur(path):
    return float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]).decode().strip())


async def synth(text, voice, rate, out_mp3, tries=3):
    last = None
    for i in range(tries):
        try:
            c = edge_tts.Communicate(text, voice, rate=rate, boundary="WordBoundary")
            words = []
            with open(out_mp3, "wb") as f:
                async for ch in c.stream():
                    if ch["type"] == "audio":
                        f.write(ch["data"])
                    elif ch["type"] == "WordBoundary":
                        words.append({"text": ch["text"], "start": round(ch["offset"] / 1e7, 3), "dur": round(ch["duration"] / 1e7, 3)})
            if os.path.getsize(out_mp3) > 500:
                return words
        except Exception as e:
            last = e; await asyncio.sleep(1.5)
    raise RuntimeError(f"TTS failed for {out_mp3}: {last}")


async def main():
    manifest = {"voice": VOICE, "rate": RATE, "gap_s": GAP, "beats": []}
    sil = os.path.join(BUILD, "_sil.mp3")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
                    "-t", str(GAP), "-c:a", "libmp3lame", "-b:a", "48k", sil], check=True)
    concat = []; t = 0.0
    for b in BEATS:
        mp3 = os.path.join(BUILD, f"beat_{b['id']}.mp3")
        words = await synth(b["text"], VOICE, RATE, mp3)
        d = dur(mp3)
        abswords = [{"text": w["text"], "start": round(t + w["start"], 3), "dur": w["dur"]} for w in words]
        manifest["beats"].append({"id": b["id"], "label": b["label"], "file": os.path.basename(mp3),
                                  "start": round(t, 3), "dur": round(d, 3), "text": b["text"], "words": abswords})
        with open(os.path.join(BUILD, f"beat_{b['id']}.words.json"), "w") as f:
            json.dump(abswords, f, indent=1)
        concat += [mp3, sil]; t += d + GAP
        print(f"{b['id']:9s} dur={d:6.2f}s  end={t:7.2f}s  words={len(words)}")
    concat = concat[:-1]; total = t - GAP
    manifest["total_dur"] = round(total, 3)
    listfile = os.path.join(BUILD, "_concat.txt")
    with open(listfile, "w") as f:
        for p in concat: f.write(f"file '{p}'\n")
    vo_full = os.path.join(BUILD, "vo_full.mp3")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", listfile,
                    "-c:a", "libmp3lame", "-q:a", "4", vo_full], check=True)
    with open(os.path.join(BUILD, "vo_manifest.json"), "w") as f:
        json.dump(manifest, f, indent=1)
    m, s = int(total // 60), total % 60
    print(f"\nTOTAL VO: {total:.2f}s  ({m}:{s:04.1f})   must be < 3:00")


asyncio.run(main())
