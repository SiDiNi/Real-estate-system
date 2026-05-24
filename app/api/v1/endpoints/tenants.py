from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.crud.crud_tenant import tenant_crud
from app.models.models import User
from app.schemas.schemas import TenantCreate, TenantResponse, TenantUpdate

router = APIRouter()


@router.post("/", response_model=TenantResponse, status_code=status.HTTP_201_CREATED)
async def create_tenant(
    tenant_in: TenantCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await tenant_crud.create(db, obj_in=tenant_in.dict())


@router.get("/", response_model=list[TenantResponse])
async def read_tenants(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    return await tenant_crud.get_multi(db, skip=skip, limit=limit)


@router.get("/{tenant_id}", response_model=TenantResponse)
async def read_tenant(tenant_id: int, db: AsyncSession = Depends(get_db)):
    obj = await tenant_crud.get(db, tenant_id=tenant_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Арендатор не найден")
    return obj


@router.put("/{tenant_id}", response_model=TenantResponse)
async def update_tenant(
    tenant_id: int,
    tenant_in: TenantUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = await tenant_crud.get(db, tenant_id=tenant_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Арендатор не найден")
    return await tenant_crud.update(
        db, db_obj=obj, obj_in=tenant_in.dict(exclude_unset=True)
    )


@router.delete("/{tenant_id}")
async def delete_tenant(
    tenant_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not await tenant_crud.delete(db, tenant_id=tenant_id):
        raise HTTPException(status_code=404, detail="Арендатор не найден")
    return {"message": "Арендатор удален"}
