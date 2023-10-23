from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session

from auth.models import User
from auth.service import current_user
from auth.utils import update_last_action

from posts.schemas import PostCreate, PostRead
from posts.utils import create_user_post, get_user_post, like_post, get_user_like, unlike_post
from exceptions import basic_exception

router = APIRouter()


@router.post("/me", response_model=dict)
async def create_post(
    post: PostCreate, 
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
    ):
    
    try:  
        db_post = await create_user_post(post=post, session=session, user_id=user.id)
        await update_last_action(user_id=user.id, session=session)
        await session.commit()
        
        return {
            "status": "success",
                "data": PostRead(
                    id=db_post.id, 
                    title=db_post.title, 
                    content=db_post.content, 
                    author_id=db_post.author_id
                ).dict(),
                "detail": None,
        }
    except Exception:
        await session.rollback()
        await basic_exception(status_code=500, message="Error while creating post")


@router.post("/{post_id}/like/", response_model=dict)
async def make_like(
    post_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    
    try:
        status_code=500
        message="Error while creating like"
        
        post = await get_user_post(session=session, post_id=post_id)
        
        if post is None:
            status_code=404
            message="Post not exist"
            raise Exception
            
        like = await get_user_like(session=session, post_id=post_id, user_id=user.id)
        
        if like is not None:
            status_code=200
            message="Like already exist"
            raise Exception
        
        await like_post(session=session, user_id=user.id, post_id=post_id)
        await update_last_action(user_id=user.id, session=session)
        await session.commit()
        
        return {
                "status": "success",
                    "data": f"liked post with id {post_id}",
                    "detail": None,
            }
    except Exception:
        await session.rollback()
        await basic_exception(status_code=status_code, message=message)


@router.delete("/{post_id}/unlike/", response_model=dict)
async def make_unlike(
    post_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    try:
        status_code = 500
        message="Error while deleting like"

        unlike = await unlike_post(session=session, user_id=user.id, post_id=post_id)
        await update_last_action(user_id=user.id, session=session)
        
        if len(unlike) == 0:
            status_code=200
            message= f"Post was never liked by {user.username}"
            raise Exception
            
        await session.commit()
        
        return {
                    "status": "success",
                        "data": f"Unliked post with id {post_id}",
                        "detail": None,
                }
    
    except Exception:
        await session.rollback()
        await basic_exception(status_code=status_code, message=message)
        
        
    
    