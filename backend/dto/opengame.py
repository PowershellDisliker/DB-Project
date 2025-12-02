from pydantic import BaseModel

# /api/opengames
# GET
class GetOpenGamesResponse(BaseModel):
    class InternalGame(BaseModel):
        game_id: uuid.UUID
        user_1_id: uuid.UUID
        can_join: bool

    games: list[InternalGame]

# POST
class PostOpenGamesResponse(BaseModel):
    success: bool
    game_id: uuid.UUID