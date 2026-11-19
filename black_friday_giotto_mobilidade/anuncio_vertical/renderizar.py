"""Python 3, Pillow, NumPy, OpenCV e FFmpeg. Execute a partir de qualquer pasta."""
import math
import json
import subprocess
import tempfile
import wave
from functools import lru_cache
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT/'artes'
OUT = ROOT/'videos_finais'/'giotto_black_friday_reels_20s_v02.mp4'
W,H,FPS=1080,1920,30
LIME=(184,255,19)
WHITE=(242,246,237)
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-BoldOblique.ttf'
cv2.setNumThreads(1)


def asset(project, name):
    return Image.open(ART/project/'02_elementos_separados'/f'{name}.png').convert('RGBA')


def logo():
    folder=ART/'capa_duas_motos'/'02_elementos_separados'
    img=Image.new('RGBA',(1672,941))
    for row in json.loads((folder/'camadas.json').read_text())['camadas']:
        if row['arquivo'].startswith('marca-'):
            img.alpha_composite(Image.open(folder/row['arquivo']),(row['x'],row['y']))
    return img.crop(img.getbbox())


LOGO=logo()
BLACK,FRIDAY=[asset('capa_duas_motos','titulo-'+word) for word in ('black','friday')]
RECORTES = Path(__file__).resolve().parent / 'recortes'
X1 = Image.open(RECORTES / 'moto-x1.png').convert('RGBA')
BIS = Image.open(RECORTES / 'moto-bis.png').convert('RGBA')
AC = Image.open(RECORTES / 'split.png').convert('RGBA')
def clamp(x): return max(0,min(1,x))
def ease(x): return 1-(1-clamp(x))**3
def sprite(im,obj,cx,cy,width):
    width=max(1,round(width))
    s=obj.resize((width,max(1,round(width*obj.height/obj.width))),Image.Resampling.BICUBIC)
    im.paste(s,(round(cx-width/2),round(cy-s.height/2)),s)


@lru_cache(maxsize=150)
def lettering(msg,size,color,limit):
    font=ImageFont.truetype(FONT,size)
    box=font.getbbox(msg)
    if box[2]-box[0]>limit:
        font=ImageFont.truetype(FONT,int(size*limit/(box[2]-box[0])))
        box=font.getbbox(msg)
    im=Image.new('RGBA',(box[2]-box[0]+8,box[3]-box[1]+8))
    ImageDraw.Draw(im).text((4-box[0],4-box[1]),msg,font=font,fill=color)
    return im


def text(im,msg,y,size,color=WHITE,limit=930,x=540):
    obj=lettering(msg,size,color,limit)
    im.paste(obj,(round(x-obj.width/2),round(y-obj.height/2)),obj)


def ribbon(im,msg,y,width=840,height=100,size=71):
    d=ImageDraw.Draw(im); l=(W-width)//2;r=W-l
    d.polygon([(l+26,y-height/2+6),(r+5,y-height/2+6),(r-20,y+height/2+7),(l,y+height/2+7)],fill=(50,80,17))
    d.polygon([(l+24,y-height/2),(r,y-height/2),(r-24,y+height/2),(l,y+height/2)],fill=LIME)
    text(im,msg,y,size,(13,20,12),width-74)


def backdrop():
    y,x=np.mgrid[:H,:W]
    rng=np.random.default_rng(13)
    glow=np.exp(-((x-660)/480)**2-((y-1030)/720)**2)
    floor=np.exp(-((x-480)/450)**2-((y-1430)/180)**2)
    beam=np.exp(-((x-270+.44*y)/(60+.12*y))**2)*np.exp(-y/890)
    rim=np.exp(-((x-965+.086*(y-960))/65)**2-((y-850)/630)**2)
    glow=glow+.9*beam+.72*rim
    brushed=rng.normal(0,1.1,(H,W))
    base=np.stack([7+11*glow+10*floor+brushed,11+25*glow+20*floor+brushed,
                   13+15*glow+10*floor+brushed],axis=-1)
    im=Image.fromarray(np.uint8(np.clip(base,0,255)));d=ImageDraw.Draw(im)
    for side in (1,-1):
        for k in range(5):
            a=18+k*15
            pts=[(a,0),(a,282-k*33),(a+58,340-k*33),(a+58,525-k*38),(a,585-k*38),(a,1060+k*54)]
            if side==-1:pts=[(W-u,H-v) for u,v in pts]
            d.line(pts,fill=(42+4*k,64+5*k,29),width=2)
    bloom=im.filter(ImageFilter.GaussianBlur(8))
    im=Image.blend(im,Image.fromarray(cv2.addWeighted(np.asarray(im),1,np.asarray(bloom),.46,0)),.8)
    d=ImageDraw.Draw(im)
    for end in range(-3200,4400,240):
        d.line([(540+(end-540)*.05,1210),(end,1920)],fill=(26,45,37),width=2)
    for y0 in [1250,1272,1305,1350,1415,1507,1640,1825]:d.line((0,y0,W,y0),fill=(27,43,37),width=2)
    return im
BG=backdrop()


