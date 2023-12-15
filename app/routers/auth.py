from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_session
from app.services.auth import user_by_email, user_by_name
from app.services.jwt import create_access_token, create_refresh_token, get_current_userid
from app.services.security import verify_password
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES

auth_router = APIRouter()

@auth_router.post(
    '/'
)
async def auth_user(
    auth_model: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    user = await user_by_name(session=session, username=auth_model.username)

    if not user:
        user = await user_by_email(session=session, user_email=auth_model.username)

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

    access_token_expires = timedelta(minutes=1)
    access_token = await create_access_token(
        data={'user_id': user.id}, expires_delta=access_token_expires
        )
    
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = await create_refresh_token(
        data={'user_id': user.id, 'type': 'refresh'}, expires_delta=refresh_token_expires
    )

    response = JSONResponse({"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"})
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)

    return response


@auth_router.post('/refreshtoken')
async def chech_refreshtoken(request: Request):
    refreshtoken = request.cookies.get('refresh_token')
    user_id = await get_current_userid(token=refreshtoken)

    if user_id:
        access_token_expires = timedelta(minutes=1)
        access_token = await create_access_token(
            data={'user_id': user_id}, expires_delta=access_token_expires
            )
    
    return access_token



