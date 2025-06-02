from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from .state_machine import HaveEaten
from keyboards.inline_kb import Data
from configs.dependency_injection import container
from databases.dal import DAL
from databases.rdal import RedisDal
from .independent import send_main_kb
from configs.validate_models import  CPFC

eaten = Router()

def calculate_calories(calories: int, proteins: int, fats: int, carbohydrates: int, grams: int):
    copy = dict(locals())
    del copy['grams']
    factor = grams/100
    calculated = dict(zip(copy.keys(), list(map(lambda x: int(x*factor), copy.values()))))
    cpfc = CPFC(**calculated)
    return cpfc

@eaten.callback_query(lambda c: str(c.data).startswith(Data.get_meal), HaveEaten.choose)
async def handle_get_meal(call: CallbackQuery, state: FSMContext):
    await state.set_state(HaveEaten.grams)
    dal_object = DAL(container.get('db_session'))
    meal_name = str(call.data).replace(Data.get_meal, "")
    result = dal_object.read_meal_details(meal_name, call.from_user.username)
    print("RESULT", result)
    meal_data = {
        "calories": result[0][1],
        "proteins": result[0][2],
        "fats": result[0][3],
        "carbohydrates": result[0][4],
    }
    await state.update_data(meal_data=meal_data)
    await call.message.answer(
        text=f'{meal_name.upper()}\nСостав:\n{result[0][0]}\nКаллорийность:\n{result[0][1]}'
    )
    await call.message.answer(
        text='Введите сколько грамм вы съели'
    )

@eaten.message(lambda message: message.text.isdigit(), HaveEaten.grams)
async def handle_grams(message: Message, state: FSMContext):
    data = await state.get_data()
    cpfc = data['meal_data']
    consumed = calculate_calories(grams=int(message.text), **cpfc)
    try:
        rd_object = RedisDal()
        result = rd_object.write_eaten(message.chat.username, consumed)
        print(result)
    except Exception as ex:
        raise Exception('redis error in handle grams', ex)
    else:
        await message.answer(
            text=f'Готово! Вы съели {consumed.calories} каллорий \n {consumed.proteins} белков \n {consumed.fats} жиров \n {consumed.carbohydrates} углеводов'
        )
        await state.clear()
        await send_main_kb(message)
    