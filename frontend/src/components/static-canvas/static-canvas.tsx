import { useEffect, useRef } from "react";

interface StaticCanvasProps {
    board_state: Array<string | null>;
    user_1_id: string;
}

function StaticCanvas({board_state, user_1_id}: StaticCanvasProps) {

    const canvasRef = useRef<HTMLCanvasElement>(null);

    // Render Given Board State
    useEffect(() => {
        if (!canvasRef.current) return;
        
        const ROW_COUNT = 6;
        const COL_COUNT = 7;

        const COLORS = ["red", "yellow"];

        const width = canvasRef.current.clientWidth;
        const height = canvasRef.current.clientHeight;

        const PIECE_RADIUS = Math.min((width / COL_COUNT) / 2, (height / ROW_COUNT) / 2);

        const gc = canvasRef.current.getContext('2d');

        for (let i = 0; i < ROW_COUNT * COL_COUNT; ++i) {
            if (!board_state[i]) continue;
            const value = board_state[i];
            
            let row = Math.floor(i / COL_COUNT);
            let col = i % COL_COUNT;

            gc!.beginPath()
            gc!.arc(PIECE_RADIUS + (PIECE_RADIUS * 2 * col), PIECE_RADIUS + (PIECE_RADIUS * 2 * row), PIECE_RADIUS, 0, 2 * Math.PI);
            gc!.fillStyle = value == user_1_id ? COLORS[0] : COLORS[1];
            gc!.fill()
        }

    }, [canvasRef.current])

    return (
        <canvas 
            ref={canvasRef}
        />
    )
}

export default StaticCanvas;