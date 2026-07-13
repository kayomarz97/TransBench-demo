# TransBench demo — DRAFT 5 plan

> Stored at `build/DRAFT5_PLAN.md`. From your Draft-4 review. VO v3 unchanged (visual re-timing only).

## Confirmed changes (tech beat, 0:46–0:49) — doing now
1. **Restore the "no citation → dropped" animation.** Draft 4 replaced the explicit red drop box with a subtle
   hypothesis strike. Restore the `✕ no citation → dropped` box, revealed on "…it's dropped" @42.5, with its
   edge routed from **retrieval** (clean two-path: grounded→gates→ship, uncited→dropped). H1 also goes red+struck.
2. **Add "it demotes textbook facts" animation** @47.4 — a `textbook fact` chip near the gates that visibly
   **demotes** (grays, strikes, ⤵ demoted). Currently there is NO visual for this line.
3. **Narration matches on-screen text** across the whole tech beat — every spoken phrase now has a matching visual:
   PubMed/Europe PMC · grounds (green) · no citation→dropped · 3 rigor gates · LangGraph · demotes textbook facts · ship.

## Analysis pass — decisions (user answered)
- **Road "weeks of reading" leads VO ~2s** (side effect of the D4 1.3× road speed): **RE-SYNC** (user chose).
  Fix = variable speed: road[0:13]@1.0× (text stays locked) + road[13:21.4]@2.1× (accelerate into reveal) + 0.89s freeze-hold.
  Reveal brightening now beat 23.38→25.0 ("…TransBench comes in"), text labels back on their words. Built in `assemble5.py`.
- **Tech diagram density**: **KEEP the full pipeline** (user chose) — no change.
- Not changed: "ships nothing" (drop restore already shows the reject path), 96 kHz (final-render `-ar 48000`), beat crossfades (declined — sync risk).

## Execution (after you pick from the questions)
Edit `tech.html` (+ any approved) → re-capture changed scenes → `assemble5.py` (from assemble4) → render →
self-QA (frame at each fixed word, duration=VO, loudness) → **Draft 5**.
