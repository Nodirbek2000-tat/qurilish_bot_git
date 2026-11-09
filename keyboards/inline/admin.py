from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ROLE_LABEL = {"admin": "👑 Admin", "xodim": "👤 Xodim"}


def admin_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton("📊 Statistika", callback_data="adm:stats"),
        InlineKeyboardButton("📋 Ro'yxat", callback_data="adm:list"),
        InlineKeyboardButton("👑 Admin qo'shish", callback_data="adm:add:admin"),
        InlineKeyboardButton("👤 Xodim qo'shish", callback_data="adm:add:xodim"),
    )


def back_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️ Orqaga", callback_data="adm:menu"))


def cancel_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup().add(InlineKeyboardButton("✖️ Bekor qilish", callback_data="adm:cancel"))


def list_kb(items: list, me: int) -> InlineKeyboardMarkup:
    """Har bir kishi yonida o'chirish tugmasi (o'zingizdan tashqari)."""
    kb = InlineKeyboardMarkup(row_width=1)
    for it in items:
        if it["id"] != me:
            kb.add(InlineKeyboardButton(f"❌ {it['name']}", callback_data=f"adm:del:{it['id']}"))
    return kb.add(InlineKeyboardButton("⬅️ Orqaga", callback_data="adm:menu"))


def confirm_delete_kb(pk: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton("✅ Ha, o'chirish", callback_data=f"adm:delok:{pk}"),
        InlineKeyboardButton("↩️ Yo'q", callback_data="adm:list"),
    )
