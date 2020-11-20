from kb.util.default_values import DATABASE_PATH
import kb.database_manager as fs


def add(item):
    """accesses the filesystem to add an item to the database"""

    connection = fs.create_connection(DATABASE_PATH + '\\bases\\main.db')
    fs.add_item(connection, item)
