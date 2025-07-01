import asyncio
from datetime import datetime, timezone, timedelta
from sqlalchemy import select
from database.engine import session_maker
from database.models import Remind

async def reminder_scheduler(bot):
    while True:
        async with session_maker() as session:
            now = datetime.now(timezone(timedelta(hours=5)))
            result = await session.execute(
                select(Remind).where(Remind.remind_at <= now, Remind.status == "active")
            )
            reminders = result.scalars().all()

            for remind in reminders:
                try:
                    await bot.send_message(chat_id=remind.tg_id, text=f"⏰ Напоминание: {remind.text}")
                    remind.status = "done"
                except:
                    ...
            await session.commit()

        await asyncio.sleep(5)  # Проверка каждые 5 секунд
