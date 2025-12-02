from game import ConnectFourBoard
from typing import Tuple
from dto import WebsocketIncomingCommand, WebsocketOutgoingCommand, WebsocketGameRequest, BoardState
import uuid


class GameMultiplexer:
    games: dict[uuid.UUID, ConnectFourBoard] = {}


    def __get_error_response(self, msg: str) -> WebsocketOutgoingCommand:
        return WebsocketOutgoingCommand(
            command_type="error",
            error=msg
        )


    def __get_board_state_response(self, game_id: uuid.UUID) -> WebsocketOutgoingCommand:
        board_state: BoardState = self.games[game_id].get_board_state()

        return WebsocketOutgoingCommand(
            command_type="board_state",
            board_state=board_state.positions,
            user_1_id=board_state.user_1_id,
            user_2_id=board_state.user_2_id,
            active_player=board_state.active_player
        )

    
    def __get_register_response(self, success: bool) -> WebsocketOutgoingCommand:
        return WebsocketOutgoingCommand(
            command_type="register_response",
            register_response=success
        )

    
    def __get_drop_piece_response(self, result: Tuple[bool, uuid.UUID | None]) -> WebsocketOutgoingCommand:
        return WebsocketOutgoingCommand(
            command_type="drop_piece_response",
            success=result[0],
            winner=result[1]
        )


    def create_or_load(self, request: WebsocketGameRequest, user_id: uuid.UUID) -> WebsocketOutgoingCommand:
        self.games.setdefault(request.game_id, ConnectFourBoard(user_id, None))

        return self.__get_board_state_response(request.game_id)


    def process_message(self, request: WebsocketIncomingCommand) -> WebsocketOutgoingCommand:
        match request.command_type:
            case "drop_piece":
                # Check if we received the game_id and if it exists
                if request.game_id is None or request.game_id not in self.games:
                    return self.__get_error_response("game_id does not exist")

                # Retrieve the game now that we know it exists
                requested_game: ConnectFourBoard = self.games[request.game_id]
                
                # Check if the requesting user is registered
                if request.user_id not in requested_game.get_players():
                    return self.__get_error_response("user_id not registered in game")

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
                return self.__get_register_response(success)

            case "get_board_state":
                if request.game_id is None:
                    return self.__get_error_response("game_id is missing from get_board_state request")
                return self.__get_board_state_response(request.game_id)
            
            case _:
                return self.__get_error_response("malformed websocket request")

