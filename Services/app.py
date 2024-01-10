import sqlite3

from flask import Flask, render_template, request, jsonify, redirect, url_for
from database import init_db, generate_key, activate_key, check_key, connect_to_database
import pytz
from datetime import datetime, timedelta

app = Flask(__name__)

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_key', methods=['POST'])
def generate_key_route():
    if request.method == 'POST':
        num_keys = int(request.form['num_keys'])
        duration = int(request.form['duration'])

        keys_generated = generate_key(num_keys, duration)

        return jsonify({'keys': keys_generated})


def activate_key(key):
    with connect_to_database() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM keys WHERE key = ?', (key,))
        key_data = cursor.fetchone()
        if key_data:
            key_id, _, status, activation_date, duration_days, activated = key_data
            if status == 0:
                if activated == 0:
                    # Устанавливаем activation_date только при активации
                    activation_date = datetime.utcnow().isoformat()
                    cursor.execute('UPDATE keys SET activation_date = ?, activated = 1 WHERE key = ?',
                                   (activation_date, key))

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

def load_keys_from_db():
    conn = sqlite3.connect('keys.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM keys')
    rows = cursor.fetchall()

    conn.close()

    keys = {}
    moscow_tz = pytz.timezone('Europe/Moscow')

    for row in rows:
        key_info = {
            'id': row[0],
            'key': row[1],
            'duration': row[2],
            'activation_date': (
                moscow_tz.localize(datetime.strptime(row[3], "%Y-%m-%dT%H:%M:%S.%f"))
                if row[3] and not isinstance(row[3], datetime)
                else row[3]
            ),
            'activated': row[4] == 1  # assuming 1 means True, 0 means False
        }
        keys[row[0]] = key_info

    return keys

@app.route('/activate_key_form')
def activate_key_form():
    return render_template('activate_key_form.html')

@app.route('/activate_key', methods=['POST'])
def activate_key_route():
    key = request.form['key']
    result = activate_key(key)
    return render_template('activate_key_result.html', result=result)

@app.route('/view_keys')
def view_keys_route():
    keys_data = load_keys_from_db()
    return render_template('view_keys.html', keys=keys_data)


if __name__ == '__main__':
    app.run(debug=True)
