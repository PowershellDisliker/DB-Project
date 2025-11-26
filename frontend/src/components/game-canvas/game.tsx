import {useEffect, useRef, useState} from 'react';
import { type GameState } from './game-state';
import { type GameViewModel } from './game-vm';

const HorizontalAspectRatio: number = 16;
const VerticalAspectRatio: number = 9;
const scale: number = 10;

interface GameCanvasProps {
    beginning_board_state: number[][],
    current_player: string;
}

function GameCanvas({beginning_board_state, current_player}: GameCanvasProps) {

    const canvasRef = useRef(null);
    const ws = useRef(null);

    const [viewModel, setViewModel] = useState<GameViewModel>();

    const gameState = useRef<GameState>({
        board: beginning_board_state,
        current_player: current_player,
    });

    useEffect(() => {

    }, [])

    return (
        <canvas width={HorizontalAspectRatio * scale} height={VerticalAspectRatio * scale} ref={canvasRef}/>
    )
}

export default GameCanvas;