from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.crud.crud_property import property_crud
from app.models.models import User
from app.schemas.schemas import PropertyCreate, PropertyResponse, PropertyUpdate


router = APIRouter()


@router.post("/", response_model=PropertyResponse, status_code=status.HTTP_201_CREATED)
async def create_property(
    property_in: PropertyCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Добавить новый объект недвижимости"""
    return await property_crud.create(db, obj_in=property_in.dict())


@router.get("/", response_model=list[PropertyResponse])
async def read_properties(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    """Получить список всех объектов"""
    return await property_crud.get_multi(db, skip=skip, limit=limit)


@router.get("/{property_id}", response_model=PropertyResponse)
async def read_property(property_id: int, db: AsyncSession = Depends(get_db)):
    """Получить объект по ID"""
    property_obj = await property_crud.get(db, property_id=property_id)
    if not property_obj:
        raise HTTPException(status_code=404, detail="Объект не найден")
    return property_obj


@router.put("/{property_id}", response_model=PropertyResponse)
async def update_property(
    property_id: int,
    property_in: PropertyUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Обновить данные объекта"""
    property_obj = await property_crud.get(db, property_id=property_id)
    if not property_obj:
        raise HTTPException(status_code=404, detail="Объект не найден")
    return await property_crud.update(
        db, db_obj=property_obj, obj_in=property_in.dict(exclude_unset=True)
    )


@router.delete("/{property_id}")
async def delete_property(
    property_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Удалить объект"""
    if not await property_crud.delete(db, property_id=property_id):
        raise HTTPException(status_code=404, detail="Объект не найден")
    return {"message": "Объект удален"}
