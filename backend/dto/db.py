from pydantic import BaseModel
from datetime import datetime
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

class DB_ClosedGame(BaseModel):
    game_id: uuid.UUID | None = None
    user_1_id: uuid.UUID | None = None
    user_2_id: uuid.UUID | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    winner: uuid.UUID | None = None
    pieces: list[uuid.UUID | None]

class DB_Message(BaseModel):
    message_id: uuid.UUID | None = None
    time_stamp: datetime | None = None
    sender_id: uuid.UUID | None = None
    recipient_id: uuid.UUID | None = None
    message: str | None = None