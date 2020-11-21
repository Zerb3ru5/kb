import click

import kb.commands.commands as cmd
from kb.datatypes.item import Item
from kb.id_manager import generate_item_ids


@click.group()
def main():
    pass


@main.command()
# pick the filetype
@click.option('-n', '--number', 'type', flag_value='number')
@click.option('-f', '--file', 'type', flag_value='file')
@click.option('-txt', '--text', 'type', flag_value='text', default=True)
# give the value to add
@click.argument('value')
# the title of the entry
@click.option('-t', '--title', required=True, type=str)
# the categories the entry is associated with
@click.option('-c', '--category', multiple=True, default=(None), type=str)
# the id that serves as the parent of the entry
@click.option('-to', '--parent', type=str, default='.')
def add(type, value, title, category, parent):
    """
    Add a new item to the current database

    kb add -nr/-f/-t (defaults to t) [VALUE] -n [NAME] -c [CATEGORY] -to [PARENT]
    :param type:
    :param value:
    :param title:
    :param category:
    :param parent:
    :return:
    """

    cmd.add(title, type, value, category, parent)


@main.command()
# the property to search with
@click.option('-id', '--id', 'property', flag_value='id')
@click.option('-tp', '--type', 'property', flag_value='type')
@click.option('-c', '--category', 'property', flag_value='category')
@click.option('-dt', '--date', 'property', flag_value='date')
@click.option('-t', '--title', 'property', flag_value='title')
@click.option('-p', '--parent', 'property', flag_value='parent')
@click.option('-a', '--all', 'property', flag_value='all', default=True)
# the value of the property
@click.argument('value', required=False)
def list(property, value):
    """
    List the defines entries

    kb list -tp/-c/-dt/-n (defaults to c) [VALUE]
    """
    cmd._list(property, value)

    # TODO: add special tree view of all items when tree is typed in


@main.command()
# the property to search with
@click.option('-id', '--id', 'property', flag_value='id', required=True)
@click.option('-tp', '--type', 'property', flag_value='type', required=True)
@click.option('-c', '--category', 'property', flag_value='category', required=True)
@click.option('-dt', '--date', 'property', flag_value='date', required=True)
@click.option('-t', '--title', 'property', flag_value='title', required=True)
@click.option('-a', '--all', 'property', flag_value='all', required=True)
# the value of the property
@click.argument('value', required=True)
def dis(property, value):
    """
    Deletes (discards) the item that is associated with the id given
    :param id:
    :return:
    """
    cmd.delete(property, value)


if __name__ == "__main__":
    main()
