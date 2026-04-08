from app.core.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, String, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates
from sqlalchemy.sql import func
import uuid

class Idempotency(Base):
    __tablename__ = "idempotency_db"

    idempotency_key = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_account_number = Column(ForeignKey("user_db.account"), nullable=True, index=True)
    status = Column(String(50), nullable=False, default="processing")
    response_code = Column(Integer, nullable=True)
    response_body = Column(JSON, nullable=True)
    request_hash = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

