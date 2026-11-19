"""Renderize com /usr/bin/python3 renderizar_motion.py NOME_DA_ARTE."""
import json
import math
import subprocess
import sys
import tempfile
from pathlib import Path
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parent
FPS = 30
FRAMES = 300
# Início, duração e deslocamentos iniciais em pixels do original.
CUES = {
    'circuitos': (0.05, .72, 0, 0), 'marca': (.16, .70, 0, -40),
    'titulo': (.42, .85, -155, 0), 'subtitulo': (.75, .7, 110, 0),
    'moto': (.85, 1.78, None, 0), 'chamada': (1.45, .62, -64, 0),
    'modelo': (2.0, .62, -94, 0), 'preco': (2.34, .7, -112, 0),
    'parcelamento': (2.72, .62, -66, 0), 'sorteio': (2.5, .7, 92, 0),
    'ar': (2.82, .76, 110, 0), 'premio': (3.13, .65, 72, 0),
    'rodape': (3.68, .72, 0, 29), 'whatsapp': (3.90, .78, 0, 66),
}

def render(name):
    art = ROOT / 'artes' / name
    assets = art / '02_elementos_separados'
    settings = json.loads((art / '03_projeto_animacao' / 'motion.json').read_text())
    data = json.loads((assets / 'camadas.json').read_text())
    original = Image.open(next((art / '01_arte_original').glob('*.png'))).convert('RGB')
    background = Image.open(assets / 'fundo.png').convert('RGB')
    night = Image.new('RGB', original.size, (4, 8, 12))
    layers = []
    for layer in data['camadas'][1:]:
        key = Path(layer['arquivo']).stem
        group = key.split('-')[0]
        start, duration, dx, dy = CUES[group]
        if group == 'moto':
            dx = original.width - layer['x'] + 12
        # A placa e o texto viajam juntos, com uma pequena defasagem.
        if 'texto' in key or key in ('whatsapp-icone', 'whatsapp-chamada'):
            start += .10
        if group == 'chamada':
            start += (int(key[-1]) - 1) * .095
        start += settings['atrasos'].get(key, 0)
        sprite = Image.open(assets / layer['arquivo']).convert('RGBA')
        layers.append((sprite, sprite.getchannel('A'), layer, start, duration, dx, dy))

    output = ROOT / 'videos_finais' / (name + '_v01.mp4')
    with tempfile.TemporaryDirectory(dir=output.parent) as temp:
        draft = Path(temp) / 'render.mp4'
        cmd = ['ffmpeg','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24',
               '-s',f'{original.width}x{original.height}','-r',str(FPS),'-i','pipe:0',
               '-vf','scale=1920:1080:flags=lanczos,setsar=1','-c:v','libx264',
               '-threads','3','-preset','veryfast','-crf','17','-pix_fmt','yuv420p',
               '-movflags','+faststart',str(draft)]
        with subprocess.Popen(cmd, stdin=subprocess.PIPE) as encoder:
            held = None
            for frame in range(FRAMES):
                t = frame / FPS
                if held is None:
                    canvas = Image.blend(night, background, min(1, t / 2.8))
                    for sprite, mask, layer, start, duration, dx, dy in layers:
                        progress = min(1, max(0, (t-start)/duration))
                        if progress == 0:
                            continue
                        rem = (1-progress)**3
                        x, y = round(layer['x']+dx*rem), round(layer['y']+dy*rem)
                        alpha = min(1, progress*3)
                        canvas.paste(sprite, (x,y), mask if alpha==1 else mask.point(lambda v: round(v*alpha)))
                    pixels = canvas.tobytes()
                    if t >= 5:
                        assert ImageChops.difference(canvas, original).getbbox() is None
                        held = pixels
                encoder.stdin.write(held if held is not None else pixels)
            encoder.stdin.close()
            if encoder.wait():
                raise RuntimeError('Falha ao codificar o MP4')
        draft.replace(output)

if __name__ == '__main__':
    render(sys.argv[1])
