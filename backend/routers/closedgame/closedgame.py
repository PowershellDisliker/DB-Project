from fastapi import APIRouter, Depends
from db import DBClient
from dependencies import get_db, get_current_user_id
from dto import GetClosedGameResponse, ClosedGame

router = APIRouter(
    dependencies=[Depends(get_current_user_id)]
)

@router.get("/closedgames")
async def get_closed_games(requestor_id = Depends(get_current_user_id), db: DBClient = Depends(get_db)) -> GetClosedGameResponse:
    data = db.get_closed_games(requestor_id)

    if data is None:
        return GetClosedGameResponse(
            games=None
        )
    
    # UGLY
    return GetClosedGameResponse(
        games=[ClosedGame(
            game_id=row.game_id,
            user_1_id=row.user_1_id,
            user_2_id=row.user_2_id,
            winner=row.winner,
            start_time=row.start_time,
            end_time=row.end_time,
            pieces=row.pieces,
        )
        
        for row in data if row.game_id is not None and
                           row.user_1_id is not None and
                           row.user_2_id is not None and
                           row.winner is not None and
                           row.end_time is not None and
                           row.start_time is not None and
                           row.pieces is not None]
    )