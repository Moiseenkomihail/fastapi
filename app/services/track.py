from typing import Any, Iterator, Sequence
from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.track import Track

from app.schemas.track import TrackCreate


async def create_new_track(session: AsyncSession, track_in: TrackCreate, user_id: int):

    try:
        track = Track(**track_in.model_dump())
        track.user_id = user_id
        session.add(track)
        await session.commit()
        await session.refresh(track)
        return status.HTTP_201_CREATED
    
    except:
        raise HTTPException(
            status_code=400,
            detail='cant to create track'
        )

async def get_tracks(session: AsyncSession, user_id: int, track_name: str):

    query = select(Track).where(Track.user_id == user_id, Track.name == track_name)

    try:
        print('1')
        res = await session.execute(query)
        await session.commit()
        track = res.fetchone()
        if track:
            return track[0]
    
    except:
        raise HTTPException(
            status_code=400,
            detail='cant to execute track'
        )

