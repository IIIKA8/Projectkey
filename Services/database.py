from flask import Flask, render_template, request, jsonify, redirect
import sqlite3
import random
import string
from datetime import datetime, timedelta

app = Flask(__name__)

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('keys.db')
    cursor = conn.cursor()

    # Создание таблицы keys
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS keys (
            key TEXT PRIMARY KEY,
            duration INTEGER,
            created_at DATETIME
        )
    ''')

    conn.commit()
    conn.close()

init_db()

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
            # Сохранение ключа в базе данных
            save_key_to_db(key, duration)

        return jsonify({'keys': keys_generated})

def save_key_to_db(key, duration):
    conn = sqlite3.connect('keys.db')
    cursor = conn.cursor()

    cursor.execute('INSERT INTO keys (key, duration, created_at) VALUES (?, ?, ?)',
                   (key, duration, datetime.now()))

    conn.commit()
    conn.close()

@app.route('/activate_key_form')
def activate_key_form():
    return render_template('activate_key_form.html')

@app.route('/activate_key', methods=['POST'])
def activate_key():
    key = request.form['key']
    result = activate_key_in_db(key)
    return render_template('activate_key_result.html', result=result)

def activate_key_in_db(key):
    conn = sqlite3.connect('keys.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM keys WHERE key = ?', (key,))
    key_data = cursor.fetchone()

    if key_data:
        key_info = {'duration': key_data[1], 'created_at': key_data[2]}
        if key_info['duration'] > 0:
            key_info['duration'] -= 1
            update_key_in_db(key, key_info['duration'])
            return f"Key {key} successfully activated. Remaining duration: {key_info['duration']} days."
        else:
            return f"Key {key} has expired."
    else:
        return "Invalid key."

def update_key_in_db(key, duration):
    conn = sqlite3.connect('keys.db')
    cursor = conn.cursor()

    cursor.execute('UPDATE keys SET duration = ? WHERE key = ?', (duration, key))

    conn.commit()
    conn.close()

@app.route('/view_keys')
def view_keys():
    keys = load_keys_from_db()
    return render_template('view_keys.html', keys=keys)

def load_keys_from_db():
    conn = sqlite3.connect('keys.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM keys')
    rows = cursor.fetchall()

    conn.close()

    keys = {}
    for row in rows:
        key_info = {'duration': row[1], 'created_at': row[2]}
        keys[row[0]] = key_info

    return keys

@app.route('/clear_keys')
def clear_keys():
    conn = sqlite3.connect('keys.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM keys')

    conn.commit()
    conn.close()

    return redirect('/view_keys')

if __name__ == '__main__':
    app.run(debug=True)
