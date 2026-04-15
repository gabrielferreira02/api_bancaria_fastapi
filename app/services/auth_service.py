from app.schemas.auth_schemas import RegisterSchema, LoginRequestSchema, LoginResponseSchema
from fastapi import HTTPException
from app.models.user import User
from app.helpers.generate_account_number import generate_account_number
from app.helpers.generate_token import generate_token
from sqlalchemy.orm import Session
from app.core.security import pwd_context
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm

class AuthService:
    def register(body: RegisterSchema, session: Session):
        if not body.cpf:
            raise HTTPException(status_code=400, detail="CPF field required")
        if not body.first_name:
            raise HTTPException(status_code=400, detail="Invalid first name")
        if not body.last_name:
            raise HTTPException(status_code=400, detail="Invalid last name")
        if not body.email:
            raise HTTPException(status_code=400, detail="Invalid email")
        if not body.password or len(body.password) != 4 or not body.password.isdecimal():
            raise HTTPException(status_code=400, detail="Invalid password. It Should contain 4 numbers only")
        
        try:
            user = User(
                first_name = body.first_name,
                last_name = body.last_name,
                cpf = body.cpf,
                password = pwd_context.hash(body.password),
                email = body.email,
                account = generate_account_number(),
            )
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc))

        session.add(user)
        session.commit()
        session.flush()

        return user
    
    def login(body: LoginRequestSchema, session: Session):
        if not body.account or not body.password:
            raise HTTPException(status_code=400, detail="Invalid account number or password")
        
        user = session.query(User).filter(User.account == body.account).first()

        if not user:
            raise HTTPException(status_code=404, detail="Account number not found")
        
        if not pwd_context.verify(body.password, user.password):
            raise HTTPException(status_code=400, detail="Invalid password")

        token = generate_token(user.account)
        refresh_token = generate_token(user.account, timedelta(days=7))

        return LoginResponseSchema(
            access_token=token, 
            refresh_token=refresh_token, 
            token_type="bearer")
    
    def refresh_token(user: User):
        token = generate_token(user.account)
        refresh_token = generate_token(user.account, timedelta(days=7))

        return LoginResponseSchema(
            access_token=token, 
            refresh_token=refresh_token, 
            token_type="bearer")
    
    def login_docs(body: OAuth2PasswordRequestForm, session: Session):
        if not body.username or not body.password:
            raise HTTPException(status_code=400, detail="Invalid account number or password")
        
        user = session.query(User).filter(User.account == body.username).first()

        if not user:
            raise HTTPException(status_code=404, detail="Account number not found")
        
        if not pwd_context.verify(body.password, user.password):
            raise HTTPException(status_code=400, detail="Invalid password")

        token = generate_token(user.account)
        refresh_token = generate_token(user.account, timedelta(days=7))

        return LoginResponseSchema(
            access_token=token, 
            refresh_token=refresh_token, 
            token_type="bearer")