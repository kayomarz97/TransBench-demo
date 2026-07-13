# TransBench demo — DRAFT 4 plan

> Stored at `build/DRAFT4_PLAN.md`. Built from your Draft-3 review notes (7 items).
> **Nothing renders until you answer Q1–Q3 at the bottom.** Everything else is diagnosed and mechanical.
> Sync source = `build/vo/vo_manifest.json` word times (unchanged — VO v3 is NOT being re-generated).

---

## Your notes → root cause → fix

| # | ~Time | Your note | Root cause (what I verified) | Fix | Needs you? |
|---|------|-----------|------------------------------|-----|-----------|
| 1 | 0:02 | Doctor + AI engineer should come in *as I say it*, move close together and **merge** | `intro.html` reveals both labels stacked & centered, then just **fades** them at 5.0s. No "move together / merge" motion at all. Words already land right (Medical@0.1, AI@1.2). | Re-choreograph: labels enter separated (L/R), **slide toward center on "Same person" @2.4** and fuse → KAYOMARZ. | **Q1 (merge style)** |
| 2 | 0:25 | "This is where TransBench comes in" should **stay on it, brighten, show the animation end** | Road animation (`why_road.mp4`) ends on a clean **TransBench flask reveal** — verified — but the cut moves on before "TransBench comes in" @24.1–25.0 is even finished, and it doesn't brighten. | Hold the road's TransBench end-frame + **brightness/scale ramp** timed so the reveal peaks on "TransBench comes in." ffmpeg tail-hold + `eq` ramp. | mechanical |
| 3 | 0:46 | Citations animation & VO don't sync | `tech.html`: the **gates** node fires at 40.9s but the word "gates" is @44.9 (**~4s early**); **drop** is ~0.8s late; there's **no visual** for "grounds every one in papers" @37.9–40.1. | Re-anchor the middle: retrieval logos @35.9 → **add a grounding beat @~38** → drop on "dropped" @42.5 → gates on "gates" @44.9 → LangGraph @46.5. Models already perfect. | mechanical |
| 4 | 1:24 | "minutes" still appears **super early**; delay the animation coming in, sync "minutes" to VO | `built_minutes.mp4` reveals "minutes" ~3–4s into the clip; current placement lands it ~2s **before** the spoken word @84.1. | **Delay the clip's entrance** so "minutes" reveals exactly on @84.1; let the deck's **days→hours ghost intro** ride under "days of learning / hours of building." Re-time in `assemble4.py` (hold prior frame / slow the clip). | mechanical |
| 5 | 2:08 | "a sentence at the bedside" line **overlaps the images** | **CSS Grid min-content trap** (verified on a captured frame): cells default to `min-height:auto`, so the 1117×880 panels refuse to shrink, the grid overflows its declared 560px to ~940px, and crashes onto the recap line. Draft-3 only moved the text — never fixed the overflow. | `figure2.html`: `min-height:0;min-width:0;overflow:hidden` on `.cell` so the `1fr` rows bind; give the recap band + repro a guaranteed clean zone. | mechanical |
| 6 | 2:20 | Roadmap still **bland** — more dynamic, add logos, more movement, **lighten up** when it reaches there | `roadmap.html` is a static dark horizontal rail: dots + text, no logos, no camera, no brightening at the payoff. | Add per-node **logos/icons**, camera motion + node pop/parallax, and a **brightness/glow lift** at the "it pings you" payoff. Scope depends on Q2. | **Q2 (logos + how far)** |
| 7 | — | Ending credits **VO not synced** | `outro2.html` cards run on a fixed 2.8s cadence, **not** anchored to words. Also the 3.2s Curtain (TransBench merge) pushes card #1 to **156.6s abs**, past "planned & edited by Claude Code" @155–157. | Re-anchor each card to its VO phrase (offset for the curtain). Card **content/order** vs. tight sync = your call. | **Q3 (sync strategy)** |

## Not changing (locked unless you say otherwise)
- **VO v3** (no re-record) — all sync is visual re-timing against existing word times.
- Curtain TransBench-merge open, line-art logo style, music/VO mix, < 3:00 length, model-role beats, dataset-agnostic science line.

## Execution order (after Q1–Q3)
1. Edit scenes: `intro.html` (Q1), `tech.html` (re-time), `figure2.html` (grid fix), `roadmap.html` (Q2), `outro2.html` (Q3).
2. Re-capture only the changed scenes (`capture_anim.py`, 1080p/30, deterministic).
3. New `assemble4.py` (from `assemble3.py`): road tail-hold+brighten (#2), minutes delay (#4), points at cached recording (`build/_recording_cache/rec.mp4`, already saved out of ephemeral /tmp).
4. Render `build/draft4_1080.mp4` + `output/draft4_480p.mp4`.
5. **Self-QA before handing it over:** frame-grab each fixed moment at its VO word, contact sheet, loudness/clip check, blackdetect/freezedetect, Σ-segment-durations == VO total. Report pass/fail honestly with evidence, then deliver.

## Decisions — LOCKED (user answered 2026-07-13)
- **Q1 intro:** **Meet center, cross-fade.** Labels enter (Medical@0.12, AI@1.15), converge to one center point and cross-fade into KAYOMARZ on "Same person" @2.4; KAYOMARZ holds through the spoken name "Kaeyomerz" @6.5 to 8.0s.
- **Q2 roadmap:** **Line-art icons + big lift.** Add hand-drawn icons (chat=WhatsApp, shield=de-identify, bell/ring=pings, etc.), camera motion + node pops/parallax, and a brightness/glow lift at the "it pings you" payoff.
- **Q3 credits:** **Re-map cards to post-merge lines; headings word-synced, sub-text kept.** Mapping (outro2 starts @156.58 after the 3.2s curtain):
  | Card | shows | heading (synced word) | label / sub (kept) |
  |------|-------|-----------------------|--------------------|
  | 1 | 157.6–159.6 | **Claude Code** (on "told Claude" @158.2) | "Planned, edited & co-piloted by" / "script, shot list, and the cut you're watching." |
  | 2 | 159.9–163.4 | **the Max plan · one Hetzner box** (on "Max plan" @161.6) | "Powered by" / "an unreasonable number of uv syncs." |
  | 3 | 163.8–167.4 | **one clinician · one command line** (on "command line" @165.0) | "Built by" / "…and a model that kept me honest." |
  | 4 | 167.9–170.9 | **on GitHub** (on "GitHub" @170.4) | "This is just a preview" / "github.com/kayomarz97/TransBench" |
  | site | 171.2–175.4 | **Kayomarz** / kayomarz.com | hold to end |
  (Standalone "Built by Dr. Kayomarz" and "secret-scanner" cards fold into cards 3 & site — no VO room to sync them; flag at delivery.)
