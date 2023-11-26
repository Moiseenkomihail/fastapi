from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_session
from app.schemas.track import TrackCreate
from app.services.track import create_new_track, get_track, get_tracks, add_time_to_track
from app.services.jwt import get_current_user, get_current_userid

track_router = APIRouter(tags =['Tracks'], prefix='/track')


@track_router.post(
    '/'
)
async def create_track(
    track_model: TrackCreate,
    user_id= Depends(get_current_userid),
    session: AsyncSession = Depends(get_session),
):

    if await get_track(session=session, user_id=int(user_id) , track_name=track_model.name):
        raise HTTPException(
            status_code=400,
            detail="there is already a track with the same name"
        )
    
    res = await create_new_track(session=session, track_in=track_model, user_id=int(user_id))

    return res

@track_router.get(
    '/get_user_tracks'
)
async def get_user_tracks(
    user_id= Depends(get_current_userid),
    session: AsyncSession = Depends(get_session),

):
    res = await get_tracks(session=session, user_id=user_id)
    return res


@track_router.put(
    '/'
)
async def add_time(
    track_id: int,
    time: int,
    session: AsyncSession = Depends(get_session),
    user_id= Depends(get_current_userid),
):
    
    return await add_time_to_track(track_id=track_id, time=time,session=session, user_id=user_id)