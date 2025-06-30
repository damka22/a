import os

from aiogram.enums import ParseMode
from dotenv import find_dotenv, load_dotenv

from middlewares.db import DataBaseSession

load_dotenv(find_dotenv())

from database.engine import create_db, session_maker, drop_db

import logging

import asyncio

from aiogram import Dispatcher, Bot, types
from aiogram.filters import Command

from app.handlers import router_handlers
from app.callbacks import router_callbacks
from common.bot_cmd_list import private_chat


bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()
dp.include_router(router_handlers)
dp.include_router(router_callbacks)

@dp.message(Command("clear"))
async def clear_bd(message: types.Message):
    await drop_db()
    await message.answer('—————\nбд очищена\n—————')

async def main():
    await create_db()

    dp.update.middleware(DataBaseSession(session_pool=session_maker))

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private_chat, scope=types.BotCommandScopeAllPrivateChats())

    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try: asyncio.run(main())
    except KeyboardInterrupt: print('Exit')