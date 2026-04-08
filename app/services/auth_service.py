from app.schemas.auth_schemas import RegisterSchema
from fastapi import HTTPException
from app.models.user import User
from app.helpers.generate_account_number import generate_account_number
from sqlalchemy.orm import Session
from app.core.security import pwd_context

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