from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_session
from app.models.users import User
from app.schemas.user import UserCreate
from app.services.auth import user_by_name
from app.services.registrate import create_new_user
from app.services.security import get_password_hash


reg_router = APIRouter(tags=['Reg'], prefix='/registrate')

@reg_router.post(
    '/'
)
async def create_user(
    user_model: UserCreate,
    session: AsyncSession = Depends(get_session),
    ):

    if await user_by_name(session=session, username=user_model.username):
        raise HTTPException(
            status_code=400,
            detail="there is already a user with the same name"
        )
    
    result = await create_new_user(user_in= user_model, session= session)

    return result