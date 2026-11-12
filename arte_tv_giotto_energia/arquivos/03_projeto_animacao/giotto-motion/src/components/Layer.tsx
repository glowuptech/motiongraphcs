import {Img, staticFile} from 'remotion';
export type LayerData = {id:string; name:string; file:string; x:number; y:number; width:number; height:number; zIndex:number; transformOrigin:{x:number;y:number}; offerId?:string};
export const Layer = ({layer}:{layer:LayerData}) => <Img src={staticFile(layer.file)} style={{position:'absolute',left:layer.x,top:layer.y,width:layer.width,height:layer.height,zIndex:layer.zIndex,transformOrigin:`${layer.transformOrigin.x}px ${layer.transformOrigin.y}px`}}/>;
