import {Layer, type LayerData} from './Layer';
export const Offer = ({layers}:{layers:LayerData[]}) => <>{layers.map(layer => <Layer key={layer.id} layer={layer}/>)}</>;
