**Написан на python3 с использованием aiogram 3** 
<br>




<br>
События добавляются по названию и дате, просроченные по дате события не отображаются, но остаются в БД. При просмотре и рассылке события отображаются в отсортированном по дате виде.
<br><br>

**Токены, секреты и прочая конфигурация лежит в config.py**

**Если Linux** <br>
sudo apt-get install libpq-dev <br>
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

<br>


![image](https://github.com/temlakoz/tgbot-event-notifier/assets/44872170/60a257e1-095c-401b-9724-cd36d57c16c2)

![image](https://github.com/temlakoz/tgbot-event-notifier/assets/44872170/8d9327dd-6078-4a45-8d8f-514048942708)

![image](https://github.com/temlakoz/tgbot-event-notifier/assets/44872170/b7de9001-6ef9-40a5-8acf-11e7edb7d7b5)


