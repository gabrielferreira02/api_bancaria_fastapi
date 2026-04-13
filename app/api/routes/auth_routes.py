from fastapi import APIRouter, Depends
from app.schemas.auth_schemas import RegisterSchema
from app.schemas.user_schemas import UserResponseSchema
from app.services.auth_service import AuthService
from sqlalchemy.orm import Session
from app.api.deps import get_session

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@auth_router.post("/register", response_model=UserResponseSchema, status_code=201)
async def register(body: RegisterSchema, session: Session = Depends(get_session)):
    return AuthService.register(body, session)