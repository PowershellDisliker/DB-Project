from pydantic import BaseModel
from typing import Tuple
import uuid

# /api/friends
# GET
class GetFriendResponse(BaseModel):
    friend_ids: list[Tuple[uuid.UUID, bool]] | None

# POST
class PostFriendRequest(BaseModel):
    user_1_id: uuid.UUID
    user_2_id: uuid.UUID

class PostFriendResponse(BaseModel):
    success: bool
