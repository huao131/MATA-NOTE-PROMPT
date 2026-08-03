import json,time
from pathlib import Path
from faster_whisper import WhisperModel
p=Path(r'C:\Users\huao3\OneDrive\A自媒體\歷史上的今天\2026\0731\0731_JK_ROWLING')
audio=p/'04_配音'/'voice_full.mp3'
t=time.time(); m=WhisperModel('small',device='cpu',compute_type='int8')
segs,info=m.transcribe(str(audio),language='zh',word_timestamps=True,vad_filter=True)
rows=[]
for n,s in enumerate(segs,1):
 rows.append({'cue_id':n,'spoken_text':s.text.strip(),'display_text':s.text.strip(),'start_time':round(max(0,s.start-.1),3),'end_time':round(s.end+.15,3),'confidence':round(s.avg_logprob,3),'source':'audio_alignment'})
(p/'VOICE_TIMING_V5_1.json').write_text(json.dumps({'model':'small','device':'cpu','compute_type':'int8','alignment_seconds':round(time.time()-t,2),'cues':rows},ensure_ascii=False,indent=2),encoding='utf-8')
(p/'DISPLAY_SUBTITLE_V5_1.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print('ALIGNMENT_OK',len(rows))
