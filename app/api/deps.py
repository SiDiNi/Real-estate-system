from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_user_from_token
from app.crud.crud_user import user_crud
from app.database.db import get_db as get_async_db
from app.models.models import User


async def get_db():
    async for session in get_async_db():
        yield session


async def get_current_user(
    db: AsyncSession = Depends(get_db), token: str = Depends(get_user_from_token)
) -> User:
    if token is None:
        raise HTTPException(
            status_code=401, detail="Не удалось подтвердить учетные данные"
        )

    user = await user_crud.get_by_username(db, username=token)

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Пользователь неактивен")

    return user
