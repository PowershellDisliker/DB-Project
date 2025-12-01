from fastapi import APIRouter

router = APIRouter()

@router.get("/api/user/public")
async def public_user_data(request: PublicUserDataRequest, current_user: dict = Depends(get_current_user)) -> PublicUserDataResponse:
    data = database.get_public_user(request.user)

    return {
        "username": data.Username,
        "online": data.Online
    }


@router.get("/api/user/private")
async def get_user_data(request: PrivateUserDataRequest, current_user: dict = Depends(get_current_user)) -> PrivateUserDataResponse:
    data = database.get_private_user(request.user_id)
    
    return {
        "user_id": d.ID,
        "username": d.Username,
        "pass_hash": d.PassHash,
        "online": d.Online
    }