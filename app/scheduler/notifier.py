from aiogram import Bot

from config import db, chat_id_for_mailing


async def send_message_weekly(bot: Bot, mailing=False):
    power_on = db.get_notifier_state()
    events = db.get_current_events()
    if events:
        text = "🍻 Еженедельная рассылка предстоящих событий:\n\n"
        i = 1
        for event in events:
            event_id, name, event_date = event
            text += f"{i}. <b>{name}</b>  |  {event_date}\n"
            i += 1
    else:
        text = "➖ Предстоящие события отсутствуют"

    if power_on or mailing:
        await bot.send_message(chat_id=chat_id_for_mailing, text=text, parse_mode="HTML")
