from pydantic import BaseModel

# /api/login
class LoginRequest(BaseModel):
    user: str
    passw: str

class LoginResponse(BaseModel):
    success: bool
    token: str

# /api/register
class RegisterRequest(BaseModel):
    user: str
    passw: str

class RegisterResponse(BaseModel):
    success: bool