from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import auth_router, closedgame_router, friend_router, message_router, opengame_router, user_router, ws_router
from dto import *


# Python services
app = FastAPI()


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

# Routes
app.include_router(auth_router, prefix="/api")
app.include_router(closedgame_router, prefix="/api")
app.include_router(friend_router, prefix="/api")
app.include_router(message_router, prefix="/api")
app.include_router(opengame_router, prefix="/api")
app.include_router(user_router, prefix="/api")

# Websocket Route
app.include_router(ws_router, prefix="/api")
