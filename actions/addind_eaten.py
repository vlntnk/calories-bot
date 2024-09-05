from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from .state_machine import HaveEaten
from keyboards.inline_kb import Data
from configs.dependency_injection import container
from databases.dal import DAL
from databases.rdal import RedisDal
from .independent import send_main_kb

eaten = Router()

def calculate_calories(calories: int, grams: int):
    return calories*(grams/100)

@eaten.callback_query(lambda c: str(c.data).startswith(Data.get_meal), HaveEaten.choose)
async def handle_get_meal(call: CallbackQuery, state: FSMContext):
    await state.set_state(HaveEaten.grams)
    dal_object = DAL(container.get('db_session'))
    meal_name = str(call.data).replace(Data.get_meal, "")
    result = dal_object.read_meal_details(meal_name, call.from_user.username)
    await state.update_data(calories=result[0][1])
    await call.message.answer(
        text=f'{meal_name.upper()}\nСостав:\n{result[0][0]}\nКаллорийность:\n{result[0][1]}'
    )
    await call.message.answer(
        text='Введите сколько грамм вы съели'
    )

@eaten.message(lambda message: message.text.isdigit(), HaveEaten.grams)
async def handle_grams(message: Message, state: FSMContext):
    calr = await state.get_data()
    consumed = calculate_calories(int(calr['calories']), int(message.text))
    try:
        rd_object = RedisDal()
        result = rd_object.write_eaten(message.chat.username, consumed)
        print(result)
    except Exception as ex:
        raise Exception('redis error in handle grams', ex)
    else:
        await message.answer(
            text=f'Готов! Съеденные {consumed} каллории сохранены'
        )
        await state.clear()
        await send_main_kb(message)
    