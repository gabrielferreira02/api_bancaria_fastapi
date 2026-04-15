from sqlalchemy.orm import Session
from app.models.user import User
from fastapi import HTTPException

class AccountService:
    def get_balance(account_number: str, session: Session, user: User):
        if user.account != account_number:
            raise HTTPException(status_code=403, detail="Access denied. You can see your balance only")
        account = session.query(User).filter(User.account == account_number).first()
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        
        return account