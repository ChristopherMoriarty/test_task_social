from fastapi import FastAPI

from auth.service import auth_backend, fastapi_users
from auth.schemas import UserRead, UserCreate

from posts.router import router as post_router
from analitics.router import router as analitics_router


app = FastAPI(
    title="Social_test_task",
    version="1.0",
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/api/v1.0/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/api/v1.0/auth",
    tags=["Auth"],
)

app.include_router(
    post_router,
    prefix="/api/v1.0/posts",
    tags=["Post"]
)

app.include_router(
    analitics_router,
    prefix="/api/v1.0/analistics",
    tags=["Analistics"]
)