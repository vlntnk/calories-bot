from aiogram import Router, types
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from keyboards.keyboards import Buttons, gender_keyboard, aim_keyboard, activity_level_keyboard
from .state_machine import CalculatePlan
from api_interaction import calculate_calories
from databases.dal import DAL
from configs.dependency_injection import container
from .independent import send_main_kb
from calculate_PFC import calculate_PFC


others = Router()

translater = {Buttons.male: 'male', Buttons.female: 'female', Buttons.lost: 'weight_loss', Buttons.keep_fit: 'maintenance', 
              Buttons.gain: 'weight_gain', Buttons.sedentary: 'sedentary', Buttons.lightly: 'ligthtly_active',
              Buttons.moderate: 'moderately_active', Buttons.very: 'very_active', Buttons.extra: 'extra_active'}


@others.message(lambda message: message.text == Buttons.lets_go_button)
async def handle_lets_go(message: types.Message, state: FSMContext):
    await state.set_state(CalculatePlan.gender)
    await message.answer(
        'Замечательно! Чтобы рассчитать план питания мне надо узнать твои данные и цель, к которой мы будем двигаться.\
        Для начало дай мне знать какой у тебя пол.',
        reply_markup = gender_keyboard()
    )

@others.message(CalculatePlan.gender, lambda message: message.text == Buttons.male or message.text == Buttons.female)
async def handle_gender(message: types.Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await state.set_state(CalculatePlan.age)
    await message.answer(
        'Замечательно! Теперь скажи мне свой возраст.',
        reply_markup=ReplyKeyboardRemove()
    )

@others.message(CalculatePlan.age, lambda message: message.text.isdigit())
async def handle_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(CalculatePlan.aim)
    await message.answer(
        'Теперь расскажи какого результат ты хотел бы достичь.',
        reply_markup=aim_keyboard()
    )

@others.message(CalculatePlan.aim, lambda message: message.text in (Buttons.gain, Buttons.lost, Buttons.keep_fit))
async def handle_aim(message: types.Message, state:FSMContext):
    await state.update_data(goal=message.text)
    await state.set_state(CalculatePlan.height)
    await message.answer(
        'Задача ясна. Напиши какой у тебя рост.',
        reply_markup=ReplyKeyboardRemove()
    )

@others.message(CalculatePlan.height, lambda message: message.text.isdigit())
async def handle_height(message: types.Message, state:FSMContext):
    await state.update_data(height=message.text)
    await state.set_state(CalculatePlan.weight)
    await message.answer(
        'А вес?'
    )

@others.message(CalculatePlan.weight)
async def handle_height(message: types.Message, state:FSMContext):
    await state.set_state(CalculatePlan.activity)
    await state.update_data(weight=message.text)
    await message.answer(
        'Расскажи насколько ты активный. Как часто занимаешься спортом.',
        reply_markup=activity_level_keyboard()
    )

@others.message(CalculatePlan.activity)
async def handle_calculate(message: types.Message, state: FSMContext):
    await state.update_data(activity_level=message.text)
    data = await state.get_data()
    print(data)
    for parametr in data:
        if data[parametr] in translater:
            data[parametr] = translater[data[parametr]]
    print(data)
    response = calculate_calories(data)
    calories = int(response)
    proteins, fats, carbohydrates = calculate_PFC(calories, data["goal"], data['weight'])
    try:
        dal_object = DAL(container.get('db_session'))
        dal_object.write_calories(message.from_user.username, calories, proteins, fats, carbohydrates)
    except Exception as e:
        print(f'{e}')
    finally:
        await message.answer(
            f'Твоя дневная норма {calories} калорий, {proteins} грамм белков, {fats} жиров и {carbohydrates} грамм углеводов.'
        )
        await send_main_kb(message)

