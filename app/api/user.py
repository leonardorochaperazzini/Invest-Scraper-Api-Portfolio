from typing import Annotated

from fastapi import APIRouter, Depends

from service.Auth.model.User import User as UserModel

from service.Auth import get_current_active_user

router = APIRouter()

@router.get("/users/me/", response_model=UserModel)
async def read_users_me(
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
):
    return current_user