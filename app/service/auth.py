from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import jwt

from app.config import settings
from app.exceptions import (
    ObjectAlreadyExistsException,
    UserEmailAlreadyExistsException,
    IncorrectPasswordException,
    InvalidTokenHTTPException,
    TokenExpiredHTTPException,
    UserWasDeletedOrBannedHTTPException,
)
from app.schemas.users import UsersRequestAdd, UsersAdd, UsersLoginData, UserPATCH
from app.service.base import BaseService


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(password, hashed_password)

    def decode_token(self, token: str):
        try:
            data = jwt.decode(
                token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
            )
        except jwt.exceptions.DecodeError:
            raise InvalidTokenHTTPException
        except jwt.exceptions.ExpiredSignatureError:
            raise TokenExpiredHTTPException
        return data

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        return jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )

    async def register(self, data: UsersRequestAdd):
        hashed_password = self.hash_password(data.password)
        user = UsersAdd(
            name=data.name,
            surname=data.surname,
            patronym=data.patronym,
            email=data.email,
            hashed_password=hashed_password,
        )
        try:
            result = await self.db.auth.add(user)
            await self.db.commit()
            return result
        except ObjectAlreadyExistsException:
            raise UserEmailAlreadyExistsException

    async def login(self, data: UsersLoginData):
        user = await self.db.auth.get_hashed_password(email=data.email)
        if not user.is_active:
            raise UserWasDeletedOrBannedHTTPException
        if not self.verify_password(data.password, user.hashed_password):
            raise IncorrectPasswordException
        access_token = self.create_access_token(data={"user_id": user.id})
        return access_token

    async def get_me(self, user_id: int):
        return await self.db.auth.get_filtered(id=user_id)

    async def is_active(self, user_id: int):
        return await self.db.auth.is_active(user_id=user_id)

    async def delete_user(self, user_id: int):
        await self.db.auth.delete_user(user_id=user_id)
        await self.db.commit()

    async def update_user(self, data: UserPATCH, user_id: int):
        data = await self.db.auth.update(data, id=user_id)
        await self.db.commit()
        return data
