import os
import jwt

from typing import Annotated
from passlib.context import CryptContext
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

from app.contract.repository.Base import Base as BaseRepositoryInterface

from app.model.User import User as UserModelDB

from app.repository.User import User as UserRepository

from app.service.Auth.model.TokenData import TokenData
from app.service.Auth.model.User import User as UserModel

SECRET_KEY = os.getenv("AUTH_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

class Auth:
    def __init__(self, user_repository: BaseRepositoryInterface):
        self.user_repository = user_repository
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __get_user(self, username: str) -> UserModelDB:
        users = self.user_repository.all(filter = {"username": username})

        if not users:
            return None
        return users[0]
    
    def __verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def authenticate_user(self, username: str, password: str) -> UserModelDB | bool:
        user = self.__get_user(username)
        
        if not user:
            return False
        if not self.__verify_password(password, user.hashed_password):
            return False
        return user
    
    def create_access_token(self, data: dict) -> str:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    async def get_current_user(self, token: Annotated[str, Depends(oauth2_scheme)]):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except InvalidTokenError:
            raise credentials_exception
        user = self.__get_user(username=token_data.username)
        if user is None:
            raise credentials_exception
        return user


auth_service = Auth(UserRepository(UserModelDB))

async def get_current_active_user(
    current_user: Annotated[UserModel, Depends(auth_service.get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
