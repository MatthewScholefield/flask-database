# Flask Database

*Simple Flask database integration*

This is a library to make it simple to run sql queries using flask.

When running [database](https://www.python.org/dev/peps/pep-0249/#module-interface) queries in Python with Flask, you either need to create a new connection for each request (quite slow) or manage some pool of connections (complicated). [DBUtils](https://webwareforpython.github.io/DBUtils/) already solves this problem. This package hooks DBUtils into flask's session so that you can access the database in a simple manner.

## Usage

```python
import pymysql  # Can be any database type
import sys
from flask_database import Database
from flask import Flask, request

app = Flask(__name__)
db = Database(
    app,
    pymysql,
    host='127.0.0.1',
    port=3306,
    user='my_user',
    password='123',
    database='my_database'
)

@app.route('/revenue', methods=['GET'])
def get_revenue():
    purchases = db.fetch_all('SELECT price, quantity FROM Purchases')
    revenue = sum(price * quantity for price, quantity in purchases)
    return 'Revenue: ' + str(revenue)

@app.route('/purchase', methods=['POST'])
def post_purchase():
    price = float(request.form['price'])
    quantity = int(request.form['quantity'])
    db.run('INSERT INTO Purchases(price, quantity) VALUES (%s, %s)', (price, quantity))
    return 'Success'


def init_tables():
    db.detach()  # Allows use of database outside Flask request
    db.run('CREATE TABLE Purchases(price DOUBLE NOT NULL, quantity INTEGER NOT NULL)')


if sys.argv[1] == 'init':
    init_tables()
else:
    app.run()
```

Now, we can interact with our service as you would expect:

```bash
curl http://127.0.0.1:5000/revenue
# Revenue: 0

curl -X POST -F 'price=1.25' -F 'quantity=9' http://127.0.0.1:5000/purchase
# Success

curl http://127.0.0.1:5000/revenue
# Revenue: 11.25
```

Note: to replicate this example you'll have MySQL runnning with the provided database and user set up. Example commands:

```bash
sudo apt-get install mysql-server
sudo mysql -u root # If you already set a password use 'mysql -u root -p'
```

```sql
CREATE DATABASE my_database;
CREATE USER my_user@localhost IDENTIFIED BY '123';
```

```bash
python3 example.py init  # Setup tables
python3 example.py  # Run server
```

## Installation

Install via [PyPI](https://pypi.org/project/flask-database/):

```bash
pip3 install --user flask-database
```
