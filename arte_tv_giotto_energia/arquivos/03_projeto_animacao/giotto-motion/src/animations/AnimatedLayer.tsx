import {AbsoluteFill, Img, staticFile, Easing, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {Layer, type LayerData} from '../components/Layer';
import {timeline} from '../config/animation-timeline';
const clamp={extrapolateLeft:'clamp',extrapolateRight:'clamp'} as const;
export const AnimatedLayer=({layer}:{layer:LayerData})=>{
 const f=useCurrentFrame();const {fps}=useVideoConfig();
 const id=layer.id; const start=layer.offerId?timeline.offers[layer.offerId]:timeline.starts[id]??0;
 const t=f-start;const done=f>=264||t>=30;
 const s=done?1:spring({frame:Math.max(0,t),fps,config:{damping:15,stiffness:180,mass:0.65}});
 const settle=1-s;let x=0,y=0,scale=1,rotate=0,sx=1;
 const origin=`${layer.x+layer.width/2}px ${layer.y+layer.height/2}px`;
 if(id==='background')return <AbsoluteFill style={{transform:`scale(${interpolate(f,[0,264],[1.015,1],clamp)})`}}><Img src={staticFile('assets/background/background-motion.png')} style={{width:1920,height:1080}}/><AbsoluteFill style={{opacity:interpolate(f,[240,264],[0,1],clamp)}}><Layer layer={layer}/></AbsoluteFill></AbsoluteFill>;
 if(t<0)return null;
 if(id==='logo')scale=0.8+0.2*s;
 else if(id==='90-dias'){
  const travel=interpolate(t,[16,35],[0,1],{...clamp,easing:Easing.inOut(Easing.cubic)});
  scale= t<16?1.1+0.7*(1-s):1.1-0.1*travel;y=170*(1-travel);
 }else if(layer.offerId){
  const n=layer.offerId;x=(n==='471'?-110:n==='628'?110:0)*settle;
  y=(n==='315'?-45:n==='785'||n==='942'?45:0)*settle;scale=1+0.04*settle;
 }else if(id==='ar-condicionado'){x=150*settle;rotate=4*settle;scale=1+0.15*settle;}
 else if(id==='banner')sx=Math.max(0.01,s);
 else if(id==='9000-btus')scale=0.75+0.25*s;
 else y=32*settle;
 const visible=interpolate(t,[0,5],[0,1],clamp);
 const blur=done?0:Math.max(0,settle)*2;
 return <AbsoluteFill style={{zIndex:layer.zIndex,opacity:visible,transformOrigin:origin,transform:`translate(${x}px,${y}px) rotate(${rotate}deg) scale(${scale*sx},${scale})`,filter:`blur(${blur}px)`}}><Layer layer={layer}/></AbsoluteFill>;
};
