from pydantic import BaseModel

# /api/friends
# GET
class GetFriendRequest(BaseModel):
    user_id: uuid.UUID

class GetFriendResponse(BaseModel):
    friend_ids: list[uuid.UUID]

# POST
class PostFriendRequest(BaseModel):
    ID1: uuid.UUID
    ID2: uuid.UUID

class PostFriendResponse(BaseModel):
    success: bool
