from app.models.users import UsersOrm
from app.repository.datamapper.base import DataMapper
from app.schemas.users import User


class UsersMapper(DataMapper):
    model = UsersOrm
    schema = User
