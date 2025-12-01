from fastapi import APIRouter

router = APIRouter()

@router.get("/api/opengames")
async def get_open_games(current_user: dict = Depends(get_current_user)) -> GetOpenGamesResponse:
    data = database.get_open_games()

    return [
        {
            "gameID": d.GameID,
            "user1ID": d.User1ID,
            "canJoin": d.User2ID == None
        } 
        for d in data
    ]

@router.post("/api/opengames")
async def create_new_game(current_user: dict = Depends(get_current_user)) -> PostOpenGamesResponse:
    data = database.post_open_game(current_user["user_id"])

    return {
        "success": True,
        "game_id": data.ID
    }