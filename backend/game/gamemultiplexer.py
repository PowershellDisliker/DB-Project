from .game import ConnectFourBoard
from typing import dict, Optional
from .dto import *
import uuid

class GameMultiplexer:
    games: dict[uuid.UUID, ConnectFourBoard] = {}

    def json_board_state(game_id: uuid.UUID) -> str:
        if games[game_id]:
            return games[game_id].json_board_state()


    def process_message(request: MultiplexerMessage) -> bool:
        if request.game_id not in games:
            return False

        relevant_game = games[request.game_id]

        match request.request_type:
            case "drop_piece":
                relevant_game.drop_piece(request.value["owner"], request.value["column"])
                return True

            case "store_game":
                pass

        return True
