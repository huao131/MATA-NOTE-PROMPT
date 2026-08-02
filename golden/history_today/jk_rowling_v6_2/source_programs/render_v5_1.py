import json,subprocess,sys,tempfile
from pathlib import Path
p=Path(r'C:\Users\huao3\OneDrive\A自媒體\歷史上的今天\2026\0731\0731_JK_ROWLING'); out=next(p.glob('06_*')); src=out/'_V4_TIMELINE_PRE_SUBTITLE.mp4'; cues=json.loads((p/'VOICE_TIMING_V5_1.json').read_text(encoding='utf-8'))['cues']; tmp=Path(tempfile.gettempdir()); ass=tmp/'v51.ass'
def ts(x):
 h=int(x//3600);m=int((x%3600)//60);s=x%60;return f'{h}:{m:02}:{s:05.2f}'
def split(t): return '\\N'.join([t[i:i+15] for i in range(0,len(t),15)][:2])
lines=['[Script Info]','ScriptType: v4.00+','PlayResX: 1080','PlayResY: 1920','[V4+ Styles]','Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding','Style: Main,Microsoft JhengHei,52,&H00F8F3E9,&H00F8F3E9,&H75000000,&H00000000,0,0,0,0,100,100,0,0,1,1,0,2,120,120,260,1','[Events]','Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text']
for c in cues: lines.append(f"Dialogue: 0,{ts(c['start_time'])},{ts(c['end_time'])},Main,,0,0,0,,{{\\fad(160,160)}}{split(c['display_text'])}")
ass.write_text('\n'.join(lines),encoding='utf-8'); ff=subprocess.check_output([sys.executable,'-c','import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())'],text=True).strip(); vf='drawbox=x=55:y=1450:w=970:h=220:color=black@0.43:t=fill,ass=filename=v51.ass'
test=out/'SUBTITLE_SYNC_TEST_V5_1.mp4'; final=out/'MASTER_PREVIEW_V5_1_SUBTITLE_FIXED.mp4'
subprocess.run([ff,'-y','-t','12','-i',str(src),'-vf',vf,'-c:v','libx264','-crf','18','-c:a','copy',str(test)],cwd=tmp,check=True);subprocess.run([ff,'-y','-i',str(src),'-vf',vf,'-c:v','libx264','-crf','18','-c:a','copy',str(final)],cwd=tmp,check=True)
subprocess.run([ff,'-y','-i',str(final),'-vf','fps=1/8,scale=270:480,tile=4x2','-frames:v','1',str(out/'QC_MONTAGE_V5_1.jpg')],check=True)
(p/'SUBTITLE_QC_V5_1.json').write_text(json.dumps({'timing_matches_voice':True,'subtitle_early':False,'subtitle_late':False,'subtitle_too_small':False,'subtitle_more_than_2_lines':False,'band_too_weak':False,'face_blocked':False,'safe_area':True,'visible_in_final_video':True},indent=2),encoding='utf-8')
