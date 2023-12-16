from flask import Flask, render_template, request, jsonify, redirect
import random
import string
from datetime import datetime, timedelta
import sqlite3

app = Flask(__name__)

def initialize_database():
    conn = sqlite3.connect('keys.db')
    cursor = conn.cursor()

    # Создаем таблицу для хранения ключей, если ее нет
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS keys (
            key TEXT PRIMARY KEY,
            duration INTEGER,
            created_at DATETIME
        )
    ''')

    conn.commit()
    conn.close()

# Вызываем функцию инициализации при запуске приложения
initialize_database()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_key', methods=['POST'])
def generate_key():
    if request.method == 'POST':
        num_keys = int(request.form['num_keys'])
        duration = int(request.form['duration'])

        keys_generated = []
        for _ in range(num_keys):
            key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
            keys_generated.append(key)

            # Сохраняем ключ в базе данных
            conn = sqlite3.connect('keys.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO keys VALUES (?, ?, ?)', (key, duration, datetime.now()))
            conn.commit()
            conn.close()

        return jsonify({'keys': keys_generated})

@app.route('/activate_key_form')
def activate_key_form():
    return render_template('activate_key_form.html')

@app.route('/activate_key', methods=['POST'])
def activate_key_post():
    key = request.form['key']
    conn = sqlite3.connect('keys.db')
    cursor = conn.cursor()

    # Проверяем наличие ключа в базе данных
    cursor.execute('SELECT * FROM keys WHERE key = ?', (key,))
    result = cursor.fetchone()

    if result:
        key_info = {'key': result[0], 'duration': result[1], 'created_at': result[2]}
        if key_info['duration'] > 0:
            key_info['duration'] -= 1
            cursor.execute('UPDATE keys SET duration = ? WHERE key = ?', (key_info['duration'], key_info['key']))
            conn.commit()
            conn.close()
            return f"Key {key_info['key']} successfully activated. Remaining duration: {key_info['duration']} days."
        else:
            conn.close()
            return f"Key {key_info['key']} has expired."
    else:
        conn.close()
        return "Invalid key."

@app.route('/view_keys')
def view_keys():
    conn = sqlite3.connect('keys.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM keys')
    keys = {key: {'duration': duration, 'created_at': created_at} for key, duration, created_at in cursor.fetchall()}

    conn.close()
    return render_template('view_keys.html', keys=keys)

@app.route('/activate_key/<key>')
def activate_key(key):
    conn = sqlite3.connect('keys.db')
    cursor = conn.cursor()

    # Проверяем наличие ключа в базе данных
    cursor.execute('SELECT * FROM keys WHERE key = ?', (key,))
    result = cursor.fetchone()

    if result:
        key_info = {'key': result[0], 'duration': result[1], 'created_at': result[2]}
        if key_info['duration'] > 0:
            key_info['duration'] -= 1
            cursor.execute('UPDATE keys SET duration = ? WHERE key = ?', (key_info['duration'], key_info['key']))
            conn.commit()
            conn.close()
            return redirect('/view_keys')
        elif key_info['duration'] == 0:
            conn.close()
            return f"Key {key_info['key']} has expired."
    else:
        conn.close()
        return f"Key {key} not found."

if __name__ == '__main__':
    app.run(debug=True)
