from fastapi import APIRouter

router = APIRouter()

@router.get("/api/friends")
async def get_friends(request: FriendsGetRequest, current_user: dict = Depends(get_current_user)):
    data = database.get_friends()
    
    return GetFriendsRespnse(

    )


@router.post("/api/friends")
async def post_friends(request: FriendsPostRequest, current_user: dict = Depends(get_current_user)):
    return {"success": database.post_friend()}
