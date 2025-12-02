from fastapi import APIRouter, Depends
from db import DBClient
from app import get_db, get_current_user
from dto import GetPublicUserDataResponse
import uuid

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

@router.get("/api/user/public")
async def public_user_data(user_id: str, current_user: dict = Depends(get_current_user), db: DBClient = Depends(get_db)) -> GetPublicUserDataResponse:
    data = db.get_public_user(uuid.UUID(user_id))

    if data is None:
        return GetPublicUserDataResponse()

    return GetPublicUserDataResponse(
        username=data.user_id,
        online=data.online
    )


@router.get("/api/user/private")
async def get_user_data(request: GetPrivateUserDataRequest, current_user: dict = Depends(get_current_user), db: DBClient = Depends(get_db)) -> GetPrivateUserDataResponse:
    data = db.get_private_user(request.user_id)

    if data is None:
        return GetPrivateUserDataResponse()
    
    return GetPrivateUserDataResponse(
        user_id=d.ID,
        username=d.Username,
        pass_hash=d.PassHash,
        online=d.Online
    )