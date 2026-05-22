import logging

from asyncpg import UniqueViolationError
from pydantic import BaseModel
from sqlalchemy import update, select, insert
from sqlalchemy.exc import IntegrityError

from app.exceptions import ObjectAlreadyExistsException
from app.models.roles import PermissionsOrm
from app.models.users import UsersOrm
from app.repository.base import BaseRepository
from app.schemas.permissions import PermissionSchema, PermissionCreateSchema


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class AdminRepository(BaseRepository):
    model = UsersOrm
    mapper = None

    async def ban_user(self, ban_id: int):
        stmt = update(self.model).filter_by(id=ban_id).values(is_active=False)
        await self.session.execute(stmt)

    async def is_admin(self, user_id: int):
        query = select(self.model).filter_by(id=user_id, role_id=1)
        res = await self.session.execute(query)
        result = res.scalars().one_or_none()
        if result is not None:
            return True
        return False

    async def assign_role(self, user_id: int, role_id: int):
        query = update(self.model).filter_by(id=user_id).values(role_id=role_id)
        await self.session.execute(query)

    async def get_all_rules(self):
        query = select(PermissionsOrm)
        res = await self.session.execute(query)
        result = res.scalars().all()
        return [
            PermissionSchema.model_validate(perm, from_attributes=True)
            for perm in result
        ]

    async def create_new_rule(self, data: PermissionCreateSchema):
        stmt = insert(PermissionsOrm).values(**data.model_dump())
        try:
            await self.session.execute(stmt)
        except IntegrityError as ex:
            if isinstance(ex.orig.__cause__, UniqueViolationError):
                raise ObjectAlreadyExistsException
            else:
                logger.info(
                    f"Не удалось обработать, переданные данные {data.model_dump()} - ошибка {ex.orig.__cause__}"
                )
                raise ex
