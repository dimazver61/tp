import sqlite3


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def db_con():
    mydb = sqlite3.connect(f'db.sqlite')
    mydb.row_factory = dict_factory
    return mydb


def init():
    mydb = db_con()
    cursor = mydb.cursor()
    cursor.execute(""" CREATE TABLE IF NOT EXISTS items (
                         id INTEGER PRIMARY KEY,
                         name TEXT,
                         average FLOAT,
                         min_price FLOAT,
                         max_price FLOAT,
                         rarity TEXT,
                         traits TEXT,
                         lvl TEXT,
                         update_datetime DATETIME DEFAULT (strftime('%Y-%m-%d %H:%M:%S','now', 'localtime'))) """)

    cursor.execute(""" CREATE TABLE IF NOT EXISTS shows (
                         id INTEGER PRIMARY KEY,
                         hash TEXT,
                         update_datetime DATETIME DEFAULT (strftime('%Y-%m-%d %H:%M:%S','now', 'localtime'))) """)
    cursor.close()


# =======shows=======
def get_show(_hash: str):
    mysql = db_con()
    cursor = mysql.cursor()
    cursor.execute("SELECT * FROM shows WHERE hash = ?", (_hash, ))
    result = cursor.fetchone()
    cursor.close()
    return result


def add_show(_hash: str):
    mysql = db_con()
    cursor = mysql.cursor()
    cursor.execute("""INSERT INTO shows (hash) VALUES (?)""", (_hash, ))
    mysql.commit()
    result = cursor.lastrowid
    cursor.close()
    return result


# =======collections=======
def get_item(name: str, rarity: str, traits: str, lvl: str):
    mysql = db_con()
    cursor = mysql.cursor()
    cursor.execute("SELECT * FROM items WHERE name = ? and rarity = ? and traits = ? and lvl = ?",
                   (name, rarity, traits, lvl))
    result = cursor.fetchone()
    cursor.close()
    return result


def add_item(name: str, average: float, min_price: float, max_price: float, rarity: str, traits: str, lvl: str):
    mysql = db_con()
    cursor = mysql.cursor()
    cursor.execute("""INSERT INTO items (name, average, min_price, max_price, rarity, traits, lvl) 
                   VALUES (?,?,?,?,?,?,?)""", (name, average, min_price, max_price, rarity, traits, lvl))
    mysql.commit()
    result = cursor.lastrowid
    cursor.close()
    return result


def update_item(name: str, average: float, min_price: float, max_price: float, rarity: str, traits: str, lvl: str):
    mysql = db_con()
    cursor = mysql.cursor()
    cursor.execute(f"UPDATE items SET average = ?, min_price = ?, max_price = ?, "
                   f"update_datetime=(strftime('%Y-%m-%d %H:%M:%S','now', 'localtime')) WHERE "
                   f"name = ? and rarity = ? and traits = ? and lvl = ?",
                   (average, min_price, max_price, name, rarity, traits, lvl))
    mysql.commit()
    cursor.close()

