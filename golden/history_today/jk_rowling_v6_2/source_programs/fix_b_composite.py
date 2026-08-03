from pathlib import Path
import sys,time,subprocess
import numpy as np
from PIL import Image,ImageFilter
from rembg import remove
import imageio_ffmpeg
p=Path(sys.argv[1]);out=p/"07_CINEMATIC_TECH_TEST";src=next((p/"03_視覺素材").glob("*HUMAN_PRESENCE_V2.png"))
im=Image.open(src).convert("RGB");W,H,N=1080,1920,210;ff=imageio_ffmpeg.get_ffmpeg_exe()
def fit(x,scale,dx=0,dy=0):
 r=max(W/x.width,H/x.height)*scale;x=x.resize((int(x.width*r),int(x.height*r)),Image.Resampling.LANCZOS);cx=(x.width-W)//2+dx;cy=(x.height-H)//2+dy
 return x.crop((cx,cy,cx+W,cy+H)).convert("RGB")
t=time.time();small=im.resize((320,int(im.height*320/im.width)),Image.Resampling.LANCZOS);mask=remove(small.convert("RGBA")).getchannel("A").resize(im.size,Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(1))
mask.save(out/"DEBUG_MASK.png"); subject=np.asarray(im).astype(np.float32); bg=im.filter(ImageFilter.GaussianBlur(9))
(out/"DEBUG_SUBJECT_RGBA.png").write_bytes(remove(small.convert("RGBA")).resize(im.size,Image.Resampling.LANCZOS).tobytes())
frames=out/"B_FIXED_frames";frames.mkdir(exist_ok=True)
for i in [0,105,209]:
 f=i/(N-1);b=np.asarray(fit(bg,1.03+.025*f,int(16*f))).astype(np.float32);s=np.asarray(fit(im,1.00+.045*f,int(-5*f),int(-3*f))).astype(np.float32);a=np.asarray(fit(mask.convert("RGB"),1.00+.045*f,int(-5*f),int(-3*f))).mean(2,keepdims=True)/255.;final=np.clip(s*a+b*(1-a),0,255).astype(np.uint8);Image.fromarray(final,"RGB").save(out/f"DEBUG_FINAL_{i:03d}.png")
if any(np.asarray(Image.open(out/f"DEBUG_FINAL_{i:03d}.png")).max()==0 for i in [0,105,209]):raise RuntimeError("DEBUG_FRAME_BLACK")
for i in range(N):
 f=i/(N-1);b=np.asarray(fit(bg,1.03+.025*f,int(16*f))).astype(np.float32);s=np.asarray(fit(im,1.00+.045*f,int(-5*f),int(-3*f))).astype(np.float32);a=np.asarray(fit(mask.convert("RGB"),1.00+.045*f,int(-5*f),int(-3*f))).mean(2,keepdims=True)/255.;Image.fromarray(np.clip(s*a+b*(1-a),0,255).astype(np.uint8),"RGB").save(frames/f"{i:04d}.png")
target=out/"TEST_B_LOCAL_2_5D_FIXED.mp4";subprocess.run([ff,"-y","-framerate","30","-i",str(frames/"%04d.png"),"-c:v","libx264","-pix_fmt","yuv420p","-crf","18",str(target)],check=True)
for tsec in [0,3.5,6.9]:subprocess.run([ff,"-y","-ss",str(tsec),"-i",str(target),"-frames:v","1",str(out/f"B_FIXED_QC_{int(tsec*10):02d}.jpg")],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
print("B_TEST_COMPLETE",target,"seconds",time.time()-t)
