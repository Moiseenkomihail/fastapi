from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.config import DATABASE_ECHO, DATABASE_URL


engine = create_async_engine(
            url=DATABASE_URL,
            echo=DATABASE_ECHO,
)

# async_session= async_sessionmaker(
#             bind=engine,
#             autoflush=False,
#             autocommit=False,
#             expire_on_commit=False,
# )

async_session = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )

async def get_session():
    session = async_session()
    try:
        yield session
    finally:
        await session.close()