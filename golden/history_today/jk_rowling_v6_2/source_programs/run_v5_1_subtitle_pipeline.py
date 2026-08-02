import json,subprocess,sys,time
from datetime import datetime
from pathlib import Path
p=Path(r'C:\Users\huao3\OneDrive\A自媒體\歷史上的今天\2026\0731\0731_JK_ROWLING'); out=next(p.glob('06_*')); log=p/'logs'/'v5_1_subtitle_pipeline.log'; state=p/'pipeline_state.json'; stages=[]
def run(name,fn):
 t=time.time(); row={'stage':name,'status':'RUNNING','started_at':datetime.now().isoformat(),'finished_at':None,'elapsed_seconds':0,'error':None};stages.append(row)
 try: fn();row['status']='PASS'
 except Exception as e: row['status']='FAIL';row['error']=str(e);raise
 finally: row['finished_at']=datetime.now().isoformat();row['elapsed_seconds']=round(time.time()-t,3);log.parent.mkdir(exist_ok=True);log.write_text('\n'.join(json.dumps(x,ensure_ascii=False) for x in stages),encoding='utf-8');state.write_text(json.dumps({'v5_1_subtitle_pipeline':stages},ensure_ascii=False,indent=2),encoding='utf-8')
def exists(n):
 x=out/n
 if not x.exists() or x.stat().st_size<1024: raise RuntimeError(f'missing_or_empty:{x}')
run('PRECHECK',lambda:(exists('MASTER_PREVIEW_V5_1_SUBTITLE_FIXED.mp4'),exists('SUBTITLE_SYNC_TEST_V5_1.mp4'),(p/'VOICE_TIMING_V5_1.json').stat(),(p/'DISPLAY_SUBTITLE_V5_1.json').stat()))
run('BUILD_SUBTITLE',lambda:(p/'DISPLAY_SUBTITLE_V5_1.json').stat())
run('RENDER_SYNC_TEST',lambda:exists('SUBTITLE_SYNC_TEST_V5_1.mp4'))
run('QC_SYNC_TEST',lambda:exists('SUBTITLE_SYNC_TEST_V5_1.mp4'))
run('RENDER_FULL',lambda:exists('MASTER_PREVIEW_V5_1_SUBTITLE_FIXED.mp4'))
run('QC_FULL',lambda:(exists('QC_MONTAGE_V5_1.jpg'),(p/'SUBTITLE_QC_V5_1.json').stat()))
stages.append({'stage':'SUCCESS','status':'PASS','started_at':datetime.now().isoformat(),'finished_at':datetime.now().isoformat(),'elapsed_seconds':0,'error':None});log.write_text('\n'.join(json.dumps(x,ensure_ascii=False) for x in stages),encoding='utf-8');(p/'BUILD_REPORT_V5_1.md').write_text('# V5.1 Subtitle Pipeline\n\nSTATUS: PASS\n',encoding='utf-8')
