import pymssql
from flask import g, current_app 

server = 'localhost:1435'
database = 'ARNutri'
username = 'sa'
password = 'ARNutri123!@#'

def get_db():
    if 'db' not in g:
        g.db = pymssql.connect(
            server=server, user=username, password=password, database=database, as_dict=True
        )
        return g.db

def close_db(error):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)



"""

conn = pymssql.connect(server=server, user=username, password=password, database=database)
cursor = conn.cursor()

cursor.execute('SELECT * FROM Users;')
row = cursor.fetchone()

while row:
    print(str(row))
    row = cursor.fetchone()"""