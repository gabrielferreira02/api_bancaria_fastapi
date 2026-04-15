from pydantic import BaseModel
from datetime import datetime

class RegisterSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    cpf: str
    password: str

    class Config:
        from_attributes = True

class RegisterResponseSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    cpf: str
    account: str
    balance: float
    created_at: datetime

    class Config:
        from_attributes = True

class LoginRequestSchema(BaseModel):
    account: str
    password: str

    class Config:
        from_attributes = True

class LoginResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

    class Config:
        from_attributes = True