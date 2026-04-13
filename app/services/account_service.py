from sqlalchemy.orm import Session
from app.models.user import User
from fastapi import HTTPException

class AccountService:
    def get_balance(account_number: str, session: Session):
        account = session.query(User).filter(User.account == account_number).first()
        if not account:
            raise HTTPException()
        
        return account