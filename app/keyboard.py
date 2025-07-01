from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder


add_agree = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅ Подтвердить', callback_data="Agree"),
     InlineKeyboardButton(text='❌ Отменить', callback_data="Disagree")]
])


async def reminders_keyboard(reminders):
    # reminders — список объектов или словарей с id и текстом
    keyboard = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(text=remind.text[:30], callback_data=f"reminder_{remind.id}")
        for remind in reminders if remind.status=='active'
    ]
    keyboard.add(*buttons)
    return keyboard.adjust(2).as_markup()