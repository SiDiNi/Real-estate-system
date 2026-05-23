from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    message: str


class CustomExceptionModel(BaseModel):
    status_code: int
    detail: str
    message: str = ""


# Property
class PropertyBase(BaseModel):
    name: str
    address: str
    property_type: str
    area: float
    price: float
    rooms_count: Optional[int] = None
    description: Optional[str] = None


class PropertyCreate(PropertyBase):
    pass


class PropertyUpdate(PropertyBase):
    pass


class PropertyResponse(PropertyBase):
    id: int
    is_available: bool

    class Config:
        from_attributes = True


# Tenant
class TenantBase(BaseModel):
    name: str
    phone: str
    passport: str
    email: Optional[EmailStr] = None


class TenantCreate(TenantBase):
    pass


class TenantUpdate(TenantBase):
    pass


class TenantResponse(TenantBase):
    id: int

    class Config:
        from_attributes = True


# Contract
class ContractBase(BaseModel):
    property_id: int
    tenant_id: int
    start_date: date
    end_date: date
    monthly_payment: float
    contract_number: str


class ContractCreate(ContractBase):
    pass


class ContractUpdate(ContractBase):
    status: Optional[str] = "active"


class ContractResponse(ContractBase):
    id: int
    status: str

    class Config:
        from_attributes = True
