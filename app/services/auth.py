from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.users import User


async def user_by_name(session: AsyncSession, username: str):
    
    query = select(User).where(User.username == username)

    user = await session.execute(query)
    await session.commit()
    user_row = user.fetchone()
    if user_row:
        return user_row[0]
    







    