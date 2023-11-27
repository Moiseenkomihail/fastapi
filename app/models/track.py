from typing import Optional

from sqlalchemy import ForeignKey
from app.database.DBmodel import Base

from sqlalchemy.orm import Mapped, mapped_column

class Track(Base):
    __tablename__ = 'tracks'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    total_time: Mapped[int] = mapped_column(default= 0)
    is_active: Mapped[bool] = mapped_column(default= True, nullable=False)

    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id')
    )