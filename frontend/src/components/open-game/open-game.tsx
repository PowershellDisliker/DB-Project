import React from 'react';
import { useNavigate } from 'react-router-dom';

import type { OpenGame } from '../../dto/opengame';
import globalStyles from '../../global.module.css';

function OpenGameComp({game_id, user_1_id}: OpenGame) {

    const navigator = useNavigate();

    const joinGame = () => {
        navigator(`/game?game_id=${game_id}`);
    }

    return (
        <div className={globalStyles.roundedContainer}>
            <button onClick={joinGame}>
                <p>Player: {user_1_id}</p>
            </button>
        </div>
    )
}

export default OpenGameComp;