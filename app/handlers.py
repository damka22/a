from sqlalchemy.ext.asyncio import AsyncSession

from aiogram.types import Message, FSInputFile
from aiogram import Router, F
from aiogram.filters import CommandStart, Command, StateFilter
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
    reminders = await orm_get_reminds(session)
    await message.answer("меню", reply_markup=kb.reminders_keyboard(reminders))





@router_handlers.message(Command("remind"))
async def add_remind(message: Message, state: FSMContext):
    await state.set_state(Remind.text)
    await message.answer("Что мне напомнить?")


@router_handlers.message(StateFilter("*"), F.text.casefold() == "отмена")
async def cancel_handler(message: Message, state: FSMContext, session: AsyncSession) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    if Remind.remind_for_change:
        Remind.remind_for_change = None
    await state.clear()
    await message.answer("Действия отменены", reply_markup=kb.reminders_keyboard(await orm_get_reminds(session)))


@router_handlers.message(Remind.text)
async def first_process_text(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    await state.set_state(Remind.time)
    await message.answer("Через сколько минут напомнить?")

@router_handlers.message(Remind.time)
async def second_process_time(message: Message, state: FSMContext):
    try:
        delta_minutes = int(message.text)

        if delta_minutes < 1 or delta_minutes > 1440:
            await message.reply("Время должно быть не меньше 1 и не больше 1440 минут.")
            return

        await state.update_data(time=message.text)
        data = await state.get_data()
        wait_time = int(data['time'])
        text = data['text']
        await message.answer(f"Создать напоминание <{text}> через {wait_time} минут?", reply_markup=kb.add_agree)

    except ValueError:
        await message.reply("Введите целое число минут.")
    except Exception as e:
        await message.reply("Произошла ошибка, попробуйте ещё раз.")



