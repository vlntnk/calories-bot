from aiogram import Bot, Dispatcher
import asyncio
import logging

from configs.config import settings
from actions.commands import command_router
from actions.calculate import others
from actions.set_plan import set_p
from actions.start import start_router
from actions.add_dish import adding_dish
from actions.addind_eaten import eaten
from configs.single_source import CaloriesBot


bot = CaloriesBot(token=settings.BOT_TOKEN)
dispatcher = Dispatcher()

dispatcher.include_routers(command_router, others, set_p, start_router, adding_dish,
                           eaten)


async def main():
    logging.basicConfig(level=logging.INFO)
    await dispatcher.start_polling(bot)

# @main_router.message()
# async def echo(message: types.Message = None):
#     if message.text:
#         await bot.send_message(
#             chat_id=message.chat.id, 
#             text=f'No such command: "{message.text}"',
#             reply_to_message_id=message.message_id
#         )
#     elif message.sticker:
#         await bot.send_message(
#             chat_id=message.chat.id,
#             text=f'No such command: "{message.sticker.emoji}"'
#         )
#     else:
#         await message.send_copy(message.chat.id)


if __name__ == "__main__":
    asyncio.run(main())