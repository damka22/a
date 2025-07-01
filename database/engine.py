import os
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import delete

from database.models import Remind


engine = create_async_engine(os.getenv('DB_LITE'))
#engine = create_async_engine(os.getenv('DB_LITE'), echo=True)
session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)



async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Remind.metadata.create_all)


async def drop_db():
    async with session_maker() as session:
        await session.execute(delete(Remind))  # удаляет все записи из таблицы
        await session.commit()