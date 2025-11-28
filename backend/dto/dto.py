from pydantic import BaseModel

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

class Friend(BaseModel):
    identity: str
    online: bool
    friendssince: str

class Message(BaseModel):
    sender: str
    message: str