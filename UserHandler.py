from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types.message import Message

from config import router1, router2


@router1.message(CommandStart())
async def start1(message: Message, state: FSMContext):
    print(1)

@router2.message(CommandStart())
async def start2(message: Message, state: FSMContext):
    print(2)