from fastapi import APIRouter, Depends, Header, Path, Query
from app.schemas.transaction_schemas import CreateTransactionSchema, CreditSchema
from app.schemas.auth_schemas import RegisterResponseSchema
from sqlalchemy.orm import Session
from app.api.deps import get_session
from uuid import UUID
from app.services.transaction_service import TransactionService

transaction_router = APIRouter(prefix="/transactions", tags=["Transactions"])

@transaction_router.post("", status_code=201)
async def create_transaction(
    body: CreateTransactionSchema, 
    session: Session = Depends(get_session),
    transaction_key: UUID = Header(...)):
    return TransactionService.create_transaction(body, session, transaction_key)

@transaction_router.get("/list/{account}")
async def list_account_transactions(
    account: str,
    range: int = Query(30),
    page: int = Query(1),
    session: Session = Depends(get_session)):
    return TransactionService.list_transactions(range, account, page, session)

@transaction_router.patch("/credit", response_model=RegisterResponseSchema)
async def account_credit(body: CreditSchema, session: Session = Depends(get_session)):
    return TransactionService.credit(body.amount, body.account, session)