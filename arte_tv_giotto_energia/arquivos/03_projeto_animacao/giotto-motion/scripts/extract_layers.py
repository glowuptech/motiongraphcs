from pathlib import Path
import numpy as np, cv2, json
from PIL import Image
root=Path(__file__).resolve().parents[4]
p=root/'arquivos/03_projeto_animacao/giotto-motion'
src=next((root/'arquivos/01_arte_original').glob('*.png'))
im=np.array(Image.open(src).convert('RGB')); h,w=im.shape[:2]
current=im.copy(); layers=[]; z=100
# Peel foreground first; each mask restores exactly the pixels removed at this step.
def peel(id,folder,box,kind='light',offer=None):
 global current,z
 x,y,x2,y2=box
 # Include the existing shadow around each glyph and solve a smooth underlying plate.
 pad=0 if id.startswith('label-') else 6
 x=max(0,x-pad);y=max(0,y-pad);x2=min(w,x2+pad);y2=min(h,y2+pad)
 crop=current[y:y2,x:x2].copy(); ch,cw=crop.shape[:2]
 m=np.zeros((ch,cw),np.uint8)
 if kind in ('light','dark'):
  if kind=='light': seed=(crop.max(2)>105).astype(np.uint8)*255
  else: seed=(crop.min(2)<100).astype(np.uint8)*255
  # Constrain seeds to the original specified content rectangle.
  if pad: seed[:pad]=0;seed[-pad:]=0;seed[:,:pad]=0;seed[:,-pad:]=0
  m=cv2.dilate(seed,np.ones((13,13),np.uint8))
 elif kind=='product':
  pts=np.array([[1144-x,735-y],[1430-x,698-y],[1454-x,703-y],[1456-x,830-y],[1418-x,834-y],[1165-x,815-y],[1140-x,793-y]])
  cv2.fillPoly(m,[pts],255)
  m=cv2.dilate(m,np.ones((17,17),np.uint8))
 else:
  # Rounded silhouettes for cards, labels and banner, instead of opaque rectangular crops.
  radius=18 if id.startswith('label') else 24
  radius=min(radius,ch//2-1)
  cv2.rectangle(m,(radius,1),(cw-radius-1,ch-2),255,-1)
  cv2.rectangle(m,(1,radius),(cw-2,ch-radius-1),255,-1)
  for cx,cy in [(radius,radius),(cw-radius-1,radius),(radius,ch-radius-1),(cw-radius-1,ch-radius-1)]: cv2.circle(m,(cx,cy),radius,255,-1)
 full=np.zeros((h,w),np.uint8);full[y:y2,x:x2]=m
 # Harmonic fill: no generative lettering, no background texture cloned into glyphs.
 margin=24; ax=max(0,x-margin);ay=max(0,y-margin);bx=min(w,x2+margin);by=min(h,y2+margin)
 region=current[ay:by,ax:bx].astype(np.float32); hole=full[ay:by,ax:bx]>0
 fill=cv2.inpaint(region.astype(np.uint8),hole.astype(np.uint8)*255,5,cv2.INPAINT_TELEA).astype(np.float32)
 for _ in range(350):
  sm=cv2.GaussianBlur(fill,(0,0),3)
  fill[hole]=sm[hole]
 after=current.copy();after[ay:by,ax:bx][hole]=np.clip(fill[hole],0,255).astype(np.uint8)
 back=after[y:y2,x:x2].astype(float);orig=crop.astype(float);delta=orig-back
 # Solve C = alpha*F + (1-alpha)*B with a bounded foreground, preserving pixel colors.
 pos=np.maximum(delta,0)/np.maximum(255-back,1)
 neg=np.maximum(-delta,0)/np.maximum(back,1)
 alpha=np.maximum(pos,neg).max(2)
 alpha=np.ceil(alpha*255)/255
 alpha[m==0]=0
 fg=np.where(alpha[:,:,None]>0,back+delta/np.maximum(alpha[:,:,None],1/255),0)
 rgba=np.dstack([np.clip(np.rint(fg),0,255).astype(np.uint8),np.rint(alpha*255).astype(np.uint8)])
 path=p/'public/assets'/folder/(id+'.png');path.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(rgba).save(path)
 current=after
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
 peel('text-'+power,folder,text,'light',power)
 peel('label-'+power,folder,label,'full',power)
 peel('box-'+power,folder,box,'full',power)
peel('logo','logo',(702,6,952,100))
peel('black-friday','titles',(497,97,1210,165))
peel('primeira-parcela','titles',(598,168,1070,201))
peel('90-dias','titles',(646,201,1031,260))
peel('confira-ofertas','titles',(705,261,970,289))
peel('brilho-produto','effects',(1080,650,1530,865))
peel('brilho-titulo','effects',(370,106,1240,170))
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
(p/'previews/extraction-metrics.json').write_text(json.dumps({'nativeWidth':w,'nativeHeight':h,'layers':len(layers),'nativeRecompositionMAE':float(diff.mean()),'nativeMaxDifference':int(diff.max()),'method':'continuous alpha solved against harmonic background plates; hidden scenery reconstructed'},indent=2))
print('Layers',len(layers),'native MAE',diff.mean(),'max',diff.max())
