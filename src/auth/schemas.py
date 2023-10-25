from fastapi_users.schemas import BaseUser, BaseUserCreate


class UserRead(BaseUser[int]):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True


class UserCreate(BaseUserCreate):
    username: str
    email: str
    password: str
