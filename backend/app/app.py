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
    # Python services
    app = FastAPI()
    configuration = Config()
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
            if identity is None:
                raise credentials_exception

            return {"id": identity}

        except JWTError:
            raise credentials_exception


    # HTTP / HTTPS endpoints
    # Login route, used by Login page
    @app.post("/api/login")
    async def login(request: LoginRequest) -> LoginResponse:
        if request.user == "test" and request.passw == "test":
            return LoginResponse(success=True)
        return LoginResponse(success=False)

        # Real return value, stubbed above.
        success = database.login_user(self, request.user, request.passw)

        return {
            "success": success
        }
        

    # Registers a new user
    @app.post("/api/register")
    async def register_new_user(request: RegisterRequest) -> RegisterResponse:
        success = database.register_user(request.username, request.password)

        return {
            "success": success
        }

    
    # DB routes
    @app.get("/api/user/public")
    async def public_user_data(request: PublicUserDataRequest, current_user: dict = Depends(get_current_user)) -> PublicUserDataResponse:
        data = database.get_public_user(user_id)

        return {
            "username": data.Username,
            "online": data.Online
        }


    @app.get("/api/user/private")
    async def get_user_data(request: PrivateUserDataRequest, current_user: dict = Depends(get_current_user)) -> PrivateUserDataResponse:
        data = database.get_private_user(request.user_id)

        return {
            "user_id": d.ID,
            "username": d.Username,
            "pass_hash": d.PassHash,
            "online": d.Online
        }


    @app.get("/api/opengames")
    async def get_open_games(current_user: dict = Depends(get_current_user)) -> list[GetOpenGamesResponse]:
        data = database.get_open_games()

        return [
            {
                "gameID": d.GameID,
                "user1ID": d.User1ID,
                "canJoin": d.User2ID == None
            } 
            for d in data
        ]

    
    @app.post("/api/opengames")
    async def create_new_game(request: PostOpenGamesRequest, current_user: dict = Depends(get_current_user)) -> PostOpenGamesResponse:
        data = database.post_open_game()

        success = True

        if data is not None:
            success = False

        return {
            "success": success,
            "game_id": data.ID
        }


    @app.get("/api/closedgames")
    async def get_closed_games(request: GetClosedGameRequest, current_user: dict = Depends(get_current_user)) -> GetClosedGameResponse:
        data = database.get_closed_games()
        
        return {
            "uuid": data.ID,
            "user_1_id": data.User1ID,
            "user_2_id": data.User2ID,
            "winner": data.Winner,
            "duration": (data.EndTime - data.StartTime)
        }


    @app.post("/api/closedgames")
    async def create_closed_game(request: PostClosedGameRequest, current_user: dict = Depends(get_current_user)):
        data = database.post_closed_game(request.identity)
        
        return PostClosedGameResponse(
            success=data.success
        )

    
    @app.get("/api/friends")
    async def get_friends(request: FriendsGetRequest, current_user: dict = Depends(get_current_user)):
        data = database.get_friends()
        
        return GetFriendsRespnse(

        )

    
    @app.post("/api/friends")
    async def post_friends(request: FriendsPostRequest, current_user: dict = Depends(get_current_user)):
        return {"success": database.post_friend()}

    
    @app.get("/api/messages")
    async def get_messages(current_user: dict = Depends(get_current_user)):
        return database.get_messages(user_id)

    
    @app.post("/api/messages")
    async def send_message(request: NewMessageRequest, current_user: dict = Depends(get_current_user)):
        return {"success": database.send_message(current_user['id'], request.recipient, request.message)}
    

    # WS endpoint
    @app.websocket("/ws/game")
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
