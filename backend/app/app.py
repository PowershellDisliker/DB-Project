from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .dto import LoginRequest
from db import DBClient
from config import Config

def run() -> FastAPI: 
    app = FastAPI()
    databse = DBClient()
    configuration = Config()

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

    # Login route, used by Login page
    @app.post("/api/login")
    async def login(request: LoginRequest):
        if request.user == "test" and request.passw == "test":
            return {"success": True}
        return {"success": False}

    return app
