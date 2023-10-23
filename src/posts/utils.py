from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from posts.schemas import PostCreate

from models import Post, Like

async def get_user_post(
    session: AsyncSession,
    post_id: int
) -> Post:
    
    stmt = select(Post).filter_by(id=post_id)
    db_post = await session.execute(stmt)
    
    return db_post.scalars().first()

async def create_user_post(
        session: AsyncSession,
        post: PostCreate,
        user_id: int
) -> Post:
    
    db_post = Post(**post.dict(), author_id=user_id)
    session.add(db_post)
    
    return db_post

async def get_user_like(
    session: AsyncSession,
    post_id: int,
    user_id: int
) -> Like:
    
    stmt = select(Like).filter_by(post_id=post_id, user_id=user_id)
    db_like = await session.execute(stmt)
    
    return db_like.scalars().first()


async def like_post(
        session: AsyncSession,
        user_id: int,
        post_id: int
) -> None:
    
    stmt = insert(Like).values(post_id=post_id, user_id=user_id)
    await session.execute(stmt)
        
    
async def unlike_post(
    session: AsyncSession,
        user_id: int,
        post_id: int
) -> None:
    stmt = delete(Like).where(
            Like.post_id == post_id, 
            Like.user_id == user_id,
        ).returning(Like.id)
    del_like = await session.execute(stmt)
    
    return del_like.fetchall()
     