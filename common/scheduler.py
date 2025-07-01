import asyncio
from datetime import datetime, timezone, timedelta
from sqlalchemy import select
from database.engine import session_maker
from database.models import Remind
from database.orm_query import orm_delete_remind

async def reminder_scheduler(bot):
    while True:
        async with session_maker() as session:
            now = datetime.now(timezone(timedelta(hours=5)))

            result = await session.execute(
                select(Remind).where(Remind.remind_at <= now, Remind.status == "active")
            )
            reminders = result.scalars().all()

            to_delete = await session.execute(
                select(Remind).where(Remind.remind_at <= now, Remind.status != "active")
            )
            to_delete = to_delete.scalars().all()

            for remind in reminders:
                try:
                    await bot.send_message(chat_id=remind.tg_id, text=f"⏰ Напоминание: {remind.text}")
                    remind.status = "done"
                except: ...

            for remind in to_delete:
                try:
                    await orm_delete_remind(session, remind.id, remind.tg_id)
                except: ...

            await session.commit()

        await asyncio.sleep(5)
