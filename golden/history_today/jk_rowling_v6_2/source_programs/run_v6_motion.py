import json,subprocess,sys
from pathlib import Path
p=Path(r'C:\Users\huao3\OneDrive\A自媒體\歷史上的今天\2026\0731\0731_JK_ROWLING');out=next(p.glob('06_*'));vis=next(p.glob('03_*'));pack=next(x for x in p.glob('05_*') if x.name!='05_FLOW_QUEUE');ff=subprocess.check_output([sys.executable,'-c','import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())'],text=True).strip()
plan=[]
spec=[('01','Scene_01.png','PAN_LEFT_TO_RIGHT','zoom+0.08:x left-to-right'),('02','Scene_02.png','SLOW_PUSH_IN','100% to 110%'),('04','Scene_04.png','TILT_BOTTOM_TO_TOP','bottom-to-top'),('05','Scene_05.png','SLOW_PULL_OUT','110% to 100%')]
for n,img,m,r in spec:
 dst=out / ('TEST_SCENE_'+n+'_'+{'01':'PAN_LR','02':'PUSH_IN','04':'TILT_UP','05':'PULL_OUT'}[n]+'.mp4'); z={'01':"zoom='1.10':x='(iw-iw/zoom)*on/150':y='(ih-ih/zoom)/2'",'02':"zoom='1+0.10*on/150':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2'",'04':"zoom='1.10':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)*(1-on/150)'",'05':"zoom='1.10-0.10*on/150':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2'"}[n]+":d=150:s=1080x1920:fps=30";subprocess.run([ff,'-y','-loop','1','-i',str(vis/img),'-vf',z,'-t','5','-c:v','libx264','-pix_fmt','yuv420p',str(dst)],check=True);plan.append({'scene_id':'Scene '+n,'source_asset':str(vis/img),'camera_motion':m,'reason':r,'flow_scene':False})
plan.insert(2,{'scene_id':'Scene 03','source_asset':str(p/'05_FLOW_QUEUE'/'SCENE_03'/'FLOW_SCENE_03.mp4'),'camera_motion':'FLOW HERO','flow_scene':True});(p/'CAMERA_MOTION_PLAN_V6.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
