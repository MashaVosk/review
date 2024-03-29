from flask import request, render_template, Flask
import sqlite3

class Bd:
    connection = None
    cursor = None

app = Flask(__name__)
con_cur = Bd()

def filtered(comp=None, sort_type=None):
    if comp:
        con_cur.cursor.execute('SELECT * FROM Product WHERE Company == ?', (comp,))
    else:
        con_cur.cursor.execute('SELECT * FROM Product')
    data = con_cur.cursor.fetchall()

    if sort_type == "1":
        data = sorted(data, key=lambda x: x[1])
    elif sort_type == "2":
        data = sorted(data, key=lambda x: x[1], reverse=True)
    elif sort_type == "3":
        data = sorted(data, key=lambda x: x[2])
    elif sort_type == "4":
        data = sorted(data, key=lambda x: x[2], reverse=True)
    elif sort_type == "5":
        data = sorted(data, key=lambda x: x[3])
    elif sort_type == "6":
        data = sorted(data, key=lambda x: x[3], reverse=True)

    return data

@app.route('/', methods=['GET'])
def main():
    comp = request.args.get('comp')
    if comp:
        comp = comp.replace('@', ' ')
    sort_type = request.args.get('sortType')
    con_cur.cursor.execute('SELECT DISTINCT Company FROM Product')
    company = [i[0].replace(' ', '@') for i in con_cur.cursor.fetchall()]
    company.sort()
    data = filtered(comp, sort_type)
    return render_template('site.html', comp = company, products = data)

def start_app(connection):
    con_cur.connection = connection
    con_cur.cursor = connection.cursor()
    if con_cur.connection:
        app.run(debug=True)

if __name__ == "__main__":
    con_cur.connection = sqlite3.connect('my_database.db')
    con_cur.cursor = con_cur.connection.cursor()
    start_app(con_cur.connection)