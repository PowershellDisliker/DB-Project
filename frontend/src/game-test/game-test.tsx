import globalStyles from '../global.module.css';
import { GameCanvas } from '../components/game-canvas';

export default function GameTest() {

    const beginningBoardState: number[][] = [];
    
    return (

        <div className={`${globalStyles.globalCenter}`}>
            <GameCanvas current_player={"user1"} beginning_board_state={beginningBoardState}></GameCanvas>
        </div>
    )
}