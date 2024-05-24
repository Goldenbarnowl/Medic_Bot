from aiogram import F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto
from aiogram.types.message import Message

from config import router, bot, dp
from Parser import parse
from States import *
from keyboards import webapp_maker
from chat_history_cleaner import chat_history_cleaner


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    chat_id = message.chat.id
    message_id = await bot.send_message(chat_id,
                                        "Добро пожаловать! Вас приветствует сервис по поиску лекарств в аптеке "
                                        "uteka.ru\n"
                                        "Пожалуйста введите название лекарства или симптом, и я найду нужный вам "
                                        "препарат!")
    await chat_history_cleaner(chat_id, message_id.message_id, state)
    await state.set_state(User.wait_medical_name)


@router.message(User.wait_medical_name)
async def medical_search(message: Message, state: FSMContext):
    array_of_drugs = parse(message.text)
    chat_id = message.chat.id
    if len(array_of_drugs) != 0:
        await state.update_data(array_of_drugs=array_of_drugs)
        await state.set_state(User.drugs_carousel)
        await drug_carousel_printer(array_of_drugs, message, state)
    else:
        message_id = await bot.send_message(chat_id, "К сожалению по вашему запросу ничего не найдено")
        await chat_history_cleaner(chat_id, message_id.message_id, state)
        await state.set_state(User.wait_medical_name)


async def drug_carousel_printer(array_of_drugs: list, message: Message, state: FSMContext):
    data = await state.get_data()
    chat_id = message.chat.id
    counter = data.get('counter')
    if counter is None:
        counter = 0
        await state.update_data(counter=counter)
    inline_murkup = webapp_maker(array_of_drugs[counter]['url'])
    await bot.send_photo(chat_id=chat_id,
                         photo=array_of_drugs[counter]['image_url'],
                         caption=f'{array_of_drugs[counter]["name"]}\nЦена: {array_of_drugs[counter]["cost"]}',
                         reply_markup=inline_murkup)


@dp.callback_query(User.drugs_carousel, F.data == 'left')
async def left(call: CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    data = await state.get_data()
    array_of_drugs = data.get('array_of_drugs')
    counter = data.get('counter') - 1
    if counter < 0:
        counter = len(array_of_drugs) - 1
    await state.update_data(counter=counter)
    media = InputMediaPhoto(media=array_of_drugs[counter]['image_url'],
                            caption=f'{array_of_drugs[counter]["name"]}\nЦена: {array_of_drugs[counter]["cost"]}')
    inline_murkup = webapp_maker(array_of_drugs[counter]['url'])
    await bot.edit_message_media(chat_id=chat_id,
                                 message_id=call.message.message_id,
                                 media=media,
                                 reply_markup=inline_murkup)


@dp.callback_query(User.drugs_carousel, F.data == 'right')
async def right(call: CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    data = await state.get_data()
    array_of_drugs = data.get('array_of_drugs')
    counter = data.get('counter') + 1
    if counter > len(array_of_drugs) - 1:
        counter = 0
    await state.update_data(counter=counter)
    media = InputMediaPhoto(media=array_of_drugs[counter]['image_url'],
                            caption=f'{array_of_drugs[counter]["name"]}\nЦена: {array_of_drugs[counter]["cost"]}')
    inline_murkup = webapp_maker(array_of_drugs[counter]['url'])
    await bot.edit_message_media(chat_id=chat_id,
                                 message_id=call.message.message_id,
                                 media=media,
                                 reply_markup=inline_murkup)


@dp.callback_query(User.drugs_carousel, F.data == 'back')
async def back(call: CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    await state.set_state(User.wait_medical_name)
    await state.update_data(counter=0)
    await bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
    message_id = await bot.send_message(chat_id,
                                        "Пожалуйста введите название лекарства или симптом, и я найду нужный вам препарат!")
    await chat_history_cleaner(chat_id, message_id.message_id, state)


@router.message()
async def Last_frontier(message: Message, state: FSMContext):
    chat_id = message.chat.id
    await state.update_data(counter=0)
    message_id = await bot.send_message(chat_id,
                                        "Пожалуйста введите название лекарства или симптом, и я найду нужный вам "
                                        "препарат!")
    await chat_history_cleaner(chat_id, message_id.message_id, state)
    await state.set_state(User.wait_medical_name)