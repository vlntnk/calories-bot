from aiogram import Router, types
from aiogram.fsm.context import FSMContext


from .state_machine import SetPlan
from .independent import send_main_kb


set_p = Router()

@set_p.message(SetPlan.calories, lambda message: message.text.isdigit())
async def handle_calories(message: types.Message, state: FSMContext):
    await state.set_state()
    await message.answer(
        'Хорошо, я запомню сколько калорий ты должен потреблять.'
    )
    await send_main_kb(message)