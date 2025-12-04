from pydantic import BaseModel
import uuid
from datetime import timedelta

# /api/closedgames
# GET
class ClosedGame(BaseModel):
    game_id: uuid.UUID
    user_1_id: uuid.UUID
    user_2_id: uuid.UUID
    winner: uuid.UUID
    duration: timedelta

class GetClosedGameResponse(BaseModel):
    games: list[ClosedGame] | None

# POST
class PostClosedGameRequest(BaseModel):
    game_id: uuid.UUID
    winner: uuid.UUID

class PostClosedGameResponse(BaseModel):
    success: bool
    game_id: uuid.UUID | None = None