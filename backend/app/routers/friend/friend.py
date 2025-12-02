from fastapi import APIRouter, Depends
from db import DBClient
from app import get_db, get_current_user
from dto import GetFriendRequest, GetFriendResponse, PostFriendRequest, PostFriendResponse

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

@router.get("/api/friends")
async def get_friends(request: GetFriendRequest, db: DBClient = Depends(get_db)):
    data = db.get_friends(request.user_id)

    data = [data]

    return GetFriendResponse(
        friend_ids=data
    )


@router.post("/api/friends")
async def post_friends(request: FriendsPostRequest, db: DBClient = Depends(get_db)):
    return 
