from aiogram.fsm.state import StatesGroup, State


class AddForm(StatesGroup):
    name = State()
    date = State()


class DelForm(StatesGroup):
    num = State()
    confirm = State()


class MailingForm(StatesGroup):
    confirm = State()
