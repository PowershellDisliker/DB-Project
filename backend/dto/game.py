from pydantic import BaseModel
from typing import Tuple
import uuid

class DropPieceResponse(BaseModel):
    success: bool
    winner_id: uuid.UUID | None = None
    coords: Tuple[int, int] | None = None
    next_active_player_id: uuid.UUID | None = None


class BoardState(BaseModel):
    user_1_id: uuid.UUID | None
    user_2_id: uuid.UUID | None
    positions: list[uuid.UUID | None]
    active_player: uuid.UUID | None
    winner_id: uuid.UUID | None