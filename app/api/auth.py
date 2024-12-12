from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from model.User import User as UserModel

from repository.User import User as UserRepository

from service.Auth.model.Token import Token
from service.Auth import Auth as AuthService

router = APIRouter()

@router.post("/auth/token")
async def login_for_access_token( form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    auth_service = AuthService(UserRepository(UserModel))

    user = auth_service.authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth_service.create_access_token( data= {"sub": user.username} ) 
    
    return Token(access_token=access_token, token_type="bearer")