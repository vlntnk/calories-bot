from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from .state_machine import Adding
from configs.dependency_injection import container
from databases.dal import DAL
from .independent import send_main_kb
from configs.validate_models import Dish

adding_dish = Router()

@adding_dish.message(Adding.name)
async def handle_new_dish_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Adding.dish)
    await message.answer(
        text='Введи состав блюда. \nПример: курица отварная, помидоры черри.'
    )

@adding_dish.message(Adding.dish)
async def handle_new_dish(message: Message, state: FSMContext):
    await state.update_data(dish=message.text)
    await state.set_state(Adding.calories)
    await message.answer(
        text='Введи сколько каллорий содрежит одна порция 100г'
    )

@adding_dish.message(Adding.calories, lambda message: message.text.isdigit())
async def handle_new_dish_calories(message: Message, state: FSMContext):
    await state.update_data(calories=message.text)
    new_dish = await state.get_data()
    new_dish['author'] = message.from_user.username
    dal_object = DAL(container.get('db_session'))
    try:
        dal_object.write_dish(Dish.model_validate(new_dish, from_attributes=True))
    except Exception as e:
        print(f'{e}, outter error')
    finally:
        await state.clear()
        await message.answer(
            text='Готово! Блюдо добавлено в твое меню'
        )
        await send_main_kb(message)
