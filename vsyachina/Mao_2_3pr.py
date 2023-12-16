import csv
import sqlite3

bd = sqlite3.connect('friendss.db')
cur = bd.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS friends (
        user_id INTEGER NOT NULL PRIMARY KEY,
        friend_name TEXT NOT NULL
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS address (
        user_id INTEGER NOT NULL PRIMARY KEY,
        street TEXT NOT NULL,
        numbers INTEGER NOT NULL
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS hobbies (
        user_id INTEGER NOT NULL PRIMARY KEY,
        hobby_name TEXT NOT NULL
    )
''')


cur.execute("INSERT INTO friends (user_id, friend_name) VALUES (?, ?)", (1, "Maksim"))
cur.execute("INSERT INTO friends (user_id, friend_name) VALUES (?, ?)", (2, "Arina"))
cur.execute("INSERT INTO friends (user_id, friend_name) VALUES (?, ?)", (3, "Lida"))

cur.execute("INSERT INTO address (user_id, street, numbers) VALUES (?, ?, ?)", (1, "Sadovaya", 22))
cur.execute("INSERT INTO address (user_id, street, numbers) VALUES (?, ?, ?)", (2, "Polyanovskaya", 16))
cur.execute("INSERT INTO address (user_id, street, numbers) VALUES (?, ?, ?)", (3, "Sadovaya", 43))

cur.execute("INSERT INTO hobbies (user_id, hobby_name) VALUES (?, ?)", (1, "Volleyboll"))
cur.execute("INSERT INTO hobbies (user_id, hobby_name) VALUES (?, ?)", (2, "Games"))
cur.execute("INSERT INTO hobbies (user_id, hobby_name) VALUES (?, ?)", (3, "Programmer"))

new_hobbie = 'Eating'
user_id = 1
cur.execute("UPDATE hobbies SET hobby_name = ? WHERE \
            user_id = ?", (new_hobbie, user_id))

cur.execute('''
    DELETE FROM friends WHERE user_id = 1
''')

bd.commit()

zapros = '''
    SELECT friends.user_id, friends.friend_name, address.street, address.numbers, hobbies.hobby_name
    FROM friends
    INNER JOIN address ON friends.user_id = address.user_id
    INNER JOIN hobbies ON friends.user_id = hobbies.user_id
'''

cur.execute(zapros)
rows = cur.fetchall()
for row in rows:
    print(row)

with open('csv_friends.csv', 'w+') as f:
    wr = csv.writer(f)
    wr.writerows(rows)

bd.close()
