from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Contract


class CRUDContract:
    async def get(self, db: AsyncSession, contract_id: int) -> Optional[Contract]:
        result = await db.execute(select(Contract).where(Contract.id == contract_id))
        return result.scalar_one_or_none()

    async def get_multi(
        self, db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[Contract]:
        result = await db.execute(select(Contract).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, db: AsyncSession, obj_in: dict) -> Contract:
        db_obj = Contract(**obj_in)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self, db: AsyncSession, db_obj: Contract, obj_in: dict
    ) -> Contract:
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, contract_id: int) -> bool:
        obj = await self.get(db, contract_id)
        if obj:
            await db.delete(obj)
            await db.commit()
            return True
        return False


contract_crud = CRUDContract()
