from pydantic import BaseModel

from typing import Optional

class TrackBase(BaseModel):
    name: str 

class TrackCreate(TrackBase):
    description: str