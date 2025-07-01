from sqlalchemy.ext.asyncio import AsyncSession

from aiogram.types import Message, FSInputFile
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database.orm_query import orm_get_reminds
import app.keyboard as kb

router_handlers = Router()

class Remind(StatesGroup):
    text = State()
    time = State()


@router_handlers.message(CommandStart())
async def start(message: Message):
    await message.reply("Привет!")


@router_handlers.message(Command("help"))
async def help_msg(message: Message):
    photo = FSInputFile("pictures/help_tyan.jpg")
    await message.answer_photo(photo=photo, caption="ステップ左、ステップ右-2ステップ")


@router_handlers.message(Command("menu"))
async def menu(message: Message, session: AsyncSession):
    #вывод всех напоминаний
    s = 'меню:\n'
    for task in await orm_get_reminds(session):
        if task.status == 'active':
            s = s + f"{task.text} — {task.end_time}\n"
    await message.answer(s)









@router_handlers.message(Command("remind"))
async def add_remind(message: Message, state: FSMContext):
    await state.set_state(Remind.text)
    await message.answer("Что мне напомнить?")

@router_handlers.message(Remind.text)
async def first_process_text(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    await state.set_state(Remind.time)
    await message.answer("Через сколько минут напомнить?")

@router_handlers.message(Remind.time)
async def second_process_time(message: Message, state: FSMContext):
    try:
        await state.update_data(time=message.text)
        data = await state.get_data()
        wait_time = int(data['time'])
        text = data['text']
        await message.answer(f"Создать напоминание <{text}> через {wait_time} минут?", reply_markup=kb.add_agree)
    except ValueError:
        await message.answer("Введи число")




