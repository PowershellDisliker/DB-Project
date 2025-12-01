from pydantic import BaseModel
import uuid

# in-flight dtos
class LoginRequest(BaseModel):
    user: str
    passw: str

class RegisterRequest(BaseModel):
    user: str
    passw: str

class NewGameRequest(BaseModel):
    user1id: str

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

class ClosedGamePostRequest(BaseModel):
    identity: uuid.UUID

class ClosedGameGetRequest(BaseModel):
    player_id: uuid.UUID

class Friend(BaseModel):
    identity: str
    online: bool
    friendssince: str

class NewMessageRequest(BaseModel):
    recipient: str
    message: str