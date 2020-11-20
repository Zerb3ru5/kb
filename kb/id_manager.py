from datetime import date, datetime
import kb.util.numbersystems as ns
from kb.util.default_values import DATABASE_PATH

import sqlite3


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


def get_ids_by_category(conn, category):
    """
    get all the items associated with the given category
    :param conn:
    :param category:
    :return:
    """
    # get the id of the given category
    category_id = get_category_id(conn, category)

    c = conn.cursor()

    c.execute('''SELECT * FROM main WHERE category_id=?''', (category_id, ))
    result = c.fetchall()

    return {}


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

    print(result)

    ids = []

    for i in range(amount):
        id = len(result) + i + 1
        ids.append(ns.dec_to_base(int(id)))

    print(ids)

    return ids


def get_category_id(conn, category_name):
    """
    get the id of a category by it's name
    :param conn:
    :param category_name:
    :return:
    """
    c = conn.cursor()

    c.execute('''SELECT category_id FROM categories WHERE name=?''', (category_name,))
    id = c.fetchall()[0][0]  # the actual id is nested in a list and a tuple

    return id
