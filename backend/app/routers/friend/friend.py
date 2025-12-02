from fastapi import APIRouter, Depends
from db import DBClient
from app import get_db, get_current_user_id
from dto import GetFriendResponse, PostFriendRequest, PostFriendResponse

router = APIRouter(
    dependencies=[Depends(get_current_user_id)]
)

@router.get("/api/friends")
async def get_friends(user = Depends(get_current_user_id), db: DBClient = Depends(get_db)) -> GetFriendResponse:
    data = db.get_friends(user.user_id)

    if data is None:
        return GetFriendResponse(
            friend_ids=None
        )

    data = [(d.friend_id, d.accepted) for d in data if d.friend_id is not None and d.accepted is not None]

    return GetFriendResponse(
        friend_ids=data
    )


@router.post("/api/friends")
async def post_friends(request: PostFriendRequest, db: DBClient = Depends(get_db)) -> PostFriendResponse:
    success = db.post_friend(request.user_1_id, request.user_2_id)

    return PostFriendResponse(
        success=success
    )