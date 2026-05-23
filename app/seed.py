import asyncio
from passlib.context import CryptContext
from sqlalchemy import select

from app.database import session
from app.models.roles import RolesOrm, PermissionsOrm
from app.models.users import UsersOrm

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def seed_data():
    async with session() as db:
        result = await db.execute(select(RolesOrm))
        if result.scalars().first() is not None:
            print("База данных уже содержит тестовые данные. Пропускаем сид.")
            return

        print("Запуск инициализации тестовых данных...")

        admin_role = RolesOrm(role_name="admin")
        manager_role = RolesOrm(role_name="manager")
        client_role = RolesOrm(role_name="client")
        support_role = RolesOrm(role_name="support")

        db.add_all([admin_role, manager_role, client_role, support_role])
        await db.flush()

        hashed_password_example = pwd_context.hash("secret_pass")

        users = [
            UsersOrm(
                name="Иван",
                surname="Админов",
                patronym="Игоревич",
                email="admin@mail.ru",
                hashed_password=hashed_password_example,
                is_active=True,
                role_id=1,
            ),
            UsersOrm(
                name="Петр",
                surname="Менеджеров",
                patronym="Алексеевич",
                email="manager@mail.ru",
                hashed_password=hashed_password_example,
                is_active=True,
                role_id=2,
            ),
            UsersOrm(
                name="Алексей",
                surname="Клиентов",
                patronym="Сергеевич",
                email="client@mail.ru",
                hashed_password=hashed_password_example,
                is_active=True,
                role_id=3,
            ),
            UsersOrm(
                name="Елена",
                surname="Саппортова",
                patronym="Владимировна",
                email="support@mail.ru",
                hashed_password=hashed_password_example,
                is_active=True,
                role_id=4,
            ),
            UsersOrm(
                name="Забаненный",
                surname="Пользователь",
                patronym="Отшельникович",
                email="banned@mail.ru",
                hashed_password=hashed_password_example,
                is_active=False,  # Мягкий бан для проверки 401 ошибки
                role_id=3,
            ),
        ]

        db.add_all(users)
        await db.flush()

        # 4. Правила CLIENT (role_id = 3)
        client_perms = [
            PermissionsOrm(role_id=3, resource="document", action="read"),
            PermissionsOrm(role_id=3, resource="ticket", action="create"),
            PermissionsOrm(role_id=3, resource="ticket", action="read"),
        ]

        # 5. Правила SUPPORT (role_id = 4)
        support_perms = [
            PermissionsOrm(role_id=4, resource="document", action="read"),
            PermissionsOrm(role_id=4, resource="user", action="read"),
            PermissionsOrm(role_id=4, resource="ticket", action="read"),
            PermissionsOrm(role_id=4, resource="ticket", action="update"),
        ]

        # 6. Правила MANAGER (role_id = 2)
        manager_perms = [
            PermissionsOrm(role_id=2, resource="document", action="read"),
            PermissionsOrm(role_id=2, resource="document", action="create"),
            PermissionsOrm(role_id=2, resource="document", action="update"),
            PermissionsOrm(role_id=2, resource="analytics", action="read"),
        ]

        # 7. Правила ADMIN (role_id = 1) — Полный доступ
        admin_perms = [
            PermissionsOrm(role_id=1, resource="document", action="read"),
            PermissionsOrm(role_id=1, resource="document", action="create"),
            PermissionsOrm(role_id=1, resource="document", action="update"),
            PermissionsOrm(role_id=1, resource="document", action="delete"),
            PermissionsOrm(role_id=1, resource="user", action="read"),
            PermissionsOrm(role_id=1, resource="user", action="create"),
            PermissionsOrm(role_id=1, resource="user", action="ban"),
            PermissionsOrm(role_id=1, resource="user", action="update"),
            PermissionsOrm(role_id=1, resource="ticket", action="create"),
            PermissionsOrm(role_id=1, resource="ticket", action="read"),
            PermissionsOrm(role_id=1, resource="ticket", action="update"),
            PermissionsOrm(role_id=1, resource="analytics", action="read"),
            PermissionsOrm(role_id=1, resource="analytics", action="delete"),
        ]

        db.add_all(client_perms + support_perms + manager_perms + admin_perms)
        await db.commit()
        print("Тестовые данные успешно загружены")


if __name__ == "__main__":
    asyncio.run(seed_data())
