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
        text='Введи сколько каллорий содрежит одна порция 100г.'
    )

@adding_dish.message(Adding.calories)
async def handle_new_dish_calories(message: Message, state: FSMContext):
    await state.update_data(calories=message.text)
    await state.set_state(Adding.proteins)
    await message.answer(
        text='Введи сколько грамм белков содержится в 100 грамм блюда.'
    )

@adding_dish.message(Adding.proteins)
async def handle_new_dish_proteins(message: Message, state: FSMContext):
    await state.update_data(proteins=message.text)
    await state.set_state(Adding.fats)
    await message.answer(
        text='Укажи содержание жиров тоже на 100 грамм.'
    )

@adding_dish.message(Adding.fats)
async def handle_new_dish_fats(message: Message, state: FSMContext):
    await state.update_data(fats=message.text)
    await state.set_state(Adding.carbohydrates)
    await message.answer(
        text='А сколько углеводов?'
    )

@adding_dish.message(Adding.carbohydrates, lambda message: message.text.isdigit())
async def handle_new_dish_carbohydrates(message: Message, state: FSMContext):
    await state.update_data(carbohydrates=message.text)
    new_dish = await state.get_data()
    print(new_dish)
    new_dish['author'] = message.from_user.username
    dal_object = DAL(container.get('db_session'))
    dish_object = Dish.model_validate(new_dish, from_attributes=True)
    try:
        dal_object.write_dish(dish_object)
    except Exception as e:
        print(f'{e}, outter error')
    finally:
        await state.clear()
        await message.answer(
            text='Готово! Блюдо добавлено в твое меню'
        )
        await send_main_kb(message)
