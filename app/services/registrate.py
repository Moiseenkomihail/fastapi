from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import User
from app.schemas.user import UserCreate
from app.services.security import get_password_hash

async def create_new_user(user_in: UserCreate, session: AsyncSession):
    
    hashpassword = get_password_hash(user_in.password)
    user_in.password = hashpassword

    try:
        user = User(**user_in.model_dump())
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return status.HTTP_201_CREATED
    
    except:
        raise HTTPException(
            status_code=400,
            detail='server error'
        )
