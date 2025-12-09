from pydantic import BaseModel
from dto import DB_User
import uuid

# /api/friends
# GET
class GetFriendResponse(BaseModel):
    users: list[DB_User] | None = None

class GetFriendRequestsResponse(BaseModel):
    users: list[DB_User] | None = None

# POST
class PostFriendRequest(BaseModel):
    requestor_id: uuid.UUID
    requestee_id: uuid.UUID

class PostFriendResponse(BaseModel):
    success: bool
