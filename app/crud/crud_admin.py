import asyncio

from app.crud.crud_user import user_crud
from app.database.db import get_db
from app.schemas.schemas import UserCreate


async def create_admin():
    async for db in get_db():
        admin_data = UserCreate(
            username="admin", password="admin", email="admin@mail.ru"
        )

        # Проверяем, есть ли уже админ
        existing = await user_crud.get_by_username(db, username="admin")
        if existing:
            print("Админ уже существует!")
            return

        new_admin = await user_crud.create(db, obj_in=admin_data)
        print(f"Админ создан: {new_admin.username} / пароль: admin")
        break


if __name__ == "__main__":
    asyncio.run(create_admin())
