from pydantic import BaseModel

class LoginRequest(BaseModel):
    user_attempt: str
    pass_attempt: str