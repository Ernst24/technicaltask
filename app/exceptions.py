from fastapi.exceptions import HTTPException


class ProjectException(Exception):
    detail = "Что то пошло не так"

    def __init__(self, detail: str | None = None):
        super().__init__(detail or self.detail)


class ObjectNotFoundException(ProjectException):
    detail = "Обьект не найден"


class ObjectAlreadyExistsException(ProjectException):
    detail = "Такой обьект уже существует"


class InvalidTokenException(ProjectException):
    detail = "Неправильный токен"


class SelfBlockException(ProjectException):
    detail = "Ошибка: Вы пытаетесь заблокировать себя"


class UserEmailAlreadyExistsException(ObjectAlreadyExistsException):
    detail = "Пользователь с такой почтой существует"


class IncorrectPasswordException(ProjectException):
    detail = "Неправильный пароль"


class EmailNotRegisteredException(ProjectException):
    detail = "Почта не зарегистрирована"


class RuleAlreadyExistsException(ProjectException):
    detail = "Такое правило доступа уже существует"


class ProjectHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self, detail: str | None = None):
        super().__init__(status_code=self.status_code, detail=detail or self.detail)


class ObjectAlreadyExistsHTTPException(ProjectHTTPException):
    status_code = 409
    detail = "Такой обьект уже существует"


class UserAlreadyExistsHTTPException(ObjectAlreadyExistsHTTPException):
    status_code = 409
    detail = "Такой пользователь уже существует"


class UserEmailAlreadyExistsHTTPException(ObjectAlreadyExistsHTTPException):
    status_code = 409
    detail = "Пользователь с такой почтой уже существует"


class RuleAlreadyExistsHTTPException(ProjectException):
    status_code = 409
    detail = "Такое правило доступа уже существует"


class UserNotAuthenticatedHTTPException(ProjectHTTPException):
    status_code = 401
    detail = "Аутентифицируйтесь пожалуйста"


class EmailNotRegisteredHTTPException(ProjectHTTPException):
    status_code = 401
    detail = "Неверная почта или пароль"


class IncorrectPasswordHTTPException(ProjectHTTPException):
    status_code = 401
    detail = "Неверная почта или пароль"


class InvalidTokenHTTPException(ProjectHTTPException):
    status_code = 401
    detail = "Неправильный токен"


class PermissionDeniedHTTPException(ProjectHTTPException):
    status_code = 403
    detail = "У вас недостаточно прав"


class TokenExpiredHTTPException(ProjectHTTPException):
    status_code = 401
    detail = "Токен истёк, Аутентифицируйтесь заново"


class AuthTokenMissingHTTPException(ProjectHTTPException):
    status_code = 401
    detail = "Вы не предоставили токен доступа"


class UserWasDeletedOrBannedHTTPException(ProjectHTTPException):
    status_code = 403
    detail = "Данный аккаунт был удален / забанен"


class SelfBlockHTTPException(ProjectHTTPException):
    status_code = 403
    detail = "Ошибка: Вы пытаетесь заблокировать себя"
