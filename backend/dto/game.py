from pydantic import BaseModel
import uuid

class DropPieceResponse(BaseModel):
    success: bool
    winner_id: str | None = None
    coords: Tuple[int, int]
    next_active_player_id: str | None = None


class BoardState(BaseModel):
    user_1_id: uuid.UUID | None
    user_2_id: uuid.UUID | None
    positions: list[uuid.UUID | None]
    active_player: uuid.UUID | None