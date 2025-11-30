import {useEffect, useRef, useState, useContext} from 'react';
import { type SlowState, type RealTimeState } from './game-vm';
import { ConfigContext } from '../../config';

const HorizontalAspectRatio: number = 16;
const VerticalAspectRatio: number = 9;
const scale: number = 60;
const margin: number = 100;

const ROWS: number = 6;
const COLS: number = 7;

const PIECE_RADIUS: number = 60;

interface GameCanvasProps {
    starting_player: string;
}

function GameCanvas({starting_player}: GameCanvasProps) {

    // setup state
    const [viewModel, setViewModel] = useState<SlowState>();
    const RealTimeState = useRef<RealTimeState>(null);
    const ws = useRef<WebSocket>(null);
    const Config = useContext(ConfigContext);
    const canvasRef = useRef<HTMLCanvasElement>(null);
    
    // get user input and send it to backend
    const canvasClickHandler = (e: React.MouseEvent<HTMLCanvasElement>) => {
        // If it isn't our turn.
        if (!viewModel?.current_player) return;

        const x = e.clientX;

        // clicked out of bounds
        if (x < margin / 2 || x > margin / 2 + (e.currentTarget.width - margin)) return;

        const ColumnWidth = (e.currentTarget.width - margin) / COLS;
        const piece_col = Math.floor((x - (margin / 2)) / ColumnWidth);

        const message = {
            "type": "drop_piece",
            "player": RealTimeState.current!.current_player,
            "column": piece_col,
        }

        ws.current!.send(JSON.stringify(message));
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
            RealTimeState.current!.pieces.forEach(() => {
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
        ws.current = new WebSocket(Config!.BACKEND_WS_URL!);

        // message structure: 
        ws.current.addEventListener("message", (message: MessageEvent) => {
            let json_data = JSON.parse(message.data);

            switch (json_data["type"]) {
                case "add_piece":
                
                break;

                case "board_state":
                
                break;
            }
        })

        ws.current.addEventListener("close", (closeEvent: CloseEvent) => {
            console.log("Disconnected from ws backend");
        })

        return () => {
            ws.current?.close();
        }
    }, [])

    return <canvas width={HorizontalAspectRatio * scale} height={VerticalAspectRatio * scale} ref={canvasRef} onClick={canvasClickHandler}/>
}

export default GameCanvas;