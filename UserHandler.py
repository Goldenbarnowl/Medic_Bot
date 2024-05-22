from aiogram import F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types.message import Message

from config import router, bot, dp
from Parser import parse, parse_errors
from States import *


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    chat_id = message.chat.id
    await bot.send_message(chat_id, "Добро пожаловать! Вас приветствует сервис по поиску лекарств в аптеке uteka.ru\n"
                                    "Пожалуйста введите название лекарства или симптом, и я найду нужный вам препарат!")
    await state.set_state(User.wait_medical_name)


@router.message(User.wait_medical_name)
async def medical_search(message: Message, state: FSMContext):
    print(parse_errors(message.text))
