from typing import Any
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from config import Config
from dependencies import get_config, get_multiplexer
from game import GameMultiplexer
from dto import WebsocketGameRequest, WebsocketIncomingCommand, WebsocketOutgoingCommand
import jwt
import json
import uuid
from collections import defaultdict

router = APIRouter()

rooms: dict[uuid.UUID, set[WebSocket]] = defaultdict(set)


async def broadcast(game_id: uuid.UUID, message: str):
    """Send a message to all clients in the game room"""
    dead = []

    for client in rooms[game_id]:
        try:
            print(message)
            await client.send_text(message)
        except Exception:
            dead.append(client)

    # Cleanup dead connections
    for client in dead:
        rooms[game_id].remove(client)


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
        su = payload.get("su")
        snapshot = game_multiplexer.create_or_load(initial_request, su)
        print(snapshot)
        await ws.send_text(snapshot.model_dump_json())

        # --- Step 4: main loop ---
        while True:
            msg = await ws.receive_text()
            command = WebsocketIncomingCommand(**json.loads(msg))

            response: WebsocketOutgoingCommand = game_multiplexer.process_message(command)
            response_json = response.model_dump_json()

            print(response_json)

            # broadcast the initial response (e.g., success/failure/log)
            await broadcast(initial_request.game_id, response_json)

            # --- FIX 2: Check if a piece was dropped or a user registered ---
            # Trigger a full board state broadcast after any action that changes the board structure.
            if response.command_type == "register_user" and response.success or \
            response.command_type == "drop_piece_response" and response.success:
                
                # After a successful registration or piece drop, broadcast the full board state
                board_state_response = game_multiplexer.__get_board_state_response(initial_request.game_id)
                await broadcast(initial_request.game_id, board_state_response.model_dump_json())

    except WebSocketDisconnect:
        pass

    finally:
        # --- cleanup ---
        if initial_request is not None:
            game_id = initial_request.game_id

            if payload is not None:
                su = payload.get("su")
                print(f"{su} disconnected from {game_id}")
                game_multiplexer.disconnect(game_id, su)

                if game_id in game_multiplexer.games and rooms[game_id]:
                    board_state_response = game_multiplexer.__get_board_state_response(game_id)

                    await broadcast(game_id, board_state_response.model_dump_json())

            if ws in rooms[game_id]:
                rooms[game_id].remove(ws)
                if not rooms[game_id]:
                    del rooms[game_id]