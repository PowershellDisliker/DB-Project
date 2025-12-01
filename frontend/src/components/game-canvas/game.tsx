import { useEffect, useRef, useState, useContext } from 'react';
import { type SlowState, type RealTimeState } from './game-vm';
import { ConfigContext } from '../../config';
import { Piece } from './game-vm';

// CONSTANTS MOVE TO CONFIG?
const HorizontalAspectRatio = 16;
const VerticalAspectRatio = 9;
const scale = 60;
const margin = 100;
const gravity = 5;
const timeScale = 1;

const ROWS = 6;
const COLS = 7;

const PIECE_RADIUS = 30; // changed to make pieces smaller and easier to see

// PROPS
interface GameCanvasProps {
  startingPlayer: string;
}

// COMPONENT
function GameCanvas({ startingPlayer }: GameCanvasProps) {
    const config = useContext(ConfigContext);
    
    // State
    const [viewModel, setViewModel] = useState<SlowState>();
    const RealTimeState = useRef<RealTimeState>(null);

    // sub-component references
    const ws = useRef<WebSocket>(null);
    const canvasRef = useRef<HTMLCanvasElement>(null);
    
    useEffect(() => {
    if (!canvasRef.current) return;

    const gc = canvasRef.current.getContext('2d');
    if (!gc) return;

    const imageMask = new Image();
    imageMask.src = '../../../public/board-mask.png';

    // TODO remove test pieces
    let pieces: Piece[] = [
        new Piece(0, 0, "black"),
        new Piece(0, 1, "red"),
        new Piece(0, 2, "black"),
    ];

    const drawFrame = () => {
      gc.clearRect(0, 0, canvasRef.current!.width, canvasRef.current!.height);

      // Draw and update all the pieces
      pieces.forEach((piece) => {
        gc.beginPath();
        gc.arc(piece.col * 80, piece.yPos, PIECE_RADIUS, 0, Math.PI * 2);
        gc.fillStyle = piece.color;
        gc.fill();

        piece.yPos += piece.dy * timeScale;
        
        piece.dy -= gravity * timeScale;

        if (piece.yPos > piece.row * 80 && piece.dy > 0) piece.dy *= -1;
      });
    //   gc.drawImage(imageMask, 0, 0);

            requestAnimationFrame(drawFrame);
    };

    let animationID = requestAnimationFrame(drawFrame);
        return () => {
      cancelAnimationFrame(animationID);
    };
  }, []);

  useEffect(() => {
    ws.current = new WebSocket(config!.BACKEND_WS_URL!);

    ws.current.addEventListener('message', (message) => {
      const jsonData = JSON.parse(message.data);

      switch (jsonData.type) {
        case 'add_piece':
          // update pieces array
          RealTimeState.current!.pieces.push(new Piece(jsonData.row, jsonData.col, "black"));
          break;

        case 'board_state':
          // update visual state here
          setViewModel(jsonData.newBoardState);
          break;
}
    });

    ws.current.addEventListener('close', (event) => {
      console.log('Disconnected from ws backend');
    });

    return () => {
      ws.current?.close();
    };
  }, []);

  const canvasClickHandler = (e: React.MouseEvent<HTMLCanvasElement>) => {
    if (!viewModel?.currentPlayer) return;

    const x = e.clientX;

    if (x < margin / 2 || x > margin / 2 + (canvasRef.current!.width - margin)) return;

    const columnWidth = (canvasRef.current!.width - margin) / COLS;
    const pieceCol = Math.floor((x - (margin / 2)) / columnWidth);

    const message = {
      type: 'drop_piece',
      player: RealTimeState.current!.currentPlayer,
      column: pieceCol,
    };

    ws.current?.send(JSON.stringify(message));
  };

  return (
    <canvas
      width={HorizontalAspectRatio * scale}
      height={VerticalAspectRatio * scale}
      ref={canvasRef}
      onClick={canvasClickHandler}
    />
  );
}

export default GameCanvas;