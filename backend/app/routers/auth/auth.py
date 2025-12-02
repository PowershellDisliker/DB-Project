from fastapi import APIRouter, Depends
from db import DBClient
from config import Config
from app import get_db, get_config
from dto import LoginRequest, RegisterRequest, AuthResponse, DB_User

import jwt

router = APIRouter()

# Login route, used by Login page
@router.post("/login")
async def login(request: AuthRequest, db: DBClient = Depends(get_db), config: Config = Depends(get_config)) -> AuthResponse:
    db_request: DB_User | None = db.validate_user(request.username, request.password)

    return AuthResponse(
        success=db_request is not None,
        token=jwt.encode({"sub": db_request.user_id}, config.SECRET_KEY, config.JWT_ALGO) if db_request is not None else None
    )
        

# Registers a new user
@router.post("/register")
async def register_new_user(request: AuthRequest, db: DBClient = Depends(get_db), config: Config = Depends(get_config)) -> AuthResponse:
    db_request: DB_User | None = db.post_user(request.username, request.password)

    return AuthResponse(
        success=db_request is not None,
        token=jwt.encode({"sub": db_request.user_id}, config.SECRET_KEY, config.JWT_ALGO) if db_request is not None else None
    )