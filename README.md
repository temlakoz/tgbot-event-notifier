**Написан на python3 с использованием aiogram 3** 
<br><br>

![image](https://github.com/temlakoz/tgbot-event-notifier/assets/44872170/795d31e4-1b24-43a0-85e6-fc21ccfc5dd6)

<br>
События добавляются по названию и дате, просроченные по дате события не отображаются, но остаются в БД. При просмотре и рассылке события отображаются в отсортированном по дате виде.


**Токены и секреты лежат в config.py**

**Если Linux** <br>
sudo apt-get install libpq-dev
python3 -m pip install psycopg2-binary<br>

**БД: PostgreSQL** <br>
psql -U postgres 
CREATE DATABASE ctf_events WITH ENCODING='UTF8' LC_COLLATE='en_US.utf8' LC_CTYPE='en_US.utf8' TEMPLATE=template0;


**Запуск**
<br>
python3 -m venv venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 run.py
