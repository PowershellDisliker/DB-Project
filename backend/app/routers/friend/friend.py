from fastapi import APIRouter, Depends
from db import DBClient
from app import get_db, get_current_user
from dto import GetFriendRequest, GetFriendResponse, PostFriendRequest, PostFriendResponse

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

@router.get("/api/friends")
async def get_friends(user = Depends(get_current_user), db: DBClient = Depends(get_db)) -> GetFriendResponse:
    data = db.get_friends(user.user_id)

    if data is None:
        return GetFriendResponse()

    data = [d.friend_id for d in data]

    return GetFriendResponse(
        friend_ids=data
    )


@router.post("/api/friends")
async def post_friends(request: FriendsPostRequest, db: DBClient = Depends(get_db)) -> PostFriendResponse:
    success = db.post_friend(request.user_1_id, request.user_2_id)

    return PostFriendRequest(
        success=success
    )