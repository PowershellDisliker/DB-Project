from pydantic import BaseModel

class Message(BaseModel):
    message_id: uuid.UUID
    time_stamp: int
    message: str

# /api/message
# GET
class GetMessageResponse(BaseModel):
    messages: list[Message] | None = None

# POST
class PostMessageRequest(BaseModel):
    recipient_id: uuid.UUID
    message: str

class PostMessageResponse(BaseModel):
    success: bool