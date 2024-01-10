import sqlite3
from datetime import datetime, timedelta
import random
import string

DATABASE_NAME = 'keys.db'

def connect_to_database():
    return sqlite3.connect(DATABASE_NAME)

def init_db():
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS keys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT NOT NULL UNIQUE,
                status INTEGER NOT NULL DEFAULT 0,
                activation_date TEXT,
                duration_days INTEGER,
                activated INTEGER NOT NULL DEFAULT 0
)
        ''')
        conn.commit()

def generate_key(num_keys, duration_days):
    keys_generated = []
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        for _ in range(num_keys):
            key = generate_random_key()
            cursor.execute('''
                INSERT INTO keys (key, activation_date, duration_days, status, activated)
                VALUES (?, ?, ?, ?, ?)
            ''', (key, None, duration_days, 0, 0))
            keys_generated.append(key)
        conn.commit()
    return keys_generated



def activate_key(key):
    with connect_to_database() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM keys WHERE key = ?', (key,))
        key_data = cursor.fetchone()
        if key_data:
            key_id, _, status, activation_date, duration_days = key_data
            if status == 0:
                if activation_date is None:
                    # Устанавливаем activation_date только при активации
                    activation_date = datetime.utcnow().isoformat()
                    cursor.execute('UPDATE keys SET activation_date = ? WHERE key = ?', (activation_date, key))

                remaining_time = datetime.fromisoformat(activation_date) + timedelta(
                    days=duration_days) - datetime.utcnow()
                remaining_days = remaining_time.days
                remaining_hours, remainder = divmod(remaining_time.seconds, 3600)
                remaining_minutes, _ = divmod(remainder, 60)

                if remaining_time.total_seconds() > 0:
                    return f"Ключ активирован! Осталось {remaining_days} дней, {remaining_hours} часов и {remaining_minutes} минут."
                else:
                    return f"Ключ истек."
            else:
                return "Ключ уже активирован!"
        else:
            return "Недействительный ключ."

def check_key(key):
    with connect_to_database() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM keys WHERE key = ?', (key,))
        result = cursor.fetchone()
        if result:
            key_data = {
                'id': result[0],
                'key': result[1],
                'status': result[2],
                'activation_date': result[3],
                'duration_days': result[4],
            }
            return key_data
        else:
            return None

def generate_random_key(length=12):
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=length))
