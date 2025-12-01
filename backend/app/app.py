import json
import jwt
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, CursorResult, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from dto import LoginRequest, RegisterRequest, NewGameRequest
from db import DBClient
from config import Config
from game import GameMultiplexer

def run() -> FastAPI:
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
            if identity is None:
                raise credentials_exception

            return {
                "user_id": identity
            }

        except JWTError:
            raise credentials_exception


    # HTTP / HTTPS endpoints
    # Login route, used by Login page
    @app.post("/api/login")
    async def login(request: LoginRequest) -> LoginResponse:
        # TODO Must return JWT here
        success = database.validate_user(self, request.user, request.passw)

        return {
            "success": bool(success),
            "token": jwt.encode({"user_id": success}, configuration.SECRET_KEY, configuration.JWT_ALGO) if success else None
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
        data = database.get_public_user(request.user)

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
    async def get_open_games(current_user: dict = Depends(get_current_user)) -> GetOpenGamesResponse:
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
    async def create_new_game(current_user: dict = Depends(get_current_user)) -> PostOpenGamesResponse:
        data = database.post_open_game(current_user["user_id"])

        return {
            "success": True,
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
    async def get_messages(request: GetMessagesRequest, current_user: dict = Depends(get_current_user)) -> GetMessageResponse:
        data = database.get_messages(rquest.recipient_id, request.sender_id)
        
        return [
            {
                "sender_id": d.ID,
                "timestamp": d.TimeStamp,
                "Message": d.Message
            }
            for d in data
        ]

    
    @app.post("/api/messages")
    async def send_message(request: PostMessageRequest, current_user: dict = Depends(get_current_user)) -> PostMessageResponse:
        data = database.post_message(current_user['identity'], request.recipient, request.message)

        return {
            "success": data.success
        }
    

    # WS endpoint
    @app.websocket("/game/ws")
    async def game_websocket(conn: WebSocket) -> None:
        # Accept connection
        await conn.accept()

        # Handle Disconnect
        try:
            #TODO Handle authentication, no Depends()

            # Pre-game setup
            request: WebsocketGameRequest = json.loads(await conn.recieve_text())
            await conn.send_text(game_multiplexer.json_board_state(request.game_id))

            # Game-loop ws communication
            while True:
                command: WebsocketIncomingCommand = json.loads(await conn.recieve_text())
                json_response: WebsocketOutgoingCommand = game_multiplexer.process_message(request.game_id, command)
                await conn.send_text(json.dumps(json_response))
        
        except WebSocketDisconnect:
            # Cleanup
            print("Client disconnected")

    return app
