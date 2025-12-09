from fastapi import APIRouter, Depends
from game import GameMultiplexer
from dependencies import get_current_user_id, get_multiplexer
from dto import GetOpenGamesResponse, OpenGame, PostOpenGameResponse, PostOpenGameRequest
import uuid

router = APIRouter(
    dependencies=[Depends(get_current_user_id)]
)

@router.get("/opengames")
async def get_open_games(game_manager: GameMultiplexer = Depends(get_multiplexer)) -> GetOpenGamesResponse:
    return GetOpenGamesResponse(games=game_manager.get_open_game_ids())


@router.get("/opengames/detail")
async def get_open_game_detail(game_id: uuid.UUID, game_manager: GameMultiplexer = Depends(get_multiplexer)) -> OpenGame:
    return game_manager.get_open_game_detail(game_id)


@router.post("/opengames")
async def post_open_game(user_id: uuid.UUID = Depends(get_current_user_id), game_manager: GameMultiplexer = Depends(get_multiplexer)) -> PostOpenGameResponse:
    return game_manager.create_game(user_id)