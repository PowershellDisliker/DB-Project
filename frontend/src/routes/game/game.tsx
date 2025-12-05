import React from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import {GameCanvas} from '../../components/game-canvas';
import globalStyles from "../../global.module.css";
import gameStyles from "./game.module.css";

function Game() {

    const [searchParams, setSearchParams] = useSearchParams();
    const navigate = useNavigate();

    const exitHandler = () => {
        navigate("/home");
    }

    return (
        <div className={gameStyles.gameBorder}>
            <div className={`${globalStyles.center} ${globalStyles.height} ${globalStyles.roundedContainer}`}>
                <GameCanvas game_id={searchParams.get("game_id")}/>
            </div>
          <button onClick={exitHandler}>Exit</button>
        </div>
    )
}

export default Game;