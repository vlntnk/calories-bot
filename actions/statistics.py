from keyboards.inline_kb import Data
from databases.rdal import RedisDal
from databases.dal import DAL
from .independent import send_main_kb

from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram import Router, types, F
from configs.dependency_injection import container

statistics = Router()

@statistics.callback_query(F.data == Data.show_todays)
@statistics.message(Command('view'))
async def handle_view_todays(income: Message | CallbackQuery):
    match type(income):
        case types.Message:
            username = income.chat.username
            chat_id = income.chat.id
        case types.CallbackQuery:
            username = income.message.chat.username
            chat_id = income.message.chat.id
    try:
        rd_object = RedisDal()
        result = rd_object.show_todays(username)
        print(result)
    except Exception as ex:
        raise Exception('redis error in handle view todays', ex)
    else:
        if any(x > 0 for x in result.model_dump().values()):
            text = f'Вы сегодня съели📆 \n {result.calories} каллорий \n {result.proteins} белков \n {result.fats} жиров \n {result.carbohydrates} углеводов'
        else:
            text = 'Вы сегодня ничего не ели пока что🍏'
        await income.bot.send_message(
            chat_id = chat_id,
            text = text
        )
        await send_main_kb(income)

@statistics.callback_query(F.data == Data.show_statistics)
async def handle_statistics(call: types.CallbackQuery):
    username = call.message.chat.username
    try:
        rd_object = RedisDal()
        result = rd_object.show_statistics(username)
        print(result)
    except Exception as ex:
        raise Exception('redis exception in handle statistics', ex)
    else:
        statistics = []
        for date in result:
            statistics.append(f'{date["date"]} калории: {date["calories"]} белки: {date["proteins"]} жиры: {date["fats"]} углеводы: {date["carbohydrates"]}')
        statistics_str = "\n".join(statistics)
    await call.bot.send_message(
        chat_id = call.message.chat.id,
        text = statistics_str
    )
    await send_main_kb(call)

@statistics.callback_query(F.data == Data.show_limits)
async def handle_vlimits(income: CallbackQuery):
    username = income.message.chat.username
    chat_id = income.message.chat.id
    try:
        dal_object = DAL(container.get('db_session'))
        result = dal_object.get_limits(username)
        print(result)
    except Exception as ex:
        raise Exception('postgres error in handle limits', ex)
    else:
        text = f'Ваша дневная норма: \n {result.calories} каллорий \n {result.proteins} белков\n {result.fats} жиров\n {result.carbohydrates} углеводов'
        await income.bot.send_message(
            chat_id = chat_id,
            text = text
        )
        await send_main_kb(income)
