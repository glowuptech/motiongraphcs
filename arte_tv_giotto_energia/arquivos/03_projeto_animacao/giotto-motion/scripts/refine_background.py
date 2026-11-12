from pathlib import Path
import numpy as np, cv2,json
from PIL import Image
p=Path('/workspace/motiongraphcs/arte_tv_giotto_energia/arquivos/03_projeto_animacao/giotto-motion')
layers=json.loads((p/'src/data/layers.json').read_text()); bg=np.array(Image.open(p/'public/assets/background/background.png').convert('RGB'));h,w=bg.shape[:2]
mask=np.zeros((h,w),np.uint8)
for l in layers[1:]:
 x=round(l['x']*w/1920);y=round(l['y']*h/1080); a=np.array(Image.open(p/'public'/l['file']))[:,:,3];mask[y:y+a.shape[0],x:x+a.shape[1]]|=a
mask=cv2.dilate(mask,np.ones((31,31),np.uint8))
small=cv2.resize(bg,(418,235));m=cv2.resize(mask,(418,235),interpolation=cv2.INTER_NEAREST)
clean=cv2.resize(cv2.inpaint(small,m,5,cv2.INPAINT_TELEA),(w,h))
clean[mask==0]=bg[mask==0]
Image.fromarray(clean).save(p/'public/assets/background/background.png')
# Preserve extracted edge context explicitly, not mislabelled as a product effect.
alpha=np.any(clean!=bg,axis=2).astype(np.uint8)*255
Image.fromarray(np.dstack([bg,alpha])).save(p/'public/assets/effects/extraction-context.png')
layers.insert(1,dict(id='extraction-context',name='Contexto residual da extração — requer refinamento',file='assets/effects/extraction-context.png',x=0,y=0,width=1920,height=1080,zIndex=1,transformOrigin={'x':960,'y':540}))
(p/'src/data/layers.json').write_text(json.dumps(layers,ensure_ascii=False,indent=2)+'\n')
