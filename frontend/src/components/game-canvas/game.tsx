import { useEffect, useRef, useState, useContext } from 'react';
import { type SlowState, type RealTimeState } from './game-vm';
import { AuthContext, ConfigContext } from '../../context';
import { Piece } from './game-vm';
import type { WebsocketGameRequest, WebsocketRequest, WebsocketResponse } from '../../dto';
import gameStyles from './canvas.module.css';

// CONSTANTS MOVE TO CONFIG?
const marginPercentage = 0.05;
const gravity = 5;
const timeScale = 1;

const ROWS = 6;
const COLS = 7;

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


  // Websocket Effect
  useEffect(() => {
    if (!game_id || !auth.token) return;
    ws.current = new WebSocket(config!.BACKEND_WS_URL!);

    // OnOpen
    ws.current!.addEventListener('open', async () => {
      ws.current!.send(JSON.stringify({
        jwt: auth.token,
        game_id: game_id,
        user_id: auth.user_id,
      } as WebsocketGameRequest));
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
          RealTimeState.current!.pieces.push(new Piece(jsonData.row, jsonData.col, current_player_id == RealTimeState.current!.player_1_id ? COLORS[0] : COLORS[1], false));
          RealTimeState.current!.active_player = jsonData.next_active_player_id;

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
          if (jsonData.user_1_id && !jsonData.user_2_id && jsonData.user_1_id != auth.user_id) {
            ws.current!.send(JSON.stringify({
              command_type: "register_user",
              user_id: auth.user_id,
              game_id: game_id
            } as WebsocketRequest));
          }

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
          } else {
            setViewModel(() => ({
                game_running: true,
                active_player: jsonData.active_player == auth.user_id,
              }))
          }

          RealTimeState.current.pieces = jsonData.board_state!.map((value, index) => {
            if (!value) return null;
            let row = Math.floor(index / COLS)
            let col = index % COLS

            return new Piece(row, col, value == jsonData.user_1_id ? COLORS[0] : COLORS[1], true);
          });
          break;

        case 'log':
          console.log(jsonData.message);
          break;
    }});

    // OnClose
    // ws.current.addEventListener('close', () => {
    // });

    // Cleanup
    return () => {
      if (ws.current && ws.current.readyState !== WebSocket.CLOSED) {
        ws.current.close();
      }
    };
  }, []);

  // Animation Effect
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const gc = canvas.getContext('2d');
    if (!gc) return;
    
    // 1. Canvas Size Synchronization Function
    const synchronizeCanvasSize = () => {
        // Read the actual size the CSS gave the element
        canvas.width = canvas.offsetWidth;
        canvas.height = canvas.offsetHeight;
    };
    
    // Set initial size and start listening for window resize events
    synchronizeCanvasSize();
    window.addEventListener('resize', synchronizeCanvasSize);

    const drawFrame = () => {
      // Clear canvas using the synchronized dimensions
      gc.clearRect(0, 0, canvas.width, canvas.height); 

      // Draw and update all the pieces
      RealTimeState.current.pieces.forEach((piece) => {
        if (!piece) return;

        // Use the synchronized dimensions
        const width = canvas.width;
        const height = canvas.height;

        const widthMargin = width * marginPercentage;
        // heightMargin is calculated but only used here for determining piece size constraint
        const heightMargin = height * marginPercentage; 

        // Calculation of drawing parameters remains identical
        const pieceRadius = Math.min(((width - widthMargin) / COLS) / 2, ((height - heightMargin) / ROWS) / 2); 
        const pieceDiameter = pieceRadius * 2;
        
        const boardWidth = pieceDiameter * COLS;
        const boardHeight = pieceDiameter * ROWS;

        const marginX = (width - boardWidth) / 2;
        const marginY = (height - boardHeight) / 2;
        
        // Piece Center X calculation
        const centerX = marginX + (piece.col * pieceDiameter) + pieceRadius; 
        
        // Calculate the correct scaled target Y position (relative to board top)
        const targetYPos = (piece.row * pieceDiameter) + pieceRadius; 

        gc.beginPath();
        gc.arc(centerX, marginY + piece.yPos, pieceRadius, 0, Math.PI * 2);
        gc.fillStyle = piece.color;
        gc.fill();

        // Update piece positions (Physics)
        piece.dy += gravity * timeScale;
        piece.yPos += piece.dy * timeScale;

        // 2. Corrected stopping condition
        if (piece.yPos >= targetYPos) {
            piece.yPos = targetYPos; // Stops precisely at the target Y-coordinate
            piece.dy = 0;
        }
      });

      currentFrame.current = requestAnimationFrame(drawFrame);
    };

    // Start the animation loop
    currentFrame.current = requestAnimationFrame(drawFrame);
  
    // Cleanup function runs on component unmount
    return () => {
      cancelAnimationFrame(currentFrame.current!);
      window.removeEventListener('resize', synchronizeCanvasSize);
    };
  }, []);
  

  const canvasClickHandler = (e: React.MouseEvent<HTMLCanvasElement>) => {
    if (!viewModel.active_player || !viewModel.game_running) return;

    const width = canvasRef.current!.width;
    const height = canvasRef.current!.height;
    const widthMargin = width * marginPercentage;
    const heightMargin = height * marginPercentage;

    // 1. Calculate the actual piece size based on the most restrictive dimension
    const pieceRadius = Math.min(((width - widthMargin) / COLS) / 2, ((height - heightMargin) / ROWS) / 2); 
    const pieceDiameter = pieceRadius * 2;
    
    // 2. Define the actual dimensions of the drawn board
    const boardWidth = pieceDiameter * COLS;
    
    // 3. Define the margin used to center the drawn board
    const marginX = (width - boardWidth) / 2;
    // ----------------------------------------------

    const rect = canvasRef.current!.getBoundingClientRect();
    const x = e.clientX - rect.left;

    // Check if the click is within the actual DRAWN board area
    if (x < marginX || x > marginX + boardWidth) return;

    // The width of a column is the piece's diameter
    const columnWidth = pieceDiameter; 
    
    // Calculate the column index relative to the DRAWN board's left edge (marginX)
    // pieceCol = floor( (Absolute Click X - Drawn Board Start X) / Column Width )
    const pieceCol = Math.floor((x - marginX) / columnWidth);

    
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
      ref={canvasRef}
      className={gameStyles.canvas}
      onClick={canvasClickHandler}
    />
  );
}

export default GameCanvas;