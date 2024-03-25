from flask import request, render_template, Flask
import sqlite3

app = Flask(__name__)
connection = None
cursor = None

def filtered(comp=None, sort_type=None):
    if comp:
        cursor.execute('SELECT * FROM Product WHERE Company == ?', (comp,))
    else:
        cursor.execute('SELECT * FROM Product')
    data = cursor.fetchall()

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
    cursor.execute('SELECT DISTINCT Company FROM Product')
    company = [i[0].replace(' ', '@') for i in cursor.fetchall()]
    company.sort()
    data = filtered(comp, sort_type)
    return render_template('site.html', comp = company, products = data)

def start_app(c):
    global connection, cursor
    connection = c
    cursor = connection.cursor()
    if connection:
        app.run(debug=True)

if __name__ == "__main__":
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    start_app(connection)