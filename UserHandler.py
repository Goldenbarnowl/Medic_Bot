from aiogram import F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types.message import Message


from config import router, bot, dp
from States import *


@router.message()
async def start1(message: Message, state: FSMContext):
    print(message)
