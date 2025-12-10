from pydantic import BaseModel
import uuid
from datetime import datetime

# /api/opengames
# GET
class OpenGame(BaseModel):
    game_id: uuid.UUID
    user_1_id: uuid.UUID | None
    user_2_id: uuid.UUID | None
    start_time: datetime | None
    board_state: list[uuid.UUID | None] | None = None

class GetOpenGamesResponse(BaseModel):
    games: list[uuid.UUID] | None = None

class PostOpenGameRequest(BaseModel):
    user_id: uuid.UUID

class PostOpenGameResponse(BaseModel):
    success: bool
    game_id: uuid.UUID | None = None