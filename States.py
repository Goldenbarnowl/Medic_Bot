from aiogram.fsm.state import State, StatesGroup
class User(StatesGroup):
    name_wait = State()
    menu = State()