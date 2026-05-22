from fastapi import APIRouter, Response

from app.api.dependencies import DBDep, UserIdDep
from app.exceptions import (
    UserEmailAlreadyExistsException,
    UserEmailAlreadyExistsHTTPException,
    EmailNotRegisteredException,
    EmailNotRegisteredHTTPException,
    IncorrectPasswordException,
    IncorrectPasswordHTTPException,
)
from app.schemas.users import UsersRequestAdd, UsersLoginData, UserPATCH
from app.service.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Аутентификация, Регистрация"])


@router.get("/me", summary="Информация о себе")
async def get_me(user_id: UserIdDep, db: DBDep):
    return await AuthService(db).get_me(user_id)


@router.post("/register", summary="Регистрация пользователя")
async def register(user_data: UsersRequestAdd, db: DBDep):
    try:
        result = await AuthService(db).register(user_data)
        return {"Registration successful": result}
    except UserEmailAlreadyExistsException:
        raise UserEmailAlreadyExistsHTTPException


@router.post("/login", summary="Аутентификация")
async def login(user_data: UsersLoginData, response: Response, db: DBDep):
    try:
        result = await AuthService(db).login(user_data)
    except EmailNotRegisteredException:
        raise EmailNotRegisteredHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException
    response.set_cookie("access_token", result)
    return {"Logged In!": "Successfully"}


@router.get("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"Logged Out!": "Successfully"}


@router.delete("/delete", summary="Удалить свой аккаунт!, ставим is_active=False")
async def delete(response: Response, user_id: UserIdDep, db: DBDep):
    await AuthService(db).delete_user(user_id)
    response.delete_cookie("access_token")
    return {"Deleted!": "Successfully"}


@router.patch("/", summary="Изменение информации о пользователе")
async def update_users_info(data: UserPATCH, user_id: UserIdDep, db: DBDep):
    result = await AuthService(db).update_user(data, user_id)
    return {"Updated!": result}
