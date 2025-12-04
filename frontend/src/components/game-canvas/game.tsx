import { useEffect, useRef, useState, useContext } from 'react';
import { type SlowState, type RealTimeState } from './game-vm';
import { AuthContext, ConfigContext } from '../../context';
import { Piece } from './game-vm';
import type { WebsocketRequest, WebsocketResponse } from '../../dto';

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
    // Get contexts
    const config = useContext(ConfigContext);
    const auth = useContext(AuthContext);
    
    // State
    const [viewModel, setViewModel] = useState<SlowState>({
      active_player: null,
      game_running: null
    });

    const RealTimeState = useRef<RealTimeState>({
      active_player: null,
      player_1_id: null,
      player_2_id: null,
      pieces: [],
      winner_id: null
    });

    // sub-component references
    const ws = useRef<WebSocket>(null);
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const currentFrame = useRef<number>(null);
    
    // Animation Effect
    useEffect(() => {
    if (!canvasRef.current) return;

    const gc = canvasRef.current.getContext('2d');
    if (!gc) return;

    // const imageMask = new Image();
    // imageMask.src = '../../../public/board-mask.png';

    const drawFrame = () => {
      gc.clearRect(0, 0, canvasRef.current!.width, canvasRef.current!.height);

      // Draw and update all the pieces
      RealTimeState.current.pieces.forEach((piece) => {
        if (!piece) {
          return;
        }

        gc.beginPath();
        gc.arc(piece.col * PIECE_RADIUS * 2, piece.yPos, PIECE_RADIUS, 0, Math.PI * 2);
        gc.fillStyle = piece.color;
        gc.fill();

        // Update piece positions
        piece.dy += gravity * timeScale;
        piece.yPos += piece.dy * timeScale;

        if (piece.yPos >= piece.targetY) {
            piece.yPos = piece.targetY;
            piece.dy = 0;
        }

      });
    //   gc.drawImage(imageMask, 0, 0);

      currentFrame.current = requestAnimationFrame(drawFrame);
    };

    currentFrame.current = requestAnimationFrame(drawFrame);
        return () => {
      cancelAnimationFrame(currentFrame.current!);
    };
  }, []);

  // Websocket Effect
  useEffect(() => {
    ws.current = new WebSocket(config!.BACKEND_WS_URL!);

    // OnOpen
    ws.current.addEventListener('open', async (event: Event) => {
      ws.current!.send(JSON.stringify({
        command_type: 'get_board_state',
        game_id: game_id,
        user_id: auth.user_id,
      } as WebsocketRequest));

      ws.current!.send(JSON.stringify({
        command_type: 'register_user',
        user_id: auth.user_id,
      } as WebsocketRequest))
    });

    // in-loop
    ws.current.addEventListener('message', (message: MessageEvent) => {
      const jsonData: WebsocketResponse = JSON.parse(message.data);

      switch (jsonData.command_type) {
        case 'drop_piece_response':
          const current_player_id = RealTimeState.current!.active_player;

          if (!jsonData.row || !jsonData.col) {
            console.log("No row or column in drop_piece_ressponse");
            break;
          }
          
          // Realtime state update
          RealTimeState.current!.pieces.push(new Piece(jsonData.row, jsonData.col, current_player_id == RealTimeState.current!.player_1_id ? COLORS[0] : COLORS[1]));

          if (jsonData.winner_id) {
            setViewModel(() => ({
              game_running: false,
              active_player: false,
            }))
            break;
          }

          // Visual state update
          setViewModel(() => ({
            game_running: true,
            active_player: jsonData.next_active_player_id == auth.user_id,
          }));
          break;

        case 'board_state':
          // Real time state update
          RealTimeState.current.active_player = jsonData.active_player;
          RealTimeState.current.player_1_id = jsonData.user_1_id;
          RealTimeState.current.player_2_id = jsonData.user_2_id;
          RealTimeState.current.winner_id = jsonData.winner_id;

          if (jsonData.winner_id) {
            setViewModel(() => ({
              game_running: false,
              active_player: false, 
            }))
          }

          RealTimeState.current.pieces = jsonData.board_state!.map((value, index) => {
            if (!value) return null;
            let row = Math.floor(index / COLS)
            let col = index % COLS

            return new Piece(row, col, value == jsonData.user_1_id ? COLORS[0] : COLORS[1]);
          });
          break;
        
        case 'register_response':
          if (!jsonData.success) {
            console.log(`error registering user ${auth.user_id != jsonData.user_1_id ? jsonData.user_1_id : jsonData.user_2_id}`)
          }

          // State updates:
          // realtime
          RealTimeState.current!.player_1_id = jsonData.user_1_id;
          RealTimeState.current!.player_2_id = jsonData.user_2_id;
    }});

    // OnClose
    ws.current.addEventListener('close', () => {
      console.log('Disconnected from ws backend');
    });

    // Cleanup
    return () => {
      ws.current?.close();
    };
  }, []);

  const canvasClickHandler = (e: React.MouseEvent<HTMLCanvasElement>) => {
    if (!viewModel.active_player || !viewModel.game_running) return;

    const rect = canvasRef.current!.getBoundingClientRect();
    const x = e.clientX - rect.left;


    if (x < 0 || x > canvasRef.current!.width - margin) return;

    const columnWidth = (canvasRef.current!.width - margin) / COLS;
    const pieceCol = Math.floor((x - (margin / 2)) / columnWidth);

    const message = {
      command_type: 'drop_piece',

      game_id: game_id,
      col: pieceCol,
      user_id: auth.user_id,
    } as WebsocketRequest;

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