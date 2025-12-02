from pydantic import BaseModel
import uuid

class BoardState(BaseModel):
    user_1_id: uuid.UUID | None
    user_2_id: uuid.UUID | None
    positions: list[uuid.UUID | None]
    active_player: uuid.UUID | None