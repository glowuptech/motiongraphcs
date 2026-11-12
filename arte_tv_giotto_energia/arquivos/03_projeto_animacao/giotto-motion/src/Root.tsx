import {Composition} from 'remotion';
import {GiottoBlackFriday} from './compositions/GiottoBlackFriday';
export const Root = () => <Composition id="GiottoBlackFriday" component={GiottoBlackFriday} width={1920} height={1080} fps={30} durationInFrames={300}/>;
