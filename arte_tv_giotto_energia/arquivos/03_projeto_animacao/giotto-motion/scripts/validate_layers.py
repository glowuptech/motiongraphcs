from pathlib import Path
from PIL import Image,ImageDraw,ImageChops,ImageEnhance
import numpy as np,json
p=Path(__file__).resolve().parents[1]
layers=json.loads((p/'src/data/layers.json').read_text());tiles=[]
for l in layers:
 if l['id']=='background':continue
 tile=Image.new('RGB',(400,180));dr=ImageDraw.Draw(tile)
 for y in range(0,180,16):
  for x in range(0,400,16):dr.rectangle((x,y,x+15,y+15),fill=(90,90,90) if (x//16+y//16)%2 else (150,150,150))
 im=Image.open(p/'public'/l['file']).convert('RGBA');im.thumbnail((390,145));tile.paste(im,((400-im.width)//2,25+(145-im.height)//2),im);dr.rectangle((0,0,400,23),fill='white');dr.text((5,5),l['id'],fill='black');tiles.append(tile)
out=Image.new('RGB',(1600,180*((len(tiles)+3)//4)), 'white')
for i,t in enumerate(tiles):out.paste(t,((i%4)*400,(i//4)*180))
out.save(p/'previews/layers-contact-sheet.jpg',quality=92)
a=Image.open(p/'previews/reference-1920x1080.png').convert('RGB');b=Image.open(p/'previews/frame.png').convert('RGB');d=ImageChops.difference(a,b);ImageEnhance.Brightness(d).enhance(5).save(p/'previews/difference-x5.png')
c=Image.new('RGB',(3840,1080));c.paste(a);c.paste(b,(1920,0));c.save(p/'previews/comparison.png')
print('Layers',len(layers),'Remotion MAE',np.array(d).mean())
