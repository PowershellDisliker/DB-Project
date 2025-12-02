from pydantic import BaseModel

# /api/opengames
# GET
class OpenGame(BaseModel):
    game_id: uuid.UUID
    user_1_id: uuid.UUID
    can_join: bool

class GetOpenGamesResponse(BaseModel):
    games: list[OpenGame] | None = None

# POST
class PostOpenGamesResponse(BaseModel):
    success: bool
    game_id: uuid.UUID | None = None