from pydantic import BaseModel
import uuid

# /api/opengames
# GET
class OpenGame(BaseModel):
    game_id: uuid.UUID
    user_1_id: uuid.UUID | None
    user_2_id: uuid.UUID | None

class GetOpenGamesResponse(BaseModel):
    games: list[uuid.UUID] | None = None

class PostOpenGameResponse(BaseModel):
    success: bool
    game_id: uuid.UUID | None = None