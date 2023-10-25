from typing import Optional
from datetime import datetime

from fastapi import Depends, Request, Response
from fastapi_users import BaseUserManager, IntegerIDMixin

from auth.models import User
from auth.utils import get_user_db

from config import SECRET_AUTH


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET_AUTH
    verification_token_secret = SECRET_AUTH

    async def on_after_login(
        self,
        user: User,
        request: Optional[Request] = None,
        response: Optional[Response] = None,
    ):
        user = await self.user_db.get(user.id)
        if user:
            user.last_login = datetime.utcnow()
            await self.user_db.update(user, {"last_login": user.last_login})


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)