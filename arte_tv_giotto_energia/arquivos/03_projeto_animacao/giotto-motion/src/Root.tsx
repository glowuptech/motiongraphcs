import {Composition} from 'remotion';
import {GiottoBlackFriday} from './compositions/GiottoBlackFriday';
import {GiottoBlackFridayMotion} from './compositions/GiottoBlackFridayMotion';
export const Root=()=> <>
 <Composition id="GiottoBlackFriday" component={GiottoBlackFriday} width={1920} height={1080} fps={30} durationInFrames={300}/>
 <Composition id="GiottoBlackFridayMotion" component={GiottoBlackFridayMotion} defaultProps={{muted:false}} width={1920} height={1080} fps={30} durationInFrames={300}/>
 </>;
