from typing import Annotated
from fastapi import Depends, Request

from app.database import session
from app.schemas.permissions import ResourceEnum, ActionEnum
from app.exceptions import (
    AuthTokenMissingHTTPException,
    UserWasDeletedOrBannedHTTPException,
    PermissionDeniedHTTPException,
)
from app.service.auth import AuthService
from app.utils.db_manager import DBManager


def db_manager():
    return DBManager(session_factory=session)


async def get_db():
    async with db_manager() as db:
        yield db


DBDep = Annotated[DBManager | None, Depends(get_db)]


def get_token(request: Request):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise AuthTokenMissingHTTPException
    return access_token


async def get_current_user(db: DBDep, token: str = Depends(get_token)):
    data = AuthService(db).decode_token(token)
    user_id = data["user_id"]
    active = await AuthService(db).is_active(user_id)
    if not active:
        raise UserWasDeletedOrBannedHTTPException
    return user_id


UserIdDep = Annotated[int, Depends(get_current_user)]


class PermissionChecker:
    def __init__(self, resource: ResourceEnum, action: ActionEnum):
        self.resource = resource
        self.action = action

    async def __call__(self, db: DBDep, user_id: UserIdDep) -> int:
        user = await db.permissions.get_user_role(user_id)

        has_permission = await db.permissions.check_permission_exists(
            role_id=user.role_id, resource=self.resource, action=self.action
        )

        if not has_permission:
            raise PermissionDeniedHTTPException

        return user_id
