from aiogram.types import CallbackQuery
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_add_remind, orm_get_remind, orm_get_reminds, orm_delete_remind

from app.keyboard import create_remind_keyboard, reminders_keyboard

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
    end_time = datetime.now(timezone(timedelta(hours=5))) + timedelta(minutes=float(wait_time))
    data['end_time'] = f"{end_time.day} {mounths[end_time.month]} {end_time.strftime('%H:%M')}"

    data['remind_at'] = datetime.now(timezone(timedelta(hours=5))) + timedelta(minutes=float(wait_time))
    await state.clear()

    #запись в бд
    await orm_add_remind(session, data, callback.from_user.id)
    await callback.message.edit_text(f"Ок! Напомню через {wait_time} минут.", reply_markup=None)

@router_callbacks.callback_query(F.data == "Disagree")
async def disagree_add(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    await callback.answer("Отмена")
    await callback.message.edit_text(f"Отменено", reply_markup=None)


@router_callbacks.callback_query(F.data.startswith("remind_"))
async def open_remind(callback: CallbackQuery, session: AsyncSession):
    await callback.answer(" ")
    ID_remind = int(callback.data.split("_")[-1])
    obj = await orm_get_remind(session, ID_remind, callback.from_user.id)
    remind_kb = create_remind_keyboard(obj)
    await callback.message.edit_text(f"{obj.text} — {obj.end_time}", reply_markup=remind_kb)

@router_callbacks.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery, session: AsyncSession):
    await callback.answer("меню")

    reminders = await orm_get_reminds(session)
    await callback.message.edit_text("меню", reply_markup=reminders_keyboard(reminders))


@router_callbacks.callback_query(F.data.startswith("delete_"))
async def change_remind(callback: CallbackQuery, session: AsyncSession):
    await callback.answer()
    ID_remind = int(callback.data.split("_")[-1])

    await orm_delete_remind(session, ID_remind, callback.from_user.id)
    
    reminders = await orm_get_reminds(session)
    await callback.message.edit_text("меню", reply_markup=reminders_keyboard(reminders))



