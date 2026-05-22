from app.repository.admin import AdminRepository
from app.repository.permissions import PermissionsRepository
from app.repository.users import UsersRepository


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.auth = UsersRepository(self.session)
        self.admin = AdminRepository(self.session)
        self.permissions = PermissionsRepository(self.session)

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()
