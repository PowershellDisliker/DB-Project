import React from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import {GameCanvas} from '../../components/game-canvas';
import globalStyles from "../../global.module.css";

function Game() {

    const [searchParams, setSearchParams] = useSearchParams();
    const navigate = useNavigate();

    const exitHandler = () => {
        navigate("/home");
    }

    return (
        <div>
            <button onClick={exitHandler}>Exit</button>

            <div className={`${globalStyles.centerContainer} ${globalStyles.roundedContainer}`}>
                <GameCanvas game_id={searchParams.get("game_id")}/>
            </div>
        </div>
    )
}

export default Game;