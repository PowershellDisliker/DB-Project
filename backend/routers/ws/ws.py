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
    for client in rooms.get(game_id, set()): # Use .get() defensively
        try:
            print(f"Sending to client {client.scope.get('headers')}: {message[:50]}...")
            await client.send_text(message)
        except Exception as e:
            # We encountered an error, but DO NOT remove the client here.
            # A genuine disconnect will be handled by the main WebSocket handler's finally block.
            # If this is a recoverable error, we want the client to stay.
            # If it's a fatal error, the main loop for that client will soon break.
            print(f"Error sending to client in room {game_id}: {e}")


@router.websocket("/")
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
        sub: uuid.UUID = uuid.UUID(payload.get("sub"))
        snapshot = game_multiplexer.load_game(initial_request, sub)
        await ws.send_text(snapshot.model_dump_json())

        # --- Step 4: main loop ---
        while True:
            msg = await ws.receive_text()
            command = WebsocketIncomingCommand(**json.loads(msg))

            response: WebsocketOutgoingCommand = game_multiplexer.process_message(command)
            response_json = response.model_dump_json()

            # broadcast the initial response (e.g., success/failure/log)
            await broadcast(initial_request.game_id, response_json)

            # --- FIX 2: Check if a piece was dropped or a user registered ---
            # Trigger a full board state broadcast after any action that changes the board structure.
            if response.command_type == "register_user" and response.success or \
            response.command_type == "drop_piece_response" and response.success:
                
                # After a successful registration or piece drop, broadcast the full board state
                board_state_response = game_multiplexer._get_board_state_response(initial_request.game_id)
                await broadcast(initial_request.game_id, board_state_response.model_dump_json())
            
            if response.command_type == "drop_piece_response" and response.winner_id is not None and command.game_id:
                db = get_db()
                game_to_close = game_multiplexer.get_open_game_detail(command.game_id)
                db.post_closed_game(command.game_id, game_to_close.user_1_id, game_to_close.user_2_id, )

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