import asyncio
import logging
from aiogram.fsm.context import FSMContext
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.chat_action import ChatActionMiddleware
import keyboards
import yes_no_fun

class SearchState(StatesGroup):
    vibor = State()

answer_lek = ""
in_user = {}
logging.basicConfig(level=logging.INFO)
bot = Bot(token='6482847951:AAEAgELCq4akgS3k6IQMZX5qNG6ySN43os0')
dp = Dispatcher()
storage = MemoryStorage()
dp.message.middleware(ChatActionMiddleware())
check1 = 0
check2 = 1
in_img = []
current_index = 0

@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("Добро пожаловать! Вас приветствует сервис по поиску лекарств в аптеке uteka.ru")
    await message.answer("Вот немного обо мне: я могу найти как лекарство по его названию, так и найти что-то, подходящее вашим симптомам. "
                         "К сожалению, я не умею осуществлять бронь напярмую, но я могу упростить вам поиск лекарств на сервисе uteka.ru и вывести краткую информацию о лекарствах, которые есть в наличии в аптеках города Омск")
    await message.answer("Если вы уже искали лекарства, можно не писать снова /start, достаточно отправить название лекарства или симптом в чат. Я тут же начну поиск по вашему запросу.")
    await message.answer("Чтобы я начал работу, подскажите, что вы ищите?")

@dp.message(StateFilter(None), F.text)
async def on_text_message(message: types.Message, state: FSMContext):
    await state.clear()
    await yes_no_fun.on_text_message(message, state)

@dp.message(lambda message: message.text == "Да", state )
async def yes(message: types.Message, state: FSMContext):
    data = await state.get_data()
    current_index = data.get("index", 0)
    if current_index >= len(in_user):
        await message.answer("Больше вариантов нет.")
        return
    if len(in_user) == 1:
        key = keys(in_user, current_index)
        value = in_user[key]
        image_url = in_img[current_index]  # URL-адрес изображения
        text = f"Вот например {key} по цене {value}"
        await bot.send_photo(chat_id=message.chat.id, photo=image_url, caption=text)
    else:
        check1 = data.get("check1", 0)
        check2 = data.get("check2", 1)
        if check1 == 0:
            key = keys(in_user, current_index)
            value = in_user[key]
            image_url = in_img[current_index]  # URL-адрес изображения
            text = f"Вот например {key} по цене {value}"
            await bot.send_photo(chat_id=message.chat.id, photo=image_url, caption=text)
            current_index += 1
        elif check1 == 1:
            if check2 == 1:
                current_index -= 2
                key = keys(in_user, current_index)
                value = in_user[key]
                image_url = in_img[current_index]  # URL-адрес изображения
                text = f"Вот например {key} по цене {value}"
                await bot.send_photo(chat_id=message.chat.id, photo=image_url, caption=text)
                await state.update_data(check2=0)
                await ask_for_more(message)
            else:
                current_index -= 1
                key = keys(in_user, current_index)
                value = in_user[key]
                image_url = in_img[current_index]  # URL-адрес изображения
                text = f"Вот например {key} по цене {value}"
                await bot.send_photo(chat_id=message.chat.id, photo=image_url, caption=text)
        await state.update_data(index=current_index)
    await ask_for_more(message)


@dp.message(lambda message: message.text == "Нет", SearchState.vibor)
async def no(message: types.Message, state: FSMContext):
    await message.answer("Мне жаль, что я не смог вам ничем помочь :(", reply_markup=types.ReplyKeyboardRemove())
    yes_no_fun.all_url.clear()
    clear_list()
    await state.clear()

async def ask_for_more(message: types.Message):
    if len(in_user) == 1:
        await message.answer("Это все варианты, которые я смог найти", reply_markup=keyboards.yes_no())
    else:
        await message.answer("Хотите увидеть ещё варианты?", reply_markup=keyboards.make_keyboard_ynb())

@dp.message(lambda message: message.text in {"Да", "Нет", "Назад", "Я определился на текущем", "Не то, что нужно", "Да, это то"}, SearchState.vibor)
async def handle_yes_no(message: types.Message, state: FSMContext):
    await yes_no_fun.yes_no_back(message,state)


def filter(key, value):
    in_user[key] = value
    return in_user

def clear_list():
    in_user.clear()
    in_img.clear()
def img(x):
    in_img.append(x)
async def main():
    await dp.start_polling(bot)
def start():
    return asyncio.run(main())
def keys(in_user, current_index):
    key = list(in_user.keys())
    return key[current_index]