from fastapi import APIRouter, Depends
from game import GameMultiplexer
from dependencies import get_current_user_id, get_multiplexer
from dto import GetOpenGamesResponse, OpenGame
import uuid

router = APIRouter(
    dependencies=[Depends(get_current_user_id)]
)

@router.get("/opengames")
async def get_open_games(user_id: uuid.UUID = Depends(get_current_user_id), game_manager: GameMultiplexer = Depends(get_multiplexer)) -> GetOpenGamesResponse:
    return GetOpenGamesResponse(games=game_manager.get_open_game_ids())


@router.get("/opengame/detail")
async def get_open_game_detail(game_id: uuid.UUID, game_manager: GameMultiplexer = Depends(get_multiplexer)) -> OpenGame:
    return game_manager.get_open_game_detail(game_id)