def stage(im,x,y,rx,ry):
    d=ImageDraw.Draw(im)
    for inset,drop,col in [(0,14,(24,33,34)),(0,7,(85,116,51)),(0,3,(131,180,60)),(1,0,(32,42,39))]:
        d.ellipse((x-rx+inset,y-ry+drop,x+rx-inset,y+ry+drop),fill=col)
    d.ellipse((x-rx+14,y-ry+3,x+rx-14,y+ry-3),outline=(69,88,68),width=2)
    d.ellipse((x-rx*.66,y-ry*.48,x+rx*.66,y+ry*.58),fill=(18,25,24))


def product3d(im,t):
    # A foto inclui a saída de ar e as bordas arredondadas do gabinete.
    # Transforme toda a silhueta junta durante o giro.
    yaw = math.radians(8) * math.sin(t * 1.38 - .7)
    width = 765
    height = width * AC.height / AC.width
    corners = []
    for x, y in [(-width/2, -height/2), (width/2, -height/2),
                 (width/2, height/2), (-width/2, height/2)]:
        perspective = 1800 / (1800 - x * math.sin(yaw))
        corners.append((540 + x * math.cos(yaw) * perspective,
                        945 + y * perspective - 7 * math.sin(t * 1.7)))
    target = np.float32(corners)
    origin = np.floor(target.min(axis=0)).astype(int) - 2
    extent = np.ceil(target.max(axis=0) - origin).astype(int) + 3
    source = np.float32([[0, 0], [AC.width-1, 0],
                         [AC.width-1, AC.height-1], [0, AC.height-1]])
    transform = cv2.getPerspectiveTransform(source, target - origin.astype(np.float32))
    premultiplied = np.asarray(AC.convert('RGBa'))
    warp = cv2.warpPerspective(premultiplied, transform, tuple(map(int, extent)),
                               flags=cv2.INTER_LINEAR)
    patch = Image.frombytes('RGBa', tuple(map(int, extent)), warp.tobytes()).convert('RGBA')
    im.paste(patch, tuple(map(int, origin)), patch)


def energy(im,t,boost):
    d=ImageDraw.Draw(im)
    for k in range(8):
        x=16+k*9 if k<4 else 1064-(k-4)*9
        y=int((t*(260+32*k)+173*k)%2150)-140
        d.line((x,y-110,x,y+30),fill=(75,120,43),width=4)
        d.line((x,y,x,y+30),fill=LIME,width=3)
    if boost:
        for k in range(3):
            points=[(int(960-800*i/20+29*math.sin(83*i+k*7+t*63)),i*96) for i in range(21)]
            d.line(points,fill=(round(96*boost),round(203*boost),round(56*boost)),width=9-k*3)


@lru_cache(maxsize=160)
def polished(word,phase):
    base=BLACK if word=='black' else FRIDAY
    if phase>=32:return base
    a=np.array(base); yy,xx=np.ogrid[:base.height,:base.width]
    shine=100*np.exp(-((xx-.42*yy-(phase/31*1.6-.26)*base.width)/48)**2)
    a[:,:,:3]=np.minimum(255,a[:,:,:3]+shine[:,:,None]).astype('uint8')
    return Image.fromarray(a)


def titles(im,cy,width,phase):
    sprite(im,polished("black",phase),540,cy-width*.125,width)
    sprite(im,polished("friday",phase),540,cy+width*.125,width*.98)


