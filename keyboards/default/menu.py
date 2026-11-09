from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

CONTACT_TEXT = "📱 Raqamni yuborish"
LOGIN_TEXT = "🔐 Panelga kirish"

contact_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
    KeyboardButton(CONTACT_TEXT, request_contact=True))

login_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(LOGIN_TEXT))
