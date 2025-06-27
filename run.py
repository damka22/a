import os
from dotenv import find_dotenv, load_dotenv
import logging

import asyncio

from aiogram import Dispatcher, Bot, types

from app.handlers import router
from common.bot_cmd_list import private_chat

load_dotenv(find_dotenv())
bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()


async def main():
    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private_chat, scope=types.BotCommandScopeAllPrivateChats())

    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try: asyncio.run(main())
    except KeyboardInterrupt: print('Exit')