"""
The `Filesystem` class is used to manage the files of the kb databases. It can create
and manage the databases itself, but also the files and values in them.
"""

import os
from kb.util.output_parser import output_parse
from datetime import date, datetime
import kb.util.numbersystems as ns

import sqlite3

from kb.datatypes.item import Item


@output_parse
def create_connection(db_file: str):
    """
    Connects to the given database file, if possible.
    :param db_file:
    :return conn:
    """

    if os.path.isfile(db_file):
        conn = sqlite3.connect(db_file)
        c = conn.cursor()

        # check if the registry exists
        c.execute('''CREATE TABLE IF NOT EXISTS registry (
                                                id TEXT PRIMARY KEY,
                                                title TEXT NOT NULL,
                                                type TEXT NOT NULL, 
                                                value TEXT NOT NULL,
                                                date TEXT,
                                                time TEXT,
                                                author TEXT,
                                                parent TEXT NOT NULL)''')
        conn.commit()

        # check if the category table exists
        c.execute('''CREATE TABLE IF NOT EXISTS categories (
                                                category_id TEXT PRIMARY KEY,
                                                name TEXT NOT NULL UNIQUE)''')
        conn.commit()

        # check if the main table exists
        c.execute('''CREATE TABLE IF NOT EXISTS main (
                                                id TEXT,
                                                category_id TEXT,
                                                PRIMARY KEY (id, category_id),
                                                FOREIGN KEY (id)
                                                    REFERENCES registry (id)
                                                        ON DELETE CASCADE
                                                        ON UPDATE NO ACTION,
                                                FOREIGN KEY (category_id)
                                                    REFERENCES categories (category_id)
                                                        ON DELETE CASCADE
                                                        ON UPDATE NO ACTION)''')
        conn.commit()

        return {'code': 0, 'return': conn}
    else:
        return {'code': 1, 'return': 'Database Not Found'}


def add_item(conn, item: Item):
    """
    adds an item to the given connection
    :param conn:
    :param item:
    :return:
    """
    
    c = conn.cursor()

    # add the item to the registy table
    c.execute('''INSERT INTO registry (id, title, type, value, date, time, author, parent) VALUES (?, ?, ?, ?, ?, ?, 
    ?, ?)''',
              (item.id, item.title, item.type, item.value, item.date, item.time, item.author, item.parent))
    conn.commit()

    # connect the file to the category in the main table
    for category in item.categories:
        c.execute('''INSERT INTO main (id, category_id) VALUES (?, ?)''', (item.id, get_category_id(conn, category)))
        conn.commit()


def delete_items_by_column(conn, column, value):
    """
    use the id of an item to delete is
    :param conn:
    :param column:
    :param value:
    :return:
    """
    c = conn.cursor()

    # get the id of the item
    id = get_item_ids_by_property(conn, column, value)

    # delete the item in the main table
    c.execute(f'''DELETE FROM main WHERE id=?''', (id[0][0],))
    conn.commit()

    # delete the item in the registry
    c.execute(f'''DELETE FROM registry WHERE {column}=?''', (value,))
    conn.commit()


def generate_item_ids(amount=1):
    """
    generate a unique id for an item in the database
    :param amount:
    :return:
    """
    today = date.today()
    today_str = today.strftime('%Y%m%d')

    time = datetime.now()
    time_str = time.strftime('%H%M%S')

    ids = []

    for i in range(amount):
        id = today_str + time_str + str(i)
        ids.append(ns.dec_to_base(int(id)))

    return ids


@output_parse
def get_item_ids_by_property(conn, property, value):
    """
    get all the items with some specific property
    :param conn:
    :param property:
    :param value:
    :return:
    """
    c = conn.cursor()

    try:
        c.execute(f'''SELECT id FROM registry WHERE {property}=?''', (value,))
        result = c.fetchall()
    except Exception:
        return {'code': 1, 'return': f'There is no property called {property}'}

    return {'code': 0, 'return': result}


@output_parse
def get_item_ids_by_category_id(conn, category_name, category_id):
    """
    get all the items associated with the given category
    :param conn:
    :param category:
    :return:
    """
    c = conn.cursor()

    c.execute('''SELECT id FROM main WHERE category_id=?''', (category_id,))
    result = c.fetchall()

    if result == ():
        return {'code': 3, 'return': f'Unkown category \'{category_name}\''}
    else:
        # make the output a list
        item_ids = []
        for item_id in result:
            item_ids.append(item_id[0])

        return {'code': 0, 'return': item_ids}


def get_all_items(conn):
    """
    get everything from the database
    :param conn:
    :return:
    """

    c = conn.cursor()

    c.execute('''SELECT * FROM registry''')
    result = c.fetchall()

    return result


@output_parse
def get_items_by_column(conn, column, value):
    """
    get all entries with a specific value at a specific column
    :param conn:
    :param column:
    :param value:
    :return:
    """
    c = conn.cursor()

    try:
        c.execute(f'''SELECT * FROM registry WHERE {column}="{value}"''')
        result = c.fetchall()
    except Exception:
        return {'code': 1, 'return': f'Unknown property \'{column}\''}

    # if the result is empty
    if not result:
        return {'code': 1, 'return': f'No item found with {value} in the {column}'}
    else:
        return {'code': 0, 'return': result}


def check_item_existence(conn, id):
    """
    checks if an items exists by checking the id
    :param conn:
    :param id:
    :return:
    """
    c = conn.cursor()

    c.execute('''SELECT title FROM registry WHERE id=?''', (id,))
    result = c.fetchone()

    if result:
        return True
    else:
        return False


def create_category(conn, category_name):
    """
    adds a new category to the database
    :param conn:
    :param category_name:
    :return:
    """
    c = conn.cursor()

    id = generate_category_ids(conn)[0]

    # check if it already exists
    if check_category(conn, category_name):
        return {'code': 1, 'return': 'Category already exists'}
    else:
        # make a new entry
        c.execute('''INSERT INTO categories (category_id, name) VALUES (?, ?)''', (id, category_name, ))
        conn.commit()


def generate_category_ids(conn, amount=1):
    """
    generate a unique id for a category
    :param conn:
    :param amount:
    :return:
    """
    c = conn.cursor()

    c.execute('''SELECT * FROM categories''')
    result = c.fetchall()

    ids = []

    for i in range(amount):
        id = len(result) + i + 1
        ids.append(ns.dec_to_base(int(id)))

    return ids


@output_parse
def get_category_id(conn, category_name):
    """
    get the id of a category by it's name
    :param conn:
    :param category_name:
    :return:
    """
    c = conn.cursor()

    c.execute('''SELECT category_id FROM categories WHERE name=?''', (category_name,))
    id = c.fetchall()  # the actual id is nested in a list and a tuple

    if not id:
        return {'code': 1, 'return': f'Unknown category \'{category_name}\''}
    else:
        return {'code': 0, 'return': id[0][0]}


def get_all_categories(conn):
    """
    return all the categories
    :param conn:
    :return:
    """
    c = conn.cursor()

    c.execute('''SELECT name FROM categories''')
    result = c.fetchall()

    print('all the categories available', result)

    return result


def check_category(conn, category_name):
    """
    checks in the given connection if a category already exists
    :param conn:
    :param category_name:
    :return bool:
    """
    c = conn.cursor()

    # search for the category name in the database
    c.execute('''SELECT name FROM categories WHERE name=?''', (category_name, ))
    result = c.fetchone()

    # check if it is empty
    if result:
        return True
    else:
        return False
