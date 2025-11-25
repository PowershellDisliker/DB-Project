import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from dto import LoginRequest, RegisterRequest, NewGameRequest
from db import DBClient
from config import Config
from game import GameMultiplexer

def run() -> FastAPI:
    configuration = Config()
    app = FastAPI()
    databse = DBClient(configuration.POSTGRES_URL, configuration.POSTGRES_DB_NAME)
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

    # HTTP / HTTPS endpoints
    # Login route, used by Login page
    @app.post("/api/login")
    async def login(request: LoginRequest):
        if request.user == "test" and request.passw == "test":
            return {"success": True}
        return {"success": False}

        # Real return value, stubbed above.
        return {"success": database.login_user(self, request.user, request.passw)}
        

    # Registers a new user
    @app.post("/api/register")
    async def register_new_user(request: RegisterRequest):
        return database.register_user(request.username, request.password)

    
    # DB routes (Need to be protected still)
    # Gets relevant user data
    @app.get("/api/user/{user_id}")
    async def get_user_data(user_id: str):
        return database.get_user_details(user_id)


    # Gets open, ongoing games
    @app.get("/api/opengames")
    async def get_open_games():
        return database.get_open_games()

    
    @app.post("/api/creategame")
    async def create_new_game(request: NewGameRequest):
        return {identity: database.create_open_game()}
    

    # WS endpoint
    @app.websocket("/ws/game/{game_id}")
    async def game_websocket(conn: WebSocket, game_id: str):
        await conn.accept()

        try:
            while True:
                data = await conn.recieve_text()
                game_multiplexer.process_message(game_id, data)
                conn.send_text(game_multiplexer.json_board_state())
        
        except WebSocketDisconnect:
            print("Client disconnected")

    return app
