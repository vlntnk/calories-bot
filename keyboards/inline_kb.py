from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_answer import CallbackAnswer

class Inline():
    afresh = 'Начать заново'
    carry_on = 'Продолжить'
    delete = 'Удалить информацию'

def user_exists_inline():
    first_exists = InlineKeyboardButton(text=Inline.afresh, callback_data=Inline.afresh)
    second_exists = InlineKeyboardButton(text=Inline.carry_on, callback_data=Inline.carry_on)
    third_exists = InlineKeyboardButton(text=Inline.delete, callback_data=Inline.delete)
    markup = InlineKeyboardMarkup(inline_keyboard=[[first_exists], [second_exists], [third_exists]])
    return markup