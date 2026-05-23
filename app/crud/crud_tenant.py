from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Tenant


class CRUDTenant:
    async def get(self, db: AsyncSession, tenant_id: int) -> Optional[Tenant]:
        result = await db.execute(select(Tenant).where(Tenant.id == tenant_id))
        return result.scalar_one_or_none()

    async def get_multi(
        self, db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[Tenant]:
        result = await db.execute(select(Tenant).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, db: AsyncSession, obj_in: dict) -> Tenant:
        db_obj = Tenant(**obj_in)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, db_obj: Tenant, obj_in: dict) -> Tenant:
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, tenant_id: int) -> bool:
        obj = await self.get(db, tenant_id)
        if obj:
            await db.delete(obj)
            await db.commit()
            return True
        return False


tenant_crud = CRUDTenant()
