from pathlib import Path
import sys,time,subprocess
import numpy as np
from PIL import Image,ImageFilter,ImageEnhance
import imageio_ffmpeg
p=Path(sys.argv[1]);o=p/"07_CINEMATIC_TECH_TEST";src=next((p/"03_視覺素材").glob("*HUMAN_PRESENCE_V2.png"))
im=Image.open(src).convert("RGB");mask=Image.open(o/"DEBUG_MASK.png").convert("L");bg=im.filter(ImageFilter.GaussianBlur(9));W,H,N=1080,1920,210;ff=imageio_ffmpeg.get_ffmpeg_exe()
def fit(x,scale,dx=0,dy=0):
 r=max(W/x.width,H/x.height)*scale;x=x.resize((int(x.width*r),int(x.height*r)),Image.Resampling.LANCZOS);cx=(x.width-W)//2+dx;cy=(x.height-H)//2+dy
 return x.crop((cx,cy,cx+W,cy+H)).convert("RGB")
def render(name,push,bgd,subd,fgd,light):
 t=time.time();d=o/f"{name}_frames";d.mkdir(exist_ok=True)
 for i in range(N):
  f=i/(N-1);b=np.asarray(fit(bg,1.03+push*f,bgd*f)).astype(np.float32);s=np.asarray(fit(im,1.0+push*.55*f,-subd*f)).astype(np.float32);a=np.asarray(fit(mask,1.0+push*.55*f,-subd*f)).astype(np.float32).mean(axis=2,keepdims=True)/255
  x=np.clip(s*a+b*(1-a),0,255).astype(np.uint8)
  frame=Image.fromarray(x,"RGB")
  if light: frame=ImageEnhance.Brightness(frame).enhance(1+0.025*np.sin(f*np.pi))
  frame.save(d/f"{i:04d}.jpg",quality=92)
 target=o/f"{name}.mp4";subprocess.run([ff,"-y","-framerate","30","-i",str(d/"%04d.jpg"),"-c:v","libx264","-pix_fmt","yuv420p","-crf","18",str(target)],check=True)
 return time.time()-t,target
t2,v2=render("TEST_B2_MEDIUM_MOTION",.05,32,10,50,False)
t3,v3=render("TEST_B3_CINEMATIC_MOTION",.085,48,15,75,True)
(o/"MOTION_INTENSITY_TEST.json").write_text('{"mask_reused":true,"onnx_rerun":false,"b2_seconds":%.3f,"b3_seconds":%.3f}'%(t2,t3))
print(v2,t2,v3,t3)
