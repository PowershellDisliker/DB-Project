from typing import Any
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from config import Config
from dependencies import get_config, get_multiplexer, get_db
from game import GameMultiplexer
from dto import WebsocketGameRequest, WebsocketIncomingCommand, WebsocketOutgoingCommand
import jwt
import json
import uuid
from collections import defaultdict

router = APIRouter()

rooms: dict[uuid.UUID, set[WebSocket]] = defaultdict(set)


async def broadcast(game_id: uuid.UUID, message: str):
    """Send a message to all clients in the game room, ignoring non-fatal errors."""
    for client in rooms.get(game_id, set()):
        try:
            print(f"Sending to client {client.scope.get('headers')}: {message[:50]}...")
            await client.send_text(message)

        except Exception as e:
            print(f"Error sending to client in room {game_id}: {e}")


@router.websocket("/ws")
async def game_websocket(ws: WebSocket, config: Config = Depends(get_config), game_multiplexer: GameMultiplexer = Depends(get_multiplexer)) -> None:
    await ws.accept()

    payload = None
    initial_request: WebsocketGameRequest | None = None

    try:
        # --- Step 1: receive initial join request ---
        msg = await ws.receive_text()
        initial_request = WebsocketGameRequest(**json.loads(msg))

        rooms[initial_request.game_id].add(ws)

        # --- Step 2: validate JWT ---
        try:
            payload = jwt.decode(
                initial_request.jwt,
                config.SECRET_KEY,
                algorithms=[config.JWT_ALGO],
            )

        except jwt.InvalidTokenError:
            await ws.send_text("INVALID")
            await ws.close()
            return

        # --- Step 3: send initial game snapshot ---
        snapshot = game_multiplexer.load_game(initial_request)
        await ws.send_text(snapshot.model_dump_json())

        # --- Step 4: main loop ---
        while True:
            msg = await ws.receive_text()
            command = WebsocketIncomingCommand(**json.loads(msg))

            response: WebsocketOutgoingCommand = game_multiplexer.process_message(command)
            response_json = response.model_dump_json()

            # broadcast the initial response (e.g., success/failure/log)
            await broadcast(initial_request.game_id, response_json)

            # Trigger a full board state broadcast after any action that changes the board structure.
            if response.command_type == "register_user" and response.success or \
            response.command_type == "drop_piece_response" and response.success:
                
                board_state_response = game_multiplexer._get_board_state_response(initial_request.game_id)
                await broadcast(initial_request.game_id, board_state_response.model_dump_json())
            
            # If there was a winner, post the game to the backend.
            if response.command_type == "drop_piece_response" and response.winner_id is not None:
                db = get_db()
                game_to_close = game_multiplexer.get_open_game_detail(initial_request.game_id)

                if game_to_close.user_1_id is None or game_to_close.user_2_id is None or game_to_close.start_time is None:
                    await broadcast(initial_request.game_id, "Cannot post game to ClosedGames")
                    continue

                if game_to_close.board_state:
                    db.post_closed_game(initial_request.game_id, game_to_close.user_1_id, game_to_close.user_2_id, game_to_close.start_time, response.winner_id, game_to_close.board_state)
                game_multiplexer.remove(initial_request.game_id)

    except WebSocketDisconnect:
        pass

    finally:
        # --- cleanup ---
        if initial_request is not None:
            game_id = initial_request.game_id
            
            game_to_broadcast = game_multiplexer.games.get(game_id) # <--- Get the reference safely

            if payload is not None:
                sub = payload.get("sub") # Use "sub" as per jwt payload, not "su"
                print(f"{sub} disconnected from {game_id}")
                
                # Disconnect logic runs and might delete the game from the dict
                game_multiplexer.disconnect(game_id, sub) 

                # Check if the game existed before disconnect, and if there are still clients in the room
                if game_to_broadcast and rooms.get(game_id):
                    
                    # For a quick fix, let's just make the call robust:
                    if game_id in game_multiplexer.games: # Re-check existence after disconnect
                        board_state_response = game_multiplexer._get_board_state_response(game_id)
                        await broadcast(game_id, board_state_response.model_dump_json())

            if ws in rooms.get(game_id, set()): # Use .get() defensively here too
                rooms[game_id].remove(ws)
                if not rooms[game_id]:
                    del rooms[game_id]