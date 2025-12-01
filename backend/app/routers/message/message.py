from fastapi import APIRouter

router = APIRouter()

@router.get("/api/messages")
async def get_messages(request: GetMessagesRequest, current_user: dict = Depends(get_current_user)) -> GetMessageResponse:
    data = database.get_messages(rquest.recipient_id, request.sender_id)
    
    return [
        {
            "sender_id": d.ID,
            "timestamp": d.TimeStamp,
            "Message": d.Message
        }
        for d in data
    ]


@router.post("/api/messages")
async def send_message(request: PostMessageRequest, current_user: dict = Depends(get_current_user)) -> PostMessageResponse:
    data = database.post_message(current_user['identity'], request.recipient, request.message)

    return {
        "success": data.success
    }