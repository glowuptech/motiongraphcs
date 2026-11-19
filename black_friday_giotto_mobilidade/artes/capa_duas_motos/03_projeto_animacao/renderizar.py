"""Renderize com Python 3, Pillow, NumPy e FFmpeg."""
from pathlib import Path
import json
import math
import subprocess
import tempfile
import wave

import numpy as np
from PIL import Image, ImageChops, ImageFilter

ART = Path(__file__).resolve().parents[1]
LAYERS = ART / '02_elementos_separados'
OUT = ART.parents[1] / 'videos_finais' / 'capa_duas_motos_impacto_v01.mp4'
TIMELINE = json.loads((LAYERS / 'camadas.json').read_text())
W, H = TIMELINE['largura'], TIMELINE['altura']
HIT = 1.2
FPS = 30


def group(prefixes):
    canvas = Image.new('RGBA', (W, H))
    for item in TIMELINE['camadas']:
        if item['arquivo'].startswith(prefixes):
            canvas.alpha_composite(Image.open(LAYERS / item['arquivo']).convert('RGBA'), (item['x'], item['y']))
    bounds = canvas.getbbox()
    return canvas.crop(bounds), bounds[:2]


def progress(t, start, length):
    return max(0, min(1, (t-start)/length))


def place(canvas, layer, dx=0, dy=0, opacity=1):
    sprite, (x, y) = layer
    alpha = sprite.getchannel('A')
    if opacity < 1:
        alpha = alpha.point(lambda a: round(a*opacity))
    canvas.paste(sprite, (round(x+dx), round(y+dy)), alpha)


def smoke_texture(rng):
    size = 142
    yy, xx = np.mgrid[-1:1:complex(size), -1:1:complex(size)]
    noise = np.zeros((size,size))
    for grid, weight in [(5,.48), (12,.29), (27,.15), (56,.08)]:
        field = Image.fromarray(rng.integers(0,256,(grid,grid),dtype=np.uint8)).resize((size,size),Image.Resampling.BICUBIC)
        noise += weight*np.asarray(field)/255
    mass = np.clip(1-xx*xx-yy*yy+(noise-.5)*1.6,0,1)**1.5
    shade = 78+113*noise
    rgba = np.stack((shade*.91,shade,shade*.88, mass*noise*210), axis=-1)
    return Image.fromarray(rgba.astype('uint8'))


def soundtrack(path):
    rate = 48000
    t = np.arange(10*rate)/rate
    rng = np.random.default_rng(51)
    noise = rng.uniform(-1,1,t.size)
    hiss = np.convolve(noise,np.ones(9)/9,'same')
    dt = np.maximum(t-HIT,0)
    hit = (t>=HIT)*(1-np.exp(-dt*750))*(.67*np.sin(2*np.pi*(42*dt+4*(1-np.exp(-dt*13))))*np.exp(-dt*5)
          + .53*noise*np.exp(-dt*33)+.29*hiss*np.exp(-dt*2.6))
    sweep = np.clip((t-.47)/.73,0,1)**2 * (t<HIT)*hiss*.64
    sound = np.tanh(hit+sweep)
    with wave.open(str(path),'wb') as wav:
        wav.setparams((1,2,rate,0,'NONE',''))
        wav.writeframes((sound*27000).astype('<i2').tobytes())


def render():
    background = group(('fundo','circuitos'))[0].convert('RGB')
    # Escureça o cenário no início para destacar o letreiro e a fumaça.
    soft = background.filter(ImageFilter.GaussianBlur(20))
    dimmed = Image.blend(Image.new('RGB',(W,H),(3,7,9)),soft,.32)
    title = group(('placa-black','titulo-'))
    band = group(('faixa-','subtitulo-'))
    left, right, logo = group('moto-bis'), group('moto-x1'), group('marca-')
    rng = np.random.default_rng(71)
    clouds = [(s, rng.uniform(0,.22), rng.uniform(24,130), rng.uniform(240,510),
               rng.uniform(70,175), rng.uniform(90,175), smoke_texture(rng))
              for s in (-1,1) for _ in range(12)]
    original = Image.open(next((ART/'01_arte_original').glob('*.png'))).convert('RGB')
    with tempfile.TemporaryDirectory(dir=OUT.parent) as temp:
        temp = Path(temp)
        soundtrack(temp/'impacto.wav')
        cmd = ['ffmpeg','-v','error','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}',
               '-framerate',str(FPS),'-i','pipe:0','-i',str(temp/'impacto.wav'),'-vf','scale=1920:1080:flags=lanczos,setsar=1',
               '-c:v','libx264','-threads','3','-preset','veryfast','-crf','17','-pix_fmt','yuv420p',
               '-c:a','aac','-b:a','128k','-movflags','+faststart',str(temp/'video.mp4')]
        with subprocess.Popen(cmd,stdin=subprocess.PIPE) as proc:
            hold = None
            for frame in range(300):
                t = frame/FPS
                if hold is not None:
                    proc.stdin.write(hold)
                    continue
                scene = Image.blend(dimmed,background,progress(t,2.9,3.4))
                fall = progress(t,.37,HIT-.37)
                dt = t-HIT
                bounce = -39*abs(math.sin(dt*12))*math.exp(-dt*6) if dt>=0 else 0
                place(scene,title,dy=-690*(1-fall**2.25)+bounce)
                for side,delay,offset,travel,rise,base,texture in clouds:
                    age = dt-delay
                    if 0<age<1.85:
                        phase=age/1.85
                        drift=1-math.exp(-2.4*age)
                        size=round(base*(.48+1.75*drift))
                        puff=texture.resize((round(size*1.4),size),Image.Resampling.BILINEAR)
                        x=W*.5+side*(offset+travel*drift)-puff.width/2
                        y=H*.68-rise*phase+16*math.sin(phase*4+offset)-size/2
                        place(scene,(puff,(x,y)),opacity=min(1,age*14)*(1-phase)**1.6)
                for layer,start,length,dx,dy in [(band,2.64,.70,0,46),(left,3.48,1.32,-555,0),
                                                (right,4.89,1.3,580,0),(logo,6.34,.83,0,-45)]:
                    p=progress(t,start,length)
                    if p:
                        place(scene,layer,dx*(1-p)**3,dy*(1-p)**3,min(1,p*3))
                if 0<=dt<.55:
                    shake=math.exp(-dt*7)
                    sx=round(10*shake*math.sin(dt*77)); sy=round(17*shake*math.cos(dt*62))
                    zoom=.045*shake
                    scene=scene.transform(scene.size, Image.Transform.AFFINE,(1-zoom,0,W*zoom/2+sx,0,1-zoom,H*zoom/2+sy))
                    scene=Image.blend(scene,Image.new('RGB',scene.size,(218,234,184)),.14*math.exp(-dt*22))
                pixels=scene.tobytes()
                if t>=7.2:
                    assert not ImageChops.difference(scene,original).getbbox()
                    hold=pixels
                proc.stdin.write(pixels)
            proc.stdin.close()
            if proc.wait():
                raise RuntimeError('Falha na exportação')
        (temp/'video.mp4').replace(OUT)


if __name__ == '__main__':
    render()
