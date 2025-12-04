from fastapi import APIRouter, Depends
from db import DBClient
from dependencies import get_db, get_current_user_id
from dto import GetMessageResponse, PostMessageRequest, PostMessageResponse, Message
import uuid

router = APIRouter(
    dependencies=[Depends(get_current_user_id)]
)

@router.get("/messages")
async def get_messages(sender_id: str, current_user = Depends(get_current_user_id), db: DBClient = Depends(get_db)) -> GetMessageResponse:
    data = db.get_messages(current_user.user_id, uuid.UUID(sender_id))

    if data is None:
        return GetMessageResponse()
    
    # UGLY
    return GetMessageResponse(
        messages=[
            Message(
                message_id=d.message_id,
                time_stamp=d.time_stamp,
                message=d.message
            ) for d in data if d.message_id is not None and
                             d.time_stamp is not None and 
                             d.message is not None
        ] 
    )


@router.post("/messages")
async def send_message(request: PostMessageRequest, user_id: uuid.UUID = Depends(get_current_user_id), db: DBClient = Depends(get_db)) -> PostMessageResponse:
    success = db.post_message(user_id, request.recipient_id, request.message)

    return PostMessageResponse(
        success=success
    )