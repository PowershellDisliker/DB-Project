from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
import uuid

from db import DBClient
from config import Config
from game import GameMultiplexer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

configuration = Config()
database = DBClient(configuration.POSTGRES_URL, configuration.POSTGRES_DB_NAME)
game_multiplexer = GameMultiplexer()


# Strips authenitcation header for jwt and returns current users id
async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> HTTPException | uuid.UUID:

    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, configuration.SECRET_KEY, algorithms=[configuration.JWT_ALGO])

    except jwt.InvalidTokenError:
        raise credentials_exception
        
    identity: uuid.UUID = uuid.UUID(payload.get("su"))

    return identity


def get_db() -> DBClient:
    return database


def get_config() -> Config:
    return configuration


def get_multiplexer() -> GameMultiplexer:
    return game_multiplexer