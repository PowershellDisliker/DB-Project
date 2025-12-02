from fastapi import APIRouter, Depends
from db import DBClient
from app import get_db
from dto import LoginRequest, LoginResponse, RegisterRequest, RegisterResponse

router = APIRouter()

# Login route, used by Login page
@router.post("/login")
async def login(request: LoginRequest, db: DBClient = Depends(get_db)) -> LoginResponse:
    success = db.validate_user(self, request.user, request.passw)

    return LoginResponse(
        success=bool(success),
        token=jwt.encode({"user_id": success}, configuration.SECRET_KEY, configuration.JWT_ALGO) if success else None
    )
        

# Registers a new user
@router.post("/register")
async def register_new_user(request: RegisterRequest, db: DBClient = Depends(get_db)) -> RegisterResponse:
    success = db.register_user(request.username, request.password)

    return RegisterResponse(
        success=success
    )