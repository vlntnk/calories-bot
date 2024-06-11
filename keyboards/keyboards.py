from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


class Buttons():
    calculate_button = 'Рассчитать план питания📊'
    set_plan_button = 'Установить собственный план🧮'
    lets_go_button = 'Давай!'
    male = 'Мужской'
    female = 'Женский'
    gain = 'Хочу набрать мышечную массу'
    lost = 'Надо похудеть к лету'
    keep_fit = 'Меня все устраивает!'
    sedentary = 'Малоподвижный, сидячий образ жизни'
    lightly = 'Иногда занимаюсь спортом'
    moderate = 'Занимаюсь дома регулярно'
    very = 'Хожу в зал 3+ раза в неделю'
    extra = 'Профессиональный спортсмен'

def start_keyboard():
    first_row = [KeyboardButton(text=Buttons.calculate_button)]
    second_row = [KeyboardButton(text=Buttons.set_plan_button)]
    markup = ReplyKeyboardMarkup(
        keyboard=[first_row, second_row],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return markup

def lets_go_keyboard():
    buttons = [KeyboardButton(text=Buttons.lets_go_button)]
    markup = ReplyKeyboardMarkup(
        keyboard=[buttons],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return markup

def gender_keyboard():
    first_row = [KeyboardButton(text=Buttons.male)]
    second_row = [KeyboardButton(text=Buttons.female)]
    markup = ReplyKeyboardMarkup(
        keyboard=[first_row, second_row],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return markup

def aim_keyboard():
    first_row = [KeyboardButton(text=Buttons.lost)]
    second_row = [KeyboardButton(text=Buttons.gain)]
    third_row = [KeyboardButton(text=Buttons.keep_fit)]
    markup = ReplyKeyboardMarkup(
        keyboard=(first_row, second_row, third_row),
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return markup

def activity_level_keyboard():
    first = [KeyboardButton(text=Buttons.sedentary)]
    second = [KeyboardButton(text=Buttons.lightly)]
    third = [KeyboardButton(text=Buttons.moderate)]
    fourth = [KeyboardButton(text=Buttons.very)]
    fifth = [KeyboardButton(text=Buttons.extra)]
    markup = ReplyKeyboardMarkup(
        keyboard = (first, second, third, fourth, fifth),
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return markup

# def user_exists_keyboard():
#     first = [KeyboardButton(text=Buttons.afresh)]
#     second = [KeyboardButton(text=Buttons.carry_on)]
#     third = [KeyboardButton(text=Buttons.delete)]
#     markup = ReplyKeyboardMarkup(
#         keyboard=[first, second, third],
#         resize_keyboard=True,
#         one_time_keyboard=True
#     )
#     return markup
    