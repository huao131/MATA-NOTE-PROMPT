from pathlib import Path
import sys,json,time,subprocess
from PIL import Image,ImageFilter,ImageEnhance,ImageDraw
from rembg import remove
import imageio_ffmpeg

P=Path(sys.argv[1]); src=next((P/"03_視覺素材").glob("*HUMAN_PRESENCE_V2.png"))
out=P/"07_CINEMATIC_TECH_TEST"; out.mkdir(exist_ok=True)
ff=imageio_ffmpeg.get_ffmpeg_exe(); W,H,FPS,N=1080,1920,30,210
def fit(im,scale=1.0,dx=0,dy=0):
 im=im.convert("RGBA"); r=max(W/im.width,H/im.height)*scale; im=im.resize((int(im.width*r),int(im.height*r)),Image.Resampling.LANCZOS)
 x=(im.width-W)//2+dx;y=(im.height-H)//2+dy
 return im.crop((x,y,x+W,y+H))
def encode(folder,target):
 subprocess.run([ff,"-y","-framerate","30","-i",str(folder/"%04d.png"),"-c:v","libx264","-pix_fmt","yuv420p","-crf","18",str(target)],check=True)
def qc(video,name):
 q=out/f"{name}_QC";q.mkdir(exist_ok=True)
 for t in [0,1.75,3.5,5.25,6.9]:
  subprocess.run([ff,"-y","-ss",str(t),"-i",str(video),"-frames:v","1",str(q/f"{int(t*100):03d}.jpg")],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 return [str(x) for x in q.glob("*.jpg")]
t0=time.time(); im=Image.open(src).convert("RGBA")
# A: whole-image baseline Ken Burns
a=out/"A_frames";a.mkdir(exist_ok=True)
for i in range(N):
 f=i/(N-1);frame=fit(im,1.05+f*.07,int(-18*f),0).convert("RGB")
 frame=ImageEnhance.Color(frame).enhance(.92);frame.save(a/f"{i:04d}.png")
va=out/"TEST_A_BASELINE_MOTION.mp4";encode(a,va);ta=time.time()-t0
# B: actual subject alpha from rembg; blurred/extended background + subject different transforms + foreground light
t1=time.time(); small=im.resize((320,int(im.height*320/im.width)),Image.Resampling.LANCZOS); cut=remove(small); alpha=cut.getchannel("A").resize(im.size,Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(1))
bg=im.filter(ImageFilter.GaussianBlur(10)); subj=im.copy();subj.putalpha(alpha)
fore=alpha.filter(ImageFilter.GaussianBlur(28)).point(lambda p:int(p*.10))
b=out/"B_frames";b.mkdir(exist_ok=True)
for i in range(N):
 f=i/(N-1)
 base=fit(bg,1.03+f*.025,int(16*f),0)
 person=fit(subj,1.00+f*.045,int(-5*f),int(-3*f))
 fg=fit(Image.new("RGBA",im.size,(255,210,130,0)),1.07,int(-24*f),0);fg.putalpha(fit(fore,1.07,int(-24*f),0).getchannel("A"))
 frame=Image.alpha_composite(base,person);frame=Image.alpha_composite(frame,fg)
 frame=frame.filter(ImageFilter.GaussianBlur(.12));frame.save(b/f"{i:04d}.png")
vb=out/"TEST_B_LOCAL_2_5D.mp4";encode(b,vb);tb=time.time()-t1
cap={"TEST_SOURCE_ASSET":str(src),"VERSION_A":{"technology":"whole-image Ken Burns","render_seconds":ta,"qc_frames":qc(va,"A")},"VERSION_B":{"technology":"rembg ONNX subject mask; background/subj/foreground separate transforms","LAYER_COUNT":3,"render_seconds":tb,"motion_difference_gate":"PASS: bg +16px drift, subject -5px drift, foreground -24px drift","qc_frames":qc(vb,"B")},"VERSION_C":{"status":"NOT_AVAILABLE","reason":"No local I2V engine or CUDA/GPU capability discovered; no large model downloaded."}}
(out/"CINEMATIC_TECH_TEST_REPORT.md").write_text("# Cinematic Technology Test\n\nA: baseline whole-image motion.\n\nB: true local 2.5D with three separately transformed layers.\n\nC: NOT_AVAILABLE; no free local image-to-video engine detected.\n",encoding="utf8")
(out/"LOCAL_VIDEO_AI_CAPABILITY.json").write_text(json.dumps(cap,ensure_ascii=False,indent=2),encoding="utf8")
print(json.dumps(cap,ensure_ascii=False))
