from aiogram import Router, F
from aiogram.types import CallbackQuery
from time import sleep
from random import randint

from keyboards.keyboards import start_keyboard
from databases.dal import DAL
from configs.dependency_injection import container
from keyboards.inline_kb import Inline
from .independent import send_main_kb

start_router = Router()


@start_router.callback_query(F.data == Inline.afresh)
async def handle_afresh(call: CallbackQuery):
    await call.message.answer(
        text='Давай еще раз посчитаем твою норму каллорий',
        reply_markup=start_keyboard()
    )


@start_router.callback_query(F.data == Inline.delete)
async def handle_delet(call: CallbackQuery):
    try:
        for sending in ('1️⃣', '2️⃣', '3️⃣'):
            await call.message.answer(text=sending)
            sleep(1)
        dal_object = DAL(container.get('db_session'))
        username = call.from_user.username
        dal_object.delet_users_dishes(username)
        dal_object.delete_user(username)
    except Exception as e:
        print(f'{e}')
    finally:
        bot_me = await call.bot.me()
        await call.answer(
            url=f't.me/{bot_me.username}?start={randint(1, 100)}'
        )

@start_router.callback_query(F.data == Inline.carry_on)
async def handle_continuing(call: CallbackQuery):
    await send_main_kb(call)
        