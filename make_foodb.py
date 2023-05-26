import sqlite3

def create_db():
    conn = sqlite3.connect('foods.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS foods(
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         food_name TEXT,
         food_nutrients TEXT
         )
    ''')

    conn.commit()
    conn.close()

create_db()