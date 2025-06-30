import asyncio
from sqlalchemy import select, delete

from aiogram.types import CallbackQuery
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_add_remind, orm_delete_remind, orm_check_remind

from datetime import datetime, timedelta, timezone

router_callbacks = Router()

mounths = {
    1: 'Января', 2: 'Февраля', 3: 'Марта', 4: 'Апреля',
    5: 'Мая', 6: 'Июня', 7: 'Июля', 8: 'Августа',
    9: 'Сентября', 10: 'Октября', 11: 'Ноября', 12: 'Декабря'
}

@router_callbacks.callback_query(F.data == "Agree")
async def agree_add(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    await callback.answer("Подтверждено")

    data = await state.get_data()
    wait_time = int(data['time'])
    text = data['text']
    end_time = datetime.now(timezone(timedelta(hours=5))) + timedelta(minutes=float(wait_time))
    end_time =f"{end_time.day} {mounths[end_time.month]} {end_time.strftime('%H:%M')}"
    data['end_time'] = end_time
    data['end_date'] = datetime.now()
    await state.clear()

    #запись в бд
    obj_id = await orm_add_remind(session, data, callback.message.from_user.id)


    await callback.message.edit_text(f"Ок! Напомню через {wait_time} минут.", reply_markup=None)
    await asyncio.sleep(wait_time * 60)
    # если за всё это время запись не удалилась из бд
    if await orm_check_remind(session, obj_id, callback.message.from_user.id):
        await callback.message.answer(f"⏰ Напоминание: {text}")

        #удаление истекшего напоминания из бд
        await orm_delete_remind(session, obj_id, callback.message.from_user.id)

@router_callbacks.callback_query(F.data == "Disagree")
async def disagree_add(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    await callback.answer("Отмена")
    await callback.message.edit_text(f"Отменено", reply_markup=None)

