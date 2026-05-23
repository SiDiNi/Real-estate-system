from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.crud.crud_contract import contract_crud
from app.crud.crud_property import property_crud
from app.crud.crud_tenant import tenant_crud
from app.models.models import Contract, User
from app.schemas.schemas import ContractCreate, ContractResponse, ContractUpdate


router = APIRouter()


@router.post("/", response_model=ContractResponse, status_code=status.HTTP_201_CREATED)
async def create_contract(
    contract_in: ContractCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Создать новый договор с расчётом итоговой суммы.
    """
    # Проверки
    prop = await property_crud.get(db, property_id=contract_in.property_id)
    tenant = await tenant_crud.get(db, tenant_id=contract_in.tenant_id)

    if not prop:
        raise HTTPException(status_code=404, detail="Недвижимость не найдена")
    if not tenant:
        raise HTTPException(status_code=404, detail="Арендатор не найден")

    db_obj = Contract(**contract_in.dict())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)

    return db_obj


@router.get("/", response_model=list[ContractResponse])
async def read_contracts(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    return await contract_crud.get_multi(db, skip=skip, limit=limit)


@router.get("/{contract_id}", response_model=ContractResponse)
async def read_contract(contract_id: int, db: AsyncSession = Depends(get_db)):
    contract = await contract_crud.get(db, contract_id=contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail="Договор не найден")
    return contract


@router.put("/{contract_id}", response_model=ContractResponse)
async def update_contract(
    contract_id: int,
    contract_in: ContractUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    contract = await contract_crud.get(db, contract_id=contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail="Договор не найден")
    return await contract_crud.update(
        db, db_obj=contract, obj_in=contract_in.dict(exclude_unset=True)
    )


@router.delete("/{contract_id}")
async def delete_contract(
    contract_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not await contract_crud.delete(db, contract_id=contract_id):
        raise HTTPException(status_code=404, detail="Договор не найден")
    return {"message": "Договор удален"}
