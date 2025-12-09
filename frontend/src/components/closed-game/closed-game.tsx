import type { ClosedGame } from "../../dto/closedgame";
import StaticCanvas from "../static-canvas/static-canvas";
import { getPublicUser } from "../../api";
import { useEffect, useContext, useState } from 'react';
import { ConfigContext } from "../../context";
import type { GetPublicUserResponse } from "../../dto";
import globalStyles from '../../global.module.css';
import { useCookies } from "react-cookie";

interface ClosedGameProps {
    game: ClosedGame;
}

function ClosedGameComp({game}: ClosedGameProps) {
    const config = useContext(ConfigContext);
    const [cookies, setCookies, removeCookies] = useCookies(['jwt', 'id']);

    const [userProfile1, setUserProfile1] = useState<GetPublicUserResponse>({
        user_id: null,
        username: null,
        online: null,
    });

    const [userProfile2, setUserProfile2] = useState<GetPublicUserResponse>({
        user_id: null,
        username: null,
        online: null,
    })

    useEffect(() => {
        const inner = async () => {
            const user1result = await getPublicUser(config.BACKEND_URL, cookies.jwt, game.user_1_id);

            setUserProfile1({
                user_id: user1result.user_id,
                username: user1result.username,
                online: user1result.online,
            });

            const user2result = await getPublicUser(config.BACKEND_URL, cookies.jwt, game.user_2_id);

            setUserProfile2({
                user_id: user2result.user_id,
                username: user2result.username,
                online: user2result.online,
            })
        };

        inner();
    }, [])

    return (
        <div className={`${globalStyles.column} ${globalStyles.roundedContainer}`}>
            <p>Winner: {userProfile1.user_id == game.winner ? userProfile1.username : userProfile2.username}</p>
            <StaticCanvas board_state={game.pieces} user_1_id={game.user_1_id}/>
        </div>
    )
}

export default ClosedGameComp;