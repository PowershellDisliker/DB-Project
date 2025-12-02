from pydantic import BaseModel

# Websocket Data Models
class WebsocketGameRequest(BaseModel):
    game_id: uuid.UUID

class WebsocketIncomingCommand(BaseModel):
    command_type: str

class WebsocketOutgoingCommand(BaseModel):
    command_type: str