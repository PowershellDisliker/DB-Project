from pydantic import BaseModel
import uuid

# db -> backend vice versa models
# all marked optional and None as default
class DB_User(BaseModel):
    user_id: uuid.UUID | None = None
    username: str | None = None
    pass_hash: str | None = None
    online: bool | None = None

class DB_Token(BaseModel):
    owner: uuid.UUID | None = None
    token: str | None = None

class DB_OpenGame(BaseModel):
    game_id: uuid.UUID | None = None
    user_1_id: uuid.UUID | None = None
    user_2_id: uuid.UUID | None = None
    start_time: int | None = None

class DB_ClosedGame(BaseModel):
    game_id: uuid.UUID | None = None
    user_1_id: uuid.UUID | None = None
    user_2_id: uuid.UUID | None = None
    start_time: int | None = None
    end_time: int | None = None
    winner: uuid.UUID | None = None

class DB_Friend(BaseModel):
    friend_id: uuid.UUID | None = None
    accepted: bool | None = None

class DB_Message(BaseModel):
    message_id: uuid.UUID | None = None
    time_stamp: int | None = None
    sender_id: uuid.UUID | None = None
    recipient_id: uuid.UUID | None = None
    message: str | None = None

# Multiplexer DTOs
class MultiplexerMessage(BaseModel):
    game_id: uuid.UUID | None = None
    request_type: str | None = None
    request_value: str | None = None