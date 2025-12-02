from pydantic import BaseModel

# /api/friends
# GET
class GetFriendResponse(BaseModel):
    friend_ids: list[uuid.UUID] | None

# POST
class PostFriendRequest(BaseModel):
    user_1_id: uuid.UUID
    user_2_id: uuid.UUID

class PostFriendResponse(BaseModel):
    success: bool
