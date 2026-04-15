from fastapi import HTTPException
from app.schemas.transaction_schemas import CreateTransactionSchema, CreateTransactionResponseSchema
from sqlalchemy.orm import Session
from uuid import UUID
from app.models.idempotency import Idempotency
from app.models.user import User
from app.models.transaction import Transaction
from app.helpers.generate_request_hash import generate_request_hash
from datetime import datetime, timedelta

class TransactionService:
    def create_transaction(body: CreateTransactionSchema,
                            session: Session,
                            transaction_key: UUID,
                            user: User):
        exist_idempotency = (session.query(Idempotency)
                             .filter(Idempotency.idempotency_key == transaction_key)
                             .first())
        
        request_hash = generate_request_hash(body)
        
        if exist_idempotency:
            if exist_idempotency.request_hash != request_hash:
                raise HTTPException(status_code=400, detail="This transaction key was already used in another transaction")
            if exist_idempotency.status == "completed":
                return CreateTransactionResponseSchema(**exist_idempotency.response_body)
            if exist_idempotency.status == "processing":
                raise HTTPException(status_code=409, detail="Processing transaction")
            
        idempotency = Idempotency(
            user_account_number = body.sender_account,
            idempotency_key = transaction_key,
            status = "processing",
            request_hash = request_hash
        )
        session.add(idempotency)

        try:
            session.flush() 
        except Exception:
            session.rollback()
            raise HTTPException(status_code=409, detail="Transaction key or concurrency error")

        sender = (session.query(User)
                             .filter(User.account == body.sender_account)
                             .first())
        
        beneficiary = (session.query(User)
                             .filter(User.account == body.beneficiary_account)
                             .first())
        
        if not sender or not beneficiary:
            session.rollback()
            raise HTTPException(status_code=400, detail="Sender or beneficiary account doesnt exists")
        
        if sender.account == beneficiary.account:
            raise HTTPException(status_code=400, detail="Sender and beneficiary accont cant be the same")
        
        if user.account != body.sender_account:
            raise HTTPException(status_code=403, detail="Acess denied to this operation")

        try:
            sender.debit(body.amount)
            beneficiary.credit(body.amount)
            transaction = Transaction(
                amount = body.amount,
                sender_account_number = body.sender_account,
                beneficiary_account_number = body.beneficiary_account,
                idempotency_key = transaction_key
            )
            session.add(transaction)
            session.flush()

            response = CreateTransactionResponseSchema(
                id = transaction.id,
                status = "success",
                amount = body.amount,
                created_at = transaction.created_at
            )

            idempotency.status = "completed"
            idempotency.response_code = 200
            idempotency.response_body = response.model_dump(mode="json")

            session.commit()
            return response
        except ValueError as exc:
            session.rollback()
            raise HTTPException(status_code=400, detail=str(exc))
        except Exception as exc:
            session.rollback()
            raise HTTPException(status_code=500, detail=str(exc))

    def list_transactions(range: int, account: str, page: int, session: Session, user: User):
        if user.account != account:
            raise HTTPException(status_code=403, detail="You can see your transactions only")
        
        ranges = [30, 60, 90]
        if not range in ranges:
            raise HTTPException(status_code=400, detail="Invalid range. Only 30, 60 or 90 days")
        
        date_limit = datetime.now() - timedelta(days=range)

        if page < 1:
            raise HTTPException(status_code=400, detail="Page must be >= 1")
        
        items_per_page = 15

        base_query = (
            session.query(Transaction)
            .filter((
                (Transaction.beneficiary_account_number == account) | 
                (Transaction.sender_account_number == account)
                &
                (Transaction.created_at >= date_limit)
                )))

        total = base_query.count()
        offset = (page - 1) * items_per_page
        transactions = (
            base_query.order_by(Transaction.created_at.desc())
            .offset(offset)
            .limit(items_per_page)
            .all())
            
        return {
            "data": transactions,
            "page": page,
            "total_pages": (total + items_per_page - 1) // items_per_page,
            "range_days": range
        }
    
    def credit(amount: float, account: str, session: Session, user: User):
        exist_user = session.query(User).filter(User.account == account).first()
        if not exist_user:
            raise HTTPException(status_code = 404, detail="User account not found")
        
        if user.account != account:
            raise HTTPException(status_code=403, detail="You can credit your account only")
        try:
            exist_user.credit(amount)
            exist_user.updated_at = datetime.now()
            session.commit()
            return exist_user
        except ValueError as exc:
            raise HTTPException(status_code = 400, detail=str(exc))
        except Exception as exc:
            raise HTTPException(status_code = 500, detail="Internal server error")

