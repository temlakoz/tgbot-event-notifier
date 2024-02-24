import asyncio
import logging
from datetime import datetime

from aiogram import Dispatcher
from aiogram.methods import SetMyCommands, DeleteMyCommands
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import bot
from app.handlers.admin import router
from app.scheduler.notifier import send_message_weekly


async def main():
    dp = Dispatcher()
    
    dp.include_router(router)
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(send_message_weekly, trigger='cron', day_of_week='3',
                      hour='12', minute='0', kwargs={'bot': bot})
    scheduler.start()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Pressed Ctrl + C.")
