
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
