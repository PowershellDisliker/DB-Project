from fastapi import APIRouter, Depends
from db import DBClient
from app import get_db, get_current_user
from dto import GetMessageResponse, PostMessageRequest, PostMessageResponse, Message
import uuid

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

@router.get("/messages")
async def get_messages(sender_id: str, current_user = Depends(get_current_user), db: DBClient = Depends(get_db)) -> GetMessageResponse:
    data = db.get_messages(current_user.user_id, uuid.UUID(sender_id))

    if data is None:
        return GetMessageResponse()
    
    return GetMessageResponse(
        [
            Message(
                message_id=d.ID,
                time_stamp=d.TimeStamp,
                message=d.Message
            )
        for d in data ] 
    )


@router.post("/messages")
async def send_message(request: PostMessageRequest, current_user: dict = Depends(get_current_user), db: DBClient = Depends(get_db)) -> PostMessageResponse:
    success = db.post_message(current_user.user_id, request.recipient, request.message)

    return PostMessageResponse(
        success=success
    )