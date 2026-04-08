from fastapi import APIRouter, Depends
from app.schemas.auth_schemas import RegisterSchema, RegisterResponseSchema
from app.services.auth_service import AuthService
from sqlalchemy.orm import Session
from app.api.deps import get_session

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@auth_router.post("/register", response_model=RegisterResponseSchema, status_code=201)
async def register(body: RegisterSchema, session: Session = Depends(get_session)):
    return AuthService.register(body, session)