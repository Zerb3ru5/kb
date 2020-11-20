from datetime import date
import json

from kb.util.default_values import DATABASE_PATH


def get_count() -> 'int':

    history = get_history()
    print(history)

    t = date.today()
    today = t.strftime('%d%m%Y')

    print(today, history['date'], today == history['date'])

    if today == history['date']:
        return history['count']

    else:
        history['date'] = today
        history['count'] = 0

        write_history(history)

        return 0


def increase_count() -> 'None':
    
    history = get_history()
    history['count'] = history['count'] + 1
    write_history(history)

    
def get_history() -> 'dict':

    with open(DATABASE_PATH + '\\historyfile.json', 'r') as hfile:
        history_data = json.load(hfile)
    return history_data


def write_history(history_data: dict) -> 'None':

    with open(DATABASE_PATH + '\\historyfile.json', 'w') as hfile:
        json.dump(history_data, hfile)