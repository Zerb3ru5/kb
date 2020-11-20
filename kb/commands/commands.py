import kb.util.default_values as default_values
import kb.database_manager as db
import kb.util.output_parser as op
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
    # check if the parent exists
    if not db.check_item_existence(connection, parent):
        return {'code': 1, 'return': f'Unknown item {parent}'}

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
def list(property, value):
    """
    calls the get_all function from the filesystem to print all the items in the database
    :param property:
    :param value:
    :return:
    """
    connection = db.create_connection(db_file=default_values.DATABASE_PATH + '\\bases\\main.db')

    # if the property is all just print the whole database
    if property == 'all' and value is None:
        items = db.get_all_items(connection)

    # if there are special arguments after -a
    elif property == 'all' and value is not None:
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
    elif property != 'all' and value is None:
        return {'code': 1, 'return': 'Missing argument \'VALUE\''}

    # if the search key is a category
    elif property == 'category':
        category_id = db.get_category_id(connection, value)
        item_ids = db.get_item_ids_by_category_id(connection, value, category_id)

        items = []

        # get the item data associated with the ids
        for item_id in item_ids:
            item = db.get_items_by_column(connection, 'id', item_id)[0]
            items.append(item)

    # if the search key is any other property
    else:
        items = db.get_items_by_column(connection, property, value)
        print(items)

    # TODO: Make it possible to search for multiple things  at once [example: kb list -c eagle -tp number; meaning:
    #  list all the entries that are associated with the category eagle and are numbers]

    # TODO: Shorten the table (The metadata is not necessary)

    table = op.to_table(items, ['Id', 'Title', 'Type', 'Value', 'Date of creation', 'Time of creation', 'Author', 'Parent'])

    return {'code': 2, 'return': table}


def delete(property, value):
    """
    delete an item by looking for the right property - value pairs
    :param value:
    :param property:
    :return:
    """
    connection = db.create_connection(db_file=default_values.DATABASE_PATH + '\\bases\\main.db')

    db.delete_items_by_column(connection, property, value)
