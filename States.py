from aiogram.fsm.state import State, StatesGroup


class User(StatesGroup):
    wait_medical_name = State()