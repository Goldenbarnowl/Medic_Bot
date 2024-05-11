from os import getenv

from aiogram import Bot, Dispatcher, Router
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv


# Загрузка переменных среды.
load_dotenv()

"""
Короче, роутер это такая штука...
Он работает как dp, только хенделы диспатчера выполняются в первую очередь, 
а потом уже выполняются все остальные роутеры в порядке их инициализации!!!
"""
router1 = Router()
router2 = Router()
async def main():
    bot = Bot(token=getenv("TOKEN"), parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router1)
    dp.include_router(router2)

    await dp.start_polling(bot)
