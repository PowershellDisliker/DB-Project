from fastapi import APIRouter, Depends
from db import DBClient
from app import get_db, get_current_user
from dto import GetClosedGameRequest, GetClosedGameResponse, PostClosedGameRequest, PostClosedGameResponse
import uuid

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

@router.get("/closedgames/")
async def get_closed_games(user = Depends(get_current_user), db: DBClient = Depends(get_db)) -> list[GetClosedGameResponse]:
    data = db.get_closed_games(uuid.UUID(user_id))

    if data is None:
        return []
    
    return [
        GetClosedGameResponse(
            game_id=row.game_id,
            user_1_id=row.user_1_id,
            user_2_id=row.user_2_id,
            winner=row.winner,
            duration=(row.end_time - row.start_time)
        )
        for row in data]


@router.post("/api/closedgames")
async def create_closed_game(request: PostClosedGameRequest, db: DBClient = Depends(get_db)) -> PostClosedGameResponse:
    data = db.post_closed_game(request.game_id, request.winner)

    if data is None:
        return PostClosedGameRequest(
            success=False
        )
    
    return PostClosedGameResponse(
        success=True,
        game_id=data.game_id
    )