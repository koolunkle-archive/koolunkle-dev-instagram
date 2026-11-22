# Extract the K-keycap characters from card PNGs into transparent PNGs.
from PIL import Image; import numpy as np, cv2
BG=np.array([23,28,34],float)
src={'smile':('legacy/05/01.png',(440,790,1010,1250)),'anxious':('legacy/01/01.png',(520,770,1010,1250)),
     'angry':('legacy/03/03.png',(600,835,1060,1260)),'healing':('legacy/01/05.png',(640,860,1070,1300))}
for name,(f,box) in src.items():
  c=np.asarray(Image.open(f).convert('RGB').crop(box),float)
  d=c-BG
  glow=np.where(d>0, d/(255-BG), -d/BG).max(-1).clip(0,1)
  glow=np.where(glow<0.14,0,(glow-0.14)/0.86)          # kill compression-noise rings
  lum=c.mean(-1); bgl=BG.mean()
  body=(lum>120).astype(np.uint8)
  ring=cv2.dilate(body,np.ones((15,15),np.uint8))
  solid=body | (ring & (lum<bgl+12))                     # dark ink outline next to bright body
  ff=solid.copy()*255; h,w=ff.shape; m=np.zeros((h+2,w+2),np.uint8)
  cv2.floodFill(ff,m,(0,0),128); solid=(ff!=128).astype(np.uint8)  # fill interior holes
  a=np.maximum(glow,solid.astype(float))
  fg=np.where(solid[...,None]==1, c, (c-(1-a[...,None])*BG)/np.maximum(a[...,None],1e-6))
  im=Image.fromarray(np.dstack([fg.clip(0,255),a*255]).astype('uint8'),'RGBA')
  im=im.crop(im.getbbox()); im.save(f'assets/characters/{name}.png'); print(name,im.size)
