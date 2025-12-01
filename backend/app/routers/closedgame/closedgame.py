from fastapi import APIRouter

router = APIRouter()

@router.get("/api/closedgames")
async def get_closed_games(request: GetClosedGameRequest, current_user: dict = Depends(get_current_user)) -> GetClosedGameResponse:
    data = database.get_closed_games()
    
    return {
        "uuid": data.ID,
        "user_1_id": data.User1ID,
        "user_2_id": data.User2ID,
        "winner": data.Winner,
        "duration": (data.EndTime - data.StartTime)
    }


@router.post("/api/closedgames")
async def create_closed_game(request: PostClosedGameRequest, current_user: dict = Depends(get_current_user)):
    data = database.post_closed_game(request.identity)
    
    return PostClosedGameResponse(
        success=data.success
    )