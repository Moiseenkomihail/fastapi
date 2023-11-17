from typing import Optional
from app.database.DBmodel import Base

from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__='users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True,)
    # mail: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)

    
    
