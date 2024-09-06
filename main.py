from aiogram import Dispatcher, Router
from aiogram.types import Message
import asyncio
import logging

from configs.config import settings
from actions.commands import command_router
from actions.calculate import others
from actions.set_plan import set_p
from actions.start import start_router
from actions.add_dish import adding_dish
from actions.addind_eaten import eaten
from actions.statistics import statistics
from configs.single_source import CaloriesBot


bot = CaloriesBot(token=settings.BOT_TOKEN)
dispatcher = Dispatcher()

exception = Router()

@exception.message()
async def handle_other_message(message: Message):
    await message.answer(
        text = 'Немного не то('
    )

dispatcher.include_routers(command_router, others, set_p, start_router, adding_dish,
                           eaten, statistics, exception)


async def main():
    logging.basicConfig(level=logging.INFO)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())