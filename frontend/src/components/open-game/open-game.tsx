import { useEffect, useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';

import type { OpenGame } from '../../dto/opengame';
import globalStyles from '../../global.module.css';
import { getPublicUser } from '../../api';
import { AuthContext, ConfigContext } from '../../context';
import type { GetPublicUserResponse } from '../../dto';

function OpenGameComp({game_id, user_1_id}: OpenGame) {

    const [username, setUsername] = useState<string | null>(null);
    const navigator = useNavigate();
    const config = useContext(ConfigContext);
    const auth = useContext(AuthContext);

    const joinGame = () => {
        navigator(`/game?game_id=${game_id}`);
    }

    useEffect(() => {const inner = async () => {
        if (!auth.token) return;
        const user: GetPublicUserResponse = await getPublicUser(config.BACKEND_URL, auth.token, user_1_id);
        setUsername(user.username);
    }

    inner();
    }, [])

    return (
        <div className={globalStyles.roundedContainer}>
            <button onClick={joinGame}>
                <p>Player: {username}</p>
            </button>
        </div>
    )
}

export default OpenGameComp;