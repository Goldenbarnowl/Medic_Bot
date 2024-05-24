from aiogram.types import InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder


def webapp_maker(url):
    medical_carousel_keyboard = InlineKeyboardBuilder()
    medical_carousel_keyboard_buttons = {'left': '⬅️', 'right': '➡️', 'go': '⏺', 'back': '↩️Назад'}
    left_button = InlineKeyboardButton(text=medical_carousel_keyboard_buttons['left'], callback_data="left")
    go_url_button = InlineKeyboardButton(text=medical_carousel_keyboard_buttons['go'], web_app=WebAppInfo(url=url))
    right_button = InlineKeyboardButton(text=medical_carousel_keyboard_buttons['right'], callback_data="right")
    back_button = InlineKeyboardButton(text=medical_carousel_keyboard_buttons['back'], callback_data="back")
    medical_carousel_keyboard.row(left_button, go_url_button, right_button)
    medical_carousel_keyboard.row(back_button)
    return medical_carousel_keyboard.as_markup()
