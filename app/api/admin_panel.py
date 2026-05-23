from fastapi import APIRouter, Depends
from fastapi.params import Path

from app.api.dependencies import DBDep, PermissionChecker
from app.exceptions import (
    RuleAlreadyExistsException,
    RuleAlreadyExistsHTTPException,
    SelfBlockException,
    SelfBlockHTTPException,
)
from app.schemas.permissions import ResourceEnum, ActionEnum, PermissionCreateSchema
from app.service.admin import AdminService

router = APIRouter(prefix="/admin/permissions", tags=["Администрирование"])


@router.get(
    "/",
    summary="Просмотреть все правила доступа в системе - [SUPPORT][MANAGER][ADMIN]",
)
async def get_all_rules(
    db: DBDep, user_id=Depends(PermissionChecker(ResourceEnum.USER, ActionEnum.READ))
):
    return await AdminService(db).get_all_rules()


@router.post("/", summary="Создать правило доступа - [ADMIN]")
async def create_new_rule(
    data: PermissionCreateSchema,
    db: DBDep,
    user_id=Depends(PermissionChecker(ResourceEnum.USER, ActionEnum.CREATE)),
):
    try:
        await AdminService(db).create_new_rule(data)
    except RuleAlreadyExistsException:
        raise RuleAlreadyExistsHTTPException
    return {"Status": "Success"}


@router.post(
    "/ban/user/{ban_id}", summary="Бан пользователя-active=False [ADMIN]"
)
async def ban_user(
    db: DBDep,
    ban_id: int = Path(..., description="ID человека для бана"),
    user_id=Depends(PermissionChecker(ResourceEnum.USER, ActionEnum.BAN)),
):
    try:
        await AdminService(db).ban_user(ban_id, user_id)
    except SelfBlockException:
        raise SelfBlockHTTPException
    return {
        "Status": "Success",
        "message": f"Пользователь с ID={ban_id} успешно забанен",
    }


@router.put("/assign/user/{assign_id}", summary="Назначать на новую роль - [ADMIN]")
async def assign_user(
    role_id: int,
    db: DBDep,
    assign_id: int = Path(..., description="Человек которому выдается новая роль"),
    user_id: int = Depends(PermissionChecker(ResourceEnum.USER, ActionEnum.UPDATE)),
):
    await AdminService(db).assign_role(assign_id, role_id)
    return {"Status": "Success"}
