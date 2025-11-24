import {useRef} from 'react';

const HorizontalAspectRatio: number = 16;
const VerticalAspectRatio: number = 9;
const scale: number = 10;

function GameCanvas() {

    const canvasRef = useRef(null);

    return (
        <canvas width={HorizontalAspectRatio * scale} height={VerticalAspectRatio * scale} ref={canvasRef}/>
    )
}

export default GameCanvas;