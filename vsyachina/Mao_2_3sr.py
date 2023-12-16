import sqlite3 as sq

bd = sq.connect('Money.db')
cur = bd.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS cash (money_id INTEGER NOT NULL PRIMARY KEY, 
            valute TEXT NOT NULL, country TEXT NOT NULL, symbol TEXT NOT NULL, in_rubles INTEGER NOT NULL);
            ''')

cur.execute('''INSERT INTO cash (money_id, valute, country, symbol, in_rubles) 
            VALUES (1, "USD", "USA", "$", 89)
            ''')

cur.execute('''INSERT INTO cash (money_id, valute, country, symbol, in_rubles) 
            VALUES (2, "EUR", "Grece", "€", 96)
            ''')

cur.execute('''INSERT INTO cash (money_id, valute, country, symbol, in_rubles) 
            VALUES (3, "TRC", "Turkie", "₺", 3.1)
            ''')

cur.execute('''INSERT INTO cash (money_id, valute, country, symbol, in_rubles) 
            VALUES (4, "CNY", "China", "¥", 12.5)
            ''')

cur.execute('''INSERT INTO cash (money_id, valute, country, symbol, in_rubles)
            VALUES (5, "KZT", "Kazakhstan", "₸", 0.19)
            ''')

cur.execute('DELETE FROM cash WHERE money_id = 2')
bd.commit()
cur.execute('SELECT money_id, valute, country, symbol, in_rubles FROM cash WHERE money_id <= 3')
print(cur.fetchall())
bd.close()