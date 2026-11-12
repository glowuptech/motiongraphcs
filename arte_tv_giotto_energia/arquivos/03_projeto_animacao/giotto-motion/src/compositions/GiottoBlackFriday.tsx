import {AbsoluteFill} from 'remotion';
import {Layer, type LayerData} from '../components/Layer';
import {Offer} from '../components/Offer';
import data from '../data/layers.json';
import offers from '../data/offers.json';
export const GiottoBlackFriday = () => {
 const layers = data as LayerData[];
 if (!layers.length) throw new Error('Extração pendente: anexe a imagem original em PNG/JPG antes de renderizar.');
 return <AbsoluteFill>{layers.filter(l=>!l.offerId).map(layer=><Layer key={layer.id} layer={layer}/>)}{offers.map(o=><Offer key={o.id} layers={layers.filter(l=>l.offerId===o.id)}/>)}</AbsoluteFill>;
};
