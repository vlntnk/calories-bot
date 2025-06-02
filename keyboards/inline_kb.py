from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_answer import CallbackAnswer

class Inline():
    afresh = 'Начать заново'
    carry_on = 'Продолжить'
    delete = 'Удалить информацию'
    add = 'Добавить съеденное сегодня блюдо'
    show_todays = 'Прогресс за сегодня'
    show_statistics = 'Статистика'
    show_menu = 'Меню блюд'
    add_dish = 'Добавить новое блюдо'
    limits = 'Показать мою норму'

class Data():
    add_meal = 'add_meal'
    show_todays = 'today_progress'
    show_statistics = 'statistics'
    show_menu = 'menu'
    add_dish = 'add_dish'
    get_meal = 'get_meal'
    show_limits = 'show_limits'


def user_exists_inline():
    first_exists = InlineKeyboardButton(text=Inline.afresh, callback_data=Inline.afresh)
    second_exists = InlineKeyboardButton(text=Inline.carry_on, callback_data=Inline.carry_on)
    third_exists = InlineKeyboardButton(text=Inline.delete, callback_data=Inline.delete)
    markup = InlineKeyboardMarkup(inline_keyboard=[[first_exists], [second_exists], [third_exists]])
    return markup

def main_inline():
    first = [InlineKeyboardButton(text=Inline.add, callback_data=Data.add_meal)]
    second = [InlineKeyboardButton(text=Inline.show_todays, callback_data=Data.show_todays), 
              InlineKeyboardButton(text=Inline.show_statistics, callback_data=Data.show_statistics)]
    third = [InlineKeyboardButton(text=Inline.add_dish, callback_data=Data.add_dish)]
    fourth = [InlineKeyboardButton(text=Inline.limits, callback_data=Data.show_limits)]
    markup = InlineKeyboardMarkup(inline_keyboard=[first, second, third, fourth])
    return markup

def menu_inline(result: list):
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=meal[1][0], callback_data=Data.get_meal+meal[1][0])] for meal in enumerate(result)])
    return markup