from aiogram import Router, F
from aiogram.types import CallbackQuery
from time import sleep
from random import randint

from keyboards.keyboards import start_keyboard
from databases.dal import DAL
from configs.dependency_injection import container
from keyboards.inline_kb import Inline
from .independent import send_main_kb
from databases.rdal import RedisDal

start_router = Router()


@start_router.callback_query(F.data == Inline.afresh)
async def handle_afresh(call: CallbackQuery):
    username = call.message.chat.username
    try:
        rd_object = RedisDal()
        rd_object.delete_user(username)
    except Exception as ex:
        raise Exception('error while deleting redis data for refreshing', ex)
    else:
        await call.message.answer(
            text='Давай еще раз посчитаем сколько каллорий ты должен потреблять в день',
            reply_markup=start_keyboard()
        )


@start_router.callback_query(F.data == Inline.delete)
async def handle_delete(call: CallbackQuery):
    try:
        for sending in ('1️⃣', '2️⃣', '3️⃣'):
            await call.message.answer(text=sending)
            sleep(1)
        dal_object = DAL(container.get('db_session'))
        username = call.from_user.username
        dal_object.delet_users_dishes(username)
        dal_object.delete_user(username)
        rd_object = RedisDal()
        rd_object.delete_user(username)
    except Exception as ex:
        raise Exception('error while deleting redis or postgres data', ex)
    finally:
        bot_me = await call.bot.me()
        await call.answer(
            url=f't.me/{bot_me.username}?start={randint(1, 100)}'
        )

@start_router.callback_query(F.data == Inline.carry_on)
async def handle_continuing(call: CallbackQuery):
    await send_main_kb(call)
        