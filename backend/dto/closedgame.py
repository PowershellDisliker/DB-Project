from pydantic import BaseModel
import uuid
from datetime import datetime

# /api/closedgames
# GET
class ClosedGame(BaseModel):
    game_id: uuid.UUID
    user_1_id: uuid.UUID
    user_2_id: uuid.UUID
    winner: uuid.UUID
    start_time: datetime
    end_time: datetime
    pieces: list[uuid.UUID | None]