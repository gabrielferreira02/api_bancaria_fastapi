from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class CreateTransactionSchema(BaseModel):
    sender_account: str
    beneficiary_account: str
    amount: float
    class Config:
        from_attributes = True

class CreateTransactionResponseSchema(BaseModel):
    id: UUID
    amount: float
    status: str
    created_at: datetime
    class Config:
        from_attributes = True

class CreditSchema(BaseModel):
    account: str
    amount: float
    class Config:
        from_attributes = True