from aiogram import types


async def set_default_commands(dp):
    # /admin ro'yxatda ko'rsatilmaydi — u faqat adminlarga ishlaydi
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Panelga kirish"),
            types.BotCommand("help", "Yordam"),
        ]
    )
