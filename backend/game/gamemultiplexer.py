from game import ConnectFourBoard
from typing import dict, Optional
from dto import WebsocketIncomingCommand, WebsocketOutgoingCommand, WebsocketGameRequest
import uuid

class GameMultiplexer:
    games: dict[uuid.UUID, ConnectFourBoard] = {}

    def create_or_load(self, request: WebsocketGameRequest, user_id: uuid.UUID) -> str:
        return self.games.setdefault(request.game_id, ConnectFourBoard())


    def process_message(self, request: WebsocketIncomingCommand) -> WebsocketOutgoingCommand:
        if request.game_id not in self.games:
            return WebsocketOutgoingCommand(
                type="error"
            )

        relevant_game = games[request.game_id]

        match request.request_type:
            case "drop_piece":
                relevant_game.drop_piece(request.value["owner"], request.value["column"])
                return True

            case "store_game":
                pass

        return True
