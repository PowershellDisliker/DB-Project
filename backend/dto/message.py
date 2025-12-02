from pydantic import BaseModel

# /api/message
# GET
class GetMessageRequest(BaseModel):
    sender_id: uuid.UUID
    recipient_id: uuid.UUID


class GetMessageResponse(BaseModel):
    class InternalMessage(BaseModel):
        message_id: uuid.UUID
        time_stamp: int
        message: str

    messages: list[InternalMessage]

# POST
class PostMessageRequest(BaseModel):
    sender_id: uuid.UUID
    recipient_id: uuid.UUID
    message: str

class PostMessageResponse(BaseModel):
    success: bool