from bs4 import BeautifulSoup
import requests
import sqlite3
import re

def parser(connection, url, numpage = 20):
    cursor = connection.cursor()

    for p in range(1, numpage):
        new_url = url + '?p=' + str(p)
        page = requests.get(new_url)
        soup = BeautifulSoup(page.text, 'html.parser')

        list_name1 = soup.findAll('meta', itemprop='name')
        list_price1 = soup.findAll('meta', itemprop='price')

        list_company = []
        list_name = []
        list_price = []
        i = 0
        while i+1 < len(list_name1):
            if not("Золотое яблоко" in list_name1[i+1]['content'] or "Золотое яблоко" in list_name1[i]['content']):
                list_company.append(list_name1[i]['content'])
                list_name.append(list_name1[i+1]['content'])
            i += 2

        for i in range(len(list_price1)):
            if list_price1[i]['content'] != '0':
                list_price.append(list_price1[i]['content'])

        links = soup.findAll(href=re.compile("/\d{11}-"))
        list_link = ["https://goldapple.ru" + i["href"] for i in links]
        i = 0
        while i < len(list_company) and i < len(list_price) and i < len(list_name) and i < len(list_link):
            cursor.execute('INSERT INTO Product (Company, Name, Price, Link) VALUES (?, ?, ?, ?)', (list_company[i], list_name[i], int(list_price[i]), list_link[i]))
            i += 1

        # Сохраняем изменения
        connection.commit()

if __name__ == "__main__":
    url = 'https://goldapple.ru/aptechnaja-kosmetika'
    connection = sqlite3.connect('my_database.db', check_same_thread=False)
    parser(connection, url)

