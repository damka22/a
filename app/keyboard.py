from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder


add_agree = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅ Подтвердить', callback_data="Agree"),
     InlineKeyboardButton(text='❌ Отменить', callback_data="Disagree")]
])


def reminders_keyboard(reminders):
    keyboard = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(text=remind.text[:30], callback_data=f"remind_{remind.id}")
        for remind in reminders if remind.status=='active'
    ]
    keyboard.add(*buttons)
    return keyboard.adjust(2).as_markup()


def create_remind_keyboard(remind):
    remind_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='◀️ Назад', callback_data="back_to_menu"),
         InlineKeyboardButton(text='❌ Удалить', callback_data=f"delete_{remind.id}")],
    ])
    return remind_keyboard