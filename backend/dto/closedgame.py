from pydantic import BaseModel
import uuid

# /api/closedgames
# GET
class GetClosedGameRequest(BaseModel):
    player_id: uuid.UUID

class GetClosedGameResponse(BaseModel):
    game_id: uuid.UUID
    user_1_id: uuid.UUID
    user_2_id: uuid.UUID
    winner: uuid.UUID
    duration: timedelta

# POST
class PostClosedGameRequest(BaseModel):
    game_id: uuid.UUID
    winner: uuid.UUID

class PostClosedGameResponse(BaseModel):
    success: bool
    game_id: uuid.UUID | None = None