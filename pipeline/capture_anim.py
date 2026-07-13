#!/usr/bin/env python3
"""Deterministic capture of a Two-Voices animation → 1080p/30 mp4.

Injects a virtual clock (overrides performance.now / rAF / setTimeout / Date.now)
so the scene is stepped frame-by-frame — frame-perfect, no jitter. Hides the deck
playback chrome ([data-omelette-chrome]). Works for both the rAF .dc.html decks and
the setTimeout .html scenes.

Usage: /usr/bin/python3 build/capture_anim.py "<in.html>" "<out.mp4>" [duration_s|auto] [fps]
"""
import sys, os, re, subprocess, tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright

# Virtual clock: page time is driven only by __vc.step(); nothing advances on its own.
INIT = r"""
(() => {
  let vnow = 0; const EPOCH = 1700000000000;
  performance.now = () => vnow;
  try { Date.now = () => EPOCH + vnow; } catch(e){}
  let rafs = [], rid = 1;
  window.requestAnimationFrame = (cb) => { rafs.push([rid, cb]); return rid++; };
  window.cancelAnimationFrame = (id) => { rafs = rafs.filter(x => x[0] !== id); };
  let timers = [], tid = 1;
  window.setTimeout = (cb, d, ...a) => { const id = tid++; timers.push({id, due: vnow + (+d||0), cb, a}); return id; };
  window.clearTimeout = (id) => { timers = timers.filter(t => t.id !== id); };
  window.setInterval = (cb, d, ...a) => { const id = tid++; timers.push({id, due: vnow + (+d||16), cb, a, every: (+d||16)}); return id; };
  window.clearInterval = (id) => { timers = timers.filter(t => t.id !== id); };
  window.__vc = {
    now: () => vnow,
    step(ms) {
      const target = vnow + ms; let guard = 0;
      while (guard++ < 500000) {
        let next = null;
        for (const t of timers) if (t.due <= target && (next === null || t.due < next.due)) next = t;
        if (!next) break;
        vnow = Math.max(vnow, next.due);
        if (next.every) next.due = vnow + next.every; else timers = timers.filter(x => x.id !== next.id);
        try { next.cb.apply(null, next.a); } catch(e){}
      }
      vnow = target;
      const cbs = rafs; rafs = [];
      for (const [,cb] of cbs) { try { cb(vnow); } catch(e){} }
    }
  };
})();
"""
HIDE = ("document.addEventListener('DOMContentLoaded',()=>{var s=document.createElement('style');"
        "s.textContent='[data-omelette-chrome]{display:none!important}';"
        "(document.head||document.documentElement).appendChild(s);});")

def declared_duration(html):
    t = open(html, encoding='utf-8', errors='ignore').read()
    m = re.search(r'data-om-exportable-video-with-duration-secs="([\d.]+)"', t)
    return float(m.group(1)) if m else None

def capture(html, out, duration=None, fps=30, warmup=8):
    dur = duration or declared_duration(html) or 10.0
    n = int(round(dur * fps)); fms = 1000.0 / fps
    tmp = tempfile.mkdtemp(prefix="anifrm_")
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True, args=["--no-sandbox","--force-color-profile=srgb",
            "--hide-scrollbars","--disable-gpu","--disable-dev-shm-usage","--allow-file-access-from-files"])
        pg = b.new_page(viewport={"width":1920,"height":1080}, device_scale_factor=1)
        pg.add_init_script(INIT); pg.add_init_script(HIDE)
        pg.goto(Path(html).resolve().as_uri(), wait_until="load", timeout=45000)
        for _ in range(warmup):
            pg.evaluate("__vc.step(0)")     # let the component mount at t=0 without advancing
        for i in range(n):
            pg.evaluate("void document.body && document.body.offsetHeight")  # force layout
            pg.screenshot(path=f"{tmp}/f{i:05d}.png")
            pg.evaluate(f"__vc.step({fms})")
        b.close()
    subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate",str(fps),"-i",f"{tmp}/f%05d.png",
        "-c:v","libx264","-pix_fmt","yuv420p","-crf","16","-preset","medium","-movflags","+faststart", out], check=True)
    d = float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",out]).decode().strip())
    print(f"{os.path.basename(out)}: {n} frames @ {fps} = {d:.2f}s (declared {dur}s)")
    subprocess.run(["rm","-rf",tmp])

if __name__ == "__main__":
    html, out = sys.argv[1], sys.argv[2]
    dur = None if (len(sys.argv) < 4 or sys.argv[3] == "auto") else float(sys.argv[3])
    fps = int(sys.argv[4]) if len(sys.argv) > 4 else 30
    capture(html, out, dur, fps)
