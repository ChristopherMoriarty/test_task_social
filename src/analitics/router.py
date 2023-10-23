from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session

from auth.models import User
from auth.service import current_user

from analitics.utils import get_likes_analitics, get_user

from exceptions import basic_exception

router = APIRouter()


@router.get("/me", response_model=dict)
async def current_user_activity(
    user: User = Depends(current_user)
):
    try:
        return {
                "status": "success",
                    "data": (
                        f"username: {user.username}",
                        f"last_login: {user.last_login}",
                        f"last_action: {user.last_action}",
                    ),
                    "detail": None,
            }
    except Exception:
        await basic_exception(status_code=500, message="Error while get analistics")
        


@router.get("/{user_id}", response_model=dict)
async def user_activity(
    user_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    try:
        status_code=500
        message="Error while get analistics"
        user = await get_user(session=session, user_id=user_id)
        
        
        if user is None:
            status_code=404
            message="User is not exist"
            raise Exception
        
        session.commit()
        
        return {
                "status": "success",
                    "data": (
                        f"username: {user.username}",
                        f"last_login: {user.last_login}",
                        f"last_action: {user.last_action}",
                    ),
                    "detail": None,
            }
    except Exception:
        await session.rollback()
        await basic_exception(status_code=status_code, message=message)


@router.get("/", response_model=dict)
async def likes_by_period(
        session: AsyncSession = Depends(get_async_session),
        date_from: date = Query(),
        date_to: date = Query()
):
    try:
        status_code = 500
        message = "error while get like analistics"
        
        if date_to < date_from:
            status_code = 400
            message = "date_to should be greater than or equal to date_from"
            raise Exception
            
        
        analistics = await get_likes_analitics(
            date_from=date_from, date_to=date_to, session=session
        )
        await session.commit()
        
        return {
                "status": "success",
                    "data": analistics,
                    "detail": None,
            }
    
    except Exception:
        await session.rollback()
        await basic_exception(status_code=status_code, message=message)