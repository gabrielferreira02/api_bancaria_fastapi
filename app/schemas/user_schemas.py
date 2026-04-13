from pydantic import BaseModel
from datetime import datetime

class UserResponseSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    cpf: str
    account: str
    balance: float
    created_at: datetime

    class Config:
        from_attributes = True

class UserBalanceSchema(BaseModel):
    account: str
    balance: float
    updated_at: datetime