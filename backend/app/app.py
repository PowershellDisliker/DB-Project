import json
import jwt
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

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

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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
            if identity is None:
                raise credentials_exception

            return {"id": identity}

        except JWTError:
            raise credentials_exception


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
    @app.get("/api/user/{user_id}")
    async def get_user_data(user_id: str, current_user: dict = Depends(get_current_user)):
        return database.get_user_details(user_id)


    @app.get("/api/opengames")
    async def get_open_games(current_user: dict = Depends(get_current_user)):
        return database.get_open_games()

    
    @app.post("/api/creategame")
    async def create_new_game(request: NewGameRequest, current_user: dict = Depends(get_current_user)):
        return {identity: database.create_open_game()}

    
    @app.get("/api/messages")
    async def get_messages(current_user: dict = Depends(get_current_user)):
        return database.get_messages(user_id)

    
    @app.post("/api/messages")
    async def send_message(request: NewMessageRequest, current_user: dict = Depends(get_current_user)):
        return {"success": database.send_message(current_user['id'], request.recipient, request.message)}
    

    # WS endpoint
    @app.websocket("/ws/game/{game_id}")
    async def game_websocket(conn: WebSocket, game_id: str, current_user: dict = Depends(get_current_user)):
        await conn.accept()

        try:
            # creates game if it doesn't already and sends board state
            conn.send_text(game_multiplexer.json_board_state(game_id))
            while True:
                data = json.loads(await conn.recieve_text())
                json_response = game_multiplexer.process_message(game_id, data)
                conn.send_text(json_response)
        
        except WebSocketDisconnect:
            print("Client disconnected")

    return app
