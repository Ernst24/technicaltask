from sqlalchemy import select
from app.models.roles import PermissionsOrm
from app.models.users import UsersOrm

from app.repository.base import BaseRepository
from app.schemas.permissions import ResourceEnum, ActionEnum
from app.schemas.users import UserRole


class PermissionsRepository(BaseRepository):
    model = PermissionsOrm
    mapper = None

    async def check_permission_exists(
        self, role_id: int, resource: ResourceEnum, action: ActionEnum
    ) -> bool:
        query = select(self.model).filter_by(
            role_id=role_id, resource=resource, action=action
        )
        res = await self.session.execute(query)
        result = res.scalars().one_or_none()
        return result

    async def get_user_role(self, user_id: int):
        query = select(UsersOrm).filter_by(id=user_id)
        res = await self.session.execute(query)
        result = res.scalars().one()
        return UserRole.model_validate(result, from_attributes=True)
