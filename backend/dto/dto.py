from pydantic import BaseModel
from typing import TypedDict
import uuid

# in-flight dtos
# /api/login
class LoginRequest(BaseModel):
    user: str
    passw: str

class LoginResponse(TypedDict):
    success: bool

# /api/register
class RegisterRequest(BaseModel):
    user: str
    passw: str

class RegisterResponse(TypedDict):
    success: bool

# /api/user/public
class PublicUserDataRequest(BaseModel):
    user_id: uuid.UUID

class PublicUserDataResponse(TypedDict):
    username: str
    online: bool

# /api/user/private
class PrivateUserDataRequest(BaseModel):
    user_id: uuid.UUID

class PrivateUserDataResponse(TypedDict):
    user_id: uuid.UUID
    username: str
    online: bool
    pass_hash: str

# /api/opengames
# GET
class GetOpenGamesResponse(TypedDict):
    class InternalGame(TypedDict):
        game_id: uuid.UUID
        user_1_id: uuid.UUID
        can_join: bool

    games: list[InternalGame]

# POST
class PostOpenGamesResponse(TypedDict):
    success: bool
    game_id: uuid.UUID

# /api/closedgames
# GET
class GetClosedGameRequest(BaseModel):
    player_id: uuid.UUID

class GetClosedGameResponse(TypedDict):
    game_id: uuid.UUID
    user_1_id: uuid.UUID
    user_2_id: uuid.UUID
    winner: uuid.UUID
    duration: timedelta

# POST
class PostClosedGameRequest(BaseModel):
    identity: uuid.UUID

class PostClosedGameResponse(TypedDict):
    success: bool

# /api/friends
# GET
class GetFriendRequest(BaseModel):
    user_id: uuid.UUID

class GetFriendResponse(TypedDict):
    friends: list[{
        "identity": uuid.UUID,

    }]

# POST
class PostFriendRequest(BaseModel):
    ID1: uuid.UUID
    ID2: uuid.UUID

class PostFriendResponse(TypedDict):
    success: bool

# /api/message
# GET
class GetMessageRequest(BaseModel):
    sender_id: uuid.UUID
    recipient_id: uuid.UUID


class GetMessageResponse(TypedDict):
    class InternalMessage(TypedDict):
        message_id: uuid.UUID
        time_stamp: int
        message: str

    messages: list[InternalMessage]

# POST
class PostMessageRequest(BaseModel):
    sender_id: uuid.UUID
    recipient_id: uuid.UUID
    message: str

class PostMessageResponse(TypedDict):
    success: bool

# Websocket Data Models
class WebsocketGameRequest(BaseModel):
    game_id: uuid.UUID

class WebsocketIncomingCommand(BaseModel):
    command_type: str

class WebsocketOutgoingCommand(BaseModel):
    command_type: str


# db -> backend vice versa models
class DB_User(BaseModel):
    user_id: uuid.UUID
    username: str
    pass_hash: str
    online: bool

class DB_Token(BaseModel):
    owner: uuid.UUID
    token: str

class DB_OpenGame(BaseModel):
    game_id: uuid.UUID
    user_1_id: uuid.UUID
    user_2_id: uuid.UUID | None
    start_time: int

class DB_ClosedGame(BaseModel):
    game_id: uuid.UUID
    user_1_id: uuid.UUID
    user_2_id: uuid.UUID
    start_time: int
    end_time: int
    winner: uuid.UUID

class DB_Friend(BaseModel):
    friend_id: uuid.UUID
    accepted: bool

class DB_Message(BaseModel):
    message_id: uuid.UUID
    time_stamp: int
    sender_id: uuid.UUID
    recipient_id: uuid.UUID
    message: str

# Multiplexer DTOs
class MultiplexerMessage(BaseModel):
    game_id: uuid.UUID
    request_type: str
    request_value: str