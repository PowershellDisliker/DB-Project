from operator import mul
from fastapi import APIRouter, Depends
import uuid
from game import GameMultiplexer
from db import DBClient
from dependencies import get_db, get_current_user_id, get_multiplexer
from dto import GetOpenGamesResponse, PostOpenGamesResponse, OpenGame, OpenGameProps

router = APIRouter(
    dependencies=[Depends(get_current_user_id)]
)

@router.get("/opengames")
async def get_open_games(user_id: uuid.UUID = Depends(get_current_user_id), db: DBClient = Depends(get_db)) -> GetOpenGamesResponse:
    data = db.get_open_games()

    if data is None:
        return GetOpenGamesResponse(
            games=None
        )

    return GetOpenGamesResponse(
            games=[
            OpenGame(
                game_id=d.game_id,
                user_1_id=d.user_1_id,
                user_2_id=d.user_2_id,
                can_join=d.user_2_id == None
            ) for d in data if d.game_id is not None and
                d.user_1_id is not None
        ]
    )


@router.post("/opengames")
async def create_new_game(user_id: uuid.UUID = Depends(get_current_user_id), db: DBClient = Depends(get_db)) -> PostOpenGamesResponse:
    data = db.post_open_game(user_id)

    if data is None:
        return PostOpenGamesResponse(
            success=False
        )

    return PostOpenGamesResponse(
        success=True,
        game_id=data.game_id
    )


@router.get("/opengamedetails")
async def get_open_game_details(game_id: uuid.UUID, multiplexer: GameMultiplexer = Depends(get_multiplexer)) -> OpenGameProps:
    game_board = multiplexer._get_board_state_response(game_id)

    return OpenGameProps(
        game=OpenGame(
        game_id=game_id,
        user_1_id=game_board.user_1_id,
        user_2_id=game_board.user_2_id,
        can_join=game_board.user_2_id == None
        )
    )