def frame(t):
    im=BG.copy()
    bounds=(0,3,7,11,16)
    idx=max(i for i in range(5) if bounds[i]<=t)
    u=t-bounds[idx];d=ImageDraw.Draw(im)
    energy(im,t,(1-clamp(u/.24)) if idx else 0)
    if idx==0:
        sprite(im,LOGO,540,475,320*ease(u/.42)+1)
        if u>.45:
            q=ease((u-.45)/.52)
            titles(im,915+80*(1-q),890+120*(1-q),max(0,min(32,int((u-.6)*31))))
        if u>.90:ribbon(im,'GIOTTO MOBILIDADE',1245+round(66*(1-ease((u-.9)/.33))))
        flash=max(0,1-abs(u-.49)/.13)*.54
        if flash:im=Image.blend(im,Image.new('RGB',im.size,(217,255,165)),flash)
        if t<.26:im=Image.blend(Image.new('RGB',im.size),im,ease(t/.26))
    elif idx==1:
        stage(im,565,1250,504,94)
        # Staggered positions and camera push create parallax between the models.
        sprite(im,BIS,287-490*(1-ease(u/.64))+9*u,939,475+5*u)
        sprite(im,X1,740+520*(1-ease((u-.10)/.78))-9*u,1007,561+6*u)
        if u<2.06:
            text(im,'SUA ELÉTRICA NOVA',450,107)
            text(im,'ESTÁ AQUI!',575,143,LIME)
        else:
            text(im,'MODELOS',450,67)
            text(im,'X1 E BIS',580,167,LIME)
    elif idx==2:
        stage(im,541,855,385,60)
        sprite(im,X1,540+80*(1-ease(u/.55)),584,550)
        rise=round(125*(1-ease(u/.52)))
        panel=[(78,916+rise),(950,916+rise),(1004,970+rise),(1004,1280+rise),(947,1337+rise),(78,1337+rise)]
        d.polygon(panel,fill=(17,24,25),outline=(146,202,61),width=3)
        text(im,'A PARTIR DE',996+rise,63)
        # Revele o valor de baixo para cima, mantendo o preço original.
        val=lettering('R$ 8.500',204,LIME,880)
        reveal=ease((u-.16)/.46)
        if reveal:
            strip=val.crop((0,0,val.width,max(1,round(val.height*reveal))))
            im.paste(strip,((W-val.width)//2,round(1134+rise-val.height/2+36*(1-reveal))),strip)
        text(im,'À VISTA',1260+rise,66)
        if u>.65:ribbon(im,'ATÉ 21X SEM JUROS NO CARTÃO',1452,956,102,58)
    elif idx==3:
        if u<2.05:
            text(im,'COMPROU SUA ELÉTRICA',491,92)
            text(im,'EM NOVEMBRO?',605,112,LIME)
        else:
            text(im,'PARTICIPE DO',477,94)
            text(im,'SORTEIO DE UM',588,112,LIME)
        for k in range(34):
            x=(k*143+38*math.sin(u+k))%960+60;y=820+((k*89-u*(35+k))%370)
            d.ellipse((x,y,x+3+k%3,y+3+k%3),fill=(115,162,65))
        stage(im,540,1166,437,58)
        product3d(im,u)
        if u>=2.05:ribbon(im,'AR-CONDICIONADO!',1344,950,140,98)
    else:
        sprite(im,LOGO,540,410,288)
        titles(im,719,696,min(32,int(u*26)))
        ribbon(im,'GIOTTO MOBILIDADE',970,785,80,64)
        stage(im,540,1412,493,46)
        sprite(im,BIS,290-380*(1-ease(u/.61)),1221,386)
        sprite(im,X1,778+380*(1-ease(u/.72)),1235,408)
        if u>.48:text(im,'APROVEITE AS CONDIÇÕES ESPECIAIS!',1502,64,LIME,958)
        for side in (35,1044):
            top=int((u*870)%2300)-290
            d.line((side,top,side,top+280),fill=LIME,width=5)
    if idx and u<.12:
        im=Image.blend(im,Image.new('RGB',im.size,(205,255,168)),.48*(1-u/.12))
    return im


def score(path):
    sr=48000; total=20*sr
    music=np.zeros(total);rng=np.random.default_rng(84)
    def add(start,wav):
        i=round(start*sr);n=min(len(wav),total-i)
        if n>0:music[i:i+n]+=wav[:n]
    def times(s):return np.arange(round(s*sr))/sr
    roots=[41.203,41.203,49,36.708]
    for step in range(160):
        start=step*.125;root=roots[(step//16)%4];x=times(.24)
        env=(1-np.exp(-x*150))*np.exp(-x*18)
        if step%4 in (0,3):
            add(start,.21*env*(np.sin(2*np.pi*root*x)+.32*np.sin(4*np.pi*root*x)))
        pitch=root*4*[1,1.5,2,1.25,1.5,2,2.5,1.5][step%8]
        add(start,.080*env*(np.sin(2*np.pi*pitch*x)+.32*np.sin(4*np.pi*pitch*x)))
        if step%4==0:add(start,.48*np.exp(-x*16)*np.sin(2*np.pi*(48*x+2.6*(1-np.exp(-x*35)))))
        noise=rng.normal(0,1,len(x));noise=np.diff(noise,prepend=0)
        if step%2==0:add(start,.075*noise*np.exp(-x*83))
        if step%8==4:add(start,.14*noise*np.exp(-x*29))
    for hit in (.49,3,7,11,16):
        x=times(.35);add(hit-.35,.15*rng.uniform(-1,1,len(x))*(x/.35)**2)
        x=times(.65);add(hit,.36*np.exp(-x*9)*np.sin(2*np.pi*(40*x+3*(1-np.exp(-x*16)))))
    music[-12000:]*=np.linspace(1,0,12000)
    with wave.open(str(path),'wb') as wav:
        wav.setparams((1,2,sr,0,'NONE',''));wav.writeframes((np.tanh(music*1.45)*30600).astype('<i2').tobytes())


if __name__=='__main__':
    with tempfile.TemporaryDirectory(dir=OUT.parent) as temp:
        tmp=Path(temp);score(tmp/'trilha.wav')
        cmd=['ffmpeg','-v','error','-f','rawvideo','-pixel_format','rgb24','-video_size','1080x1920','-framerate','30','-i','pipe:0','-i',str(tmp/'trilha.wav'),'-c:v','libx264','-threads','4','-crf','17','-preset','veryfast','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-movflags','+faststart',str(tmp/'final.mp4')]
        with subprocess.Popen(cmd,stdin=subprocess.PIPE) as p:
            for i in range(FPS*20):p.stdin.write(frame(i/FPS).tobytes())
            p.stdin.close()
            if p.wait():raise RuntimeError('Falha ao exportar o vídeo')
        (tmp/'final.mp4').replace(OUT)
