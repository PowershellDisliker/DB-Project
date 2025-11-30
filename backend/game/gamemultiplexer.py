from .game import ConnectFourBoard
from typing import dict

class GameMultiplexer:
    games: dict[str, ConnectFourBoard] = {}

    def json_board_state(game_id: str) -> str:
        if games[game_id]:
            return games[game_id].json_board_state()


    def process_message(game_id: str, data: dict) -> str:
        