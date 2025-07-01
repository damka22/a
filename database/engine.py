import os
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import delete

from database.models import Remind

try:
    engine = create_async_engine(os.getenv('DB_LITE'))
    session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
except Exception as e:
    print(f"Ошибка при создании бд - {e}")

async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Remind.metadata.create_all)


async def drop_db():
    async with session_maker() as session:
        await session.execute(delete(Remind))  # удаляет все записи из таблицы
        await session.commit()