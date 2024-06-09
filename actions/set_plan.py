from aiogram import Router, types
from aiogram.fsm.context import FSMContext


from .state_machine import SetPlan


set_p = Router()

@set_p.message(SetPlan.calories, lambda message: message.text.isdigit())
async def handle_calories(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        'Хорошо, я запомню сколько калорий ты должен потреблять.'
    )