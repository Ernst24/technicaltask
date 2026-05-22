from app.service.base import BaseService


class PermissionsService(BaseService):
    async def get_user_role(self, user_id):
        return await self.db.permissions.get_user_role(user_id)
