from fastapi import APIRouter
from dto import LoginRequest, LoginResponse, RegisterRequest, RegisterResponse


router = APIRouter()


# HTTP / HTTPS endpoints
# Login route, used by Login page
@router.post("/login")
async def login(request: LoginRequest) -> LoginResponse:
    # TODO Must return JWT here
    success = database.validate_user(self, request.user, request.passw)

    return {
        "success": bool(success),
        "token": jwt.encode({"user_id": success}, configuration.SECRET_KEY, configuration.JWT_ALGO) if success else None
    }
        

# Registers a new user
@router.post("/register")
async def register_new_user(request: RegisterRequest) -> RegisterResponse:
    success = database.register_user(request.username, request.password)

    return {
        "success": success
    }