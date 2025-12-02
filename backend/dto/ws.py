from pydantic import BaseModel
from typing import Literal, Tuple
import uuid

# Websocket Data Models
class WebsocketGameRequest(BaseModel):
    jwt: str
    game_id: uuid.UUID

class WebsocketIncomingCommand(BaseModel):
    command_type: Literal["drop_piece", "register_user", "get_board_state"]
    game_id: uuid.UUID | None = None
    col: int | None = None
    user_id: uuid.UUID | None = None

class WebsocketOutgoingCommand(BaseModel):
    command_type: Literal["error", "board_state", "register_response", "drop_piece_response"]
    
    error: str | None = None
    
    user_1_id: uuid.UUID | None = None
    user_2_id: uuid.UUID | None = None
    board_state: list[uuid.UUID | None] | None = None
    active_player: uuid.UUID | None = None

    register_response: bool | None = None
    
    success: bool | None = None
    winner: uuid.UUID | None = None