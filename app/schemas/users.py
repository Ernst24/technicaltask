from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    name: str
    surname: str
    patronym: str
    email: EmailStr


class UserRole(BaseModel):
    role_id: int


class UsersRequestAdd(User):
    password: str


class UsersAdd(User):
    hashed_password: str


class UsersLoginData(BaseModel):
    email: EmailStr
    password: str


class UserHashedPassword(BaseModel):
    id: int
    hashed_password: str
    is_active: bool


class UserPATCH(BaseModel):
    name: str | None = Field(default=None, min_length=4, max_length=20)
    surname: str | None = Field(default=None, min_length=4, max_length=20)
    patronym: str | None = Field(default=None, min_length=4, max_length=25)
