from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_session
from app.services.auth import user_by_name
from app.services.jwt import create_access_token
from app.services.security import verify_password
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES

auth_router = APIRouter(tags=['Auth'], prefix='/login')

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
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if  not verify_password(plain_password=auth_model.password, hashed_password=user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={'id': user.id}, expires_delta=access_token_expires)
    
    return {'acces_token': access_token, 'token_type': 'bearer'}