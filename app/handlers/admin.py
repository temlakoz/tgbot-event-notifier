from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.methods import SetMyCommands, DeleteMyCommands
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from app.filters.is_admin import IsAdmin, IsAdminCallback
from app.keyboard import admin as keyboard
from app.scheduler.notifier import send_message_weekly
from app.states.admin import AddForm, DelForm, MailingForm
from app.utils.debug import debug_callback_handler, debug_message_handler
from config import db, bot, chat_id_for_mailing

router = Router()

start_photo_id = "AgACAgIAAxkBAANPZderBzAy2deITswzveoVkRD-fz8AAoHUMRsAAUrBSrc4wYIPmxTAAQADAgADeQADNAQ"
products_photo_id = "AgACAgIAAxkBAANSZderGfEQh2ITg_pd4iFT1_8tU7QAAoLUMRsAAUrBSk9pUK99eRc6AQADAgADeQADNAQ"


# Команда /start
@router.message(CommandStart(), IsAdmin())
@debug_message_handler
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                         "Добро пожаловать в CTF-Notifier бот\n"
                         "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                         "Вы вошли как  💼 Администратор",
                         reply_markup=keyboard.main)


# Кнопка просмотра будущих событий
@router.message(F.text == keyboard.view_events_button_text, IsAdmin())
@debug_message_handler
async def view_events(message: Message, state: FSMContext):
    await state.clear()
    events = db.get_current_events()
    if events:
        text = "🍻 Предстоящие события:\n\n"
        i = 1
        for event in events:
            event_id, name, event_date = event
            text += f"{i}. <b>{name}</b>  |  {event_date}\n"
            i += 1
    else:
        text = "➖ Предстоящие события отсутствуют"

    await message.answer(text=text, reply_markup=keyboard.main,
                         parse_mode="HTML")


# Кнопка добавления событий
@router.message(F.text == keyboard.add_event_button_text, IsAdmin())
@debug_message_handler
async def add_event(message: Message, state: FSMContext):
    await state.set_state(AddForm.name)
    await message.answer("Введите имя события", reply_markup=keyboard.cancel)


@router.message(F.text != keyboard.cancel_button_text, IsAdmin(), AddForm.name)
@debug_message_handler
async def add_event_name(message: Message, state: FSMContext):
    await state.set_state(AddForm.date)
    await state.update_data(name=message.text)
    await message.answer("Введите дату в формате ДД-ММ-ГГГГ",
                         reply_markup=keyboard.cancel)


@router.message(F.text != keyboard.cancel_button_text, IsAdmin(), AddForm.date)
@debug_message_handler
async def add_event_date(message: Message, state: FSMContext):
    name = (await state.get_data())['name']
    date = message.text

    db.add_event(name=name, event_date_str=date)
    await message.answer("Событие успешно добавлено!",
                         reply_markup=keyboard.main)


# Кнопка удаления событий
@router.message(F.text == keyboard.del_event_button_text, IsAdmin())
@debug_message_handler
async def del_event(message: Message, state: FSMContext):
    await state.set_state(DelForm.num)
    events = db.get_current_events()
    if events:
        await state.update_data(events=events)
        text = "🍻 Предстоящие события:\n\n"
        i = 1
        for event in events:
            event_id, name, event_date = event
            text += f"{i}. <b>{name}</b>  |  {event_date}\n"
            i += 1
    else:
        text = "➖ Предстоящие события отсутствуют"

    await message.answer(text=text, reply_markup=keyboard.get_del_events_ikb(),
                         parse_mode="HTML")


@router.callback_query(IsAdminCallback(), DelForm.num)
@debug_callback_handler
async def del_event(callback_query: CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=callback_query.message.message_id)
    if callback_query.data == "cancel":
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text="🔮 Главное меню",
                               reply_markup=keyboard.main)
    else:
        events = (await state.get_data())["events"]
        num = callback_query.data[0]
        event_id, event_name, event_date = events[int(num)-1]
        db.delete_event(event_id=event_id)
        text = f"Событие {event_name}  |  {event_date} удалено"
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text=text,
                               reply_markup=keyboard.main)
        await state.clear()


# Кнопка непосредственной рассылки
@router.message(F.text == keyboard.mailing_button_text, IsAdmin())
async def mailing(message: Message, state: FSMContext):
    await state.set_state(MailingForm.confirm)
    await message.answer("Вы уверены что хотите провести рассылку?", reply_markup=keyboard.mailing_ikb)


@router.callback_query(IsAdminCallback(), MailingForm.confirm)
@debug_callback_handler
async def mailing_confirm(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    callback_data = callback_query.data
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=callback_query.message.message_id)
    if callback_data == "yes":
        await send_message_weekly(bot=bot, mailing=True)
        text = "📤 Рассылка прошла успешно"
        await bot.send_message(chat_id=callback_query.from_user.id, text=text,
                               reply_markup=keyboard.main)
    else:
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text="🔮 Главное меню", reply_markup=keyboard.main)


# Кнопка включения/выключения рассылки
@router.message(F.text == keyboard.power_change_button_text, IsAdmin())
@debug_message_handler
async def powerchange(message: Message, state: FSMContext):
    await state.clear()
    power_state = db.get_notifier_state()
    if power_state:
        db.set_notifier_state(False)
        await message.answer("Рассылка включена на каждый четверг 12:00 по МСК", reply_markup=keyboard.main)
    else:
        db.set_notifier_state(True)
        await message.answer("Рассылка выключена", reply_markup=keyboard.main)


# любое сообщение не попавшее в другие хэндлеры
@router.message(IsAdmin())
@debug_message_handler
async def any_text(message: Message, state: FSMContext):
    await state.clear()
    if message.chat.id != chat_id_for_mailing:
        await message.answer(text="🔮 Главное меню", reply_markup=keyboard.main)
    else:
        # await bot.send_message(chat_id=message.chat.id, text="markup delete test", reply_markup=ReplyKeyboardRemove())
        await message.answer(text="markup delete test", reply_markup=ReplyKeyboardRemove())
