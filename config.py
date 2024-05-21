from os import getenv

from aiogram import Bot, Dispatcher, Router
from aiogram.enums import ParseMode
from dotenv import load_dotenv

# Загрузка переменных среды.
load_dotenv()

router = Router()
bot = Bot(token=getenv("TOKEN"), parse_mode=ParseMode.HTML)
dp = Dispatcher()


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)
