from aiogram.types import (reply_keyboard_markup, keyboard_button,
                           inline_keyboard_markup, inline_keyboard_button, InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder


add_agree = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅ Подтвердить', callback_data="Agree"),
     InlineKeyboardButton(text='❌ Отменить', callback_data="Disagree")]
])


# async def inline_menu(tasks):
#
#     keyboard = InlineKeyboardBuilder()
#     for task in tasks:
#         keyboard.add(InlineKeyboardButton(text=task, callback_data="task from bd"))
#     return keyboard.adjust(2).as_markup()