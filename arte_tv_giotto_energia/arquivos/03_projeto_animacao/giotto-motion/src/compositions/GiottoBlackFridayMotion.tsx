import {AbsoluteFill, Audio, staticFile, useCurrentFrame, interpolate} from 'remotion';
import layers from '../data/layers.json';
import {AnimatedLayer} from '../animations/AnimatedLayer';
export const GiottoBlackFridayMotion=({muted=false}:{muted?:boolean})=>{
 const f=useCurrentFrame();
 return <AbsoluteFill style={{backgroundColor:'#03232f',overflow:'hidden'}}>
 {layers.map(layer=><AnimatedLayer key={layer.id} layer={layer}/>)}
 {f<27&&<div style={{position:'absolute',zIndex:120,top:155,left:interpolate(f,[0,26],[-300,1920]),width:250,height:2,background:'linear-gradient(90deg,transparent,#a3ff39,transparent)',boxShadow:'0 0 16px #9aff35',opacity:Math.sin(Math.PI*f/27)}}/>}
 {!muted&&<Audio src={staticFile('audio/giotto-original.wav')}/>}
 </AbsoluteFill>;
};
