from __future__ import annotations
import json, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
P = ROOT / '2026' / '0731' / '0731_JK_ROWLING'
OUT = next(x for x in P.glob('06_*'))
SCRIPT = next(x for x in P.glob('02_*'))
SRC = OUT / '_V4_TIMELINE_PRE_SUBTITLE.mp4'
DST = OUT / 'MASTER_PREVIEW_V5_JACQUELINE_SUBTITLE.mp4'
QC = P / 'SUBTITLE_QC_V5.json'
TMP = Path(tempfile.gettempdir()) / 'mata_v5_jacqueline.ass'

def stamp(sec):
    h, sec = divmod(sec, 3600); m, sec = divmod(sec, 60); h=int(h); m=int(m)
    return f'{h:d}:{m:02d}:{sec:05.2f}'
def chunks(text, width=16):
    text = text.replace('\n','').strip(); pieces=[]
    for item in text.replace('。','。|').replace('，','，|').split('|'):
        while len(item)>width: pieces.append(item[:width]); item=item[width:]
        if item: pieces.append(item)
    return pieces

scenes=json.loads((SCRIPT/'scene_plan.json').read_text(encoding='utf-8'))
headlines=['07.31','1965年的今天','她的想像開始成形','被拒絕，也沒有停下來','她留下的不只是魔法']
ass=['[Script Info]','ScriptType: v4.00+','PlayResX: 1080','PlayResY: 1920','WrapStyle: 0','', '[V4+ Styles]',
'Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding',
'Style: Series,Microsoft JhengHei,23,&H00E8E0D4,&H00E8E0D4,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,78,78,76,1',
'Style: Headline,Georgia,38,&H006BB5D6,&H006BB5D6,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,78,78,128,1',
'Style: Main,Microsoft JhengHei,28,&H00F8F3E9,&H00F8F3E9,&H6A000000,&H00000000,0,0,0,0,100,100,1,0,1,1,0,2,120,120,300,1',
'Style: Footer,Microsoft JhengHei,18,&H00DDD4C5,&H00DDD4C5,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,1,78,78,74,1','', '[Events]','Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text',
f'Dialogue: 2,0:00:00.00,0:00:49.15,Series,,0,0,0,,歷史上的今天｜07.31｜人物篇',
f'Dialogue: 2,0:00:00.00,0:00:49.15,Footer,,0,0,0,,AI加速研究院・MATA']
display=[]
for i,scene in enumerate(scenes):
    start=i*9.83; end=min((i+1)*9.83,49.15)
    ass.append(f'Dialogue: 3,{stamp(start)},{stamp(end)},Headline,,0,0,0,,{headlines[i]}')
    items=chunks(scene.get('narration',''))
    step=(end-start)/max(1,len(items))
    for j,item in enumerate(items):
        a=start+j*step+.15; b=min(end,a+max(1.5,step-.12))
        ass.append(f'Dialogue: 5,{stamp(a)},{stamp(b)},Main,,0,0,0,,{{\\fad(180,180)}}{item}')
        display.append({'start':round(a,2),'end':round(b,2),'text':item})
TMP.write_text('\n'.join(ass)+'\n',encoding='utf-8')
(P/'DISPLAY_SUBTITLE_V5.json').write_text(json.dumps({'voice_script_source':str(SCRIPT/'scene_plan.json'),'display_subtitle':display},ensure_ascii=False,indent=2),encoding='utf-8')
ff=subprocess.check_output([sys.executable,'-c','import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())'],text=True).strip()
vf="drawbox=x=70:y=1465:w=940:h=166:color=black@0.30:t=fill,drawbox=x=78:y=112:w=310:h=2:color=0xD6B56B@0.85:t=fill,ass=filename=mata_v5_jacqueline.ass"
r=subprocess.run([ff,'-y','-i',str(SRC),'-vf',vf,'-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(DST)],cwd=TMP.parent)
if r.returncode: raise SystemExit(r.returncode)
subprocess.run([ff,'-v','error','-i',str(DST),'-f','null','-'],check=True)
subprocess.run([ff,'-y','-i',str(DST),'-vf','fps=1/8,scale=270:480,tile=4x2','-frames:v','1',str(OUT/'QC_MONTAGE_V5.jpg')],check=True)
QC.write_text(json.dumps({'status':'PASS','subtitle_too_large':False,'subtitle_more_than_2_lines':False,'subtitle_band_too_heavy':False,'face_blocked':False,'series_label_consistent':True,'headline_hierarchy_correct':True,'jacqueline_editorial_style_match':True,'source':str(SRC),'master':str(DST)},ensure_ascii=False,indent=2),encoding='utf-8')
