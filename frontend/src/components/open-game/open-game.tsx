import { useEffect, useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import type { OpenGame } from '../../dto/opengame';
import globalStyles from '../../global.module.css';
import { getPublicUser } from '../../api';
import { AuthContext, ConfigContext } from '../../context';
import type { GetPublicUserResponse } from '../../dto';

function OpenGameComp({game_id, user_1_id, user_2_id}: OpenGame) {
    const navigator = useNavigate();

    const config = useContext(ConfigContext);
    const auth = useContext(AuthContext);

    const [user1Username, setUser1Username] = useState<string | null>(null);
    const [user2Username, setUser2Username] = useState<string | null>(null);
    
    const joinGame = () => {
        navigator(`/game?game_id=${game_id}`);
    }

    useEffect(() => {const inner = async () => {
        if (!auth.token) return;
        
        if (user_1_id) {
            const user: GetPublicUserResponse = await getPublicUser(config.BACKEND_URL, auth.token, user_1_id);
            console.log(user.username);
            setUser1Username(user.username);
        }

        if (user_2_id) {
            const user2: GetPublicUserResponse = await getPublicUser(config.BACKEND_URL, auth.token, user_2_id);
            console.log(user2.username);
            setUser2Username(user2.username);
        }
    }

    inner();
    }, [])

    return (
        <div className={globalStyles.roundedContainer}>
                <p>Player 1: {user1Username}</p>
                <p>Player 2: {user2Username}</p>
            <button onClick={joinGame}>
                {user_2_id ? "Spectate Game" : "Join Game"}
            </button>
        </div>
    )
}

export default OpenGameComp;