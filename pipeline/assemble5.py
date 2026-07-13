#!/usr/bin/env python3
"""Draft 5 assembler — Draft-4 fixes plus the Draft-5 review round. Edits that live here, not the scenes:
  #2 road (0:25): VARIABLE speed — road[0:13]@1.0x keeps "weeks of reading"/"biologist" on the voice, then
     road[13:21.4]@2.1x accelerates into the TransBench self-brighten reveal (~"comes in" @25.0) + 0.89s hold.
     (Draft 4 used a uniform 1.3x, which made the text lead the VO ~2s — user asked to re-sync.)
  #4 minutes (1:24): delay built_minutes so "minutes" reveals on the word @84.1 (howbuilt 18.5->19.82,
     minutes 5.83->4.51 @1.5x); the days/hours sweep rides under "days of learning / hours of building".
Draft-5 scene change: tech.html restored the "no citation -> dropped" box (edge from retrieval) + added the
"textbook fact -> demoted" animation, so every tech-beat phrase has matching on-screen text. VO v3 unchanged
=> every other sync anchor preserved. Run: /usr/bin/python3 build/assemble5.py"""
import os, subprocess as sp
R="/root/projects/transbench"
A,S,C,B=f"{R}/build/anim",f"{R}/build/scenes",f"{R}/build/clips",f"{R}/build"
SEG=f"{B}/segments5"; os.makedirs(SEG,exist_ok=True)
REC=f"{R}/build/_recording_cache/rec.mp4"   # cached out of ephemeral /tmp so re-assembly survives a fresh session
MUSIC=f"{R}/assets/music/mixkit_124_techno-fest-vibes.mp3"
RISER=f"{R}/assets/sfx/mixkit_1492_riser_cinematic-whoosh-fast-transi.mp3"
DING =f"{R}/assets/sfx/mixkit_911_ding_interface-hint-notificat.mp3"
VO   =f"{B}/vo/vo_full.mp3"
V="scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=0x0A0E14,fps=30,format=yuv420p"
ENC=["-c:v","libx264","-crf","18","-preset","medium","-pix_fmt","yuv420p","-r","30","-an"]

def run(c):
    r=sp.run(c,capture_output=True,text=True)
    if r.returncode: raise RuntimeError("FFMPEG:\n"+r.stderr[-1600:])

def one(src,out,dur,ss=0.0,freeze=0.0,speed=1.0,vf=V):
    base=round((dur-freeze)*speed,3)
    sp_f=f",setpts=PTS/{speed}" if speed!=1.0 else ""
    vfx=vf+sp_f+(f",tpad=stop_mode=clone:stop_duration={freeze}" if freeze else "")
    run(["ffmpeg","-y","-loglevel","error","-ss",str(ss),"-t",str(base),"-i",src,"-vf",vfx,*ENC,"-t",str(dur),out])

def concat(parts,out):
    subs=[]
    for i,p in enumerate(parts):
        src,dur,ss,frz,spd=p; q=f"{out}.p{i}.mp4"; one(src,q,dur,ss,frz,spd); subs.append(q)
    inp=[]
    for q in subs: inp+=["-i",q]
    fc="".join(f"[{i}:v]" for i in range(len(subs)))+f"concat=n={len(subs)}:v=1:a=0[v]"
    run(["ffmpeg","-y","-loglevel","error",*inp,"-filter_complex",fc,"-map","[v]",*ENC,out])
    for q in subs: os.remove(q)

print("· recut cs_paste (5s clean)")
run(["ffmpeg","-y","-loglevel","error","-ss","898","-to","903","-i",REC,"-an",
     "-vf","crop=1920:918:0:162,fps=30","-c:v","libx264","-crf","18","-pix_fmt","yuv420p",f"{C}/cs_paste5.mp4"])

