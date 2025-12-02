from pydantic import BaseModel

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
    identity: uuid.UUID

class PostClosedGameResponse(BaseModel):
    success: bool