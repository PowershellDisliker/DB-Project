from pydantic import BaseModel
import uuid

# /api/opengames
# GET
class OpenGame(BaseModel):
    game_id: uuid.UUID
    user_1_id: uuid.UUID | None
    user_2_id: uuid.UUID | None
    can_join: bool

class GetOpenGamesResponse(BaseModel):
    games: list[OpenGame] | None = None

class OpenGameProps(BaseModel):
    game: OpenGame

# POST
class PostOpenGamesResponse(BaseModel):
    success: bool
    game_id: uuid.UUID | None = None

