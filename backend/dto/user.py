from pydantic import BaseModel

# /api/user/public
class GetPublicUserDataResponse(BaseModel):
    username: str | None = None
    online: bool | None = None

# /api/user/private
class GetPrivateUserDataRequest(BaseModel):
    user_id: uuid.UUID

class GetPrivateUserDataResponse(BaseModel):
    user_id: uuid.UUID | None = None
    username: str | None = None
    online: bool | None = None
    pass_hash: str | None = None
