import os
import shutil

from kb.util.output_parser import output_parse
from kb.util.default_values import DATABASE_PATH
import kb.database_manager as db


@output_parse
def add_file(conn, id, entry_parent, file_path):
    """
    add a file to the files registry of the database
    :param conn:
    :param entry_parent:
    :param file_path:
    :return:
    """
    if not os.path.isfile(file_path):
        return {'code': 1, 'return': f'Can\'t find {file_path}'}

    # get the path where the file shall be stored
    path = generate_path(conn, entry_parent)

    print('generated path', path)

    # check if the path already exists; if not create it
    if not os.path.exists(path):
        os.makedirs(path)

    # copy the file into directory
    file_extension = os.path.splitext(file_path)[1]
    path = path + f'\\{id}{file_extension}'
    shutil.copy2(file_path, path)

    print(mk_pretty_path(path))

    return {'code': 0, 'return': mk_pretty_path(path)}


def make_parent(conn, item_id, path):
    path = de_pretty_path(path)

    directory = os.path.dirname(path)

    file = os.path.basename(path)

    filename = os.path.splitext(file)[0]

    print('HELLO!', directory, directory + f'\\{filename}')
    print('path', path, 'directory', directory, 'file', file, 'filename', filename)

    # create the new directory
    if not db.isParent(conn, item_id):
        print('TADAAA!!!')
        os.makedirs(directory + f'\\{filename}')

        # move parent file into directory
        dst = directory + f'\\{filename}\\{file}'
        shutil.move(path, dst)

        # register these changes in the registry
        db.update_item_prop_by_id(conn, item_id, 'value', mk_pretty_path(dst))


def generate_path(conn, item_parent):
    """
    returns the directory an item with the given parent needs to be in
    :param conn:
    :param item_parent:
    :return path:
    """
    path = DATABASE_PATH + '\\files\\main'
    parent = item_parent
    parents = [item_parent]
    count = 0

    if item_parent == '.':
        return path

    # get all the parent
    while count < 10:
        count += 1
        item = db.get_items_by_column(conn, 'id', parent)[0]
        parent = item[7]
        if parent == '.':
            break
        else:
            parents.append(parent)

    # add the parents to the path (in inverted order)
    for i in range(len(parents)):
        path = path + f'\\{parents[-1 + i]}'

    return path


def mk_pretty_path(path):
    path = path.replace(DATABASE_PATH + '\\files\\main', '*')
    return path


def de_pretty_path(path):
    path = path.replace('*', DATABASE_PATH + '\\files\\main')
    return path
