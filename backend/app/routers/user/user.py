from fastapi import APIRouter, Depends
from db import DBClient
from app import get_db, get_current_user_id
from dto import GetPublicUserDataResponse, GetPrivateUserDataResponse
import uuid

router = APIRouter(
    dependencies=[Depends(get_current_user_id)]
)

@router.get("/api/user/public")
async def public_user_data(user_query_id: uuid.UUID, user_id: uuid.UUID = Depends(get_current_user_id), db: DBClient = Depends(get_db)) -> GetPublicUserDataResponse:
    data = db.get_public_user(user_query_id)

    if data is None:
        return GetPublicUserDataResponse()

    return GetPublicUserDataResponse(
        username=data.username,
        online=data.online
    )


@router.get("/api/user/private")
async def get_user_data(user_query_id: uuid.UUID, user_id: uuid.UUID = Depends(get_current_user_id), db: DBClient = Depends(get_db)) -> GetPrivateUserDataResponse:
    data = db.get_private_user(user_query_id)

    if data is None:
        return GetPrivateUserDataResponse()
    
    return GetPrivateUserDataResponse(
        user_id=data.user_id,
        username=data.username,
        pass_hash=data.pass_hash,
        online=data.online
    )