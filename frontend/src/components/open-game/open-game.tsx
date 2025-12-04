import { useEffect, useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';

import type { OpenGameProps } from '../../dto/opengame';
import globalStyles from '../../global.module.css';
import { getOpenGameDetails, getPublicUser } from '../../api';
import { AuthContext, ConfigContext } from '../../context';
import type { GetPublicUserResponse } from '../../dto';

function OpenGameComp({game}: OpenGameProps) {
    const navigator = useNavigate();

    const config = useContext(ConfigContext);
    const auth = useContext(AuthContext);

    const [user1Username, setUser1Username] = useState<string | null>(null);
    const [user2Username, setUser2Username] = useState<string | null>(null);
    
    const joinGame = () => {
        navigator(`/game?game_id=${game.game_id}`);
    }

    useEffect(() => {const inner = async () => {
        if (!auth.token) return;
        const fullDetails = await getOpenGameDetails(config.BACKEND_URL, auth.token, game.game_id);
        
        if (fullDetails.game.game_id) {
            if (fullDetails.game.user_1_id) {
                const user: GetPublicUserResponse = await getPublicUser(config.BACKEND_URL, auth.token, fullDetails.game.user_1_id);
                console.log(user.username);
                setUser1Username(user.username);
            }
    
            if (fullDetails.game.user_2_id) {
                const user2: GetPublicUserResponse = await getPublicUser(config.BACKEND_URL, auth.token, fullDetails.game.user_2_id);
                console.log(user2.username);
                setUser2Username(user2.username);
            }
        }
    }

    inner();
    }, [])

    return (
        <div className={globalStyles.roundedContainer}>
            <button onClick={joinGame}>
                <p>Player 1: {user1Username}</p>
                <p>Player 2: {user2Username}</p>
            </button>
        </div>
    )
}

export default OpenGameComp;