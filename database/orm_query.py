from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Remind


async def orm_add_remind(session: AsyncSession, data: dict, tg_id: int):
    obj = Remind(
        tg_id=int(tg_id),
        text=data['text'],
        time=int(data['time']),
        end_time=str(data['end_time']),
        remind_at=data['remind_at'],
    )
    session.add(obj)
    await session.commit()
    return obj.id


async def orm_get_reminds(session: AsyncSession):
    query = select(Remind)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_delete_remind(session: AsyncSession, remind_id: int, tg_id: int):
    query = delete(Remind).where(Remind.id == remind_id, Remind.tg_id==tg_id)
    await session.execute(query)
    await session.commit()

