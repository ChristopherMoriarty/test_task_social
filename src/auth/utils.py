from datetime import datetime
from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound

from auth.models import User
from database import get_async_session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def update_last_action(user_id: int, session: AsyncSession):
    stmt = update(User).where(User.id == user_id).values(last_action=datetime.utcnow())
    updated_last_request = await session.execute(stmt)

    if updated_last_request is None:
        raise NoResultFound
