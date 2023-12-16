import sqlite3

def check_key(key):
    conn = sqlite3.connect('keys.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM keys WHERE key = ?', (key,))
    result = cursor.fetchone()

    if result:
        key_info = {'key': result[0], 'duration': result[1], 'created_at': result[2]}
        if key_info['duration'] > 0:
            key_info['duration'] -= 1
            cursor.execute('UPDATE keys SET duration = ? WHERE key = ?', (key_info['duration'], key_info['key']))
            conn.commit()  # Добавляем коммит, чтобы сохранить изменения в базе данных
            return f"Key {key_info['key']} successfully activated. Remaining duration: {key_info['duration']} days."
        else:
            conn.close()
            return f"Key {key_info['key']} has expired."
    else:
        conn.close()
        return "Invalid key."

if __name__ == '__main__':
    key_to_check = input("Enter the key to check: ")
    result = check_key(key_to_check)
    print(result)
