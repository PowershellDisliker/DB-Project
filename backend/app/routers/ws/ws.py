from fastapi import APIRouter

router = APIRouter()

# WS endpoint
@router.websocket("/game/ws")
async def game_websocket(conn: WebSocket) -> None:
    # Accept connection
    await conn.accept()

    # Handle Disconnect
    try:
        #TODO Handle authentication, no Depends()

        # Pre-game setup
        request: WebsocketGameRequest = json.loads(await conn.recieve_text())
        await conn.send_text(game_multiplexer.json_board_state(request.game_id))

        # Game-loop ws communication
        while True:
            command: WebsocketIncomingCommand = json.loads(await conn.recieve_text())
            json_response: WebsocketOutgoingCommand = game_multiplexer.process_message(request.game_id, command)
            await conn.send_text(json.dumps(json_response))
    
    except WebSocketDisconnect:
        # Cleanup
        print("Client disconnected")