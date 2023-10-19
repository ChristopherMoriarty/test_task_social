from fastapi import FastAPI

from auth.service import auth_backend, fastapi_users
from auth.schemas import UserRead, UserCreate


app = FastAPI(
    title="Hypotron"
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth_doctor",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth_doctor",
    tags=["Auth"],
)