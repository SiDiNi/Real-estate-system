from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hash_password = Column(String)
    email = Column(String, unique=True, index=True)
    # phone = Column(String, unique=True, index=True)
    # full_name = Column(String)
    role = Column(String, default="admin")
    is_active = Column(Boolean, default=True)
    # created_at = Column(DateTime)

    # Связи
    managed_requests = relationship("Request", back_populates="manager")


class Property(Base):  # Объекты недвижимости
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    address = Column(String)
    property_type = Column(String)
    area = Column(Float)
    price = Column(Float)
    rooms_count = Column(Integer, nullable=True)
    description = Column(String, nullable=True)
    is_available = Column(Boolean, default=True)

    # Связи
    contracts = relationship(
        "Contract", back_populates="property_obj", cascade="all, delete-orphan"
    )
    payments = relationship("Payment", back_populates="property_obj")
    requests = relationship("Request", back_populates="property_obj")


class Tenant(Base):  # Арендаторы
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone = Column(String)
    passport = Column(String)
    email = Column(String, nullable=True)

    # Связи
    contracts = relationship(
        "Contract", back_populates="tenant_obj", cascade="all, delete-orphan"
    )
    payments = relationship("Payment", back_populates="tenant_obj")


class Contract(Base):  # Договоры аренды
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"))
    tenant_id = Column(Integer, ForeignKey("tenants.id"))

    start_date = Column(Date)
    end_date = Column(Date)
    monthly_payment = Column(Float)
    status = Column(String, default="active")
    contract_number = Column(String, unique=True)

    # Связи
    property_obj = relationship("Property", back_populates="contracts")
    tenant_obj = relationship("Tenant", back_populates="contracts")
    payments = relationship("Payment", back_populates="contract_obj")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"))
    property_id = Column(Integer, ForeignKey("properties.id"))
    tenant_id = Column(Integer, ForeignKey("tenants.id"))

    amount = Column(Numeric(10, 2))
    payment_date = Column(Date)
    status = Column(String, default="pending")
    payment_method = Column(String)

    # Связи
    contract_obj = relationship("Contract", back_populates="payments")
    property_obj = relationship("Property", back_populates="payments")
    tenant_obj = relationship("Tenant", back_populates="payments")


class Request(Base):  # Обратная связь
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"))
    manager_id = Column(Integer, ForeignKey("users.id"))

    client_name = Column(String)
    client_phone = Column(String)
    client_email = Column(String, nullable=True)
    message = Column(Text, nullable=True)
    status = Column(String, default="new")
    created_at = Column(DateTime)

    # Связи
    property_obj = relationship("Property", back_populates="requests")
    manager = relationship("User", back_populates="managed_requests")
