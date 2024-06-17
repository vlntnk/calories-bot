from aiogram import types
from keyboards.inline_kb import main_inline
from aiogram.types import CallbackQuery, Message


async def send_main_kb(income: types.Message | CallbackQuery):
    if isinstance(income, Message):
        await income.answer(
            text='Выбери следующее действие',
            reply_markup=main_inline()
        )
    elif isinstance(income, CallbackQuery):
        await income.message.answer(
            text='Выбери следующее действие',
            reply_markup=main_inline()
        )