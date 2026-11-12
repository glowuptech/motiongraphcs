from pathlib import Path
import cv2,numpy as np
from PIL import Image
root=Path(__file__).resolve().parents[4];p=root/'arquivos/03_projeto_animacao/giotto-motion'
im=np.array(Image.open(next((root/'arquivos/01_arte_original').glob('*.png'))).convert('RGB'));h,w=im.shape[:2];m=np.zeros((h,w),np.uint8)
for x,y,x2,y2 in [(690,0,965,105),(360,90,1230,170),(580,160,1085,290),(480,285,1190,418),(320,402,1350,632),(570,623,1100,720),(160,642,1520,850),(465,840,1210,920),(80,860,1600,941)]:m[y:y2,x:x2]=255
small=cv2.resize(im,(418,235));mask=cv2.resize(m,(418,235),interpolation=cv2.INTER_NEAREST);clean=cv2.inpaint(small,mask,5,cv2.INPAINT_TELEA).astype(np.float32)
for _ in range(250):
 blur=cv2.GaussianBlur(clean,(0,0),2);clean[mask>0]=blur[mask>0]
clean=cv2.resize(clean,(w,h));a=cv2.GaussianBlur(m.astype(float)/255,(0,0),4)[:,:,None]
out=np.uint8(np.clip(im*(1-a)+clean*a,0,255));Image.fromarray(out).save(p/'public/assets/background/background-motion.png')
