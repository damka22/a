import asyncio

from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import app.keyboard as kb

router = Router()

class Remind(StatesGroup):
    text = State()
    time = State()


@router.message(CommandStart())
async def start(message: Message):
    await message.reply("Привет!")


@router.message(Command("help"))
async def help_msg(message: Message):
    photo = FSInputFile("pictures/help_tyan.jpg")
    await message.answer_photo(photo=photo, caption="ステップ左、ステップ右-2ステップ")


@router.message(Command("menu"))
async def menu(message: Message):
    await message.answer('МЕНЮ', reply_markup=await kb.inline_menu())







@router.message(Command("remind"))
async def add_remind(message: Message, state: FSMContext):
    await state.set_state(Remind.text)
    await message.answer("Что мне напомнить?")

@router.message(Remind.text)
async def first_process_text(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    await state.set_state(Remind.time)
    await message.answer("Через сколько минут напомнить?")

@router.message(Remind.time)
async def second_process_time(message: Message, state: FSMContext):
    try:
        await state.update_data(time=message.text)
        data = await state.get_data()
        wait_time = int(data['time'])
        text = data['text']

        with open('test.txt', 'a+', encoding='utf-8') as f:
            f.write(f"{text}\n")

        await message.answer(f"Создать напоминание <{text}> через {wait_time} минут?", reply_markup=kb.add_agree)

    except ValueError:
        await message.answer("Введи число")



@router.callback_query(F.data == "Agree")
async def agree_add(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Подтверждено")

    data = await state.get_data()
    wait_time = data['time']
    text = data['text']
    await state.clear()

    await callback.message.edit_text(f"Ок! Напомню через {wait_time} минут.", reply_markup=None)
    await asyncio.sleep(wait_time * 60)
    await callback.message.answer(f"⏰ Напоминание: {text}", parse_mode="html")



@router.callback_query(F.data == "Disagree")
async def disagree_add(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    await callback.answer("Отмена")
    await callback.message.edit_text(f"Отменено", reply_markup=None)

