from keyboards.inline_kb import Data
from databases.rdal import RedisDal
from .independent import send_main_kb

from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram import Router, types, F
import datetime

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
        if int(result) > 0:
            text = f'Вы сегодня съели {result.decode('utf-8')} каллорий📆'
        else:
            text = 'Вы сегодня ничего не ели пока что🍏'
        await income.bot.send_message(
            chat_id = chat_id,
            text = text
        )
        await send_main_kb(income)

@statistics.callback_query(F.data == Data.show_statistics)
async def handle_statistics(call: types.CallbackQuery):
    month = datetime.datetime.now().month
    username = call.message.chat.username
    try:
        rd_object = RedisDal()
        result = rd_object.show_statistics(username)
        print(result)
    except Exception as ex:
        raise Exception('redis exception in handle statistics', ex)
    else:
        filtered = {}
        for d, c in result.items():
            d = d.decode('utf-8')
            c = c.decode('utf-8')
            if datetime.datetime.strptime(d, '%Y-%m-%d').month == month:
                filtered[d] = c
            else:
                rd_object.delete(username, d)
        text = 'sep=\n'.join([ f'{date} {calories}' for date, calories in filtered.items()])
    await call.bot.send_message(
        chat_id = call.message.chat.id,
        text = text
    )
    await send_main_kb(call)
