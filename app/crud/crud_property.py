from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Property


class CRUDProperty:
    async def get(self, db: AsyncSession, property_id: int) -> Optional[Property]:
        result = await db.execute(select(Property).where(Property.id == property_id))
        return result.scalar_one_or_none()

    async def get_multi(
        self, db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[Property]:
        result = await db.execute(select(Property).offset(skip).limit(limit))
        return result.scalars().all()

    async def get_available(self, db: AsyncSession) -> List[Property]:
        """Только свободные объекты"""
        result = await db.execute(select(Property).where(Property.is_available))
        return result.scalars().all()

    async def create(self, db: AsyncSession, obj_in: dict) -> Property:
        db_obj = Property(**obj_in)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self, db: AsyncSession, db_obj: Property, obj_in: dict
    ) -> Property:
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, property_id: int) -> bool:
        obj = await self.get(db, property_id)
        if obj:
            await db.delete(obj)
            await db.commit()
            return True
        return False


property_crud = CRUDProperty()
