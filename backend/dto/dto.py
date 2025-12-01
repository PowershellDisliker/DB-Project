from pydantic import BaseModel
import uuid

# in-flight dtos
# /api/login
class LoginRequest(BaseModel):
    user: str
    passw: str

class LoginResponse(BaseModel):
    success: bool

# /api/register
class RegisterRequest(BaseModel):
    user: str
    passw: str

class RegisterResponse(BaseModel):
    success: bool

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

# /api/opengames
# GET
class GetOpenGamesResponse(BaseModel):
    games: list[dict[str, uuid.UUID | bool]]

# POST
class PostOpenGamesRequest(BaseModel):
    user1id: str

class PostOpenGamesResponse(BaseModel):
    success: bool
    identity: uuid.UUID

# /api/closedgames
class GetClosedGameRequest(BaseModel):
    player_id: uuid.UUID

class GetClosedGameResponse(BaseModel):
    uuid: uuid.UUID
    user1uuid: uuid.UUID
    user2uuid: uuid.UUID
    winner: uuid.UUID
    duration: timedelta

class PostClosedGameRequest(BaseModel):
    identity: uuid.UUID

# db dtos
class UserDetails(BaseModel):
    identity: str
    username: str

class Token(BaseModel):
    owner: str
    token: str

class OpenGame(BaseModel):
    identity: str
    user1id: str
    user2id: str | None
    starttime: str

class ClosedGame(BaseModel):
    identity: str
    user1id: str
    user2id: str
    starttime: str
    endtime: str
    winner: str

class Friend(BaseModel):
    identity: str
    online: bool
    friendssince: str

class NewMessageRequest(BaseModel):
    recipient: str
    message: str

class MultiplexerMessage(BaseModel):
    game_id: uuid.UUID
    request_type: str
    request_value: str