from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_hash_password, verify_password
from app.models.models import User
from app.schemas.schemas import UserCreate


class CRUDUser:
    async def create(self, db: AsyncSession, obj_in: UserCreate) -> User:
        hashed_password = create_hash_password(obj_in.password)

        # ✅ Только то, что точно есть в модели User:
        db_obj = User(
            username=obj_in.username,
            email=obj_in.email,
            hash_password=hashed_password,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_by_id(self, db: AsyncSession, user_id: int) -> User | None:  # Read
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_username(
        self, db: AsyncSession, username: str
    ) -> User | None:  # Read
        result = await db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def get_by_email(self, db: AsyncSession, email: int) -> User | None:  # Read
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def update(self, db: AsyncSession, db_obj: User, obj_in: dict) -> User:
        for field, value in obj_in.items():
            if field == "hash_password":
                continue
            setattr(db_obj, field, value)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, user_id: int) -> User | None:
        user = await self.get_by_id(db, user_id=user_id)
        if not user:
            return None

        await db.delete(user)
        await db.commit()
        return user

    async def authenticate(
        self, db: AsyncSession, username: str, password: str
    ) -> User | None:  # Auth доп
        user = await self.get_by_username(db, username=username)
        if not user:
            raise HTTPException(401, detail="Пользователь не найден")
        if not verify_password(password, user.hash_password):
            raise HTTPException(401, detail="Неверный пароль")
        return user


user_crud = CRUDUser()
