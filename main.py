import sqlite3

from scrapy.scrapy import parser
from app.app import start_app

url = 'https://goldapple.ru/aptechnaja-kosmetika'
connection = sqlite3.connect('my_database.db', check_same_thread=False)
cursor = connection.cursor()

# Создаем таблицу Users
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