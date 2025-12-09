from fastapi import APIRouter, Depends
from db import DBClient
from dependencies import get_db, get_current_user_id
from dto import GetPublicUserDataResponse, GetPrivateUserDataResponse
import uuid

router = APIRouter(
    dependencies=[Depends(get_current_user_id)]
)

@router.get("/user/public/id")
async def public_user_data(query_user_id: str, user_id: uuid.UUID = Depends(get_current_user_id), db: DBClient = Depends(get_db)) -> GetPublicUserDataResponse:
    data = db.get_public_user(uuid.UUID(query_user_id))

    if data is None:
        return GetPublicUserDataResponse()

    return GetPublicUserDataResponse(
        username=data.username,
        online=data.online
    )


@router.get("/user/public/username")
async def get_public_user_data_from_username(query_username: str, db: DBClient = Depends(get_db)) -> GetPublicUserDataResponse:
    data = db.get_public_user_from_username(query_username)

    if data is None:
        return GetPublicUserDataResponse()

    return GetPublicUserDataResponse(
        user_id=data.user_id,
        username=data.username,
        online=data.online
    )


@router.get("/user/private")
async def get_user_data(query_user_id: str, user_id: uuid.UUID = Depends(get_current_user_id), db: DBClient = Depends(get_db)) -> GetPrivateUserDataResponse:
    data = db.get_private_user(uuid.UUID(query_user_id))

    if data is None:
        return GetPrivateUserDataResponse()
    
    return GetPrivateUserDataResponse(
        user_id=data.user_id,
        username=data.username,
        pass_hash=data.pass_hash,
        online=data.online
    )