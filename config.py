from aiogram import Bot
from app.db.db import Events


db = Events()
admin_ids = [1234567890]

# id чата в который будет приходить рассылка каждую неделю
chat_id_for_mailing = -1001234567890

BOT_TOKEN = "XXXXXXXXX"
bot = Bot(token=BOT_TOKEN)

# PostgreSQL
db_name = "ctf_events"
db_user = "postgres"
db_password = "1"
db_host = "localhost"
