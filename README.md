# The kb "knowledge manager"
kb is a cli based database application that can store all kinds of formats like:
- numbers
- text
- files

In addition the data can be bundled and organized in sets and tables to make the 
data easier accessible.

## Commands
The overall keyword for kb is `kb`. After the the main keyword follow the 
different commands to add, view and manipulate the data.
- `add` : add a new item to the database;
    - `--number` / `--text` / `--file` : choose one of those to specify the datatype
    - `VALUE` : specify the value of the new item
    - `--title` / `-t` : give the name of the item
    - `--category` / `-c` : specify the category (categories) of the item. This argument 
    is optional and there can be added an arbitrary number of categories to an item.
    - `--parent` / `-to` : specify which other item shall be the parent of the new item. 
    This argument is optional and defaults to the `.` which means that the item has no parent.
    - _Example:_ 
    `kb add --number 3 --title three --category below_ten --category uneven --parent myparent`
    or in short:
    `kb add -n 3 -t three -c below_ten -c uneven -to myparent`

- `list` : print contents of the database
- `dis` : discard / delete one or multiple items