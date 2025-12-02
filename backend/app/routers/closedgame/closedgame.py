from fastapi import APIRouter, Depends
from db import DBClient
from app import get_db, get_current_user
from dto import GetClosedGameRequest, GetClosedGameResponse, PostClosedGameRequest, PostClosedGameResponse

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

@router.get("/api/closedgames")
async def get_closed_games(request: GetClosedGameRequest, db: DBClient = Depends(get_db)) -> GetClosedGameResponse:
    data = db.get_closed_games()
    
    return GetClosedGameRequest(
        uuid=data.ID,
        user_1_id=data.User1ID,
        user_2_id=data.User2ID,
        winner=data.Winner,
        duration=(data.EndTime - data.StartTime)
    )


@router.post("/api/closedgames")
async def create_closed_game(request: PostClosedGameRequest, db: DBClient = Depends(get_db)) -> PostClosedGameResponse:
    data = db.post_closed_game(request.identity)
    
    return PostClosedGameResponse(
        success=data.success
    )