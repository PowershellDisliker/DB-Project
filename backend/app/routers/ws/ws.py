from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from config import Config
from db import DBClient
from app import get_config, get_multiplexer
from game import GameMultiplexer
from dto import WebsocketGameRequest, WebsocketIncomingCommand, WebsocketOutgoingCommand
import jwt
import json

router = APIRouter()

# WS endpoint
@router.websocket("/ws")
async def game_websocket(conn: WebSocket, config: Config = Depends(get_config), game_multiplexer: GameMultiplexer = Depends(get_multiplexer)) -> None:
    payload = None
    initial_request: WebsocketGameRequest | None = None
    
    # Accept connection
    await conn.accept()

    # Handle Disconnect
    try:
        # Pre-game setup
        msg = await conn.receive_text()
        initial_request = WebsocketGameRequest(**json.loads(msg))

        try:
            payload = jwt.decode(initial_request.jwt, config.SECRET_KEY, algorithms=[config.JWT_ALGO])
            
            # Load or create game and send board
            await conn.send_text(game_multiplexer.create_or_load(initial_request, payload.get('su')).model_dump_json())

        except jwt.InvalidTokenError:
            print("Invalid JWT")
            await conn.send_text("INVALID")
            await conn.close()
            return

        # Game-loop ws communication
        while True:
            # Receieve Command
            msg = await conn.receive_text()
            command: WebsocketIncomingCommand = WebsocketIncomingCommand(**json.loads(msg))

            # Parse and respond
            response: WebsocketOutgoingCommand = game_multiplexer.process_message(command)
            await conn.send_text(response.model_dump_json())
    
    except WebSocketDisconnect:
        # Cleanup
        if payload is not None and initial_request is not None:
            print(f"{payload.get('su')} disconnected from {initial_request.game_id}")

            game_multiplexer.disconnect(initial_request.game_id, payload.get('su'))