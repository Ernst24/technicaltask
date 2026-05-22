from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound
from pydantic import EmailStr, BaseModel
from app.exceptions import EmailNotRegisteredException
from app.repository.base import BaseRepository
from app.repository.datamapper.mappers import UsersMapper
from app.models.users import UsersOrm
from app.schemas.users import UserHashedPassword, UserPATCH


class UsersRepository(BaseRepository):
    model = UsersOrm
    mapper = UsersMapper

    async def get_hashed_password(self, email: EmailStr):
        user = select(self.model).filter_by(email=email)
        try:
            res = await self.session.execute(user)
            result = res.scalars().one()
        except NoResultFound:
            raise EmailNotRegisteredException
        return UserHashedPassword.model_validate(result, from_attributes=True)

    async def delete_user(self, user_id: int):
        stmt = update(self.model).filter_by(id=user_id).values(is_active=False)
        await self.session.execute(stmt)

    async def update(self, data: BaseModel, exclude_unset=True, **filter_by):
        stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        ).returning(self.model)
        res = await self.session.execute(stmt)
        result = res.scalars().one()
        return UserPATCH.model_validate(result, from_attributes=True)

    async def is_active(self, user_id: int):
        query = select(self.model).filter_by(id=user_id, is_active=True)
        res = await self.session.execute(query)
        result = res.scalars().one_or_none()
        return result
