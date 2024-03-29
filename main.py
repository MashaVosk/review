import sqlite3

from scrapy.scrapy import parser
from app.app import start_app
from config import url

connection = sqlite3.connect('my_database.db', check_same_thread=False)
cursor = connection.cursor()

if __name__ == "__main__":
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Product (
    id INTEGER PRIMARY KEY,
    Company TEXT NOT NULL,
    Name TEXT NOT NULL,
    Price INTEGER,
    Link TEXT NOT NULL
    )
    ''')

    cursor.execute('DELETE FROM Product WHERE id > 0')

    connection.commit()

    parser(connection, url, 20)

    start_app(connection)

    connection.close()