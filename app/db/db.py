import psycopg2
from datetime import datetime
from config import db_name, db_user, db_password, db_host


class Events:
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host
        )
        self.connection.autocommit = True
        self.init_db()

    def init_db(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    event_date DATE NOT NULL
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notifier (
                    id SERIAL PRIMARY KEY,
                    state BOOLEAN NOT NULL DEFAULT FALSE
                );
            """)

            cursor.execute("SELECT id FROM notifier LIMIT 1;")
            if cursor.rowcount == 0:
                cursor.execute("INSERT INTO notifier (state) VALUES (FALSE);")

    def add_event(self, name, event_date_str):
        event_date = datetime.strptime(event_date_str, '%d-%m-%Y').date()
        with self.connection.cursor() as cursor:
            cursor.execute("INSERT INTO events (name, event_date) VALUES (%s, %s);", (name, event_date))

    def delete_event(self, event_id):
        with self.connection.cursor() as cursor:
            cursor.execute("DELETE FROM events WHERE id = %s;", (event_id,))

    def get_current_events(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, name, TO_CHAR(event_date, 'DD-MM-YYYY') 
                FROM events 
                WHERE event_date >= %s
                ORDER BY event_date ASC;
            """, (datetime.now().date(),))
            return cursor.fetchall()

    def get_notifier_state(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT state FROM notifier LIMIT 1;")
            return cursor.fetchone()[0]

    def set_notifier_state(self, state):
        with self.connection.cursor() as cursor:
            cursor.execute("UPDATE notifier SET state = %s WHERE id = 1;", (state,))