print("· beat segments")
ROAD=f"{A}/why_road.mp4"
concat([(f"{S}/intro.mp4",8.0,0,0,1),(ROAD,13.0,0,0,1.0),(ROAD,4.89,13,0.89,2.1)], f"{SEG}/1intro.mp4")  # 25.89 (#2 road: 1x journey keeps "weeks of reading" synced, then 2.1x accel into the reveal + 0.89s hold)
one(f"{S}/tech.mp4", f"{SEG}/2tech.mp4", 35.06, freeze=0.10)                                     # 35.06
concat([(f"{A}/built_howbuilt_full.mp4",19.82,0,0,1),(f"{A}/built_minutes.mp4",4.51,0,0,1.5)], f"{SEG}/3built.mp4")  # 24.33  (#4 minutes delay)
one(f"{S}/onepaste.mp4", f"{SEG}/4onepaste.mp4", 11.04, freeze=0.05)                             # 11.04
one(f"{S}/works.mp4", f"{SEG}/5demo.mp4", 14.35)                                                 # 14.35
concat([(f"{C}/cs_paste5.mp4",5.0,0,0,1),(f"{S}/figure2.mp4",21.13,0,0.20,1)], f"{SEG}/6science.mp4")  # 26.13
one(f"{S}/roadmap.mp4", f"{SEG}/7future.mp4", 16.58, freeze=0.10)                                # 16.58
concat([(f"{S}/curtain_end.mp4",3.2,0,0,1),(f"{S}/outro2.mp4",19.0,0,0,1)], f"{SEG}/8outro.mp4")         # 22.20

print("· concat video master")
segs=[f"{SEG}/{n}.mp4" for n in ["1intro","2tech","3built","4onepaste","5demo","6science","7future","8outro"]]
inp=[]
for s in segs: inp+=["-i",s]
fc="".join(f"[{i}:v]" for i in range(len(segs)))+f"concat=n={len(segs)}:v=1:a=0[v]"
run(["ffmpeg","-y","-loglevel","error",*inp,"-filter_complex",fc,"-map","[v]",*ENC,"-movflags","+faststart",f"{B}/video_master5.mp4"])

print("· audio mix (music quieter, VO louder)")
DING_MS=149800  # "pings you" @149.8
AF=(f"[2:a]aloop=loop=-1:size=200000000,atrim=0:176,asetpts=N/SR/TB[mraw];"
    f"[mraw][1:a]sidechaincompress=threshold=0.03:ratio=14:attack=15:release=320[md];"
    f"[md]volume=0.22,afade=t=in:st=0:d=0.6,afade=t=out:st=173.5:d=1.8[m];"
    f"[3:a]volume=0.5,adelay=0|0[riser];"
    f"[4:a]volume=0.55,adelay={DING_MS}|{DING_MS}[ding];"
    f"[1:a]volume=1.18,aformat=channel_layouts=stereo[vo];"
    f"[vo][m][riser][ding]amix=inputs=4:normalize=0:dropout_transition=0,aformat=channel_layouts=stereo[mix];"
    f"[mix]loudnorm=I=-15:TP=-1.5:LRA=11[a]")
run(["ffmpeg","-y","-loglevel","error","-i",f"{B}/video_master5.mp4","-i",VO,"-i",MUSIC,"-i",RISER,"-i",DING,
     "-filter_complex",AF,"-map","0:v","-map","[a]","-c:v","copy","-c:a","aac","-b:a","192k","-movflags","+faststart",f"{B}/draft5_1080.mp4"])

print("· 480p proxy")
run(["ffmpeg","-y","-loglevel","error","-i",f"{B}/draft5_1080.mp4","-vf","scale=854:480",
     "-c:v","libx264","-crf","26","-preset","veryfast","-c:a","aac","-b:a","160k","-movflags","+faststart",f"{R}/output/draft5_480p.mp4"])
d=float(sp.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"{R}/output/draft5_480p.mp4"]).decode().strip())
print(f"DONE draft5_480p.mp4  {d:.2f}s ({int(d//60)}:{d%60:04.1f})")
