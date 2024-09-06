from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.keyboards import Buttons, lets_go_keyboard, start_keyboard
from keyboards.inline_kb import user_exists_inline, menu_inline, main_inline
from .state_machine import SetPlan, Adding, HaveEaten
from databases.dal import DAL
from configs.dependency_injection import container
from keyboards.inline_kb import Data
from configs.single_source import CaloriesBot
from configs.config import settings 
from .independent import send_main_kb
from databases.rdal import RedisDal

bot = CaloriesBot(token=settings.BOT_TOKEN)

command_router = Router()


@command_router.message(CommandStart())
async def handle_start(message: types.Message):
    await message.answer(text='👋')
    dal_object = DAL(container.get('db_session'))
    if dal_object.check_user_exists(username=message.from_user.username):
        await message.answer(
            text='Вы уже использовали этот бот, желаете продолжить, начать заново или удалить информацию о себе?',
            reply_markup=user_exists_inline()
        )
    else:
        dal_object.write_user(username=message.from_user.username,
                            chat_id=message.chat.id)
        await message.answer(
            text=f"Привет, {message.from_user.full_name}! Этот телеграм бот поможет тебе отслеживать количество потребляемых каллорий в день для достижения желаемого результата",
            reply_markup=start_keyboard()
        )


@command_router.message(Command('help'))
async def handle_help(message: types.Message):
    await message.answer(
        chat_id=message.chat.id,
        text='Этот бот поможет тебе отслеживать количество потребляемых каллорий в день.\
            Ты можешь добавить блюдо которое ты ешь в свое меню\
            После приема пищи не забудь записать что ты съел\
            Если надо ты можешь посмотреть сколько каллорий ты уже съел сегодня\
            Или свою статистику за текущий месяц.'
    )


@command_router.message(lambda message: message.text == Buttons.calculate_button)
@command_router.message(Command('calculate'))
async def handle_calculate(message: types.Message):
    await message.answer(
        text='Давай рассчитаем план питания в зависимости от твоей цели!',
        reply_markup=lets_go_keyboard()
    )


@command_router.message(lambda message: message.text == Buttons.set_plan_button)
@command_router.message(Command('set_plan'))
async def handle_set_plan(message: types.Message, state: FSMContext):
    await state.set_state(SetPlan.calories)
    await message.answer(
        text='Если ты хочешь сам установить план питания то сообщи мне необходимую информацию, чтобы я мог отслеживать прогресс!'
    )
    await message.answer(
        text='Сколько каллорий в день ты собираешься получать из еды?'
    )

@command_router.callback_query(F.data == Data.add_dish)
@command_router.message(Command('add_dish'))
async def handle_adding(income: types.Message | CallbackQuery,state: FSMContext = None):
    await state.set_state(Adding.name)
    match type(income):
        case types.Message:
            chat_id = income.chat.id
        case types.CallbackQuery:
            chat_id = income.message.chat.id
    await bot.send_message(
        chat_id = chat_id,
        text = 'Введи название блюда'
    )

@command_router.callback_query(F.data == Data.add_meal)
@command_router.message(Command('add_meal'))
async def handle_adding_meal(income: Message | CallbackQuery, state: FSMContext):
    match type(income):
        case types.Message:
            chat_id = income.chat.id
        case types.CallbackQuery:
            chat_id = income.message.chat.id
    dal_object = DAL(container.get('db_session'))
    meals = dal_object.read_users_menu(income.from_user.username)
    if meals is None:
        await income.bot.send_message(
            chat_id=chat_id,
            text='У вас пока что нету блюд в меню'
        )
        await send_main_kb(income)
    else:
        await state.set_state(HaveEaten.choose)
        menu_markup = menu_inline(meals)
        await income.bot.send_message(
            chat_id=chat_id,
            text='Выбери какое блюдо ты съел сегодня',
            reply_markup=menu_markup
        )
