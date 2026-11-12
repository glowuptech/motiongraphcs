from pathlib import Path
import numpy as np, cv2, json
from PIL import Image
root=Path('/workspace/motiongraphcs/arte_tv_giotto_energia')
p=root/'arquivos/03_projeto_animacao/giotto-motion'
src=next((root/'arquivos/01_arte_original').glob('*.png'))
im=np.array(Image.open(src).convert('RGB')); h,w=im.shape[:2]
current=im.copy(); layers=[]; z=100
# Peel foreground first; each mask restores exactly the pixels removed at this step.
def peel(id,folder,box,kind='light',offer=None):
 global current,z
 x,y,x2,y2=box; crop=current[y:y2,x:x2]; lum=crop.max(2)
 if kind=='light': m=(lum>105).astype('uint8')*255
 elif kind=='dark': m=(crop.min(2)<100).astype('uint8')*255
 elif kind=='product':
  m=np.zeros(lum.shape,np.uint8)
  pts=np.array([[1144-x,735-y],[1430-x,698-y],[1454-x,703-y],[1456-x,830-y],[1418-x,834-y],[1165-x,815-y],[1140-x,793-y]])
  cv2.fillPoly(m,[pts],255)
 else: m=np.full(lum.shape,255,np.uint8)
 if kind in ['light','dark']: m=cv2.dilate(m,np.ones((5,5),np.uint8))
 full=np.zeros((h,w),np.uint8);full[y:y2,x:x2]=m
 rgba=np.dstack([crop,m]);path=p/'public/assets'/folder/(id+'.png');path.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(rgba).save(path)
 # Local deterministic inpainting, never synthesizes lettering or logos.
 if kind=='full':
  small=cv2.resize(current,(w//2,h//2)); mask=cv2.resize(full,(w//2,h//2),interpolation=cv2.INTER_NEAREST)
  fill=cv2.resize(cv2.inpaint(small,mask,5,cv2.INPAINT_TELEA),(w,h));current[full>0]=fill[full>0]
 else: current=cv2.inpaint(current,full,3,cv2.INPAINT_TELEA)
 layers.append(dict(id=id,name=id,file='assets/'+folder+'/'+id+'.png',x=x*1920/w,y=y*1080/h,width=(x2-x)*1920/w,height=(y2-y)*1080/h,zIndex=z,transformOrigin={'x':(x2-x)*960/w,'y':(y2-y)*540/h},**({'offerId':offer} if offer else {})))
 z-=1
peel('ar-condicionado','promotion',(1134,693,1462,839),'product')
peel('9000-btus','promotion',(1205,650,1460,718))
peel('texto-banner','promotion',(249,735,1075,771),'dark')
peel('texto-sorteio','promotion',(245,771,1077,809),'dark')
peel('banner','promotion',(174,718,1498,833),'full')
peel('footer-title','footer',(477,846,1194,879))
peel('footer-copy','footer',(485,881,1187,911))
peel('conditions-title','conditions',(680,629,999,664))
peel('conditions-boleto','conditions',(581,662,1091,691))
peel('conditions-cartao','conditions',(645,688,1037,717))
for power,label,text,box in [
 ('315',(738,291,934,332),(641,332,1033,399),(495,309,1177,408)),
 ('471',(491,411,652,449),(437,448,727,507),(334,428,828,517)),
 ('628',(1016,411,1181,449),(957,448,1243,507),(844,428,1339,517)),
 ('785',(490,519,657,558),(434,556,729,617),(334,536,828,626)),
 ('942',(1015,519,1182,558),(951,556,1247,617),(844,536,1339,626))]:
 folder='offers/offer-'+power
 peel('label-'+power,folder,label,'full',power)
 peel('text-'+power,folder,text,'light',power)
 peel('box-'+power,folder,box,'full',power)
peel('logo','logo',(702,6,952,100))
peel('black-friday','titles',(497,97,1210,165))
peel('primeira-parcela','titles',(598,168,1070,201))
peel('90-dias','titles',(646,201,1031,260))
peel('confira-ofertas','titles',(705,261,970,289))
# Decorative bottom contour, limited to the border to retain the landscape.
peel('decoracao-inferior','footer',(86,865,1587,941),'light')
Image.fromarray(current).save(p/'public/assets/background/background.png')
layers.append(dict(id='background',name='Background reconstruído',file='assets/background/background.png',x=0,y=0,width=1920,height=1080,zIndex=0,transformOrigin={'x':960,'y':540}))
layers.sort(key=lambda l:l['zIndex'])
(p/'src/data/layers.json').write_text(json.dumps(layers,ensure_ascii=False,indent=2)+'\n')
# Native-resolution recomposition for pixel verification, before browser resampling.
canvas=Image.fromarray(current).convert('RGBA')
for l in layers[1:]:
 tile=Image.open(p/'public'/l['file']); canvas.alpha_composite(tile,(round(l['x']*w/1920),round(l['y']*h/1080)))
ref=Image.fromarray(im).resize((1920,1080),Image.Resampling.LANCZOS)
ref.save(p/'previews/reference-1920x1080.png')
canvas.convert('RGB').resize((1920,1080),Image.Resampling.LANCZOS).save(p/'previews/reconstruction-python.png')
diff=np.abs(np.array(canvas.convert('RGB')).astype(int)-im.astype(int))
(p/'previews/extraction-metrics.json').write_text(json.dumps({'nativeWidth':w,'nativeHeight':h,'layers':len(layers),'nativeRecompositionMAE':float(diff.mean()),'nativeMaxDifference':int(diff.max()),'method':'binary masks with 2px context; deterministic inpainting; not a recovered original background'},indent=2))
print('Layers',len(layers),'native MAE',diff.mean(),'max',diff.max())
