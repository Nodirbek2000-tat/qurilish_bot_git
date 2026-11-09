from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp(), state="*")
async def bot_help(message: types.Message):
    text = ("<b>Arxan admin paneliga kirish boti</b>\n",
            "/start — telefon raqamni tasdiqlash va panelga kirish",
            "/admin — adminlar uchun: statistika, admin va xodim qo'shish",
            "/help — yordam")
    await message.answer("\n".join(text))
