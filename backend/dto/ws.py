from pydantic import BaseModel
from typing import Literal

# Websocket Data Models
class WebsocketGameRequest(BaseModel):
    jwt: str
    game_id: uuid.UUID

class WebsocketIncomingCommand(BaseModel):
    command_type: Literal["drop_piece"]

class WebsocketOutgoingCommand(BaseModel):
    command_type: Literal["error"]