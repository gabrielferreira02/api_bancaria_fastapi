from app.core.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Float, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates
from sqlalchemy.sql import func
import uuid

class Transaction(Base):
    __tablename__ = "transaction_db"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    amount = Column("amount", Float, nullable=False)
    idempotency_key = Column("idempotency_key", ForeignKey("idempotency_db.idempotency_key"), nullable=False)
    sender_account_number = Column("sender_account_number", ForeignKey("user_db.account"), nullable=False)
    beneficiary_account_number = Column("beneficiary_account_number", ForeignKey("user_db.account"), nullable=False)
    created_at = Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False)

    @validates("amount")
    def is_valid_amount(self, key, amount):
        if amount <= 0:
            raise ValueError("Invalid amount")
        return amount

