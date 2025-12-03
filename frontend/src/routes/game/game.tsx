import React, {useState} from "react";
import type { GameViewModel } from "./game-vm";
import {GameCanvas} from '../../components/game-canvas';
import globalStyles from "../global.module.css";

function Game() {

    const [viewModel, setViewModel] = useState<GameViewModel>()

    return (
        <div className={`${globalStyles.centerContainer}`}>
            <GameCanvas />
        </div>
    )
}

export default Game;