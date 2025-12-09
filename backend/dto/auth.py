from pydantic import BaseModel
import uuid

# /api/login
class AuthRequest(BaseModel):
    username: str
    password: str

# Generic Response
class AuthResponse(BaseModel):
    success: bool
    token: str | None = None
    user_id: uuid.UUID | None = None

class TokenRequest(BaseModel):
    token: str