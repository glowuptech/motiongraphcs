from pathlib import Path
import numpy as np,wave
p=Path(__file__).resolve().parents[1]/'public/audio';p.mkdir(exist_ok=True)
sr=48000;t=np.arange(sr*10)/sr;out=np.zeros_like(t);rng=np.random.default_rng(61)
# Original synthesis, no third-party recordings or melodies.
for beat in np.arange(0,10,.5):
 u=t-beat;m=u>=0
 out+=m*.19*np.sin(2*np.pi*(48*u+5*(1-np.exp(-30*np.maximum(u,0)))))*np.exp(-18*np.maximum(u,0))
for j,start in enumerate(np.arange(0,10,.25)):
 u=t-start;v=np.maximum(u,0);freq=[220,329.63,440,293.66,261.63,329.63,392,293.66][j%8]
 out+=(u>=0)*.055*(np.sin(2*np.pi*freq*v)+.25*np.sin(4*np.pi*freq*v))*np.exp(-12*v)*np.minimum(v*150,1)
for frame in [14,30,66,87,108,129,150,171,207,246]:
 u=t-frame/30;v=np.maximum(u,0);noise=rng.normal(0,1,len(t));env=(u>=0)*np.minimum(v*60,1)*np.exp(-14*v)
 out+=.04*noise*env
 if frame in [14,30,207]:out+=.15*(u>=0)*np.sin(2*np.pi*52*v)*np.exp(-10*v)
out*=np.minimum(t*30,1)*np.minimum((10-t)*5,1);out=np.tanh(out);st=np.stack([out,out*.98],axis=1)
with wave.open(str(p/'giotto-original.wav'),'w') as f:f.setnchannels(2);f.setsampwidth(2);f.setframerate(sr);f.writeframes((st*26000).astype('<i2').tobytes())
(p/'README.md').write_text('Trilha e efeitos sintetizados originalmente para este projeto, sem samples ou gravações de terceiros. Gerador determinístico: scripts/generate_audio.py. Eventos sincronizados nos frames 14,30,66,87,108,129,150,171,207,246.\n')
