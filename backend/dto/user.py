from pydantic import BaseModel

# /api/user/public
class PublicUserDataRequest(BaseModel):
    user_id: uuid.UUID

class PublicUserDataResponse(BaseModel):
    username: str
    online: bool

# /api/user/private
class PrivateUserDataRequest(BaseModel):
    user_id: uuid.UUID

class PrivateUserDataResponse(BaseModel):
    user_id: uuid.UUID
    username: str
    online: bool
    pass_hash: str
