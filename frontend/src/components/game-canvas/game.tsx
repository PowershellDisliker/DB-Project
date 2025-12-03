import { useEffect, useRef, useState, useContext } from 'react';
import { type SlowState, type RealTimeState } from './game-vm';
import { ConfigContext } from '../../context';
import { Piece } from './game-vm';
import type { WebsocketResponse } from '../../dto';

// CONSTANTS MOVE TO CONFIG?
const HorizontalAspectRatio = 16;
const VerticalAspectRatio = 9;
const scale = 60;
const margin = 100;
const gravity = 5;
const timeScale = 1;

const ROWS = 6;
const COLS = 7;

const PIECE_RADIUS = 30;

const COLORS = ["red", "yellow"];

interface CanvasProps {
  game_id: string | null
}

function GameCanvas({game_id}: CanvasProps) {
    const config = useContext(ConfigContext);
    
    // State
    const [viewModel, setViewModel] = useState<SlowState>({
      game_id: game_id,
      active_player: null,
    });
    const RealTimeState = useRef<RealTimeState>(null);

    // sub-component references
    const ws = useRef<WebSocket>(null);
    const canvasRef = useRef<HTMLCanvasElement>(null);
    
    // Animation Effect
    useEffect(() => {
    if (!canvasRef.current) return;

    const gc = canvasRef.current.getContext('2d');
    if (!gc) return;

    // const imageMask = new Image();
    // imageMask.src = '../../../public/board-mask.png';

    // TODO remove test pieces
    let pieces: Piece[] = [];

    const drawFrame = () => {
      gc.clearRect(0, 0, canvasRef.current!.width, canvasRef.current!.height);

      // Draw and update all the pieces
      pieces.forEach((piece) => {
        gc.beginPath();
        gc.arc(piece.col * 80, piece.yPos, PIECE_RADIUS, 0, Math.PI * 2);
        gc.fillStyle = piece.color;
        gc.fill();

        // Update piece positions
        piece.yPos += piece.dy * timeScale;
        piece.dy -= gravity * timeScale;
        if (piece.yPos > piece.row * PIECE_RADIUS * 2 && piece.dy > 0) piece.dy *= -0.8; // debounced
      });
    //   gc.drawImage(imageMask, 0, 0);

            requestAnimationFrame(drawFrame);
    };

    let animationID = requestAnimationFrame(drawFrame);
        return () => {
      cancelAnimationFrame(animationID);
    };
  }, []);

  // Websocket Effect
  useEffect(() => {
    ws.current = new WebSocket(config!.BACKEND_WS_URL!);

    ws.current.addEventListener('open', (event: Event) => {

    })

    ws.current.addEventListener('message', (message: MessageEvent) => {
      const jsonData: WebsocketResponse = JSON.parse(message.data);

      switch (jsonData.command_type) {
        case 'drop_piece_response':
          // update pieces array
          const current_player_id = RealTimeState.current!.active_player;
          const player_1_id = RealTimeState.current!.player_1_id;

          if (!jsonData.row || !jsonData.col) {
            console.log("No row or column in drop_piece_ressponse");
            break;
          }

          RealTimeState.current!.pieces.push(new Piece(jsonData.row, jsonData.col, current_player_id == player_1_id ? COLORS[0] : COLORS[1] ));
          break;

        case 'board_state':
          // Real time state update
          RealTimeState.current!.active_player = jsonData.active_player;
          RealTimeState.current!.player_1_id = jsonData.user_1_id;
          RealTimeState.current!.player_2_id = jsonData.user_2_id;
          RealTimeState.current!.pieces = jsonData.board_state!.map((value, index) => {
            if (!value) return null;
            let row = Math.floor(index / COLS)
            let col = index % COLS

            return new Piece(row, col, value == jsonData.user_1_id ? COLORS[0] : COLORS[1]);
          })
          
          // update visual state here
          setViewModel((prev) => {
            game_id: prev.game_id
            active_player: 
          });
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