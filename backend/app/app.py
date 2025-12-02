import json
import jwt
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, CursorResult, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from app.routers import auth_router, closedgame_router, friend_router, message_router, opengame_router, user_router, ws_router
from dto import *
from db import DBClient
from config import Config
from game import GameMultiplexer

# Python services
app = FastAPI()
configuration = Config()
database = DBClient(configuration.POSTGRES_URL, configuration.POSTGRES_DB_NAME)
game_multiplexer = GameMultiplexer()

# REMOVE IN PRODUCTION!!!
origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# END REMOVE!!!
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")


# Strips authenitcation header for jwt and returns current users id
async def get_current_user(token: str = Depends(oauth2_scheme)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, configuration.SECRET_KEY, algorithms=["HS256"])
        identity: str = payload.get("id")

        if not database.validate_user():
            return credentials_exception


        return DB_User(
            user_id=identity
        )

    except JWTError:
        raise credentials_exception


def get_db() -> DBClient:
    return database


def get_config() -> Config:
    return configuration


# Routes
app.include_router(auth_router, prefix="/api/auth")
app.include_router(closedgame_router, prefix="/api/closedgame")
app.include_router(friend_router, prefix="/api/friend")
app.include_router(message_router, prefix="/api/message")
app.include_router(opengame_router, prefix="/api/opengame")
app.include_router(user_router, prefix="/api/user")

# Websocket Route
app.include_router(ws_router, prefix="/ws")
