from app.exceptions import (
    SelfBlockException,
    ObjectAlreadyExistsException,
    RuleAlreadyExistsException,
)
from app.schemas.permissions import PermissionCreateSchema
from app.service.base import BaseService


class AdminService(BaseService):
    async def ban_user(self, ban_id: int, admin_id: int):
        if ban_id == admin_id:
            raise SelfBlockException
        await self.db.admin.ban_user(ban_id)
        await self.db.commit()

    async def is_admin(self, user_id: int):
        return await self.db.admin.is_admin(user_id=user_id)

    async def assign_role(self, user_id: int, role_id: int):
        await self.db.admin.assign_role(user_id=user_id, role_id=role_id)
        await self.db.commit()

    async def get_all_rules(self):
        result = await self.db.admin.get_all_rules()
        await self.db.commit()
        return result

    async def create_new_rule(self, data: PermissionCreateSchema):
        try:
            await self.db.admin.create_new_rule(data)
            await self.db.commit()
        except ObjectAlreadyExistsException:
            raise RuleAlreadyExistsException
