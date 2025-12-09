from fastapi import APIRouter, Depends
from db import DBClient
from config import Config
from dependencies import get_db, get_config, get_current_user_id
from dto import AuthRequest, AuthResponse, TokenRequest, DB_User
from datetime import datetime
import jwt
import uuid

router = APIRouter()

# Login route, used by Login page
@router.post("/login")
async def login(request: AuthRequest, db: DBClient = Depends(get_db), config: Config = Depends(get_config)) -> AuthResponse:
    db_request: DB_User | None = db.validate_user(request.username, request.password)

    if not db_request:
        return AuthResponse(
            success=False
        )

    return AuthResponse(
        success=True,
        token=jwt.encode({"sub": str(db_request.user_id), "iss": str(datetime.now())}, config.SECRET_KEY, config.JWT_ALGO) if db_request is not None else None,
        user_id=db_request.user_id
    )
        

# Registers a new user
@router.post("/register")
async def register_new_user(request: AuthRequest, db: DBClient = Depends(get_db), config: Config = Depends(get_config)) -> AuthResponse:
    db_request: DB_User | None = db.post_user(request.username, request.password)

    if not db_request:
        return AuthResponse(
            success=False
        )

    return AuthResponse(
        success=True,
        token=jwt.encode({"sub": str(db_request.user_id), "iss": str(datetime.now())}, config.SECRET_KEY, config.JWT_ALGO) if db_request is not None else None,
        user_id=db_request.user_id
    )


@router.post("/token")
async def post_token(request: TokenRequest, db: DBClient = Depends(get_db), user_id: uuid.UUID = Depends(get_current_user_id), config: Config = Depends(get_config)) -> bool:
    decoded_user_id = jwt.decode(request.token, config.SECRET_KEY, config.JWT_ALGO)
    
    if uuid.UUID(decoded_user_id.get("sub")) != user_id:
        return False

    return db.post_token(request.token)