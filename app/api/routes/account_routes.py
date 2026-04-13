from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_session
from app.schemas.user_schemas import UserBalanceSchema
from app.services.account_service import AccountService

account_router = APIRouter(prefix="/account", tags=["Account"])

@account_router.get("/{account_number}/balance", response_model=UserBalanceSchema)
async def get_balance(account_number: str, session: Session = Depends(get_session)):
    return AccountService.get_balance(account_number, session)