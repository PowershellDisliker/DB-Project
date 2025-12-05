from fastapi import WebSocket

from backend.dto.opengame import OpenGame
from .game import ConnectFourBoard
from typing import Tuple
from dto import WebsocketIncomingCommand, WebsocketOutgoingCommand, WebsocketGameRequest, BoardState, DropPieceResponse
from dependencies import get_db
import uuid


class GameMultiplexer:
    games: dict[uuid.UUID, ConnectFourBoard] = {}

    db = get_db()

    def __get_error_response(self, msg: str) -> WebsocketOutgoingCommand:
        return WebsocketOutgoingCommand(
            command_type="error",
            error=msg
        )


    def _get_board_state_response(self, game_id: uuid.UUID) -> WebsocketOutgoingCommand:
        board_state: BoardState = self.games[game_id].get_board_state()

        return WebsocketOutgoingCommand(
            command_type="board_state",
            board_state=board_state.positions,
            user_1_id=board_state.user_1_id,
            user_2_id=board_state.user_2_id,
            winner_id=board_state.winner_id,
            active_player=board_state.active_player
        )


    def __get_drop_piece_response(self, game_response: DropPieceResponse) -> WebsocketOutgoingCommand:
        if game_response.coords is None:
            return self.__get_error_response("No position included in drop_piece_response from server")
        
        return WebsocketOutgoingCommand(
            command_type="drop_piece_response",
            success=game_response.success,
            winner_id=game_response.winner_id,
            row=game_response.coords[0],
            col=game_response.coords[1],
            next_active_player_id=game_response.next_active_player_id,
        )

    
    def __get_log_response(self, message: str) -> WebsocketOutgoingCommand:
        return WebsocketOutgoingCommand(
            command_type="log",
            message=message
        )


    def create_or_load(self, request: WebsocketGameRequest, user_id: uuid.UUID) -> WebsocketOutgoingCommand:
        game = self.games.get(request.game_id)

        if game is None:
            new_game = ConnectFourBoard(user_id)
            self.games[request.game_id] = new_game
            game = new_game

        return self._get_board_state_response(request.game_id)


    # In GameMultiplexer
    def disconnect(self, game_id: uuid.UUID, user_id: uuid.UUID) -> None:
        game = self.games.get(game_id)
        if game:
            game.deregister_player(user_id) # assuming you implement deregister_player
            
            # If the game is now empty, delete it
            if game.user_1_id is None and game.user_2_id is None:
                 del self.games[game_id]


    def process_message(self, request: WebsocketIncomingCommand) -> WebsocketOutgoingCommand:
        match request.command_type:
            case "drop_piece":
                # Check if we received the game_id and if it exists
                if request.game_id is None or request.game_id not in self.games:
                    return self.__get_error_response("game_id does not exist")

                # Retrieve the game now that we know it exists
                requested_game: ConnectFourBoard = self.games[request.game_id]
                
                # Check if the requesting user is registered
                players = requested_game.get_players()

                if request.user_id not in players:
                    print(players)
                    print(request.user_id in players)
                    return self.__get_error_response(f"user_id: {request.user_id} not registered in {players}")

                # Check if the requesting user is the active player
                if request.user_id != requested_game.get_active_player():
                    return self.__get_error_response("user_id is not the active player")

                # Ensure presence of KV pairs, drop the piece, and send the response
                if request.user_id is None:
                    return self.__get_error_response("user_id missing from drop_piece request")

                if request.col is None:
                    return self.__get_error_response("col missing from drop_piece request")

                return self.__get_drop_piece_response(requested_game.drop_piece(request.user_id, request.col))
            
            case "register_user":
                # Check for required KV pairs for request type
                if request.user_id is None:
                    return self.__get_error_response("user_id missing from register_user request")

                if request.game_id is None:
                    return self.__get_error_response("game_id missing from register_user request")

                game = self.games[request.game_id]

                # Check if there's an open slot in the game
                if None not in game.get_players():
                    return self.__get_error_response("game_id is full")

                # Make sure the user hasn't already registered
                if request.user_id in game.get_players():
                    return self.__get_error_response("user_id is already registered in game_id")

                # Register the user and send the response
                success: bool = game.register_player(request.user_id)

                if not success:
                    return self.__get_error_response("Error registering user")
                return self._get_board_state_response(request.game_id)

            case "get_board_state":
                if request.game_id is None:
                    return self.__get_error_response("game_id is missing from get_board_state request")
                return self._get_board_state_response(request.game_id)
            
            case _:
                return self.__get_error_response("malformed websocket request")


    def get_open_game_ids(self) -> list[uuid.UUID]:
        return list(self.games.keys())

    def get_open_game_detail(self, game_id: uuid.UUID) -> OpenGame:
        game = self.games.get(game_id)

        if game is None:
            return OpenGame(
                game_id=game_id,
                user_1_id=None,
                user_2_id=None
            )
        
        return OpenGame(
            game_id=game_id,
            user_1_id=game.user_1_id,
            user_2_id=game.user_2_id
        )