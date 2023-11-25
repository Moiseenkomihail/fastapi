from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_session
from app.services.auth import user_by_name
from app.services.jwt import create_access_token
from app.services.security import verify_password
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES

auth_router = APIRouter()

@auth_router.post(
    '/'
)
async def auth_user(
    auth_model: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    user = await user_by_name(session=session, username=auth_model.username)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username",
        )
    
    if  not verify_password(plain_password=auth_model.password, hashed_password=user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={'user_id': user.id}, expires_delta=access_token_expires
        )
    
    return {'access_token': access_token, 'token_type': 'bearer'}


