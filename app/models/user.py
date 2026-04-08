from app.core.database import Base
from sqlalchemy import Column, String, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import validates
from app.helpers.validate_cpf import validate_cpf
import uuid

class User(Base):
    __tablename__ = "user_db"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account = Column("account", String, unique=True, nullable=False)
    cpf = Column("cpf", String, unique=True,nullable=False)
    email = Column("email", String, nullable=False)
    first_name = Column("first_name", String, nullable=False)
    last_name = Column("last name", String, nullable=False)
    balance = Column("balance", Float, default=0)
    password = Column("password", String, nullable=False)
    created_at = Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column("updated_at", DateTime(timezone=True), server_default=func.now(), nullable=False)

    @validates('cpf')    
    def is_valid_cpf(self, key, cpf):
        if not validate_cpf(cpf):
            raise ValueError("Invalid CPF")
        return cpf

