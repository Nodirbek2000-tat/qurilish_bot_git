from aiogram import executor

from loader import dp
import middlewares, filters, handlers
from utils.db_api.api import close as close_api
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    # Birlamchi komandalar (/start va /help)
    await set_default_commands(dispatcher)


async def on_shutdown(dispatcher):
    await close_api()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
