import {useEffect, useRef, useState} from 'react';
import { type SlowState, type RealTimeState } from './game-vm';

const HorizontalAspectRatio: number = 16;
const VerticalAspectRatio: number = 9;
const scale: number = 60;
const margin: number = 100;

const ROWS: number = 6;
const COLS: number = 7;

const PIECE_RADIUS: number = 60;

interface GameCanvasProps {
    beginning_board_state: number[][],
    current_player: string;
}

function GameCanvas({beginning_board_state, current_player}: GameCanvasProps) {

    // setup state
    const [viewModel, setViewModel] = useState<SlowState>();
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const ws = useRef<WebSocket>(null);
    const RealTimeState = useRef<RealTimeState>(null);
    
    // get user input and send it to backend
    const canvasClickHandler = (e: React.MouseEvent<HTMLCanvasElement>) => {
        // If it isn't our turn.
        if (!viewModel?.current_player) return;

        const x = e.clientX;
        const y = e.clientY;

        // clicked out of bounds
        if (x < margin / 2 || x > margin / 2 + (e.currentTarget.width - margin)) return;

        const ColumnWidth = (e.currentTarget.width - margin) / COLS;
        const piece_col = (x - (margin / 2)) / ColumnWidth;

        
    }

    // animation effect
    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;

        const GC = canvas.getContext('2d');
        if (!GC) return;

        const ImageMask = new Image();
        ImageMask.src = "../../../public/board-mask.png";

        const drawFrame = () => {
            // clear the canvas
            GC.clearRect(0, 0, canvas.width, canvas.height);

            // Draw all the pieces
            pieces.current.forEach((piece: Piece) => {
                GC.beginPath();
                GC.arc(piece.x_pos, piece.y_pos, 30, 0, Math.PI * 2);
                GC.fillStyle = "black";
                GC.fill();
            })


            GC.drawImage(ImageMask, 0, 0);
            requestAnimationFrame(drawFrame);
        }

        requestAnimationFrame(drawFrame);
    }, [])

    // websocket effect
    useEffect(() => {
        ws.current = new WebSocket("");

        return () => {
            ws.current?.close();
        }
    }, [])

    return <canvas width={HorizontalAspectRatio * scale} height={VerticalAspectRatio * scale} ref={canvasRef} onClick={canvasClickHandler}/>
}

export default GameCanvas;