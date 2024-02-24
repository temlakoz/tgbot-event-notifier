from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from config import db

view_events_button_text = "👀 Просмотреть предстоящие события"
add_event_button_text = "🟢 Добавить событие"
del_event_button_text = "❌ Удалить событие"
mailing_button_text = "✉️ Провести рассылку сейчас"
power_change_button_text = "🔋 Включить или выключить еженедельные уведомления"
cancel_button_text = "Отменить"

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=view_events_button_text)],
    [KeyboardButton(text=add_event_button_text),
     KeyboardButton(text=del_event_button_text)],
    [KeyboardButton(text=mailing_button_text)],
    [KeyboardButton(text=power_change_button_text)]
], resize_keyboard=True)

cancel = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=cancel_button_text)]
], resize_keyboard=True)


def get_del_events_ikb():
    events = db.get_current_events()
    n = len(events)

    buttons = [InlineKeyboardButton(text=str(i + 1), callback_data=str(i + 1))
               for i in range(n)]

    keyboard_layout = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]

    keyboard_layout.append(
        [InlineKeyboardButton(text="Отменить", callback_data="cancel")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard_layout)


mailing_ikb = InlineKeyboardMarkup(inline_keyboard=
                                   [[InlineKeyboardButton(text="Да",
                                                          callback_data="yes"),
                                     InlineKeyboardButton(text="Нет",
                                                          callback_data="no")]])
