# TransBench — the demo film 🎬

**A 3-minute product film, made by a physician with zero video-editing skills.**
Script, animation, voiceover timing, and the entire edit were planned and produced by **Claude Code**. I just told it how I was feeling.

▶️ **Watch it below**, or on **[YouTube](https://youtu.be/RFRhDaPUonE)**:

<video src="https://github.com/kayomarz97/TransBench-demo/raw/main/demo_video/TransBench_demo_final_1080p.mp4" poster="https://github.com/kayomarz97/TransBench-demo/raw/main/demo_video/thumbnail.png" controls></video>
🌐 **Me:** [kayomarz.com](https://kayomarz.com) · 🧪 **The product:** [github.com/kayomarz97/TransBench](https://github.com/kayomarz97/TransBench)

---

## What is TransBench? (in one breath)

TransBench turns a clinician's bedside observation into a **grounded, testable, bench-ready experiment** — shipped as an **MCP connector for Claude Science**.

You write one plain sentence — *a patient who won't respond to a first-line drug, a lab value that doesn't fit* — and TransBench:

1. breaks it into **biological angles**,
2. writes **hypotheses you could prove wrong**,
3. grounds every one in **real, clickable papers** (PubMed + Europe PMC) — and **drops anything it can't cite**,
4. runs it through **8 agents and 3 rigor gates** (wired with LangGraph),
5. hands you a bench-ready brief **and** a ready-made prompt for **Claude Science**, which pulls a real, public single-cell dataset, runs the analysis, and draws the figures.

> A sentence at the bedside → a grounded hypothesis → a figure → a pipette, not another meeting.
> And it replays **byte-identical**, so the results are yours to reproduce.

Full product, docs, and one-paste install: **[github.com/kayomarz97/TransBench](https://github.com/kayomarz97/TransBench)**

---

## The part I still can't believe: I didn't edit any of this

I'm an internal-medicine resident. I have never used After Effects, Premiere, or any editing tool. This film exists because **Claude Code** treated the video like a software project:

- **The script** was written, revised across 5 drafts, and timed to the voiceover.
- **Every scene** is a hand-written **HTML page** — the pipeline diagram, the roadmap, the credits — not a video-editor timeline.
- **The voiceover** (Microsoft neural TTS) emits a **word-level timecode for every word**, and that timing file is the single source of truth: each animation is anchored to the millisecond a word is spoken.
- **Rendering** is deterministic: a headless Chromium steps each scene one frame at a time (a virtual clock, so it never jitters), then **ffmpeg** stitches the beats, mixes music under the voice, and normalizes loudness.

So "editing" here meant **changing numbers and re-rendering** — the same loop as fixing a bug. When I said "the citations don't line up with what I'm saying," Claude found the timing was 4 seconds off, fixed it, and re-rendered. Five times over.

### How a frame gets made
```
narration → edge-tts (word timings)  ─┐
HTML scenes (timings anchored to words)├─►  headless-Chromium frame capture  ─►  ffmpeg assemble  ─►  film
music / SFX ───────────────────────── ┘        (deterministic, 1080p/30)         (mix · loudnorm · concat)
```

---

## What's in this repo

| Path | What it is |
|------|------------|
| `demo_video/` | The deliverables: **captions** (`captions.srt`), **thumbnail** (1280×720), the **YouTube pack** (`YOUTUBE.md`), and audio **credits**. *(The rendered `.mp4` is on YouTube — it's git-ignored to keep the repo light.)* |
| `pipeline/scenes/` | The **HTML source** for every animated scene (intro, the how-it-works diagram, one-paste, the demo panel, the figure, the roadmap, the credits, the thumbnail). |
| `pipeline/*.py` | The **build scripts** — `capture_anim.py` (the deterministic frame-stepper), `assemble5.py` (the ffmpeg assembler), `vo/generate_vo.py` (the word-timed voiceover). |
| `pipeline/NARRATION.md`, `DRAFT*_PLAN.md` | The **script** and the **making-of trail** across drafts. |

> **Privacy note:** the raw screen recording and any local capture footage are deliberately **not** included (they contained a session URL and a server address). Everything shown in the final film is public and real.

---

## Run the pipeline yourself

The film is built like software — three deterministic stages. You need **Python 3**, **ffmpeg**
(with `ffprobe`), and two Python packages:

```bash
pip install playwright edge-tts
playwright install chromium
```

**1 · Voiceover with word-level timings** — Microsoft neural TTS emits one audio file per beat plus a
JSON of per-word timecodes, the single source of truth every animation is anchored to:

```bash
python3 pipeline/vo/generate_vo.py
```

**2 · Capture a scene → video, deterministically** — a headless Chromium renders an HTML scene under
an injected *virtual clock* (it overrides `performance.now` / `requestAnimationFrame` / `Date.now`), so
every frame is stepped by hand and the render never jitters. This stage is the reusable core and runs
standalone on any committed scene:

```bash
python3 pipeline/capture_anim.py pipeline/scenes/works.html works.mp4 auto 30
#                                 └ any scene            └ out     └ dur └ fps
```

**3 · Assemble + mix** — ffmpeg stitches the captured beats, mixes music under the voice, normalizes
loudness, and writes the final 1080p/30 film:

```bash
python3 pipeline/assemble5.py
```

> **Honest caveats.** Stages 1 and 3 encode *this* film's exact beats (and some absolute paths), and the
> final mix needs assets kept out of this repo by design — the **music/SFX** (Mixkit, licensed, not
> redistributable — see [`demo_video/CREDITS_licenses.md`](demo_video/CREDITS_licenses.md)) and the raw
> screen recording (**deliberately excluded** — it held a live session URL). So a *byte-identical*
> re-render isn't the goal; the **method** is. Stage 2 (`capture_anim.py`) is fully reproducible today —
> point it at any `pipeline/scenes/*.html` and you get a deterministic clip.

---

## Credits

- **Built by** Dr. Kayomarz — one clinician, one command line. · [kayomarz.com](https://kayomarz.com)
- **Planned, animated & edited by** Claude Code (Anthropic).
- **Music:** Mixkit — *Techno Fest Vibes* (Mixkit Free License, no attribution required). Full audio licences in [`demo_video/CREDITS_licenses.md`](demo_video/CREDITS_licenses.md).
- **Data shown** is real and public (GEO **GSE278572**; PubMed / Europe PMC PMIDs).

*One clinician, one command line, and a model that kept me honest.*
