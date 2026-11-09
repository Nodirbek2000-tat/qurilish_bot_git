from html import escape

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.menu import contact_kb, login_kb
from loader import dp
from utils.db_api.api import ApiError, call

SERVER_ERROR = "⚠️ Hozir server bilan bog'lanib bo'lmadi. Birozdan keyin qayta urinib ko'ring."


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    try:
        me = await call("me", {"telegram_id": message.from_user.id})
    except ApiError as err:
        if err.status != 404:
            return await message.answer(SERVER_ERROR)
        # Hali tasdiqlanmagan — raqamini so'raymiz
        return await message.answer(
            "Assalomu alaykum! 👋\n\n"
            "Bu bot orqali <b>Arxan</b> admin paneliga kiriladi.\n"
            "Davom etish uchun pastdagi tugma orqali telefon raqamingizni yuboring.",
            reply_markup=contact_kb,
        )
    await message.answer(
        f"Assalomu alaykum, <b>{escape(me['name'])}</b>! 👋\n"
        "Panelga kirish uchun pastdagi «🔐 Panelga kirish» tugmasini bosing.",
        reply_markup=login_kb,
    )
