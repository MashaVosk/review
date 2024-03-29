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
        for i in range(0, len(list_name1)-1, 2):
            if not("Золотое яблоко" in list_name1[i+1]['content'] or "Золотое яблоко" in list_name1[i]['content']):
                list_company.append(list_name1[i]['content'])
                list_name.append(list_name1[i+1]['content'])

        for price in list_price1:
            if price['content'] != '0':
                list_price.append(price['content'])

        links = soup.findAll(href=re.compile("/\d{11}-"))
        list_link = ["https://goldapple.ru" + i["href"] for i in links]
        for i in zip(list_company, list_name, list_price, list_link):
            cursor.execute('INSERT INTO Product (Company, Name, Price, Link) VALUES (?, ?, ?, ?)', (i[0], i[1], int(i[2]), i[3]))

        connection.commit()