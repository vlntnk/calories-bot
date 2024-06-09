from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from keyboards import Buttons, lets_go_keyboard, start_keyboard, user_exists_keyboard
from .state_machine import SetPlan
from dal import DAL
from dependency_injection import container
from .state_machine import Beginning

command_router = Router()


@command_router.message(CommandStart())
async def handle_start(message: types.Message, state: FSMContext):
    await message.answer(text='👋')
    dal_object = DAL(container.get('db_session'))
    if dal_object.check_user_exists(username=message.from_user.username):
        await state.set_state(Beginning.exists)
        await message.answer(
            text='Вы уже использовали этого бота, желаете продолжить, начать заново или удалить информацию о себе?',
            reply_markup=user_exists_keyboard()
        )
    else:
        dal_object.write_user(username=message.from_user.username,
                            chat_id=message.chat.id)
        await message.answer(
            text=f"Hello {message.from_user.full_name}! You're in bb_bot. Here you can... Enjoy and have fun!",
            reply_markup=start_keyboard()
        )


@command_router.message(Command('help'))
async def handle_help(message: types.Message):
    await message.answer(
        chat_id=message.chat.id,
        text='Hi! I\'m just a bot.\nSend me any message.'
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


