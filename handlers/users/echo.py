from aiogram import types

from loader import dp


# Boshqa har qanday xabar — eng oxirida ro'yxatdan o'tadi
@dp.message_handler(state=None, content_types=types.ContentTypes.ANY)
async def bot_echo(message: types.Message):
    await message.answer("Panelga kirish uchun /start bosing.")
