from fastapi import FastAPI

app = FastAPI()

from app.api.routes.auth_routes import auth_router
from app.api.routes.transaction_routes import transaction_router
from app.api.routes.account_routes import account_router

app.include_router(auth_router)
app.include_router(transaction_router)
app.include_router(account_router)