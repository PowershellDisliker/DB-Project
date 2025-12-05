from fastapi import APIRouter, Depends
from db import DBClient
from dependencies import get_db, get_current_user_id
from dto import GetFriendResponse, PostFriendRequest, PostFriendResponse, GetFriendRequestsResponse

router = APIRouter(
    dependencies=[Depends(get_current_user_id)]
)

@router.get("/friends")
async def get_friends(user = Depends(get_current_user_id), db: DBClient = Depends(get_db)) -> GetFriendResponse:
    data = db.get_friends(user)

    if data is None:
        return GetFriendResponse(
            friend_ids=None
        )

    data = [d.friend_id for d in data if d.friend_id is not None]

    return GetFriendResponse(
        friend_ids=data
    )


@router.get("/friends/outgoing")
async def get_outgoing_friend_request_users(user = Depends(get_current_user_id), db: DBClient = Depends(get_db)) -> GetFriendRequestsResponse:
    data = db.get_outgoing_friend_request_users(user)

    return GetFriendRequestsResponse(
        users=data
    )


@router.get("/friends/incoming")
async def get_incoming_friend_requests(user = Depends(get_current_user_id), db: DBClient = Depends(get_db)) -> GetFriendRequestsResponse:
    data = db.get_incoming_friend_request_users(user)

    return GetFriendRequestsResponse(
        users=data
    )


@router.post("/friends")
async def post_friends(request: PostFriendRequest, db: DBClient = Depends(get_db)) -> PostFriendResponse:
    success = db.post_friend(request.requestor_id, request.requestee_id)

    return PostFriendResponse(
        success=success
    )