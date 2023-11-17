from typing import Optional

from sqlalchemy import ForeignKey
from app.database.DBmodel import Base

from sqlalchemy.orm import Mapped, mapped_column

class Tracker(Base):
    __tablename__ = 'tracks'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    total_time: Mapped[int] = mapped_column()

    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id')
    )