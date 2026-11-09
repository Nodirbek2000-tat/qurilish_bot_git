"""Raqamni tasdiqlash va panelga bir martalik kirish havolasini berish."""

from html import escape

from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.exceptions import BadRequest

from keyboards.default.menu import LOGIN_TEXT, contact_kb, login_kb
from loader import dp
from utils.db_api.api import ApiError, call
from utils.misc import rate_limit

from .start import SERVER_ERROR


async def send_link(message: types.Message):
    try:
        r = await call("link", {"telegram_id": message.from_user.id})
    except ApiError as err:
        if err.status == 403:
            return await message.answer("Avval telefon raqamingizni yuboring.", reply_markup=contact_kb)
        return await message.answer(SERVER_ERROR)
    text = (f"🔐 Panelga kirish havolasi tayyor.\n"
            f"U <b>{r['minutes']} daqiqa</b> amal qiladi va faqat <b>bir marta</b> ishlaydi.\n"
            f"Havolani hech kimga bermang.")
    try:
        await message.answer(text, reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton("🔐 Panelga kirish", url=r["url"])))
    except BadRequest:
        # Telegram «localhost» kabi manzillarni tugmaga qo'ymaydi — unda havolani matn qilib beramiz
        await message.answer(f"{text}\n\n<code>{escape(r['url'])}</code>", disable_web_page_preview=True)


@dp.message_handler(content_types=types.ContentType.CONTACT, state=None)
@rate_limit(3, "contact")
async def got_contact(message: types.Message):
    contact = message.contact
    # Faqat o'zining raqami: boshqaning kontaktini yuborib kirib bo'lmaydi
    if contact.user_id != message.from_user.id:
        return await message.answer("Iltimos, <b>o'zingizning</b> raqamingizni pastdagi tugma orqali yuboring.",
                                    reply_markup=contact_kb)
    try:
        r = await call("contact", {"telegram_id": message.from_user.id, "phone": contact.phone_number,
                                   "name": message.from_user.full_name})
    except ApiError as err:
        if err.status == 403:
            return await message.answer(
                "❌ Kechirasiz, bu raqamga panelga kirish ruxsati berilmagan.\n"
                "Ruxsat olish uchun administratorga murojaat qiling.",
                reply_markup=ReplyKeyboardRemove())
        return await message.answer(SERVER_ERROR)
    await message.answer(f"✅ Raqamingiz tasdiqlandi, <b>{escape(r['name'])}</b>!", reply_markup=login_kb)
    await send_link(message)


@dp.message_handler(text=LOGIN_TEXT, state=None)
@rate_limit(3, "login")
async def login_button(message: types.Message):
    await send_link(message)
