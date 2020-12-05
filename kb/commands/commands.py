import kb.util.default_values as default_values
import kb.database_manager as db
import kb.util.output_parser as op
import kb.file_manager as fm
from kb.datatypes.item import Item
import click


@op.output_parse
def add(title, type, value, categories, parent):
    """
    creates an item based on the type and the value given; adds it to the database
    :param title:
    :param type:
    :param value:
    :param categories:
    :param parent:
    :return:
    """
    connection = db.create_connection(db_file=default_values.DATABASE_PATH + '\\bases\\main.db')

    # check if the given type exists
    if type not in default_values.TYPES:
        return {'code': 1, 'return': f'Unknown datatype \'{type}\''}

    # check if the categories exists
    print('Categories: ', categories)
    for category in categories:
        if not db.check_category(connection, category):
            if click.confirm(f'\nThe category \'{category}\' does not exist.\nDo you want to add \'{category}\' as a new category?'):
                db.create_category(connection, category)
            else:
                return {'code': 1, 'return': f'Unknown category \'{category}\''}

    # TODO: Support for giving search results as parent (the ones with only one result)
    # check if the parent id the main item (.)
    if parent == '.':
        pass
    # check if the parent exists
    elif not db.check_item_existence(connection, parent):
        return {'code': 1, 'return': f'Unknown item {parent}'}

    # check if the item is a file
    if type == 'file':
        # if the parent is also a file, prepare it to be a parent
        if parent != '.':
            parent_item = db.get_items_by_column(connection, 'id', parent)[0]

            fm.make_parent(connection, parent_item[0], parent_item[3])

        # a different adding procedure
        id = db.generate_item_ids(1)[0]
        value = fm.add_file(connection, id, parent, value)

        item = Item(
            id=id,
            title=title,
            type=type,
            value=value,
            categories=categories,
            parent=parent
        )
    # utilize the default adding procedure
    else:
        item = Item(
            id=db.generate_item_ids(1)[0],
            title=title,
            type=type,
            value=value,
            categories=categories,
            parent=parent
        )

    db.add_item(connection, item)

    return {'code': 2, 'return': 'New item added'}


@op.output_parse
def _list(_property, value):
    """
    calls the get_all function from the filesystem to print all the items in the database
    :param _property:
    :param value:
    :return:
    """
    connection = db.create_connection(db_file=default_values.DATABASE_PATH + '\\bases\\main.db')

    # if the property is all just print the whole database
    if _property == 'all' and value is None:
        items = db.get_all_items(connection)

    # if there are special arguments after -a
    elif _property == 'all' and value is not None:
        # if "c" is given, print all the categories
        if value == 'c' or value == 'categories':
            categories = db.get_all_categories(connection)
            table = op.to_list(categories)
            return {'code': 2, 'return': 'Currently available categories:\n\n' + table}

        # if it is a list of types
        if value == 't' or value == 'types':
            # format the list of types correctly
            types = []
            for type in default_values.TYPES:
                types.append((type,))
            table = op.to_list(types)
            return {'code': 2, 'return': 'Currently supported datatypes: \n\n' + table}

        # if it is just an unnecessary value
        else:
            return {'code': 1, 'return': f'Got unexpected extra argument \'{value}\''}

    # raise error if no value is given
    elif _property != 'all' and value is None:
        return {'code': 1, 'return': 'Missing argument \'VALUE\''}

    # if the search key is the id
    elif _property == 'id':
        item = db.get_items_by_column(connection, 'id', value)[0]
        description = ['   Id:', '   Title:', '   Type:', '   Value:', '   Date of creation:', '   Time of creation:',
                       '   Author:', '   Parent:']

        # format it to a table
        item_data = []

        for i in range(len(item)):
            item_data.append((description[i], item[i]))
        table = op.to_light_table(item_data)

        return {'code': 2, 'return': f'{item[0]} [ITEM] at main\n\n' + table}

    # if the search key is a category
    elif _property == 'category':
        category_id = db.get_category_id(connection, value)
        item_ids = db.get_item_ids_by_category_id(connection, value, category_id)

        items = []

        # get the item data associated with the ids
        for item_id in item_ids:
            item = db.get_items_by_column(connection, 'id', item_id)[0]
            items.append(item)

    # if the search key is any other property
    else:
        items = db.get_items_by_column(connection, _property, value)
        print(items)

    # TODO: Make it possible to search for multiple things  at once [example: kb list -c eagle -tp number; meaning:
    #  list all the entries that are associated with the category eagle and are numbers]

    # if there is only one result, display it in the special item view
    if len(items) == 1:
        item = items[0]
        description = ['   Id:', '   Title:', '   Type:', '   Value:', '   Date of creation:',
                       '   Time of creation:',
                       '   Author:', '   Parent:']

        # format it to a table
        item_data = []

        for i in range(len(item)):
            item_data.append((description[i], item[i]))
        table = op.to_light_table(item_data)

        return {'code': 2, 'return': f'{item[0]} [ITEM] at main\n\n' + table}

    # shorten the table
    formatted_list = []
    for item in items:
        formatted_item = []
        for i in range(len(item)):
            if i not in (4, 5, 6):
                formatted_item.append(item[i])
        formatted_list.append(formatted_item)

    table = op.to_table(formatted_list, ['Id', 'Title', 'Type', 'Value', 'Parent'])

    return {'code': 2, 'return': table}


def delete(_property, value):
    """
    delete an item by looking for the right property - value pairs
    :param value:
    :param _property:
    :return:
    """
    # TODO: give a feedback after deleting files
    # TODO: when a file item is deleted, delete the associated file in files as well
    connection = db.create_connection(db_file=default_values.DATABASE_PATH + '\\bases\\main.db')

    db.delete_items_by_column(connection, _property, value)
