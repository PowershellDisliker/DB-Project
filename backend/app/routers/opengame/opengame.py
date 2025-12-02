from fastapi import APIRouter, Depends
from db import DBClient
from app import get_db, get_current_user
from dto import GetOpenGamesResponse, PostOpenGamesResponse, OpenGame

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

@router.get("/opengames")
async def get_open_games(current_user: dict = Depends(get_current_user), db: DBClient = Depends(get_db)) -> GetOpenGamesResponse:
    data = db.get_open_games()

    if data is None:
        GetOpenGamesResponse()

    return GetOpenGamesResponse(
            [
            OpenGame(
                game_id=d.game_id,
                user_1_id=d.user_1_id,
                can_join=d.user_2_id == None
            )
            for d in data
        ]
    )


@router.post("/opengames")
async def create_new_game(current_user: dict = Depends(get_current_user), db: DBClient = Depends(get_db)) -> PostOpenGamesResponse:
    data = db.post_open_game(current_user.user_id)

    if data is None:
        return PostOpenGamesResponse(
            success=False
        )

    return PostOpenGamesResponse(
        success=True,
        game_id=data.ID
    )