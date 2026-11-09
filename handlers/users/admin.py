"""/admin — faqat katta ruxsat berilganlar (admin) uchun.

Statistika, ro'yxat, admin va xodim qo'shish. Huquqni server har so'rovda qayta tekshiradi.
"""

from html import escape

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.admin import ROLE_LABEL, admin_menu, back_kb, cancel_kb, confirm_delete_kb, list_kb
from loader import dp
from states.admin import AddAccess
from utils.db_api.api import ApiError, call

from .start import SERVER_ERROR

NOT_ADMIN = "⛔️ Bu bo'lim faqat adminlar uchun."
MENU_TEXT = "👑 <b>Admin bo'limi</b>\nKerakli bo'limni tanlang:"


async def admin_call(path: str, user_id: int, **data):
    """Server javobi yoki (None, xato matni)."""
    try:
        return await call(path, {"actor": user_id, **data}), None
    except ApiError as err:
        if err.status == 403:
            return None, NOT_ADMIN
        return None, err.message if err.status == 400 else SERVER_ERROR


@dp.message_handler(commands=["admin"], state="*")
async def admin_cmd(message: types.Message, state: FSMContext):
    await state.finish()
    try:
        me = await call("me", {"telegram_id": message.from_user.id})
    except ApiError as err:
        return await message.answer(SERVER_ERROR if err.status not in (403, 404) else NOT_ADMIN)
    if me.get("role") != "admin":
        return await message.answer(NOT_ADMIN)
    await message.answer(MENU_TEXT, reply_markup=admin_menu())


@dp.callback_query_handler(text="adm:menu", state="*")
async def admin_menu_cb(cq: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await cq.message.edit_text(MENU_TEXT, reply_markup=admin_menu())
    await cq.answer()


@dp.callback_query_handler(text="adm:stats")
async def stats_cb(cq: types.CallbackQuery):
    s, error = await admin_call("stats", cq.from_user.id)
    if error:
        return await cq.answer(error, show_alert=True)
    lines = [
        "📊 <b>Statistika</b>\n",
        f"📨 Raqam yuborganlar: <b>{s['requestPeople']}</b> kishi ({s['requests']} marta)",
        f"⛔️ Ruxsatsiz urinishlar: <b>{s['deniedPeople']}</b> kishi",
        f"✅ Panelga kirganlar: <b>{s['loginPeople']}</b> kishi ({s['logins']} marta)",
        f"👑 Adminlar: <b>{s['admins']}</b>   👤 Xodimlar: <b>{s['staff']}</b>",
        "",
    ]
    if s["recent"]:
        last = s["recent"][0]
        lines.append(f"🕘 <b>Oxirgi kirgan:</b> {escape(last['name'])} — {last['at']}")
        if len(s["recent"]) > 1:
            lines.append("\n<b>Oldingi kirishlar:</b>")
            lines += [f"• {escape(r['name'])} — {r['at']}" for r in s["recent"][1:]]
    else:
        lines.append("🕘 Hali hech kim panelga kirmagan.")
    await cq.message.edit_text("\n".join(lines), reply_markup=back_kb())
    await cq.answer()


async def show_list(cq: types.CallbackQuery):
    r, error = await admin_call("access", cq.from_user.id)
    if error:
        return await cq.answer(error, show_alert=True)
    items = r["items"]
    lines = ["📋 <b>Panelga ruxsat berilganlar</b>\n"]
    for it in items:
        status = f"oxirgi kirish: {it['lastLogin']}" if it["lastLogin"] else ("botga ulangan" if it["linked"] else "hali /start bosmagan")
        lines.append(f"{ROLE_LABEL.get(it['role'], it['role'])} <b>{escape(it['name'])}</b>\n"
                     f"     {it['phone']} · {status}")
    if len(items) > 1:
        lines.append("\nO'chirish uchun pastdagi ismni bosing.")
    await cq.message.edit_text("\n".join(lines), reply_markup=list_kb(items, r["me"]))
    await cq.answer()


@dp.callback_query_handler(text="adm:list")
async def list_cb(cq: types.CallbackQuery):
    await show_list(cq)


@dp.callback_query_handler(text_startswith="adm:del:")
async def delete_ask_cb(cq: types.CallbackQuery):
    pk = int(cq.data.rsplit(":", 1)[1])
    await cq.message.edit_text("Rostdan ham shu kishining panelga kirish ruxsatini olib tashlaysizmi?\n"
                               "Agar u hozir panelda bo'lsa, darhol chiqarib yuboriladi.",
                               reply_markup=confirm_delete_kb(pk))
    await cq.answer()


@dp.callback_query_handler(text_startswith="adm:delok:")
async def delete_cb(cq: types.CallbackQuery):
    _, error = await admin_call("access/delete", cq.from_user.id, id=int(cq.data.rsplit(":", 1)[1]))
    if error:
        return await cq.answer(error, show_alert=True)
    await cq.answer("✅ Ruxsat olib tashlandi")
    await show_list(cq)


# ---------- admin / xodim qo'shish ----------

@dp.callback_query_handler(text_startswith="adm:add:")
async def add_start_cb(cq: types.CallbackQuery, state: FSMContext):
    role = cq.data.rsplit(":", 1)[1]
    await state.update_data(role=role)
    await AddAccess.name.set()
    who = "admin" if role == "admin" else "xodim"
    await cq.message.edit_text(f"Yangi {who}ning <b>ism-familiyasini</b> yozing:", reply_markup=cancel_kb())
    await cq.answer()


@dp.callback_query_handler(text="adm:cancel", state="*")
async def add_cancel_cb(cq: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await cq.message.edit_text(MENU_TEXT, reply_markup=admin_menu())
    await cq.answer("Bekor qilindi")


@dp.message_handler(state=AddAccess.name)
async def add_name(message: types.Message, state: FSMContext):
    name = " ".join((message.text or "").split())
    if len(name) < 3:
        return await message.answer("Ism-familiyani to'liq yozing, masalan: <i>Aliyev Vali</i>", reply_markup=cancel_kb())
    await state.update_data(name=name)
    await AddAccess.phone.set()
    await message.answer("Endi uning <b>telefon raqamini</b> yozing (masalan: +998901234567)\n"
                         "yoki kontaktini yuboring:", reply_markup=cancel_kb())


@dp.message_handler(state=AddAccess.phone, content_types=[types.ContentType.TEXT, types.ContentType.CONTACT])
async def add_phone(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number if message.contact else (message.text or "")
    data = await state.get_data()
    r, error = await admin_call("access/add", message.from_user.id, name=data["name"], phone=phone, role=data["role"])
    if error:
        if error == NOT_ADMIN:
            await state.finish()
            return await message.answer(error)
        return await message.answer(f"⚠️ {escape(error)}\nQaytadan yozing:", reply_markup=cancel_kb())
    await state.finish()
    extra = "\nBotda /admin buyrug'i ham unga ishlaydi." if r["role"] == "admin" else ""
    await message.answer(
        f"✅ Qo'shildi: {ROLE_LABEL[r['role']]} <b>{escape(r['name'])}</b> ({r['phone']})\n\n"
        f"Endi u botga /start bosib, shu raqamni yuborsa — panelga kira oladi.{extra}",
        reply_markup=admin_menu())
