import React from "react";
import { useSearchParams } from "react-router-dom";
import {GameCanvas} from '../../components/game-canvas';
import globalStyles from "../../global.module.css";

function Game() {

    const [searchParams, setSearchParams] = useSearchParams();

    return (
        <div className={`${globalStyles.centerContainer}`}>
            <GameCanvas game_id={searchParams.get("game_id")}/>
        </div>
    )
}

export default Game;