from aiogram.dispatcher.filters.state import State, StatesGroup


class AddAccess(StatesGroup):
    """/admin → «Admin/Xodim qo'shish»: avval ism-familiya, keyin telefon raqam."""

    name = State()
    phone = State()
