from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,update

from app.models.track import Track

from app.schemas.track import TrackCreate


async def create_new_track(session: AsyncSession, track_in: TrackCreate, user_id: int):

    try:
        track = Track(**track_in.model_dump())
        track.user_id = user_id
        session.add(track)
        await session.commit()
        await session.refresh(track)
        return track
    
    except:
        raise HTTPException(
            status_code=400,
            detail='cant to create track'
        )

async def get_track(session: AsyncSession, user_id: int, track_name: str):

    query = select(Track).where(Track.user_id == user_id, Track.name == track_name, Track.is_active == True)

    try:
        res = await session.execute(query)
        await session.commit()
        track = res.fetchone()
        if track:
            return track[0]
    
    except:
        raise HTTPException(
            status_code=400,
            detail='server erorr'
        )
    
async def get_tracks(session: AsyncSession, user_id: int):

    query = select(Track).where(Track.user_id == user_id, Track.is_active == True)

    try:
        res = await session.execute(query)
        await session.commit()
        tracks = res.scalars().all()
        print(tracks)
        return tracks
    
    except:
        raise HTTPException(
            status_code=400,
            detail='server erorr'
        )
    

async def add_time_to_track(session: AsyncSession, track_id:int, time:int, user_id):
    
    query = select(Track).where(Track.user_id == user_id, Track.id == track_id, Track.is_active == True)

    try:
        res = await session.execute(query)
        track = res.scalar_one()
        track.total_time = track.total_time + time
        resp = track.__dict__
        await session.commit()
        return resp
    except: 
        raise HTTPException(
            status_code=400,
            detail='server erorr'
       )
    
async def disable_track(session: AsyncSession, track_id:int, user_id):
    
    query = select(Track).where(Track.user_id == user_id, Track.id == track_id, Track.is_active == True)

    try:
        res = await session.execute(query)
        track = res.scalar_one()
        track.is_active = False
        await session.commit()
        return status.HTTP_200_OK
    except: 
        raise HTTPException(
            status_code=400,
            detail='server erorr'
       )