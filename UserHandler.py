from aiogram import F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types.message import Message

from config import router1, router2
from States import *

@router1.message(CommandStart())
async def start1(message: Message, state: FSMContext):
    print(1)
    await state.set_state(User.menu)


@router2.message(F.text,User.menu)
async def start2(message: Message, state: FSMContext):
    print(2)