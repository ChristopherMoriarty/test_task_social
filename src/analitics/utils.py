from datetime import date, timedelta

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from posts.models import Like

async def get_user(
    session: AsyncSession,
    user_id: int
) -> User:
    stmt = select(User).filter_by(id=user_id)
    user_db = await session.execute(stmt)
    user_db = user_db.scalars().first()
    
    if user_db is not None:
        return user_db

async def get_likes_analitics(
        session: AsyncSession, 
        date_from: date, 
        date_to: date
) -> dict:
    stmt = select(
            func.date(Like.created_at),
            func.count(Like.id),
        ).filter(
            Like.created_at.between(
                date_from, date_to + timedelta(days=1)
            )
        ).group_by(
            func.date(Like.created_at)
        )
    
    like_db = await session.execute(stmt)
    
    like_db = {date: likes for date, likes in like_db.all()}
    
    return like_db